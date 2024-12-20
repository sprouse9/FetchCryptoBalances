'''
Setting up json file:
Location on iCloud drive for security:
    ~/Library/Mobile Documents/com~apple~CloudDocs/config.json
'''

import os
import requests
import json


# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://www.google.com',
    'Accept-Encoding': 'gzip, deflate, br'
}

def load_config(file_path):
    """Load the JSON configuration file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    
    # Let's start by importing the config JSON file
    # 
    # Expand the '~' to the full path
    config_path = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/config.json")
    
    config = load_config(config_path)





    for network in config["networks"]:
        #print(f"\n--- {network['name']} ---")
        #print(f"{network['name']:<42} {'Coin':<8} {'Token':<10} {'Balance':>12}")
        print(f"{network['name']:<42} {'Token':<10} {'Balance':>12}")
        print("=" * 70)

    mm_addresses = config["addresses"]

    print("\n", type(mm_addresses))



# Execute the main function
if __name__ == "__main__":
    main()
