import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TWELVE_DATA_API")

def getAssetValue(symbol: str):
    response = requests.get(f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=1&apikey={API_KEY}")
    data = response.json()
    value = data["values"]
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    print(response.status_code)
    return value