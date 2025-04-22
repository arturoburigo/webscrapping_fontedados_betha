import json
import os

def merge_enum_files(pessoal_file, folha_file, output_file):
    # Read pessoal enums
    with open(pessoal_file, 'r', encoding='utf-8') as f:
        pessoal_enums = json.load(f)
    
    # Read folha enums
    with open(folha_file, 'r', encoding='utf-8') as f:
        folha_enums = json.load(f)
    
    # Merge dictionaries, pessoal_enums takes precedence in case of duplicates
    merged_enums = {**folha_enums, **pessoal_enums}
    
    # Write merged result
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_enums, f, indent=4, ensure_ascii=False)
    
    # Print statistics
    total_pessoal = len(pessoal_enums)
    total_folha = len(folha_enums)
    total_merged = len(merged_enums)
    duplicates = total_pessoal + total_folha - total_merged
    
    print(f"Statistics:")
    print(f"Enums in pessoal: {total_pessoal}")
    print(f"Enums in folha: {total_folha}")
    print(f"Total unique enums: {total_merged}")
    print(f"Duplicates removed: {duplicates}")

def main():
    pessoal_file = "enums_pessoal.json"
    folha_file = "enums_folha.json"
    output_file = "enums.json"
    
    merge_enum_files(pessoal_file, folha_file, output_file)
    print(f"\nMerged enums have been saved to {output_file}")

if __name__ == "__main__":
    main() 