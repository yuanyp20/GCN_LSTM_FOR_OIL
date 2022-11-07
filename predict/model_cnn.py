import torch
import torch.nn as nn
from torch.nn import init

device = 'cuda:1' if torch.cuda.is_available() else 'cpu'


class Net(nn.Module):
    def __init__(self, enose_dim=16, num_class=3):
        super(Net, self).__init__()  # 调用父类的构造方法

        self.encoder = nn.Conv1d(in_channels=enose_dim,out_channels=1,kernel_size=2)
        self.predictor = nn.Linear(9, 1)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)

        for name, param in self.encoder.named_parameters():
            if name.startswith("weight"):
                nn.init.xavier_normal_(param)
            else:
                nn.init.zeros_(param)

        init.xavier_uniform_(self.predictor.weight, gain=1)
    #去掉hidden
    def forward(self, input):
        '''
        input shape : (win_len, batch_size, enose_dim)
        '''
        input = input.permute(0,2,1)
        output = self.encoder(input)

        RO = self.relu(output)
        RO = self.dropout(RO)

        RO = self.predictor(RO[:, -1, :])
        RO = self.sigmoid(RO)
        # return idx_class, RO
        return RO

