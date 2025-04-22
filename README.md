# JSON Metadata and Enum Management Tools

This project provides a suite of tools for scraping JSON metadata and managing enum definitions from Betha Cloud's API. It includes scripts for scraping metadata, extracting enums, merging files, and cleaning up enum references.

## Project Structure

```
.
├── README.md                      # This documentation file
├── scraping_metadata.py          # Script to scrape metadata from API
├── merge_jsons.py               # Script to merge JSON files by directory
├── merge_enums.py               # Script to merge enum files
├── extract_enums.py             # Script to extract enums into a consolidated file
├── delete_enums.py              # Script to remove enums from source files
├── .env                         # Environment variables configuration
├── enums.json                   # Output file containing all merged enums
├── pessoal.json                # Output file containing all merged pessoal metadata
├── folha.json                  # Output file containing all merged folha metadata
├── metadata_output/            # Directory for scraped metadata
├── pessoal_v2_metadados_json/ # Directory containing pessoal JSON files
└── folha_v2_metadados_json/   # Directory containing folha JSON files
```

## Execution Order and Process Flow

### 1. Initial Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install python-dotenv requests
   ```
4. Create `.env` file with your credentials:
   ```env
   BEARER_TOKEN=your_bearer_token_here
   USER_ACCESS_TOKEN=your_user_access_token_here
   INPUT_FILE=input_sistemas.json
   OUTPUT_DIRECTORY=metadata_output
   ```

### 2. Metadata Scraping (`scraping_metadata.py`)

This script fetches metadata from the Betha Cloud API.

1. Run the scraping script:
   ```bash
   python scraping_metadata.py
   ```

2. Expected Output:
   ```
   Processing: folha - remuneracoes (ID: 123)
   Processing: folha - cargos (ID: 124)
   ...
   
   --- Scraping Summary ---
   Total Resources: 76
   Processed Resources: 76
   Failed Resources: 0
   ```

### 3. Merge JSON Files (`merge_jsons.py`)

This script merges all JSON files from each directory (pessoal and folha) into consolidated files.

1. Run the merge script:
   ```bash
   python merge_jsons.py
   ```

2. Expected Output:
   ```
   Processing directory: pessoal_v2_metadados_json
   Processed: file1.json
   Processed: file2.json
   ...
   Merged 75 files into pessoal.json

   Processing directory: folha_v2_metadados_json
   Processed: file1.json
   Processed: file2.json
   ...
   Merged 76 files into folha.json

   Final Statistics:
   Total files processed in pessoal: 75
   Total files processed in folha: 76
   Total files processed: 151
   ```

3. Results:
   - Creates `pessoal.json` containing all merged pessoal metadata
   - Creates `folha.json` containing all merged folha metadata
   - Each output file is structured as a dictionary where keys are original filenames

### 4. Extract and Merge Enums (`extract_enums.py` and `merge_enums.py`)

These scripts extract enums from metadata and merge them into a single file.

1. First, extract enums:
   ```bash
   python extract_enums.py
   ```

2. Then, merge enum files:
   ```bash
   python merge_enums.py
   ```

3. Expected Output from merge_enums.py:
   ```
   Statistics:
   Enums in pessoal: 133
   Enums in folha: 180
   Total unique enums: 211
   Duplicates removed: 102

   Merged enums have been saved to enums.json
   ```

### 5. Enum Removal (`delete_enums.py`)

This script cleans up the JSON files by removing enum definitions and references.

1. Run the cleanup script:
   ```bash
   python delete_enums.py
   ```

2. Expected Output:
   ```
   Removed enums from configuracaoEvento_busca.json
   Removed enums from remuneracoes_busca.json
   ...
   
   Processed 76 files
   Modified 68 files
   ```

## Features in Detail

### Metadata Scraping
- Authenticates with Betha Cloud API
- Fetches metadata for all active resources
- Handles rate limiting and errors
- Generates detailed error logs
- Sanitizes filenames for cross-platform compatibility

### JSON Merging
- Merges JSON files by directory
- Maintains original file structure as keys
- Handles large files efficiently
- Provides detailed processing statistics
- Error handling for malformed JSON

### Enum Management
- Extracts and consolidates enum definitions
- Merges enum files with duplicate handling
- Removes enum sections from source files
- Maintains enum value mappings and descriptions
- Warns about inconsistent definitions

## Error Handling

The scripts include comprehensive error handling for:
- API authentication failures
- Network connectivity issues
- File reading/writing problems
- JSON parsing errors
- Invalid file structures
- Duplicate enum definitions
- Missing references

## Requirements

- Python 3.6+
- python-dotenv
- requests
- JSON files must be UTF-8 encoded
- Sufficient disk space for metadata and output files
- API access credentials

## Best Practices

1. **Before Running Scripts**:
   - Always backup your data
   - Verify API credentials
   - Check disk space requirements
   - Review input file structure
   - Follow the execution order specified above

2. **During Execution**:
   - Monitor error outputs
   - Check progress indicators
   - Verify file permissions
   - Run scripts in the specified order

3. **After Completion**:
   - Validate output files
   - Review error logs
   - Check file integrity
   - Verify enum consistency
   - Ensure all merges completed successfully

## Troubleshooting

Common issues and solutions:

1. **API Authentication Errors**:
   - Verify token validity
   - Check .env file configuration
   - Ensure proper token format

2. **File Processing Errors**:
   - Check file permissions
   - Verify JSON syntax
   - Ensure sufficient disk space
   - Check for file encoding issues

3. **Merge Issues**:
   - Verify source directory structure
   - Check for duplicate filenames
   - Ensure sufficient memory for large merges
   - Validate JSON structure before merging

4. **Missing Enums**:
   - Verify source file structure
   - Check for nested references
   - Review error logs
   - Ensure all files were processed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 