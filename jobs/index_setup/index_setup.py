import os
import time
from google.cloud import aiplatform

# --- Configuration ---
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your GCP Project ID
LOCATION = os.environ.get("GCP_REGION", "us-central1") # Replace with your GCP Region
INDEX_DISPLAY_NAME = "artisan_knowledge_index"
INDEX_DESCRIPTION = "Vector Search index for Artisan Mentor knowledge base"
EMBEDDING_DIMENSIONS = 768 # Dimension of textembedding-gecko@003 embeddings
APPROX_NEIGHBORS_COUNT = 1000 # Approximate number of neighbors to search
DISTANCE_MEASURE_TYPE = "DOT_PRODUCT_DISTANCE" # Or "COSINE_DISTANCE", "SQUARED_L2_DISTANCE"
CONTENTS_MIME_TYPE = "application/json" # Assuming JSONL input for indexing

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def create_vector_search_index():
    print(f"Creating Vector Search Index: {INDEX_DISPLAY_NAME} in {LOCATION}...")

    # Define the index configuration
    tree_ah_config = aiplatform.matching_engine.MatchingEngineIndex.TreeAhConfig(
        leaf_node_embedding_count=500,
        leaf_nodes_to_search_percent=20,
    )
    
    # Define the index metadata
    metadata = aiplatform.matching_engine.MatchingEngineIndex.Metadata(
        contents_mime_type=CONTENTS_MIME_TYPE,
        config=aiplatform.matching_engine.MatchingEngineIndex.MatchingEngineIndexConfig(
            dimensions=EMBEDDING_DIMENSIONS,
            approximate_neighbors_count=APPROX_NEIGHBORS_COUNT,
            distance_measure_type=DISTANCE_MEASURE_TYPE,
            tree_ah_config=tree_ah_config,
        ),
    )

    # Create the index
    index = aiplatform.matching_engine.MatchingEngineIndex.create_from_metadata(
        display_name=INDEX_DISPLAY_NAME,
        description=INDEX_DESCRIPTION,
        metadata=metadata,
    )

    print(f"Index created. Resource name: {index.resource_name}")
    return index

def deploy_index_to_endpoint(index):
    print(f"Deploying Index to Endpoint for {index.display_name}...")

    # Define the deployed index configuration
    deployed_index_id = "artisan_knowledge_deployed" # This ID will be used in VectorSearchService

    # Create and deploy the index to an endpoint
    index_endpoint = index.deploy_to_endpoint(
        display_name=f"{INDEX_DISPLAY_NAME}_endpoint",
        deployed_index_id=deployed_index_id,
        # machine_type="e2-standard-2", # Optional: Specify machine type
        # min_replica_count=1, # Optional: Specify min replicas
        # max_replica_count=1, # Optional: Specify max replicas
    )

    print(f"Index deployed to endpoint. Endpoint resource name: {index_endpoint.resource_name}")
    print(f"Deployed Index ID: {deployed_index_id}")
    print(f"Endpoint ID: {index_endpoint.name.split('/')[-1]}") # Extract endpoint ID
    return index_endpoint

if __name__ == "__main__":
    # Ensure the jobs/index_setup directory exists
    os.makedirs("jobs/index_setup", exist_ok=True)

    # Create the index
    index = create_vector_search_index()

    # Wait for index creation to complete (optional, but good for sequential execution)
    print("Waiting for index creation to complete (this may take a while)...")
    index.wait_for_resource_creation()
    print("Index creation complete.")

    # Deploy the index to an endpoint
    index_endpoint = deploy_index_to_endpoint(index)

    # Wait for endpoint deployment to complete
    print("Waiting for index deployment to complete (this may take a while)...")
    index_endpoint.wait_for_resource_creation()
    print("Index deployment complete.")

    print("\n--- Deployment Summary ---")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Index Resource Name: {index.resource_name}")
    print(f"Deployed Index ID: {index_endpoint.deployed_indexes[0].id}")
    print(f"Index Endpoint Resource Name: {index_endpoint.resource_name}")
    print(f"Index Endpoint ID: {index_endpoint.name.split('/')[-1]}")
    print("\nUpdate apps/api/services/vector_search.py and apps/api/config.py with these IDs.")