import tensorflow as tf
from tensorflow.keras import Input,Sequential
from tensorflow.keras.layers import Dense,LSTM,Dropout
timeslot=30
def constructureModel(x_data):
    rmodel = Sequential()
    rmodel.add(Input(shape=(timeslot,1)))
# units,activation='tanh',recurrent_activation='sigmoid',dropout=0.8
# recurrent_dropout=0.0, return_sequences=False,return_state=False,
# return_sequences = True이면 순회시 가중치를 모두 추출
# return_sequences = False이면 마지막 가중치를 모두 추출
    rmodel.add(LSTM(128,dropout=0.2,recurrent_dropout=0.2,return_sequences=True))
    rmodel.add(Dropout(0.2))
    rmodel.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2, return_sequences=True))
    rmodel.add(Dropout(0.2))
    rmodel.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2, return_sequences=False))
    rmodel.add(Dropout(0.2))
    rmodel.add(Dense(1)) #회귀문제로 가중치를 그대로 출력한다.

    rmodel.compile(loss="mse",optimizer="adam",metrics=["acc"])
    return rmodel

