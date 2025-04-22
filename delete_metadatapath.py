import json
import os
from pathlib import Path

def remove_path_fields_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        # Remove path and pathMetadata from method object if it exists
        if "method" in data:
            if "path" in data["method"]:
                del data["method"]["path"]
                modified = True
            if "pathMetadata" in data["method"]:
                del data["method"]["pathMetadata"]
                modified = True
        
        # Only write back if modifications were made
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_directory(directory):
    files_processed = 0
    files_modified = 0
    
    # Process all JSON files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            files_processed += 1
            
            if remove_path_fields_from_file(file_path):
                files_modified += 1
                print(f"Removed path fields from {filename}")
    
    return files_processed, files_modified

def main():
    directories = ["pessoal_v2_metadados_json", "folha_v2_metadados_json"]
    total_files_processed = 0
    total_files_modified = 0
    
    for directory in directories:
        print(f"\nProcessing directory: {directory}")
        files_processed, files_modified = process_directory(directory)
        total_files_processed += files_processed
        total_files_modified += files_modified
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files_processed}")
    print(f"Total files modified: {total_files_modified}")

if __name__ == "__main__":
    main() 