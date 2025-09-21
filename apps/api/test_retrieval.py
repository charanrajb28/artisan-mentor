import os
import google.generativeai as genai
from .services.vector_search import VectorSearchService

# Configure the generative AI client
api_key = "AIzaSyB9l2hc3Baf7gXlD2xnCzvbdTsx_ENfllo"
genai.configure(api_key=api_key)

# Initialize VectorSearchService
vector_search_service = VectorSearchService(
    project_id="gen-ai-471517",
    location="us-central1"
)

def test_retrieval(query: str, k: int):
    print(f"Testing retrieval for query: '{query}' with k={k}")
    try:
        embedding_model = "models/embedding-001"
        query_embedding = genai.embed_content(
            model=embedding_model,
            content=query,
            task_type="RETRIEVAL_QUERY"
        )['embedding']

        neighbors = vector_search_service.find_neighbors(
            query_embedding=query_embedding,
            num_neighbors=k
        )

        print("Retrieval successful!")
        for i, neighbor in enumerate(neighbors):
            print(f"Neighbor {i+1}: {neighbor}")

    except Exception as e:
        print(f"Error during retrieval: {e}")

if __name__ == "__main__":
    sample_query = "What are traditional craft techniques?"
    test_retrieval(sample_query, k=5)
