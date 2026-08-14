import requests
from dotenv import load_dotenv
import os

API_KEY = os.getenv("TWELVE_DATA_API")
load_dotenv()

def getHistoricalData(symbol: str):
    response = requests.get(f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=365&apikey={API_KEY}")
    data = response.json()
    value = data["values"]
    return value