import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
url = "https://api.bithumb.com/v1/market/all?isDetails=false"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
res_dict = json.loads(response.text) #json.dumps
print(res_dict[0].keys())
print(res_dict[0]["market"]) #마켓이름 KRW-BTC KRW 마켓
print(res_dict[0]["korean_name"]) #한글이름 비트코인
print(res_dict[0]["english_name"]) #영문이름 Bitcoin
print(res_dict[5]["market"]) #마켓이름 KRW-QTUM
print(res_dict[5]["korean_name"]) #한글이름 퀀텀
print(res_dict[5]["english_name"]) #영문이름 Qtum
print(res_dict[100]["market"]) #마켓이름 KRW-BFC
print(res_dict[100]["korean_name"]) #한글이름 바이프로스트
print(res_dict[100]["english_name"]) #영문이름 Bifrost
encrypto_names = []
for data in res_dict:
    if "KRW-" not in data["market"]:
        print(data["market"])#BTC-ETH BTC마켓
        continue
    encrypto_names.append({"symbol":data["market"].split("-")[1],
                           "eng":data["english_name"],"kor":data["korean_name"]})
print(encrypto_names)
order_currency = "BTC"
payment_currency = "KRW"
chart_intervals = "12h"
candle_url = f"https://api.bithumb.com/public/candlestick/{order_currency}_{payment_currency}/{chart_intervals}"
print(candle_url)
headers = {"accept":"application/json"}
response = requests.get(candle_url,headers=headers)
candle_data = json.loads(response.text)
if candle_data["status"]=='0000':
    print(len(candle_data["data"]))
    print(candle_data["data"][0])
    print(type(candle_data["data"][0][0]))
    d = datetime.datetime.fromtimestamp(candle_data["data"][0][0]/1000)
    print(d.year,d.month,d.day,d.hour,d.minute,d.second)
    d = datetime.datetime.fromtimestamp(candle_data["data"][-1][0]/1000)
    #날짜 데이터 > 날짜 포맷팅
    d_f = f"{d.year}년 {d.month}월 {d.day}일 {d.hour}시 {d.minute}분 {d.second}초"
    print(d_f)
    # 두 날짜 차이를 일 시 분 초로 변경
    gap = candle_data["data"][-1][0]//1000 - candle_data["data"][0][0]//1000
    gap_year = 60*60*24*365
    gap_day = 60*60*24
    gap_hour = 60*60
    gap_min = 60
    gapday = gap//gap_day
    gaphour = gap-gapday*gap_day//gap_hour
    gapmin = ((gap-gapday*gap_day)-(gaphour*gap_hour))//gap_min
    gapsec = (gap-gapday * gap_day) - (gaphour * gap_hour) - (gapmin * gap_min)
    print(gapday,"일",gaphour,"시",gapmin,"분",gapsec,"초")
    # 날짜포맷팅 > 날짜 데이터 변경
    d_conv = datetime.datetime.strptime(d_f,"%Y년 %m월 %d일 %H시 %M분 %S초")
    print(d_conv.year,"년",d_conv.month,"월",d_conv.day,"일",d_conv.hour,"시",d_conv.minute,"분",d_conv.second,"초")
    # 날짜 데이터 > 밀리세컨
    print(d_conv.timestamp)
    # print(d.year)
    # print(d.month)
    # print(d.day)
    # print(d.hour)
    # print(d.minute)
    # print(d.second)
    # print(d.microsecond)
    # 기준시간 변경
else:
    print("응답실패")
#print(response.text)



#정렬순서가 최근 데이터가 맨 뒤에
def generateData(res_data,timeslot): # 시계열 훈련데이터 생성
    x_data = [] ; y_data =[]
    for ix in range(len(source_data)-(timeslot)):
        slot_data = []
        for cur_ix in range(ix,timeslot+ix):
            slot_data.append(source_data[cur_ix])
        x_data.append(slot_data)
        if ix==0 or ix==1:print(slot_data)
        y_data.append(source_data[timeslot+ix])
        if ix==0 or ix==1:print("정답:",source_data[timeslot+ix])
    return np.array(x_data),np.array(y_data)

def confirm_data(x_data,y_data): #문제데이터와 정답데이터의 일치성 확인
    result_bool=True
    if y_data[0]! = x_data[1][-1]:
        result_bool=False
    if y_data[1]! = x_data[2][-1]:
        result_bool=False
    if y_data[-1]! = source_data[-1]: # 마지막 데이터 확인
        result_bool=False
    if y_data[-2]! = source_data[-2]:
        result_bool=False
    return result_bool #True일때 일치

def scatterAnal(x_data,y_data): #산점도
    # 가중평균 적용
    cvdata = np.average(x_data,axis=1,weights=(0.02,0.05,0.05,0.08,0.08,0.1,0.13,0.15,0.16,0.18))
    print(cvdata.shape)
    plt.scatter(cvdata,y_data)
    plt.show()

if __name__=="__main__":
    pass
# raw_data=np.array(candle_data["data"])
# source_data=raw_data[:,1]
# print("10",source_data[10])
# x_data,y_data = generateData(source_data,10)
# print(x_data.shape)
# print("정답문제일치성:",y_data[0]==x_data[1][-1])
# print("정답문제일치성:",y_data[1]==x_data[2][-1])
# print("정답문제일치성:",y_data[0]==x_data[2][-2])
# # 맨 마지막 데이터
# print("마지막데이터일치성:",y_data[-1]==source_data[-1])
# print("마지막데이터일치성:",y_data[-2]==source_data[-2])
# print(x_data.shape)
# print(y_data.shape)
# scatterAnal(x_data,y_data)
# print(d_conv.timestamp())