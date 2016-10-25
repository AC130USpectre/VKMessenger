from datetime import datetime
import requests
import os

with open("AccessToken.txt", "r") as file: # открыть файл с токеном доступа и вытащить токен для дальнейшего использования в API
	access_token = file.readline()

end = "lang=ru&v=5.59&access_token=" + access_token
api_addr = "https://api.vk.com/method/"

def getRequest(method_name, params = {}, response_only = False):
	full_req = api_addr + method_name + "?"
	for i in params.keys():
		full_req = full_req + i + "=" + str(params[i]) + "&"
	full_req = full_req + end
	for i in range(3): # повторить три раза
		try:
			r = requests.get(full_req).json()
			if "error" in r:
				continue
			if response_only:
				return r["response"]
			else:
				return r
		except Exception:
			os.sleep(3)
	return None

def unixTimeConvert(unix_time): # конвертируем время из unixtime в строку ДД/ММ/ГГГГ ЧЧ:ММ:СС
	time = datetime.fromtimestamp(int(unix_time))
	return "{}/{}/{} {}:{}:{}".format(str(time.day).zfill(2), str(time.month).zfill(2), str(time.year).zfill(4), str(time.hour).zfill(2), str(time.minute).zfill(2), str(time.second).zfill(2))

def sendMessage(ID, text): # отправить текстовое сообщение пользователю с данным ID
	getRequest("messages.send", {"user_id" : ID, "message" : text})

def sendChatMessage(ID, text): # отправить текстовое сообщение в чат с данным ID
	getRequest("messages.send", {"chat_id" : ID, "message" : text})

smiles = {} # временно
#smiles = { # таблица конвертации некоторых смайликов
#    128522 : ':-)',
#    128515 : ':-D',
#    128521 : ';-)',
#    128518 : 'xD',
#    128540 : ';-P',
#    128523 : ':-p',
#    128525 : '8-)',
#    128526 : 'B-)',
#    128530 : ':-(',
#    128527 : ';-]',
#    128532 : '3(',
#    128546 : ":'(",
#    128557 : ':_(',
#    128553 : ':((',
#    128552 : ':o',
#    128528 : ':|',
#    128524 : '3-)',
#    128519 : 'O:)',
#    128560 : ';o',
#    128562 : '8o',
#    128563 : '8|',
#    128567 : ':X',
#    128538 : ':-*',
#    128544 : '>(',
#    128545 : '>((',
#    128564 : 'z_Z'
#}

def replaceSmiles(text): # заменить смайлики в тексте согласно таблице, те, которые невозможно заменить, представить в виде кодов
	ans = ""
	for c in text:
		if ord(c) > 2 ** 16:
			if ord(c) in smiles:
				ans = ans + smiles[ord(c)]
			else:
				ans = ans + "~" + str(ord(c)) + "~"
		else:
			ans = ans + c
	return ans

def parseAttach(message): # распарсить медиавложения
	ans = []
	counters = {"Photo" : 0, "Video" : 0, "Audio" : 0, "Doc" : 0, "Wall" : 0, "WallComm" : 0, "Stick" : 0, "Link" : 0}
	for attach in message["attachments"]:
		bufDict = {}
		if attach["type"] == "photo":
			counters["Photo"] += 1
			bufDict["Type"] = "Photo"
			bufDict["Name"] = "Картинка №{}".format(str(counters["Photo"]))
			if "photo_2560" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_2560"]
			elif "photo_1280" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_1280"]
			elif "photo_807" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_807"]
			elif "photo_604" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_604"]
			elif "photo_130" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_130"]
			elif "photo_75" in attach["photo"]:
				bufDict["URL"] = attach["photo"]["photo_75"]
			else:
				print(attach)
		elif attach["type"] == "video":
			counters["Video"] += 1
			bufDict["Type"] = "Video"
			bufDict["Name"] = attach["video"]["title"]
			bufDict["Descr"] = attach["video"]["description"]
		elif attach["type"] == "audio":
			counters["Audio"] += 1
			bufDict["Type"] = "Audio"
			bufDict["Name"] = attach["audio"]["artist"] + " - " + attach["audio"]["title"]
			bufDict["URL"] = attach["audio"]["url"]
		elif attach["type"] == "doc":
			counters["Doc"] += 1
			bufDict["Type"] = "Doc"
			bufDict["Name"] = "Документ {0} №{1}".format(attach["doc"]["ext"], str(counters["Doc"]))
			bufDict["URL"] = attach["doc"]["url"]
		elif attach["type"] == "wall":
			counters["Wall"] += 1
			bufDict["Type"] = "Wall"
			bufDict["Name"] = "Запись со стены №{}".format(str(counters["Wall"]))
		elif attach["type"] == "wall_reply":
			counters["WallComm"] += 1
			bufDict["Type"] = "WallComm"
			bufDict["Name"] = "Комментарий к записи со стены №{}".format(str(counters["WallComm"]))
		elif attach["type"] == "sticker":
			counters["Stick"] += 1
			bufDict["Type"] = "Stick"
			bufDict["Name"] = "Стикер №{}".format(str(counters["Stick"]))
			bufDict["URL"] = attach["sticker"]["photo_352"]
		elif attach["type"] == "link":
			counters["Link"] += 1
			bufDict["Type"] = "Link"
			bufDict["Name"] = "Ссылка №{}".format(str(counters["Link"]))
			bufDict["URL"] = attach["link"]["url"]
		else:
			print(attach)
		ans.append(bufDict)
	return ans

