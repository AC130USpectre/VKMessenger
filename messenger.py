import vk
from datetime import datetime

def unixTimeConvert(unix_time):
    time = datetime.fromtimestamp(int(unix_time))
    return '{}/{}/{} {}:{}:{}'.format(time.day, time.month, time.year, time.hour, time.minute, time.second)

with open('access_token.txt', 'r') as file:
    api = vk.API(vk.Session(access_token = file.readline()))

def sendMessage(ID, text):
    print(type(ID), type(text))
    api.messages.send(user_id = ID, message = text)

def getHistory(userID):
    messages = api.messages.getHistory(user_id = str(userID), count = 200)
    history = []
    for message in messages:
        if type(message) != int:
            text = {1 : 'ОТ ВАС', 0 : 'ОТ СОБЕСЕДНИКА'}[message['out']] + '\n' + \
                   unixTimeConvert(message['date']) + '\n' + \
                   {0 : 'НЕ ПРОЧИТАНО', 1 : 'ПРОЧИТАНО'}[message['read_state']] + '\n'
            if 'title' in message:
                text = text + message['title'] + '\n'
            if 'body' in message:
                text = text + message['body'] + '\n'
            if 'attachments' in message:
                text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ МЕДИАФАЙЛЫ!\n'
            if 'fwd_messages' in message:
                text = text + 'ЕСТЬ ПРИЛОЖЕННЫЕ СООБЩЕНИЯ!\n'
            history.append(text)
    return history[::-1]

def getVKdialogsList():
    VKdialogs = api.messages.getDialogs(count = 10)
    IDS = []
    for message in VKdialogs:
        if type(message) != int:
            IDS.append(str(message['uid']))
    VKUsers = api.users.get(user_ids = ','.join(IDS), fields = 'online')
    Users = {}
    for user in VKUsers:
        Users[user['uid']] = user
    result = []
    for message in VKdialogs:
        if type(message) != int:
            ans = {}
            ans['UserName'] = Users[message['uid']]['last_name'] + ' ' + Users[message['uid']]['first_name']
            ans['UserID'] = message['uid']
            ans['Status'] = {0: 'Оффлайн', 1: 'Онлайн'}[Users[message['uid']]['online']]
            ans['IsChat'] = 'chat_id' in message
            if 'chat_id' in message:
                ans['ChatID'] = message['chat_id']
            result.append(ans)
    return result

def getUserInfo(ID):
    Info = api.users.get(user_ids = str(ID), fields = 'sex,bdate,online,status,last_seen,relation,friend_status')[0]
    ans = {}
    ans['ID'] = str(Info['uid'])
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
