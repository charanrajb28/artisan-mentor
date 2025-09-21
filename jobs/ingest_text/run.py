
import os

def run():
    # Input and output directory paths
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'text'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed_text'))

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        input_filepath = os.path.join(input_dir, filename)
        if os.path.isfile(input_filepath):
            with open(input_filepath, 'r') as f:
                content = f.read()

            # Simple paragraph-based chunking
            chunks = content.strip().split('\n\n')

            # Write chunks to a new file in the output directory
            output_filename = f"processed_{filename}"
            output_filepath = os.path.join(output_dir, output_filename)
            with open(output_filepath, 'w') as f:
                for i, chunk in enumerate(chunks):
                    f.write(f"Chunk {i+1}:\n")
                    f.write(chunk)
                    f.write("\n\n")
    print("Processing complete.")

if __name__ == "__main__":
    run()