def parseFwd(message): # распарсить вложенные сообщения
	ans = []
	for msg in message["fwd_messages"]:
		ans.append(parseMsg(msg))
	return ans

def parseMsg(message): # распарсить отдельное вложенное сообщение
	ans = {}
	Sender = getRequest("users.get", {"user_ids" : str(message["user_id"])}, True)[0]
	ans["Sender"] = Sender["last_name"] + " " + Sender["first_name"]
	ans["Date"] = unixTimeConvert(message["date"])
	if "title" in message:
		ans["Title"] = message["title"]
	else:
		ans["Title"] = ""
	if "body" in message:
		ans["Text"] = replaceSmiles(message["body"])
	else:
		ans["Text"] = ""
	if "attachments" in message:
		ans["Attach"] = parseAttach(message)
	else:
		ans["Attach"] = []
	if "fwd_messages" in message:
		ans["Fwd"] = parseFwd(message)
	else:
		ans["Fwd"] = []
	return ans

def getUserHistory(userID): # получить верхний уровень сообщений истории с пользователем с данным ID
	messages = getRequest("messages.getHistory", {"user_id" : userID, "count" : 200}, True)
	history = []
	for message in messages["items"]:
		msg = {}
		msg["Sender"] = {1 : "ВЫ:", 0 : "СОБЕСЕДНИК:"}[message["out"]]
		msg["Date"] = unixTimeConvert(message["date"])
		msg["Status"] = {0 : "НЕ ПРОЧИТАНО", 1 : "ПРОЧИТАНО"}[message["read_state"]]
		if "title" in message:
			msg["Title"] = message["title"]
		else:
			msg["Title"] = ""
		if "body" in message:
			msg["Text"] = replaceSmiles(message["body"])
		else:
			msg["Text"] = ""
		if "attachments" in message:
			msg["Attach"] = parseAttach(message)
		else:
			msg["Attach"] = []
		if "fwd_messages" in message:
			msg["Fwd"] = parseFwd(message)
		else:
			msg["Fwd"] = []
		history.append(msg)
	return history[::-1]

def getChatHistory(chatID): # получить верхний уровень сообщений истории из чата с данным ID
	messages = getRequest("messages.getHistory", {"peer_id" : 2000000000 + chatID, "count" : 200}, True)
	IDS = set()
	for message in messages["items"]:
		IDS.add(str(message["user_id"]))
	VKUsers = getRequest("users.get", {"user_ids" : ",".join(IDS)}, True)
	Users = {}
	for user in VKUsers:
		Users[user["id"]] = user
	history = []
	for message in messages["items"]:
		msg = {}
		if message["out"]:
			msg["Sender"] = "ВЫ:"
		else:
			msg["Sender"] = Users[message["user_id"]]["last_name"] + " " + Users[message["user_id"]]["first_name"] + ":"
		msg["Date"] = unixTimeConvert(message["date"])
		if "title" in message:
			msg["Title"] = message["title"]
		else:
			msg["Title"] = ""
		if "body" in message:
			msg["Text"] = replaceSmiles(message["body"])
		else:
			msg["Text"] = ""
		if "attachments" in message:
			msg["Attach"] = parseAttach(message)
		else:
			msg["Attach"] = []
		if "fwd_messages" in message:
			msg["Fwd"] = parseFwd(message)
		else:
			msg["Fwd"] = []
		msg["Status"] = ""
		history.append(msg)
	return history[::-1]

