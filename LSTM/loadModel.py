import torch
from LSTM.model import AssetLSTM
import numpy as np
import joblib
from datetime import date, timedelta

LSTMmodel = AssetLSTM()
LSTMmodel.load_state_dict(torch.load("lstm_stock_model.pth"))
LSTMmodel.eval()

input_scaler = joblib.load("input_scaler.pkl")
output_scaler = joblib.load("output_scaler.pkl")


def passTheDataToModel(listOfData):

    sorted_data = sorted(
        listOfData,
        key=lambda x: x.datetime
    )

    if len(sorted_data) == 0:
        return []

    if len(sorted_data) < 30:
        return []

    latest_data = sorted_data[-30:]

    X = []

    for data in latest_data:
        X.append([
            data.open,
            data.high,
            data.low,
            data.close,
            data.volume
        ])

    X = np.array(X, dtype=np.float64)

    X_scaled = input_scaler.transform(X)

    X_final = X_scaled.reshape(1, 30, 5)

    with torch.no_grad():
        x_tensor = torch.tensor(
            X_final,
            dtype=torch.float32
        )

        predictions = LSTMmodel(x_tensor)

    predictions = predictions.numpy()

    predictions = output_scaler.inverse_transform(
        predictions
    )

    result = []

    p = sorted_data[-1].datetime + timedelta(days=1)

    for i in range(5):

        while p.weekday() >= 5:
            p += timedelta(days=1)

        result.append({
            "prediction_date": date.today().isoformat(),
            "predicted_for_date": p.isoformat(),
            "predicted_price": float(predictions[0][i])
        })

        p += timedelta(days=1)

    return result