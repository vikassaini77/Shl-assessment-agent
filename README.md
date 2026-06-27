# SHL Conversational Assessment Recommender

## Overview
This project implements a conversational AI agent designed to help users navigate the SHL Product Catalog and find the right assessment solutions. The agent is exposed via a stateless REST API (FastAPI) that accepts a full conversation history and returns a strictly formatted JSON response containing the agent's reply and any relevant product recommendations.

## Architecture & Agent Design
To ensure scalability and robustness, this solution utilizes a **Tool-Calling Agent** combined with **Retrieval-Augmented Generation (RAG)**.

- **Semantic Search (RAG)**: The app uses `google-genai` and Gemini's `gemini-embedding-2` model to convert the SHL catalog into vector embeddings dynamically. It then performs rapid cosine similarity search using NumPy to find relevant assessments based on semantic meaning.
- **Agentic Workflow**: The Gemini LLM is provided with a `search_catalog` tool. When a user asks a question, the agent autonomously decides whether to ask a clarifying question, invoke the retrieval tool to find assessments, or politely refuse out-of-scope inquiries.
- **Stateless API**: The `/chat` endpoint is completely stateless. It accepts the full conversation history on every request, ensuring easy horizontal scaling.
- **Robustness**: All LLM calls are wrapped in the `tenacity` library to provide exponential backoff and retries, gracefully handling transient API failures or rate limits (e.g., `429 RESOURCE_EXHAUSTED`).

*Note on Data Collection*: Automated scraping of the live SHL product catalog was prohibited by WAF/Cloudflare bot-protection. To respect these security boundaries, a representative JSON catalog (`catalog.json`) was constructed manually to demonstrate the RAG architecture.

## Getting Started Locally

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

### Running the Server
Start the FastAPI server using Uvicorn:
```bash
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`. You can access the interactive Swagger UI documentation at `http://localhost:8000/docs`.

## Evaluation & Testing
The project includes an automated evaluation script (`evaluate.py`) that tests the agent against diverse simulated conversation traces (e.g., a Direct User, a Vague User, and an Off-topic User) to verify:
1. **Recall**: The agent successfully retrieves and recommends the correct items.
2. **Schema Compliance**: The agent strictly adheres to the required JSON output schema under all conditions.
3. **Scope Enforcement**: The agent successfully refuses to answer general, off-topic questions.

To run the evaluation, ensure the server is fully running, then execute:
```bash
python evaluate.py
```

## Deployment (Render)
This repository is optimized for free deployment on **Render.com** with zero cold-start model download delays.
1. Create a free account on [Render](https://render.com).
2. Connect your GitHub repository.
3. Select **New Web Service**, choose this repository, and Render will automatically detect the `render.yaml` configuration.
4. Add `GEMINI_API_KEY` as an environment variable in the Render dashboard.
5. Deploy! Your API will be instantly available at a public URL (e.g., `https://your-app.onrender.com`).

## Trade-offs & Future Improvements
Given more time and resources, the following enhancements would be prioritized:
- **Managed Vector Database**: Swap local embeddings for a managed vector database (e.g., Pinecone or Weaviate) to support automatic syncing with live catalog updates.
- **Backend Session Memory**: Instead of forcing the client to send the entire conversation history on every request, implement a Redis-backed session store to manage conversation state securely on the backend.
