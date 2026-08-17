import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY_1 = os.getenv("SECRET_API_KEY")
API_KEY_2 = os.getenv("MARKET_API_KEY")


stocks = []
symbols=[]
article_data=[]
market_data=[]
stock_list=[]
query_list =[]


def getMarketResponse(symbol):

        response = requests.get(f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&apikey={API_KEY_2}")
        response_json = response.json()

        return response_json["values"]

def getNewsList():

        all_articles=[]
        
        response = requests.get("https://finnhub.io/api/v1/company-news",params = {
                "category": "general",
                "token": API_KEY_1
        })
        articles = response.json()
        print(articles)
        # for article in articles:
        #         timestamp = article["datetime"]
        #         date = datetime.fromtimestamp(timestamp).date()
        #         all_articles.append({
        #                 "headline": article["headline"],
        #                 "summary" : article["summary"],
        #                 "date" : date,
        #                 "url" : article["url"],
        #                 "source" : article["source"]
        #         })

        # print(all_articles)
        # return all_articles
        
def getNews(symbol):

        all_articles=[]
        
        response = requests.get("https://finnhub.io/api/v1/company-news",params = {
                "symbol" : symbol,
                "from" : "2025-08-01",
                "to" : "2026-08-17",
                "token": API_KEY_1
        })
        articles = response.json()
        for article in articles:
                timestamp = article["datetime"]
                date = datetime.fromtimestamp(timestamp).date()
                all_articles.append({
                        "headline": article["headline"],
                        "summary" : article["summary"],
                        "date" : date,
                        "url" : article["url"],
                        "source" : article["source"]
                })
        return all_articles

               
        
                                
                

        