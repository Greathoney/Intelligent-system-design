# ID: 2018116323 (undergraduate)
# NAME: DaeHeon Yoon
# File name: hw4-3.py
# Platform: Python 3.8.8 on Windows 10
# Required Package(s): sys os numpy pandas sklearn
# (https://github.com/WegraLee/deep-learning-from-scratch/) ch05/two_layer_net.py

# coding: utf-8
import sys, os
sys.path.append(os.pardir)

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from two_layer_net import TwoLayerNet

def train_test_split(data, target, test_size, seed=1004):
    import numpy as np
    
    test_num = int(data.shape[0] * test_size)
    train_num = data.shape[0] - test_num

    np.random.seed(seed)
    shuffled = np.random.permutation(data.shape[0])
    data = data[shuffled,:]
    target = target[shuffled]
    
    x_train = data[:train_num]
    x_test = data[train_num:]
    t_train = target[:train_num]
    t_test = target[train_num:]

    return x_train, x_test, t_train, t_test

if len(sys.argv) < 2:
    print('usage: ' + sys.argv[0] + ' text_file_name')
else:
    # determine delimieter based on file extension - may be used by pandas
    # this is just to show how to use command line arguments. 
    # any modification is accepted depending on your implementation.
    if sys.argv[1][-3:].lower() == 'csv': delimeter = ','
    else: delimeter = '[ \t\n\r]'  # default is all white spaces 

    # read CSV/Text file with pandas
    df = pd.read_csv(sys.argv[1],sep=delimeter,engine='python')

    x = df.iloc[:, 1:].values
    transformer = MinMaxScaler()
    transformer.fit(x)
    x = transformer.transform(x)
    y = df.iloc[:, 0].values

    x_train, x_test, t_train, t_test = train_test_split(x, y, test_size=0.2)

    network = TwoLayerNet(input_size=13, hidden_size=50, output_size=10)

    iters_num = 10000
    train_size = x_train.shape[0]
    batch_size = 100
    learning_rate = 0.1

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    iter_per_epoch = int(max(train_size / batch_size, 1))

    for i in range(iters_num):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        # 기울기 계산
        #grad = network.numerical_gradient(x_batch, t_batch) # 수치 미분 방식
        grad = network.gradient(x_batch, t_batch) # 오차역전파법 방식(훨씬 빠르다)
        
        # 갱신
        for key in ('W1', 'b1', 'W2', 'b2'):
            network.params[key] -= learning_rate * grad[key]
        
        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)
        
        # if i % iter_per_epoch == 0:
        if i % (iter_per_epoch*300) == 0:
            train_acc = network.accuracy(x_train, t_train)
            test_acc = network.accuracy(x_test, t_test)
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            print(train_acc, test_acc)
    print(train_acc, test_acc)



    

    