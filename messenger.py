import vk
from datetime import datetime

def unixTimeConvert(unix_time):
    time = datetime.fromtimestamp(int(unix_time))
    return '{}/{}/{} {}:{}:{}'.format(time.day, time.month, time.year, time.hour, time.minute, time.second)

with open('access_token.txt', 'r') as file:
    api = vk.API(vk.Session(access_token = file.readline()), v='5.45', lang = 'ru')

def sendMessage(ID, text):
    api.messages.send(user_id = ID, message = text)

def sendChatMessage(ID, text):
    api.messages.send(chat_id = ID, message = text)

smiles = {
    128522 : ':-)',
    128515 : ':-D',
    128521 : ';-)',
    128518 : 'xD',
    128540 : ';-P',
    128523 : ':-p',
    128525 : '8-)',
    128526 : 'B-)',
    128530 : ':-(',
    128527 : ';-]',
    128532 : '3(',
    128546 : ":'(",
    128557 : ':_(',
    128553 : ':((',
    128552 : ':o',
    128528 : ':|',
    128524 : '3-)',
    128519 : 'O:)',
    128560 : ';o',
    128562 : '8o',
    128563 : '8|',
    128567 : ':X',
    128538 : ':-*',
    128544 : '>(',
    128545 : '>((',
    128564 : 'z_Z'
}

def replaceSmiles(text):
    ans = ''
    for c in text:
        if ord(c) > 2 ** 16:
            if ord(c) in smiles:
                ans = ans + smiles[ord(c)]
            else:
                ans = ans + '~' + str(ord(c)) + '~'
        else:
            ans = ans + c
    return ans

def getUserHistory(userID):
    messages = api.messages.getHistory(user_id = str(userID), count = 200)
    history = []
    for message in messages['items']:
        text = {1 : 'ОТ ВАС', 0 : 'ОТ СОБЕСЕДНИКА'}[message['out']] + '\n' + \
               unixTimeConvert(message['date']) + '\n' + \
               {0 : 'НЕ ПРОЧИТАНО', 1 : 'ПРОЧИТАНО'}[message['read_state']] + '\n'
        if 'title' in message:
            text = text + message['title'] + '\n'
        if 'body' in message:
            text = text + replaceSmiles(message['body']) + '\n'
        if 'attachments' in message:
            text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ МЕДИАФАЙЛЫ!\n'
        if 'fwd_messages' in message:
            text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ СООБЩЕНИЯ!\n'
        history.append(text)
    return history[::-1]

def getChatHistory(chatID):
    messages = api.messages.getHistory(peer_id = 2000000000 + chatID, count = 200)
    IDS = []
    for message in messages['items']:
        IDS.append(str(message['user_id']))
    VKUsers = api.users.get(user_ids = ','.join(IDS))
    Users = {}
    for user in VKUsers:
        Users[user['id']] = user
    history = []
    for message in messages['items']:
        if message['out']:
            text = 'ОТ ВАС\n'
        else:
            text = Users[message['user_id']]['last_name'] + ' ' + Users[message['user_id']]['first_name'] + '\n'
        text = text + unixTimeConvert(message['date']) + '\n'
        if 'body' in message:
            text = text + replaceSmiles(message['body']) + '\n'
        if 'attachments' in message:
            text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ МЕДИАФАЙЛЫ!\n'
        if 'fwd_messages' in message:
            text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ СООБЩЕНИЯ!\n'
        history.append(text)
    return history[::-1]

def getVKdialogsList():
    VKdialogs = api.messages.getDialogs(count = 10)
    IDS = []
    for message in VKdialogs['items']:
        IDS.append(str(message['message']['user_id']))
    VKUsers = api.users.get(user_ids = ','.join(IDS), fields = 'online')
    Users = {}
    for user in VKUsers:
        Users[user['id']] = user
    result = []
    for message in VKdialogs['items']:
        ans = {}
        ans['UserName'] = Users[message['message']['user_id']]['last_name'] + ' ' + Users[message['message']['user_id']]['first_name']
        ans['UserID'] = message['message']['user_id']
        ans['Status'] = {0: 'Оффлайн', 1: 'Онлайн'}[Users[message['message']['user_id']]['online']]
        ans['IsChat'] = 'chat_id' in message['message']
        if 'chat_id' in message['message']:
            ans['ChatID'] = message['message']['chat_id']
            ans['UserName'] = message['message']['title']
        result.append(ans)
    return result

def getUserInfo(ID):
    Info = api.users.get(user_ids = str(ID), fields = 'sex,bdate,online,status,last_seen,relation,friend_status')[0]
    ans = {}
    ans['ID'] = str(Info['id'])
    ans['Name'] = Info['last_name'] + ' ' + Info['first_name']
    if 'deactivated' in Info:
        ans['Sex'] = 'Не указан'
        ans['BirthDate'] = 'Не указана'
        ans['IsOnline'] = 'Деактивирован'
        ans['LastSeenDate'] = 'Неизвестно'
        ans['Relation'] = 'Не указано'
        ans['FriendStatus'] = 'Не указано'
        return ans
    ans['Sex'] = {0: 'Не указан', 1 : 'Женский', 2 : 'Мужской'}[Info['sex']]
    if 'bdate' in Info:
        ans['BirthDate'] = Info['bdate']
    else:
        ans['BirthDate'] = 'Не указана'
    ans['IsOnline'] = {0 : 'Оффлайн', 1 : 'Онлайн'}[Info['online']]
    ans['Status'] = Info['status'] or 'Статус не указан'
    ans['LastSeenDate'] = unixTimeConvert(Info['last_seen']['time'])
    relation = {1 : 'Не женат/Не замужем', 2 : 'Есть друг/Есть подруга', 3 : 'Помолвлен/Помолвлена', 4 : 'Женат/Замужем', 5 : 'Всё сложно', 6 : 'В активном поиске', 7 : 'Влюблён/влюблена', 0 : 'Отношения не указаны'}
    if 'relation' in Info:
        if 'relation_partner' in Info:
            ans['Relation'] = relation[Info['relation']] + ' (' + Info['relation_partner']['first_name'] + ')'
        else:
            ans['Relation'] = relation[Info['relation']]
    else:
        ans['Relation'] = 'Отношения не указаны'
    friendStatus = {0 : 'Пользователь не является другом', 1 : 'Отправлена заявка/подписка пользователю', 2 : 'Имеется входящая заявка/подписка от пользователя', 3 : 'Пользователь является другом'}
    ans['FriendStatus'] = friendStatus[Info['friend_status']]
    return ans

def getChatInfo(ID):
    chatInfo = api.messages.getChat(chat_id = ID, fields = 'uid,first_name,last_name,online,last_seen')
    ans = []
    for user in chatInfo['users']:
        usr = {}
        usr['Name'] = user['last_name'] + ' ' + user['first_name']
        usr['Status'] = {0 : 'Оффлайн', 1 : 'Онлайн'}[user['online']]
        usr['ID'] = user['id']
        usr['LastSeenTime'] = unixTimeConvert(user['last_seen']['time'])
        ans.append(usr)
    return (ans, chatInfo['title'])
