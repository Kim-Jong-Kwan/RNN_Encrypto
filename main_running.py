from itertools import count

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from anal_data import getInitName, getCandleData, generateData, confirm_data, scatterAnal
from util import cv_format,cv_mill2date,cv_date2milli,cv_str2date,gapCompare
from RNN_constructure import constructureModel
weight_avg = (0.005,0.005,0.007,0.007,0.008,0.008,0.009,0.009,0.009,0.01,\
              0.01,0.02,0.02,0.03,0.03,0.03,0.04,0.04,0.04,0.04,\
              0.045,0.045,0.05,0.05,0.06,0.065,0.07,0.076,0.08,0.082)
timeslot=30
count_epoch=300
if len(weight_avg)!=timeslot:
    print("가중치와 타임슬롯 수량을 동일하게 맞춰주세요")
# 1.화폐이름 목록 추출
names=getInitName()
print(names[0])
# 2.화폐 캔들 데이터 수신
candle_datas = getCandleData(currency="BTC",times="24h",payment="KRW")
print(type(candle_datas.keys()))
if candle_datas["status"]=="0000":
    # 3.훈련데이터 분석
    source_datas = np.array(candle_datas["data"])
    print(source_datas[:,1])

    # 4.데이터 일치성확인
    x_data_start, y_data_start = generateData(source_datas[:,1], timeslot)
    res = confirm_data(x_data_start,y_data_start,source_datas[:,1])
    if res:
        print("모든데이터 정답과 일치")
    else:print("데이터 혼합 잘못됨")
    scatterAnal(x_data_start,y_data_start,weight_avg,"start price")

    x_data_end, y_data_end = generateData(source_datas[:, 2], timeslot)
    res = confirm_data(x_data_end, y_data_end, source_datas[:,2])
    if res:
        print("모든데이터 정답과 일치")
    else:
        print("데이터 혼합 잘못됨")
    scatterAnal(x_data_end, y_data_end, weight_avg, "end price")

    x_data_high, y_data_high = generateData(source_datas[:, 3], timeslot)
    res = confirm_data(x_data_high, y_data_high, source_datas[:,3])
    if res:
        print("모든데이터 정답과 일치")
    else:
        print("데이터 혼합 잘못됨")
    scatterAnal(x_data_high, y_data_high, weight_avg, "maxhigh price")

    x_data_low, y_data_low = generateData(source_datas[:, 4], timeslot)
    res = confirm_data(x_data_low, y_data_low, source_datas[:,4])
    if res:
        print("모든데이터 정답과 일치")
    else:
        print("데이터 혼합 잘못됨")
    scatterAnal(x_data_low, y_data_low, weight_avg, "minlow price")

    x_data_amount, y_data_amount = generateData(source_datas[:, 5], timeslot)
    res = confirm_data(x_data_amount, y_data_amount, source_datas[:,5])
    if res:
        print("모든데이터 정답과 일치")
    else:
        print("데이터 혼합 잘못됨")
    scatterAnal(x_data_amount, y_data_amount, weight_avg, "trade quantity")

else:print("데이터 수신 실패")

# 최종 데이터 생성
x_data_start
x_data_end
x_data_high
x_data_low
x_data_amount
print(x_data_start.shape)
print(type(x_data_start))
x_dataset=[]
for ix in range(len(x_data_start)):
    x_d=[]
    for tx in range(timeslot):
        x_d.append(sum([x_data_start[ix][tx],x_data_end[ix][tx] , \
                       x_data_high[ix][tx],x_data_low[ix][tx]]) / 4)
    x_dataset.append(x_d)
y_dataset=[]
for ix in range(len(y_data_start)):

    y_dataset.append(
        sum([y_data_start[ix], y_data_end[ix], \
                   y_data_high[ix], y_data_low[ix]]) / 4)

x_data = np.array(x_dataset)
y_data = np.array(y_dataset).reshape(len(y_dataset),-1)
print(x_data.shape)
print(y_data.shape)
print(type(x_data[0]))
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x_data = scaler.fit_transform(x_data).reshape(len(x_data),timeslot,-1)
y_data = scaler.fit_transform(y_data)
print("dim",x_data.ndim)
print(x_data[0][:10])
print(y_data[:10])
# LSTM모델 생성
rmodel = constructureModel(timeslot)
fit_his = rmodel.fit(x_data,y_data,epochs=count_epoch,batch_size=len(x_data))
rmodel.save("rnn_model.keras")
import pickle
with open("fit_history","wb") as fp:
    pickle.dump(fit_his,fp)