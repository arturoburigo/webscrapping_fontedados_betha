# JSON Metadata and Enum Management Tools

This project provides a suite of tools for scraping JSON metadata and managing enum definitions from Betha Cloud's API. It includes scripts for scraping metadata, extracting enums, and cleaning up enum references.

## Project Structure

```
.
├── README.md                      # This documentation file
├── scraping_metadata.py          # Script to scrape metadata from API
├── extract_enums.py              # Script to extract enums into a consolidated file
├── delete_enums.py               # Script to remove enums from source files
├── .env                          # Environment variables configuration
├── enums.json                    # Output file containing all extracted enums
├── metadata_output/              # Directory for scraped metadata
└── folha_v2_metadados_json/      # Directory containing processed JSON files
```

## Complete Process Flow

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

3. Results:
   - Creates JSON files in `metadata_output/` directory
   - Each file contains metadata for one resource
   - Generates `scraping_errors.json` if any errors occur

### 3. Enum Extraction (`extract_enums.py`)

This script processes the scraped metadata files to extract and consolidate enum definitions.

1. Run the extraction script:
   ```bash
   python extract_enums.py
   ```

2. Expected Output:
   ```
   Extracted 180 unique enums to enums.json
   ```

3. Results:
   - Creates `enums.json` containing all unique enums
   - Example enum structure:
     ```json
     {
       "TipoDespesa": {
         "values": [
           {
             "key": "FOLHA",
             "value": 1,
             "description": "Folhas e eventos"
           },
           ...
         ]
       }
     }
     ```

### 4. Enum Removal (`delete_enums.py`)

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

3. Results:
   - Modifies original JSON files in place
   - Removes enum sections and references
   - Preserves other metadata structure

## Features in Detail

### Metadata Scraping
- Authenticates with Betha Cloud API
- Fetches metadata for all active resources
- Handles rate limiting and errors
- Generates detailed error logs
- Sanitizes filenames for cross-platform compatibility

### Enum Extraction
- Identifies enum definitions in JSON structure
- Handles nested enum references
- Consolidates duplicate definitions
- Maintains enum value mappings and descriptions
- Warns about inconsistent definitions

### Enum Removal
- Safely removes enum sections
- Cleans up enum references in expressions
- Removes enum references in types
- Preserves JSON structure and formatting
- Only modifies affected files

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

2. **During Execution**:
   - Monitor error outputs
   - Check progress indicators
   - Verify file permissions

3. **After Completion**:
   - Validate output files
   - Review error logs
   - Check file integrity
   - Verify enum consistency

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

3. **Missing Enums**:
   - Verify source file structure
   - Check for nested references
   - Review error logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 