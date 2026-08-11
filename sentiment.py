import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from fastapi import FastAPI
from enum import Enum
from youtube_comments import getComments
from market import getMarketResponse
from pydantic import BaseModel
from datetime import date


class requestModel(BaseModel):
    symbol : str
    headline : str
    summary : str 
    source : str
    url : str 
    

def sentimentForNews(news:list[requestModel]):
    title_list = []
    length = len(news)
    model_name = "ProsusAI/finbert"
    batch_size = 3
    sentiment_list = []

    positive_index = 0
    negative_index = 1 
    neutral_index = 2

    final_sentiment =[]

    sum = 0
    average = 0 

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    for i in range(0,length,1):
        title = news[i].headline + ". " + news[i].summary
        title_list.append(title)

    for i in range(0,length,batch_size):
        batch = title_list[i:i+batch_size]
        input = tokenizer(
            batch,
            return_tensors = "pt",
            padding = True,
            truncation= True
        )
        output = model(**input)
        probabilities = torch.nn.functional.softmax(output.logits,dim =1)
        sentiment_value,sentiment_indices = torch.max(probabilities,dim = 1)
        sentiment_value = sentiment_value.tolist()
        sentiment_indices = sentiment_indices.tolist()

        for value,index in zip(sentiment_value,sentiment_indices):
            if index == positive_index:
                sentiment_list.append({
                    "value" : value,
                    "label" : "POSITIVE"
                })
            elif index == negative_index:
                 sentiment_list.append({
                                    "value" : -value,
                                    "label" : "NEGATIVE"
                                })
            else: 
                     sentiment_list.append({
                                        "value" : 0,
                                        "label" : "NEUTRAL"
                                    })
                


    if(len(news)==len(sentiment_list)):
        for i in range(0,len(sentiment_list),1):
            sentiment = sentiment_list[i]
            values = sentiment["value"]
            label = sentiment["label"]
            title = news[i].headline + ". " + news[i].summary

            print(news)

            final_sentiment.append(
                {
                    "symbol" : news[i].symbol,
                    "text" : title,
                    "created_at" :  date.today(),
                    "sentimentLabel" : label,
                    "sentimentScore" : values
                }
            )
        return final_sentiment
    else:
         return []

    