from sentiment import get_sentiment
import requests

sentiment_list = get_sentiment()

url = "http://localhost:8081/SentimentEntity/store"

def sendReq():
    for item in sentiment_list:
        response = requests.post(url,json = {
            "Title" : item['Text'],
            "Source" : item['Source'],
            "Sentiment" : item['Sentiment'],
            "Sentiment_label" : item['Sentiment_label']
        })
        print(response)

sendReq()

