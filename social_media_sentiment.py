import requests
from fastapi import FastAPI
from config import API_KEY
from pydantic import BaseModel
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

search_url = "https://www.googleapis.com/youtube/v3/search"
comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"

app = FastAPI()

social_data=[]
next_token =None
youtube_id = []

class youtubeDataDTO(BaseModel):
    comment : str
    published_at : datetime
    symbol: str


def getComments(symbol):
    video_id = []
    comment_list=[]
    search_param = {
            "part" : "snippet",
            "q" : symbol + " stock",
            "type" : "video",
            "maxResults" : 50,
            "key" : API_KEY,
            "publishedAfter" : "2026-01-01T00:00:00Z",
            "publishedBefore" : "2026-07-12T00:00:00Z"
    }

  
    response = requests.get(search_url,params = search_param)
    response_json = response.json()
    items = response_json['items']
    for item in items:
        id = item['id']['videoId']
        video_id.append(id)

    for id in video_id:
        comment_param ={
                "part" : "snippet",
                "videoId":  id,
                "maxResults" : 10,
                "key" : API_KEY
            }
        response = requests.get(comment_url,params = comment_param)
        data = response.json()
        items = data['items']
        for item in items:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            published_date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            comment_list.append({
                "comment" : comment,
                "published_at" : published_date
            })
        return comment_list
    
def sendSentiment(youtubeData : list[youtubeDataDTO]):
    commentList = []
    length = len(youtubeData)
    model_name = "ProsusAI/finbert"
    sentiment_value_list = []
    positive_index = 0
    negative_index = 1 
    

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    for data in youtubeData:
        commentList.append(data.comment)

    batch_size = 3

    for i in range(0,length, batch_size):
        batch = commentList[i:i+batch_size]
        input = tokenizer(
            batch,
            return_tensors = "pt",
            padding = True,
            truncation = True
        )
        output = model(**input)
        probabilities = torch.nn.functional.softmax(output.logits,dim = 1)
        sentiment_value,sentiment_indices = torch.max(probabilities,dim =1)
        sentiment_value = sentiment_value.tolist()
        sentiment_indices = sentiment_indices.tolist()

        for value,indices in zip(sentiment_value,sentiment_indices):
            if(indices == positive_index):
                sentiment_value_list.append(value)
            elif(indices == negative_index):
                sentiment_value_list.append(-value)
            else:
                sentiment_value_list.append(0)

    sum = 0
    average = 0

    for sentiment in sentiment_value_list:
        sum += sentiment
    
    average = sum / length
    return average




    

