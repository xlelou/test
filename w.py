import requests
import itchat, time
from itchat.content import *
from pymongo import MongoClient
import os,json
import datetime
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
r = requests.get('http://news.people.com.cn/210801/211150/index.js?_=1526572197066', headers = headers)
content = json.loads(r.text)

print(len(content['items']))
for i in range(len(content['items'])):
	if i < 10:
		print(content['items'][i])







# def doSth():

#     print('test')
#     parameters = {'key':'c257ab165b705431cec519e2ea4bcc44','city':'370502','extensions':'all','output':'JSON'}
# 	r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo', params=parameters)
# 	print((r.text))

#     # 假装做这件事情需要一分钟

#     time.sleep(60)



# def main(h=22, m=17):

#     '''h表示设定的小时，m为设定的分钟'''

#     while True:

#         # 判断是否达到设定时间，例如0:00

#         while True:

#             now = datetime.datetime.now()

#             # 到达设定时间，结束内循环

#             if now.hour==h and now.minute==m:

#                 break

#             # 不到时间就等20秒之后再次检测

#             time.sleep(20)

#         # 做正事，一天做一次

#         doSth()



# main()


#  

# def w():
#     parameters = {'key':'c257ab165b705431cec519e2ea4bcc44','city':'370502','extensions':'all','output':'JSON'}
#     r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo', params=parameters)
#     obj = json.loads(r.text)
#     # print(obj['forecasts'])
#     weather = '地区：大东营帝国\r\n' + '搜集日期：' 
#     for i in obj['forecasts']:
#     	weather += i['reporttime'] + '\r\n'
#     	for j in i['casts']:
#     		weather += '日期：' + j['date'] + '\r\n' + '白天天气：' + j['dayweather'] + '\r\n' +'夜间天气：'+ j['nightweather'] + '\r\n' +'白天温度：' + j['daytemp'] + '\r\n' + '夜间温度：' + j['nighttemp'] + '\r\n'
#     	print(weather)
    

# w()