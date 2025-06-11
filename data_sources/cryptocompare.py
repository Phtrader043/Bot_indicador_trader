
import requests

API_KEY = "02816cb2d68aafdda6b92cc525cdcaf663f780978c30d9e5429d6712a52cfdff"

def get_crypto_price(pair):
    base, quote = pair.split("/")
    url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={base}&tsym={quote}&limit=10&api_key={API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()["Data"]["Data"]
        return [{"close": x["close"]} for x in data]
    return None
