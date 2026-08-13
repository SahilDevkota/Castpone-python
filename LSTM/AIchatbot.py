from pydantic import BaseModel
from langchain_groq import ChatGroq
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
    
    model_name = "openai/gpt-oss-20b"

    groq_api_key = os.getenv("GROQ_API_KEY")

    groq = ChatGroq(
        model = model_name,
        temperature = 0.1,
        max_tokens = 1024,
        api_key = groq_api_key
    )

    query = "Should I keep this asset or not?"

    

    
    

    for batch in sentiment_batches:
        prompt = f"""
                
                You are a professional financial analyst.You're given a sentiment batch. Carefully analyse the batch and explain what the sentiment score suggest.

                Give a concise summary that can be used for the final analysis. Don't give any arithmetic operations or calculations. Don't show any calculation steps. And mainly, don't make any final investment decision.

                batch: {batch}
        
                Provide a very clear answer. Make sure you don't hallucinate or give any wrong answer. 
                """

        response = groq.invoke(prompt)

        batch_result.append(response)


    groq2 = ChatGroq(
        model = model_name,
        temperature = 0.1,
        max_tokens = 1024,
        api_key = groq_api_key

    )

    final_prompt = f"""
        You are a professional financial analyst. Analyse the financial batch list and make a final investment decision based 
        on the data batches provied. Make sure you give a proper explanation and don't include any arithmetic calcualtion or 
        operaion. You should provided a clear explanation why the asset needs to kept or not. 

        Also, provide the confidentiality score with a solid reasoning. Make sure what does the confidentiality means for example good, bad or neutral. 

        batch: 
        {batch_result}

        Provide a very clear answer. Make sure you don't hallucinate or give any wrong answer. 

        
        """ 

    final_response = groq2.invoke(final_prompt)
    return final_response.content
        