def getVKdialogsList(): # получить информацию о диалогах текущего пользователя
	VKdialogs = getRequest("messages.getDialogs", {"count" : 200}, True)
	IDS = set()
	for message in VKdialogs["items"]:
		IDS.add(str(message["message"]["user_id"]))
	VKUsers = getRequest("users.get", {"user_ids" : ",".join(IDS), "fields" : "online"}, True)
	Users = {}
	for user in VKUsers:
		Users[user["id"]] = user
	result = []
	for message in VKdialogs["items"]:
		ans = {}
		if "chat_id" in message["message"]:
			ans["IsChat"] = True
			ans["UserName"] = message["message"]["title"]
			ans["ChatID"] = message["message"]["chat_id"]
			ans["Status"] = "[" + str(message["message"]["users_count"]) + "]"
		else:
			ans["IsChat"] = False
			ans["UserName"] = Users[message["message"]["user_id"]]["last_name"] + " " + Users[message["message"]["user_id"]]["first_name"]
			ans["UserID"] = message["message"]["user_id"]
			ans["Status"] = {0: "Оффлайн", 1: "Онлайн"}[Users[message["message"]["user_id"]]["online"]]
		if "unread" in message:
			ans["UnreadCount"] = message["unread"]
		else:
			ans["UnreadCount"] = 0
		result.append(ans)
	return result

def getUserInfo(ID): # получить информацию о пользователе по ID
	Info = getRequest("users.get", {"user_ids" : str(ID), "fields" : "sex,bdate,online,status,last_seen,relation,friend_status"}, True)[0]
	ans = {}
	ans["ID"] = str(Info["id"])
	ans["Name"] = Info["last_name"] + " " + Info["first_name"]
	if "deactivated" in Info:
		ans["Sex"] = "Не указан"
		ans["BirthDate"] = "Не указана"
		ans["IsOnline"] = "Деактивирован"
		ans["LastSeenDate"] = "Неизвестно"
		ans["Relation"] = "Не указано"
		ans["FriendStatus"] = "Не указано"
		return ans
	ans["Sex"] = {0: "Не указан", 1 : "Женский", 2 : "Мужской"}[Info["sex"]]
	if "bdate" in Info:
		ans["BirthDate"] = Info["bdate"]
	else:
		ans["BirthDate"] = "Не указана"
	ans["IsOnline"] = {0 : "Оффлайн", 1 : "Онлайн"}[Info["online"]]
	ans["Status"] = Info["status"] or "Статус не указан"
	ans["LastSeenDate"] = unixTimeConvert(Info["last_seen"]["time"])
	relation = {1 : "Не женат/Не замужем", 2 : "Есть друг/Есть подруга", 3 : "Помолвлен/Помолвлена", 4 : "Женат/Замужем", 5 : "Всё сложно", 6 : "В активном поиске", 7 : "Влюблён/влюблена", 0 : "Отношения не указаны"}
	if "relation" in Info:
		if "relation_partner" in Info:
			ans["Relation"] = relation[Info["relation"]] + " (" + Info["relation_partner"]["first_name"] + ")"
		else:
			ans["Relation"] = relation[Info["relation"]]
	else:
		ans["Relation"] = "Отношения не указаны"
	friendStatus = {0 : "Пользователь не является другом", 1 : "Отправлена заявка/подписка пользователю", 2 : "Имеется входящая заявка/подписка от пользователя", 3 : "Пользователь является другом"}
	ans["FriendStatus"] = friendStatus[Info["friend_status"]]
	return ans

def getChatInfo(ID): # получить информацию о пользователях чата по ID чата
	chatInfo = getRequest("messages.getChat", {"chat_id" : ID, "fields" : "uid,first_name,last_name,online,last_seen"}, True)
	ans = []
	for user in chatInfo["users"]:
		usr = {}
		usr["Name"] = user["last_name"] + " " + user["first_name"]
		usr["Status"] = {0 : "Оффлайн", 1 : "Онлайн"}[user["online"]]
		usr["ID"] = user["id"]
		usr["LastSeenTime"] = unixTimeConvert(user["last_seen"]["time"])
		ans.append(usr)
	return (ans, chatInfo["title"])
