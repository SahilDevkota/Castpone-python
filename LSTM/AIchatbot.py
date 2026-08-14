from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

class AIrequestModel(BaseModel):
    predictionPriceList : list
    sentimentList: list

def getTheData(list_of_data : AIrequestModel):
    prediction_price_list = list_of_data.predictionPriceList
    sentiment_list = list_of_data.sentimentList

    sentiments = []

    for sentiment in sentiment_list:
        sentiments.append({
            "symbol" : sentiment['symbol'],
            "sentiment_label" : sentiment['sentimentLabel'],
            "sentiment_score" : sentiment["sentimentScore"],
            "created_at" : sentiment["created_at"]

        })

   

    batch_size = 20

    sentiment_batches = [
        sentiments[i : i+batch_size]
        for i in range(0,len(sentiments),batch_size)
    ]

    batch_result =[]
    
    load_dotenv()

    client = genai.Client(
            api_key = os.getenv("GEMINI_API_KEY")
        )
    

    query = "Should I keep this asset or not?"

    prompt = f"""

    You're a financial expert. You're given sentiment and price prediction list of certain asset. Analyse the given data and give a final investment decision. 
    Make sure you provide confidientiality score and explain the reason behind the scoring as well. 
    Make sure you give a proper explanation and don't include any arithmetic calcualtion or 
    operation. You should provided a clear explanation why the asset needs to kept or not. 
    Remove the "#" symbols and present it in a professional way. 

    query:
    {query}

    sentiment : 
    {sentiment_list}

    prediction_price : 
    {prediction_price_list}

    Provide a very clear answer. Make sure you don't hallucinate or give any wrong answer. 
    
    """

    final_response = client.models.generate_content(
            model = "gemini-3.6-flash",
            contents = prompt
        )
    return final_response.text


   