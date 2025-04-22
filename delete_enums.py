import json
import os
from pathlib import Path

def remove_enums_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        # Remove the "enums" section if it exists
        if "enums" in data:
            del data["enums"]
            modified = True
        
        # Remove enum references from expressions and types
        def remove_enum_references(obj):
            if isinstance(obj, dict):
                # Remove enum field if it exists
                if "enum" in obj:
                    del obj["enum"]
                    return True
                
                # Recursively process all dictionary values
                changed = False
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        if remove_enum_references(value):
                            changed = True
                return changed
            
            elif isinstance(obj, list):
                # Recursively process all list items
                changed = False
                for item in obj:
                    if isinstance(item, (dict, list)):
                        if remove_enum_references(item):
                            changed = True
                return changed
            
            return False
        
        # Process expressions and types
        if "expressions" in data:
            if remove_enum_references(data["expressions"]):
                modified = True
        
        if "types" in data:
            if remove_enum_references(data["types"]):
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

def main():
    input_dir = "folha_v2_metadados_json"
    files_processed = 0
    files_modified = 0
    
    # Process all JSON files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            files_processed += 1
            
            if remove_enums_from_file(file_path):
                files_modified += 1
                print(f"Removed enums from {filename}")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Modified {files_modified} files")

if __name__ == "__main__":
    main() 