from fastapi import APIRouter, HTTPException
from ..schemas.retrieve import RetrieveRequest
from ..schemas.embed import EmbedRequest
from ..services.vector_search import VectorSearchService # New import

import google.generativeai as genai
import os

router = APIRouter()

# Configure the generative AI client
# IMPORTANT: It is recommended to set the API key as an environment variable for security.
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # If the environment variable is not set, fallback to the hardcoded key.
    # This is not recommended for production environments.
    api_key = "AIzaSyB9l2hc3Baf7gXlD2xnCzvbdTsx_ENfllo"

if not api_key:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable or hardcode it.")

genai.configure(api_key=api_key)

# Initialize VectorSearchService
# Using the project ID and location from index_setup.py and the endpoint resource name from the previous output.
vector_search_service = VectorSearchService(
    project_id="gen-ai-471517",
    location="us-central1"
)

@router.post("/")
def retrieve_vectors(request: RetrieveRequest):
    """
    Retrieves the top k most similar vectors from the Vertex AI Vector Search index.
    """
    try:
        # Embed the query
        embedding_model = "models/embedding-001"
        query_embedding = genai.embed_content(
            model=embedding_model,
            content=request.query,
            task_type="RETRIEVAL_QUERY"
        )['embedding']

        # Find neighbors
        neighbors_response = vector_search_service.find_neighbors(
            query_embedding=query_embedding,
            num_neighbors=request.k
        )

        # Process the response to be JSON serializable
        formatted_neighbors = []
        if neighbors_response and neighbors_response[0]:
            for neighbor in neighbors_response[0]:
                formatted_neighbors.append({
                    "id": neighbor.id,
                    "distance": neighbor.distance
                })

        return {"neighbors": formatted_neighbors}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed")
def embed_query(request: EmbedRequest):
    """
    Generates an embedding for a given query.
    """
    try:
        # Embed the query
        embedding_model = "models/embedding-001"
        embedding = genai.embed_content(
            model=embedding_model,
            content=request.query,
            task_type="RETRIEVAL_QUERY"
        )['embedding']

        return {"embedding": embedding}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
