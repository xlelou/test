from wxpy import *

bot = Bot(console_qr = True)

tuling = Tuling(api_key='5397e106da5b408d8a74fc1007db4450')

@bot.register(msg_types = FRIENDS)
def auto_accept_friends(msg):
    new_friend = bot.accept.friend(msg.card)
    new_friend.send('哈哈哈，就知道你会加我为好友！')

@bot.register(msg_types =[TEXT, MAP, CARD, NOTE, SHARING],chats=User,except_self=True, run_async=True, enabled=True)
def reply_my_friend(msg):
    tuling.do_reply(msg)
    print(msg)
bot.join()