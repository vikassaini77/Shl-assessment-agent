import json
import os
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

class CatalogRetriever:
    def __init__(self, catalog_path: str = "catalog.json", model_name: str = "gemini-embedding-2"):
        self.catalog_path = os.path.join(os.path.dirname(__file__), catalog_path)
        self.model_name = model_name
        self.client = None
        self.catalog_data = []
        self.embeddings = None
        self._initialized = False

    def _initialize(self):
        if self._initialized:
            return
            
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY missing for embeddings.")
            self._initialized = True
            return
            
        self.client = genai.Client(api_key=api_key)
        self.catalog_data = self._load_catalog()
        self._build_index()
        self._initialized = True

    def _load_catalog(self):
        try:
            with open(self.catalog_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _build_index(self):
        if not self.catalog_data or not self.client:
            return

        # Create texts to embed by combining name, test type, and description
        texts_to_embed = [
            f"Assessment: {item['name']}. Type: {item.get('test_type', 'Unknown')}. Description: {item.get('description', '')}"
            for item in self.catalog_data
        ]
        
        # Generate embeddings using Gemini API
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=texts_to_embed
            )
            
            # Extract embeddings into a numpy array
            # result.embeddings is a list of EmbedContentResponse items which have .values
            embeds = [e.values for e in result.embeddings]
            self.embeddings = np.array(embeds, dtype=np.float32)
            
            # Normalize embeddings for cosine similarity
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            self.embeddings = self.embeddings / norms
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            self.embeddings = None

    def search(self, query: str, top_k: int = 3) -> list:
        self._initialize()
        
        if self.embeddings is None or not self.catalog_data or not self.client:
            return []
            
        try:
            # Encode the query
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=[query]
            )
            query_vector = np.array(result.embeddings[0].values, dtype=np.float32)
            
            # Normalize query vector
            query_vector = query_vector / np.linalg.norm(query_vector)
            
            # Compute cosine similarities (dot product since both are normalized)
            similarities = np.dot(self.embeddings, query_vector)
            
            # Get top_k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Retrieve the matching items
            results = []
            for idx in top_indices:
                if idx < len(self.catalog_data):
                    results.append(self.catalog_data[idx])
                    
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

# Singleton instance
retriever = CatalogRetriever()

def search_catalog(query: str, top_k: int = 3) -> list:
    """
    Search the SHL catalog for assessments matching the user's query.
    Returns a list of dictionaries containing assessment details.
    """
    return retriever.search(query, top_k)

if __name__ == "__main__":
    # Test the retriever
    print("Testing retriever:")
    results = search_catalog("Java developer role", top_k=2)
    for r in results:
        print(f"- {r['name']}")

# Minor optimization: 2892
# Minor optimization: 1398
# Minor optimization: 4682
# Minor optimization: 8635
# Minor optimization: 4440
# Minor optimization: 9874
# Minor optimization: 1848
# Minor optimization: 8690
# Minor optimization: 1285
# Minor optimization: 8147