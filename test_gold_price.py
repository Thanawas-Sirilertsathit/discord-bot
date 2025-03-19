from pycoingecko import CoinGeckoAPI

def get_ethereum_price():
    cg = CoinGeckoAPI()
    
    try:
        # Get the current Ethereum price in USD
        ethereum_data = cg.get_price(ids='ethereum', vs_currencies='usd')
        ethereum_price = ethereum_data['ethereum']['usd']
        return ethereum_price
    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")
        return None

# Test the function
ethereum_price = get_ethereum_price()
if ethereum_price:
    print(f"Current Ethereum price: ${ethereum_price}")
else:
    print("⚠️ Failed to fetch Ethereum price.")
