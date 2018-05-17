#coding=utf8
import requests
import itchat, time
from itchat.content import *
from pymongo import MongoClient
import os,json
import datetime


# host = '115.28.106.252'
# client = MongoClient(host)
# client.wx.authenticate("xlelou", "wx123456.", mechanism='MONGODB-CR')
# db = client["wx"]
# collection = db["acol"]
KEY = 'ea794b8d4619440699c754179780e752'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'GUU',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return




def doSth(toUser):

    parameters = {'key':'c257ab165b705431cec519e2ea4bcc44','city':'370502','extensions':'all','output':'JSON'}
    r = requests.get('http://restapi.amap.com/v3/weather/weatherInfo', params=parameters)
    obj = json.loads(r.text)
    weather = '地区：大东营帝国\r\n' + '搜集日期：' 
    for i in obj['forecasts']:
    	weather += i['reporttime'] + '\r\n'
    	for j in i['casts']:
    		weather += '日期：' + j['date'] + '\r\n' + '白天天气：' + j['dayweather'] + '\r\n' +'夜间天气：'+ j['nightweather'] + '\r\n' +'白天温度：' + j['daytemp'] + '\r\n' + '夜间温度：' + j['nighttemp'] + '\r\n'
    	
    # 发给自己
    itchat.send(weather,toUser)
    # 一分钟只做一件事
   # time.sleep(60)


def main(h,m):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour==h and now.minute==m:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(20)
        # 做正事，一天做一次
        doSth() 

client = MongoClient("mongodb://xlelou:lanchlot@115.28.106.252:17117")
client.wx.authenticate("xlelou", "wx123456.")
# client = MongoClient("mongodb://localhost:27017")
# print (time.strftime("%Y-%m-%d"))
wx = client.wx
# collection = wx["test"]
# print(collection.find_one())
collectionName = time.strftime("%Y-%m-%d")

collection = wx[collectionName]

# 通过该命令安装该API： pip install NetEaseMusicApi
# from NetEaseMusicApi import interact_select_song
 
# HELP_MSG = u'''\
# 欢迎使用微信网易云音乐
# 帮助： 显示帮助
# 关闭： 关闭歌曲
# 歌名： 按照引导播放音乐\
# '''

# with open('stop.mp3', 'w') as f: pass
# def close_music():
#     os.startfile('stop.mp3')

def lc():
    print('登陆成功')
def ec():
    print('退出')

# ##音乐
# @itchat.msg_register(itchat.content.TEXT)
# def music_player(msg):
#     if msg['ToUserName'] != 'filehelper': return
#     if msg['Text'] == u'关闭':
#         close_music()
#         itchat.send(u'音乐已关闭', 'filehelper')
#     if msg['Text'] == u'帮助':
#         itchat.send(u'帮助信息', 'filehelper')
#     else:
#         itchat.send(interact_select_song(msg['Text']), 'filehelper')

# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
def text_reply(msg):
	 # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
 
    reply = get_response(msg['Text'])
    if msg['Text'] == '天气':
    	doSth(msg['FromUserName'])
    else:
    	itchat.send(reply, msg['FromUserName'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    # return reply or defaultReply
    

# 自动回复图片等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
# def download_files(msg):
# 	itchat.send('感谢你加我为好友，如果需要，请联系我得微信大号：xlelou', msg['FromUserName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('你好哇', msg['RecommendInfo']['UserName'])

# print(itchat.get_friends())


# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply_text(msg):
    	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# print(msg)
	# 发送者的昵称
	username = msg['ActualNickName']
	collection.insert({'name':username,'chatroom':msg['User'].NickName,'content':msg['Content'],'time':time.strftime("%Y-%m-%d %H:%M:%S")})
	# print(msg['ActualNickName'] + '--=====---' +msg['Content']+'======='+chatroom_id)
	# 消息并不是来自于需要同步的群
	if not chatroom_id in chatroom_ids:
		return

	if msg['Type'] == TEXT:
		content = msg['Content']
	elif msg['Type'] == SHARING:
		content = msg['Text']

	# # 根据消息类型转发至其他群
	# if msg['Type'] == TEXT:
	# 	for item in chatrooms:
	# 		if not item['UserName'] == chatroom_id:
	# 			itchat.send('%s\n%s' % (username, msg['Content']), item['UserName'])
	# elif msg['Type'] == SHARING:
	# 	for item in chatrooms:
	# 		if not item['UserName'] == chatroom_id:
	# 			itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), item['UserName'])

# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息          
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# 发送者的昵称
	username = msg['ActualNickName']
	# print(msg['ActualNickName'] + '--=====---' +msg['Content']+'======='+chatroom_id)
	# 消息并不是来自于需要同步的群
	if not chatroom_id in chatroom_ids:
		return

	# 如果为gif图片则不转发
	# if msg['FileName'][-4:] == '.gif':
	# 	return

	# 根据消息类型转发至其他群
	# msg['Text'](msg['FileName'])
	# for item in chatrooms:
	# 	if not item['UserName'] == chatroom_id:
	# 		itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item['UserName'])


 # 扫二维码登录
# itchat.auto_login(hotReload=True, loginCallback=lc, exitCallback=ec)
itchat.auto_login(enableCmdQR=2)

# itchat.auto_login()

# 音乐控制
# itchat.send(HELP_MSG, 'filehelper') 
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
chatroom_ids = [c['UserName'] for c in chatrooms]
print ('正在监测的群聊：', len(chatrooms), '个')
print (' '.join([item['NickName'] for item in chatrooms]))

# 开始监测
itchat.run()   
     

