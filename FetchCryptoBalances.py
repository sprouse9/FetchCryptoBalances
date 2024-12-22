'''
Setting up json file:
Location on iCloud drive for security:
    ~/Library/Mobile Documents/com~apple~CloudDocs/config.json
'''

import os
import requests
import json
import pandas as pd
import time

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

    # df = pd.DataFrame([None] + config['addresses'], columns=['Addresses'])
    # Assuming config['addresses'] is the list of full wallet addresses
    df = pd.DataFrame([f"0x{account[-4:]}" for account in config['addresses']], columns=['Addresses'])
    df.index = range(1, len(df) + 1)

    # Initialize an empty list to store the balances
    balances = []

    for network in config["networks"]:
        balances.clear()
        
        #print(f"{network['native_coin']:<42} {'Token':<10} {'Balance':>12}")
        #print("=" * 70)

        # build the URL for GET request
        addresses_string = ','.join(config['addresses'])
        url = f"{network['api_url']}&action=balancemulti&address={addresses_string}&apikey={network['api_key']}"
        #print(url)

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
        # Now we take the balances from the JSON provided from the request
        for account in data['result']:
            balances.append(float(account['balance'])/1e18)

        # copy to the dataframe as a new column
        df[network['native_coin']] = balances

        # Add the "tokens" if any
        for token in network['tokens']:
            balances = []
            print(f"Fetching {network['native_coin']} :: {token['name']}...", end='\r')
            for address in config['addresses']:
                # a new URL must be created with the token address and the addresses to fetch from the API
                # we cannot use balancemulti as we did the native token
                url = (f"{network['api_url']}"
                f"&action=tokenbalance"
                f"&contractaddress={address}"
                f"&address={token['contract_address']}"
                f"&tag=latest"
                f"&apikey={network['api_key']}")
                
                #print(url)
                
                '''
                Example Get BEP-20 Token Account Balance by ContractAddress:
                https://api.bscscan.com/api
                &action=tokenbalance
                &contractaddress=0xe9e7cea3dedca5984780bafc599bd69add087d56
                &address=0x89e73303049ee32919903c09e8de5629b84f59eb
                &tag=latest
                &apikey=YourApiKeyToken
                '''

                # perform GET request
                response = requests.get(url, headers=headers)
                data = response.json()

                '''
                Sample Response:
                {
                    "status":"1",
                    "message":"OK",
                    "result":"1420514928941209"
                }
                '''
                balances.append(float(data['result'])/1e18)
                # print(balances)
                # copy to the dataframe as a new column
                time.sleep( (1/5) )

            df[token['name']] = balances





            #print("\n")











        
        '''
        # Check if 'result' key exists
        if 'result' in data:
            print("Result data:")
            print(json.dumps(data['result'], indent=4))  # Pretty print the result
        else:
             print("Error: 'result' key not found.")
        '''

    print(df)

    

        #print(json.dumps(data, indent=4))

# Execute the main function
if __name__ == "__main__":
    main()
