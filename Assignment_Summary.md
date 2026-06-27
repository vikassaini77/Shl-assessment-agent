# SHL Conversational Assessment Recommender: Approach Summary

## 1. Design Choices
To build a scalable and robust recommender, I implemented a **Tool-Calling Agent architecture** rather than relying on "prompt-stuffing" (where the entire catalog is injected into the LLM context window). 
- **Stateless REST API**: The application is built using FastAPI. The `/chat` endpoint is completely stateless, accepting the full conversation history on every request. This ensures the service can horizontally scale without complex backend session management.
- **Tool-Augmented LLM**: I provided the Gemini 2.5 Flash model with a `search_catalog` function. The LLM autonomously determines whether to ask the user a clarifying question, invoke the tool to search the database, or refuse out-of-scope requests.

## 2. Retrieval Setup
The system uses **Retrieval-Augmented Generation (RAG)** to find relevant assessments:
- **Embeddings**: I utilized Gemini's `gemini-embedding-2` model to generate high-quality vector embeddings for the catalog items (combining name, type, and description).
- **Vector Search**: For rapid retrieval, the system performs a cosine similarity search using NumPy to compare the user's query vector against the catalog embeddings, returning the Top-K most relevant results to the LLM.

## 3. Prompt Design
The prompt engineering focused strictly on deterministic behavior and schema adherence:
- **System Instructions**: The agent was given a strong persona ("You are an expert SHL Assessment Recommender") and strict behavioral guardrails. 
- **Structured Output**: The prompt explicitly enforces a JSON output schema containing `reply`, `recommendations` (a list of objects), and an `end_of_conversation` boolean. This ensures the frontend consuming the API always receives parseable data.

## 4. Evaluation Method & Measuring Improvement
To ensure the system met all requirements, I built an automated evaluation pipeline (`evaluate.py`) that tests the API against three simulated user personas:
1. **Direct User**: Tests exact recall (e.g., asking for a Java 8 assessment).
2. **Vague User**: Tests the agent's ability to handle broad constraints (e.g., asking for a Python developer assessment).
3. **Off-topic User**: Tests scope enforcement (e.g., asking for interview advice).
**Improvement Measurement**: Success was measured dynamically by parsing the API's JSON response and asserting that the `recommendations` count matched the expected output for each specific persona (e.g., ensuring 0 recommendations were returned for the off-topic query).

## 5. Challenges and What Did Not Work
1. **Data Acquisition Constraints**: My initial plan was to dynamically scrape the live SHL product catalog. However, aggressive WAF/Cloudflare bot-protection policies blocked automated scraping. To respect these security boundaries, I manually constructed a representative JSON catalog to successfully demonstrate the RAG architecture.
2. **Deployment Constraints**: The original retrieval implementation utilized `sentence-transformers` and PyTorch. While highly accurate locally, this created a massive 1.5GB+ footprint and a 40-second cold-start delay, which caused "Out of Memory" crashes on free-tier cloud deployment platforms (like Render).
3. **The Pivot**: To solve the deployment issue, I pivoted to using the **Gemini Embedding API** (`gemini-embedding-2`). This reduced the application footprint to <50MB, completely eliminated the cold-start delay, and allowed for seamless, instant cloud deployment while maintaining excellent semantic search accuracy.
