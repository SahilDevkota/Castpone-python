import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API")

def getAllNews():
    url = "https://eodhd.com/api/news"

    params = {
        "api_token" : API_KEY,
        "fmt" : "json",
        "limit" : 20
    }

    response = requests.get(url,params = params)
    news = response.json()
    return news
