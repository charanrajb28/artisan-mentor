import os
import json
import google.generativeai as genai

def embed_job():
    # IMPORTANT: Replace with your API key
    # You can get an API key from Google AI Studio: https://aistudio.google.com/app/apikey
    api_key = "AIzaSyB9l2hc3Baf7gXlD2xnCzvbdTsx_ENfllo"
    genai.configure(api_key=api_key)

    # Input and output file paths
    input_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed_text', 'processed_crafts.txt'))
    output_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'vectors', 'vectors.json'))

    # Read the processed text
    with open(input_filepath, 'r') as f:
        content = f.read()

    # Split into chunks
    chunks = [chunk for chunk in content.strip().split('\n\n') if chunk.strip()]

    # Define the embedding model
    embedding_model = "models/embedding-001"

    # Open the output file
    with open(output_filepath, 'w') as f:
        for i, chunk in enumerate(chunks):
            # Generate embeddings
            response = genai.embed_content(
                model=embedding_model,
                content=chunk,
                task_type="RETRIEVAL_DOCUMENT"
            )

            # Create a dictionary with the chunk and embedding
            data = {"id": str(i), "text": chunk, "embedding": response['embedding']}

            # Write the dictionary to the jsonl file
            f.write(json.dumps(data) + "\n")

    print(f"Embeddings saved to {output_filepath}")

if __name__ == "__main__":
    embed_job()
