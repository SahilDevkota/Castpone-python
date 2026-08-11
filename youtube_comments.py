#from social_media_sentiment import getId
from config import API_KEY
from fastapi import FastAPI
import requests
import html

app = FastAPI()

comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"

comments = []
comment_list=[]

# def getComment():


#     for id in youtube_id:
#         query = {
#             "key" : API_KEY,    
#             "part" : "snippet",
#             "videoId": id,
#             "relevanceLanguage" : "en"
#         }

#         response = requests.get(comment_url,params = query)
#         comments.append(response.json())

#         for comment in comments:
#             items = comment['items']

#             for item in items:
#                 text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#                 text = html.unescape(text)
#                 if "tsla" in text.lower() or "tesla" in text.lower(): 
#                     comment_list.append({
#                         "Text" : text,
#                         "Source" : "Youtube",
#                         "Ticker" : "TSLA",
#                         "Published At": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
#                     })
#     return {
#         "Text" : "Tesla just got an amazing feature check it out.",
#         "Source" : "Youtube",
#         "Ticker" : "TSLA",
#         "Published At": "2026/07/11"
#     }


def getComments():
    return {
        "Text" : "Tesla just got an amazing feature check it out.",
        "Source" : "YOUTUBE",
        "Ticker" : "TSLA",
        "Published At": "2026/07/11"
    }
