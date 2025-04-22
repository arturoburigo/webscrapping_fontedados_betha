import json
import os
from pathlib import Path

def merge_json_files(directory):
    """
    Merge all JSON files in a directory into a single dictionary.
    The key will be the filename without extension, and the value will be the JSON content.
    """
    merged_data = {}
    
    # List all JSON files in directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Use filename without extension as key
                    key = os.path.splitext(filename)[0]
                    data = json.load(f)
                    merged_data[key] = data
                    print(f"Processed: {filename}")
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {str(e)}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    return merged_data

def process_directory(input_dir, output_file):
    """
    Process a directory and save merged result to output file
    """
    print(f"\nProcessing directory: {input_dir}")
    merged_data = merge_json_files(input_dir)
    
    # Save merged result
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)
    
    print(f"Merged {len(merged_data)} files into {output_file}")
    return len(merged_data)

def main():
    # Define directories and output files
    pessoal_dir = "pessoal_v2_metadados_json"
    folha_dir = "folha_v2_metadados_json"
    
    # Process each directory
    pessoal_count = process_directory(pessoal_dir, "pessoal.json")
    folha_count = process_directory(folha_dir, "folha.json")
    
    # Print final statistics
    print("\nFinal Statistics:")
    print(f"Total files processed in pessoal: {pessoal_count}")
    print(f"Total files processed in folha: {folha_count}")
    print(f"Total files processed: {pessoal_count + folha_count}")

if __name__ == "__main__":
    main() 