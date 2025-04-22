import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """
    Load configuration from environment variables or .env file
    
    :return: Dictionary with configuration settings
    """
    config = {
        'bearer_token': os.getenv('BEARER_TOKEN'),
        'user_access_token': os.getenv('USER_ACCESS_TOKEN'),
        'input_file': os.getenv('INPUT_FILE'),
        'output_directory': os.getenv('OUTPUT_DIRECTORY')
    }
    
    # Validate required configuration
    if not config['bearer_token'] or not config['user_access_token']:
        raise ValueError("""
        Missing required tokens. 
        Please set BEARER_TOKEN and USER_ACCESS_TOKEN in your .env file or environment variables.
        
        Example .env file contents:
        BEARER_TOKEN=your_bearer_token_here
        USER_ACCESS_TOKEN=your_user_access_token_here
        INPUT_FILE=input_sistemas.json
        OUTPUT_DIRECTORY=metadata_output
        """)
    
    return config

def scrape_metadata(config):
    """
    Scrape metadata for each active resource in the input JSON file
    
    :param config: Configuration dictionary with tokens and file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(config['output_directory'], exist_ok=True)
    
    # Read the input JSON file
    with open(config['input_file'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Base URL for metadata requests
    base_url = "https://plataforma-dados.betha.cloud/dados/api/sistemas/@current/ativos/{}/metadados"
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {config["bearer_token"]}',
        'User-Access': config['user_access_token']
    }
    
    print("print do header env", headers)
    
    # Tracking for logging
    total_resources = len(data.get('ativos', []))
    processed_resources = 0
    errors = []
    
    # Process each active resource
    for ativo in data.get('ativos', []):
        try:
            # Construct full metadata URL
            metadata_url = base_url.format(ativo['id'])
            
            # Make the request with headers
            response = requests.get(metadata_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses
            
            
            
            # Parse the metadata
            metadata = response.json()
            
            # Create a filename for the metadata
            filename = f"{ativo['tema']}_{ativo['nome']}.json"
            filepath = os.path.join(config['output_directory'], filename)
            
            # Sanitize filename to remove any invalid characters
            filename = "".join(x for x in filename if x.isalnum() or x in "._- ")
            filepath = os.path.join(config['output_directory'], filename)
            
            # Save the metadata to a file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            
            # Update progress
            processed_resources += 1
            print(f"Processed: {ativo['tema']} - {ativo['nome']} (ID: {ativo['id']})")
        
        except requests.RequestException as e:
            print(f"Error processing {ativo['tema']} - {ativo['nome']} (ID: {ativo['id']}): {e}")
            print(f"Request URL: {metadata_url}")
            print(f"Request Headers: {headers}")
            errors.append({
                'tema': ativo.get('tema', 'Unknown'),
                'nome': ativo.get('nome', 'Unknown'),
                'id': ativo.get('id', 'Unknown'),
                'error': str(e),
                'url': metadata_url,
                'headers': headers
            })
            print(f"Error processing {ativo['tema']} - {ativo['nome']} (ID: {ativo['id']}): {e}")
            errors.append({
                'tema': ativo.get('tema', 'Unknown'),
                'nome': ativo.get('nome', 'Unknown'),
                'id': ativo.get('id', 'Unknown'),
                'error': str(e)
            })
        except Exception as e:
            print(f"Unexpected error processing {ativo.get('tema', 'Unknown')}: {e}")
            errors.append({
                'tema': ativo.get('tema', 'Unknown'),
                'nome': ativo.get('nome', 'Unknown'),
                'id': ativo.get('id', 'Unknown'),
                'error': str(e)
            })
    
    # Print summary
    print("\n--- Scraping Summary ---")
    print(f"Total Resources: {total_resources}")
    print(f"Processed Resources: {processed_resources}")
    print(f"Failed Resources: {len(errors)}")
    
    # Save errors to a file if any
    if errors:
        errors_filepath = os.path.join(config['output_directory'], 'scraping_errors.json')
        with open(errors_filepath, 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=4)
        print(f"Error details saved to {errors_filepath}")

def main():
    try:
        # Load configuration
        config = load_config()
        
        # Run metadata scraping
        scrape_metadata(config)
        
        print("\nMetadata scraping completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you could log the full traceback
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    main()