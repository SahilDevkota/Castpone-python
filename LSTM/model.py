import torch.nn as nn

class AssetLSTM(nn.Module):
    def __init__(self):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size = 5,
            hidden_size = 64,
            num_layers = 1,
            batch_first = True
        )

        self.linear = nn.Linear(64,5)

    def forward(self,x):
        output, (hidden,cell) = self.lstm(x)

        output = output[:,-1,:]
        output = self.linear(output)
        return output