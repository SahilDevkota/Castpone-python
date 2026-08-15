
from market import getMarketResponse,getNews,getNewsList
from sentiment import sentimentForNews,requestModel
from LSTM.getTheData import DataModel,grabTheListOfData
from LSTM.loadModel import passTheDataToModel
from social_media_sentiment import getComments,youtubeDataDTO,sendSentiment
from historicalData import getHistoricalData
from LSTM.AIchatbot import AIrequestModel,getTheData
from assetValuation import getAssetValue
from getNewsOnly import getAllNews
from fastapi import FastAPI



app = FastAPI()


@app.post("/getSentimentForNews")
def getSentimentForNews(news: list[requestModel]):
    return sentimentForNews(news)

@app.get("/getNewsList")
def getTheListOfNews():
    return getNewsList()

@app.get("/getNews")
def getTheNews(symbol:str):
    return getNews(symbol)

@app.get("/getMarketData")
def MarketResponse(symbol:str):
    return getMarketResponse(symbol)

@app.get("/getYoutubeData")
def youtubeData(symbol:str):
    return getComments(symbol)

@app.post("/sendSentiment")
def sendTheSentimentValue(youtubeData : list[youtubeDataDTO]):
    return sendSentiment(youtubeData)

@app.get("/getHistoricalData")
def getTheHistoricalData(symbol:str):
    return getHistoricalData(symbol)

@app.post("/getDataforLSTM")
def getTheDataForLSTM(datalist : list[DataModel]):
    return passTheDataToModel(datalist)

@app.post("/getDataForAI")
def getTheDataForAI(datalist: AIrequestModel):
    return getTheData(datalist)

@app.get("/getTheMarketValue")
def getTheValue(symbol:str):
    return getAssetValue(symbol)

@app.get("/getAllNews")
def getNewsFromMarket():
    return getAllNews()
