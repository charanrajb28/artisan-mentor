import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List

class EmbeddingsService:
    def __init__(self, project_id: str = "gen-ai-471517", location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        # Explicitly specify the full resource name for the model
        self.model = TextEmbeddingModel.from_pretrained(f"projects/{project_id}/locations/{location}/publishers/google/models/textembedding-gecko@003")

    def get_embedding(self, text: str) -> List[float]:
        try:
            embeddings = self.model.get_embeddings([text])
            embedding_vectors = [embedding.values for embedding in embeddings]
            return embedding_vectors[0] # Return the first (and only) embedding
        except Exception as e:
            print(f"Error getting embedding for text: {text}. Error: {e}")
            return []