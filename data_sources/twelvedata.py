
import requests

API_KEY = "cd52d4f5c5924063a7af0070445d2a3b"

def get_forex_price(pair):
    base, quote = pair.split("/")
    url = f"https://api.twelvedata.com/time_series?symbol={base}/{quote}&interval=1min&apikey={API_KEY}&outputsize=10"
    r = requests.get(url)
    if "values" in r.json():
        return [{"close": float(x["close"])} for x in reversed(r.json()["values"])]
    return None
