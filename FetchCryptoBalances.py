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



    for network in config["test_networks"]:

        print(f"{network['native_coin']:<42} {'Token':<10} {'Balance':>12}")
        print("=" * 70)

        # build the URL for GET request
        addresses_string = ','.join(config['addresses'])
        url = f"{network['api_url']}{addresses_string}&apikey={network['api_key']}"
        print(url)

        # Fetch BSC balances
        response = requests.get(url, headers=headers)
        data = response.json()

        '''
        data looks like this:
        # {'status': '1', 'message': 'OK', 'result': 
        # [
        # {'account': '0x3aBcD1eF4A5b6C7D8e9F0aBc1D234567890abcde', 'balance': '0'}, 
        # {'account': '0x7aBcD9fE2a8B4C3D1eF0A5cB6d7E9F01234aBcDe', 'balance': '26586077308444'},
            ...
          ]
        '''

        print("\n", data)


        #f"https://api.bscscan.com/api?module=account&action=balancemulti&address={mm_addresses}&apikey={bsc_apikey}"



    mm_addresses = config["addresses"]

    print("\n", type(mm_addresses))



# Execute the main function
if __name__ == "__main__":
    main()
