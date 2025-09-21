import os
from google.cloud import aiplatform
# from .embeddings import EmbeddingsService # Comment out EmbeddingsService import
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from typing import List, Dict
from ..schemas.context import Context

class VectorSearchService:
    def __init__(self, project_id: str = "gen-ai-471517", location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.index_endpoint_name = (
            "projects/971297438278/locations/us-central1/indexEndpoints/3363716131645816832"
        )
        self.deployed_index_id = "artisan_knowledge_deployed"

        aiplatform.init(project=self.project_id, location=self.location)

        self.endpoint = aiplatform.MatchingEngineIndexEndpoint(
            index_endpoint_name=self.index_endpoint_name
        )
        # self.embeddings_service = EmbeddingsService(project_id=project_id, location=location) # Comment out EmbeddingsService instantiation

    def semantic_retrieve(self, query: str, craft_filters: Dict = None) -> List[Context]:
        # num_neighbors = 5 # Default number of neighbors

        # filters = []
        # if craft_filters:
        #     if "craft_cluster" in craft_filters:
        #         filters.append(Namespace(name="craft_cluster", allow_tokens=[craft_filters["craft_cluster"]]))
        #     if "region" in craft_filters:
        #         filters.append(Namespace(name="region", allow_tokens=[craft_filters["region"]]))

        # 1. Embed query (temporarily skipped)
        # query_embedding = self.embeddings_service.get_embedding(query)
        # if not query_embedding:
        #     return []

        # 2. Query Vertex AI Vector Search endpoint with filters (temporarily skipped)
        # response = self.endpoint.find_neighbors(
        #     queries=[query_embedding],
        #     num_neighbors=num_neighbors,
        #     deployed_index_id=self.deployed_index_id,
        #     filters=filters if filters else None,
        # )

        # 3. Process results and retrieve contexts with citations (Placeholder)
        retrieved_contexts = []
        # for neighbor in response.nearest_neighbors:
        #     for match in neighbor.neighbors:
        #         retrieved_contexts.append(Context(
        #             content=f"Content for ID: {match.id}",
        #             citation=f"Source for ID: {match.id}",
        #             source_id=match.id
        #         ))
        return retrieved_contexts
