from wxpy import *

bot = Bot()

tuling = Tuling(api_key='5397e106da5b408d8a74fc1007db4450')

group = bot.groups().search('a')[0]

@bot.register(chats=Friend,except_self=True, run_async=True, enabled=True)
def reply_my_friend(msg):
    if msg.type == 'FRIENDS':
        print (1)
        new_friend = msg.card.accept()
        new_friend.send('哈哈哈，就知道你会加我为好友！回复 "aaa" 可以加群啊')
    else:
        if msg.type != 'Text':
            msg.sender.send('暂时无法识别该类型，你可以只打字啊')
        else:
            if msg.text == 'aaa':
                friend = msg.sender
                if friend in group:
                    friend.send('你已经在群里了')
                else:
                    group.add_members(friend,use_invitation=True)
            else:
                tuling.do_reply(msg)
    print(msg.text)


@bot.register(chats=group,except_self=True, run_async=True, enabled=True)
def reply_msg(msg):
    a = set(group.members)
    group.update_group(members_details=False)
    b = set(group.members)
    c = list(b.difference(a))
    if c != '':
        d = c[0]
        d = str(d)
        d = d[9:-1]
        group.send('''[鼓掌]欢迎 @%s 的加入
[得意]请不要发送违规消息
[玫瑰]祝您聊天愉快！''' %d)
    if msg.is_at:
        group.send('别理我，我想静静...')

bot.join()