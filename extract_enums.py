import json
import os
from collections import defaultdict

def extract_enums_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        enums = {}
        
        # Check if the file has an "enums" section
        if "enums" in data:
            enums.update(data["enums"])
            
        # Also check for enum references in expressions and types
        def find_enum_references(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, dict) and "enum" in value:
                        enum_name = value["enum"]
                        if enum_name not in enums:
                            print(f"Warning: Found reference to enum '{enum_name}' in {file_path} but enum definition not found")
                    else:
                        find_enum_references(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for item in obj:
                    find_enum_references(item, path)
        
        if "expressions" in data:
            find_enum_references(data["expressions"])
        if "types" in data:
            find_enum_references(data["types"])
            
        return enums
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return {}

def main():
    input_dir = "folha_v2_metadados_json"
    output_file = "enums.json"
    
    all_enums = {}
    
    # Process all JSON files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            enums = extract_enums_from_file(file_path)
            
            # Merge enums, avoiding duplicates
            for enum_name, enum_data in enums.items():
                if enum_name not in all_enums:
                    all_enums[enum_name] = enum_data
                else:
                    # If enum exists, verify if it's different
                    if json.dumps(all_enums[enum_name]) != json.dumps(enum_data):
                        print(f"Warning: Different enum found for {enum_name} in {filename}")
    
    # Write the consolidated enums to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_enums, f, indent=4, ensure_ascii=False)
    
    print(f"Extracted {len(all_enums)} unique enums to {output_file}")

if __name__ == "__main__":
    main() 