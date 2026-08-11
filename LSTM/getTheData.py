from pydantic import BaseModel
from datetime import date
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader
import torch
import torch.nn as nn
from LSTM.model import AssetLSTM
import matplotlib.pyplot as plt
import joblib


model = AssetLSTM()

class DataModel(BaseModel):
    datetime : date
    open : float
    high : float
    low : float 
    close : float
    volume : int


def grabTheListOfData(list_of_data : list[DataModel]):
    list_for_lstm = []
    historical_data = sorted(list_of_data,key=lambda x: x.datetime)
    length = len(list_of_data)
    x = []
    y = []
    
    for i in range(0,length,1):
        data = historical_data[i]
        list_for_lstm.append({
                    "open_price" : data.open,
                    "high_price" : data.high,
                    "low_price" : data.low,
                    "close_price" : data.close,
                    "volume" : data.volume 
                })       

    sequence_length = 30 
    prediction_length = 5

    list_length = len(list_for_lstm)

    total_length = list_length - sequence_length - prediction_length

    for i in range(0,total_length,1):
        day_list = []
        sequence_array = list_for_lstm[i : i + sequence_length]
        for day in sequence_array:
            one_day_features = [
                day["open_price"],
                day["high_price"],
                day["low_price"],
                day["close_price"],
                day["volume"]
            ]
            day_list.append(one_day_features)
        x.append(day_list)
    
        prediction_array = list_for_lstm[sequence_length + i : sequence_length + prediction_length + i]

        
        prediction_features = []

        for j in range(prediction_length):
            prediction_features.append(prediction_array[j]["close_price"])
        y.append(prediction_features)

    X = np.array(x)
    Y = np.array(y)
        
    X_reshaped = X.reshape(-1,5)

    scaler_X = MinMaxScaler()
    scaler_Y = MinMaxScaler()

    

    X_scaled = scaler_X.fit_transform(X_reshaped)

    X_scaled = X_scaled.reshape(X.shape)
    Y_scaled = scaler_Y.fit_transform(Y)

    joblib.dump(scaler_Y,"output_scaler.pkl")


    x_train,x_test,y_train,y_test = train_test_split(
        X_scaled,
        Y_scaled,
        test_size = 0.2,
        shuffle = False
    )

    x_train_tensor = torch.tensor(x_train,dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train,dtype=torch.float32)
    x_test_tensor = torch.tensor(x_test,dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test,dtype=torch.float32)


    train_dataset = TensorDataset(x_train_tensor,y_train_tensor)
    test_dataset = TensorDataset(x_test_tensor,y_test_tensor)

    train_loader = DataLoader(
        train_dataset,
        batch_size = 8,
        shuffle = True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size  = 8,
        shuffle = False
    )

    criterion = nn.MSELoss()  #Mean Square Error (Find the difference, square them, calculate the average)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr = 0.001
    )

    epochs = 10 
    for epoch in range(epochs):
        for x_batch,y_batch in train_loader:
                predictions = model(x_batch)

                loss = criterion(predictions,y_batch)

                optimizer.zero_grad()

                loss.backward()

                optimizer.step()
        

    all_actual = []
    all_predictions =[]
    model.eval()
    with torch.no_grad():
         for x_batch,y_batch in test_loader:
              prediction = model(x_batch)
              test_loss = criterion(prediction,y_batch)

              prediction_original = scaler_Y.inverse_transform(prediction.numpy())
              all_predictions.extend(prediction_original)

              actual_original = scaler_Y.inverse_transform(y_batch.numpy())
              all_actual.extend(actual_original)    

    mae = mean_absolute_error(
            all_actual,
            all_predictions
            )
    

    rmse = root_mean_squared_error(
         all_actual,
         all_predictions
    )

    average_actual = np.mean(all_actual)
    percentage_error = (mae/average_actual) * 100


    all_actual = np.array(all_actual)
    all_predictions = np.array(all_predictions)
    plt.figure(figsize = (12,6))

    plt.plot(all_actual[:,0],label = "Actual Day 1")
    plt.plot(all_predictions[:,0],label = "Predicted Day 1")
    mae1 = mean_absolute_error(
         all_actual[:,0],
         all_predictions[:,0]
    )

    plt.plot(all_actual[:,4],label = "Actual Day 5")
    plt.plot(all_predictions[:,4],label = "Predicted Day 5")
    mae5 = mean_absolute_error(
         all_actual[:,4],
         all_predictions[:,4]
    )

    plt.xlabel("Sample")
    plt.ylabel("Price")
    plt.title("Actual vs predicted Stock Prices")
    plt.legend()
    plt.show()


    torch.save(model.state_dict(),"lstm_stock_model.pth")