#coding=utf8
import itchat, time
from itchat.content import *
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:17017/")
# print (time.strftime("%Y-%m-%d"))
wx = client.wx
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

#自动回复文本等类别消息
#isGroupChat=False表示非群聊消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
# def text_reply(msg):
# 	itchat.send('感谢你加我为好友，如果需要，请联系我得微信大号：xlelou', msg['FromUserName'])

# 自动回复图片等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
# def download_files(msg):
# 	itchat.send('感谢你加我为好友，如果需要，请联系我得微信大号：xlelou', msg['FromUserName'])

# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
#     itchat.send_msg('你好哇，请联系我得微信大号：xlelou', msg['RecommendInfo']['UserName'])

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
itchat.auto_login(hotReload=True, loginCallback=lc, exitCallback=ec)

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

