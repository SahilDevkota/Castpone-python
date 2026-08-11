import torch
from LSTM.model import AssetLSTM
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from datetime import date , timedelta


LSTMmodel = AssetLSTM()
LSTMmodel.load_state_dict(torch.load("lstm_stock_model.pth"))

def passTheDataToModel(listOfData):
    list_of_data_for_lstm = []
    length = len(listOfData)
    sorted_data = sorted(listOfData, key = lambda x : x.datetime)
    
    x=[]

    for i in range(0,length,1):
        data = sorted_data[i]
        list_of_data_for_lstm.append({
            "open": data.open,
            "close" : data.close,
            "high": data.high,
            "low" : data.low,
            "volume": data.volume
        })

    sequence_length = 30
    total_length = len(list_of_data_for_lstm) - sequence_length - 5
    
    for i in range(0,total_length,1):
        day_list=[]
        day_features = list_of_data_for_lstm[i: i + sequence_length]
        for day in day_features:
            one_day = [
                day["open"],
                day["close"],
                day["high"],
                day["low"],
                day["volume"]
            ]
            day_list.append(one_day)
        x.append(day_list)
   
    X = np.array(x)
    x_reshape = X.reshape(-1,5)
    x_scaler = MinMaxScaler()
    x_scaler.fit(x_reshape)
    x_scaled = x_scaler.transform(x_reshape)
    x_final = x_scaled.reshape(X.shape)

    LSTMmodel.eval()
    y =[]
    with torch.no_grad():
        x_tensor = torch.tensor(x_final,dtype = torch.float32)
        predictions = LSTMmodel(x_tensor)
    final_prediction = predictions[-1].numpy()
        

    Y_scaler = joblib.load("output_scaler.pkl")
    output_scaled_prediction = Y_scaler.inverse_transform(
        final_prediction.reshape(1,-1)
    )

    output_length = len(output_scaled_prediction[0])
    output_prediction_array = []
    prediction = []

    p = date.today() + timedelta(days=1)





   

    
   
  
            
    