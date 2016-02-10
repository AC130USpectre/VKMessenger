from tkinter import *
import messenger

def sendMessage(event):
    if event.widget.master.isChat:
        pass
    else:
        messenger.sendMessage(event.widget.master.userID, event.widget.master.chat.get(1.0, END))
        event.widget.master.chat.delete(1.0, END)

def refreshHistoryWindow(event):
    event.widget.config(relief = 'sunken')
    if event.widget.master.isChat:
        pass
    else:
        history = messenger.getHistory(event.widget.master.userID)
        event.widget.master.history.delete(1.0, END)
        event.widget.master.history.insert(END, '\n'.join(history))
        event.widget.master.history.see(END)
        userInfo = messenger.getUserInfo(event.widget.master.userID)
        event.widget.master.userStatus.config(text = userInfo['IsOnline'])

def openChatWindow(event):
    event.widget.config(relief = 'sunken')
    historyWindow = Toplevel(dialogWindow)
    historyWindow.minsize(width = 580, height = 425)
    historyWindow.maxsize(width = 580, height = 425)
    refreshButton = Button(historyWindow, text = 'Обновить')
    refreshButton.bind('<Button-1>', refreshHistoryWindow)
    refreshButton.bind('<ButtonRelease-1>', lambda x: x.widget.config(relief = 'raised'))
    refreshButton.place(x = 500, y = 0, width = 80, height = 25)
    historyWindow.userID = event.widget.master.userID
    historyWindow.isChat = event.widget.master.isChat
    if historyWindow.isChat:
        pass
    else:
        userInfo = messenger.getUserInfo(historyWindow.userID)
        historyWindow.title(userInfo['Name'])
        status = Label(historyWindow, text = userInfo['IsOnline'])
        status.place(x = 0, y = 0, width = 80, height = 25)
        historyWindow.userStatus = status
    historyMemo = Text(historyWindow, wrap = WORD)
    historyMemo.place(x = 0, y = 25, width = 580, height = 350)
    historyWindow.history = historyMemo
    chatMemo = Text(historyWindow, wrap = WORD)
    chatMemo.place(x = 0, y = 375, width = 500, height = 50)
    historyWindow.chat = chatMemo
    sendButton = Button(historyWindow, text = 'Отправить')
    sendButton.bind('<Button-1>', sendMessage)
    sendButton.bind('<ButtonRelease-1>', lambda x: x.widget.config(relief = 'raised'))
    sendButton.bind('<Button-1>', refreshHistoryWindow, sendMessage)
    sendButton.place(x = 500, y = 375, width = 80, height = 50)
    historyWindow.mainloop()

def openUserInfoWindow(event):
    event.widget.config(relief = 'sunken')
    userInfo = messenger.getUserInfo(event.widget.master.userID)
    infoWindow = Toplevel(dialogWindow)
    infoWindow.title(userInfo['ID'])
    name = Label(infoWindow, text = userInfo['Name'])
    name.grid(row = 1, column = 1)
    sex = Label(infoWindow, text = 'Пол: ' + userInfo['Sex'])
    sex.grid(row = 2, column = 1)
    isOnline = Label(infoWindow, text = userInfo['IsOnline'])
    isOnline.grid(row = 1, column = 2)
    lastSeenDate = Label(infoWindow, text = userInfo['LastSeenDate'])
    lastSeenDate.grid(row = 2, column = 2)
    friendStatus = Label(infoWindow, text = userInfo['FriendStatus'])
    friendStatus.grid(row = 3, column = 1, columnspan = 2)
    status = Label(infoWindow, text = userInfo['Status'])
    status.grid(row = 4, column = 1, columnspan = 2)
    birthDate = Label(infoWindow, text = 'Дата рождения: ' + userInfo['BirthDate'])
    birthDate.grid(row = 5, column = 1, columnspan = 2)
    relation = Label(infoWindow, text = userInfo['Relation'])
    relation.grid(row = 6, column = 1, columnspan = 2)
    infoWindow.mainloop()

def openChatInfoWindow(event):
    event.widget.config(relief = 'sunken')
    (chatInfo, chatTitle) = messenger.getChatInfo(event.widget.master.userID)
    infoWindow = Toplevel(dialogWindow)
    infoWindow.title(chatTitle)
    for i in range(len(chatInfo)):
        Label(infoWindow, text = chatInfo[i]['Name']).grid(row = (i + 1), column = 1)
        Label(infoWindow, text = chatInfo[i]['Status']).grid(row = (i + 1), column = 2)
        Label(infoWindow, text = chatInfo[i]['LastSeenTime']).grid(row = (i + 1), column = 3)
    infoWindow.mainloop()

class Dialog(Frame):
    def __init__(self, window, VKDialog, num):
        super(Dialog, self).__init__(window, bd = 2, bg = {False: 'white', True : 'yellow'}[VKDialog['IsChat']], relief = 'solid')
        status = Label(self, text = VKDialog['Status'], bg = 'white')
        status.grid(row = 1, column = 2)
        name = Label(self, text = VKDialog['UserName'], bg = {False: 'white', True : 'yellow'}[VKDialog['IsChat']])
        name.grid(row = 2, column = 1, columnspan = 2)
        openDialogButton = Button(self, text = 'Сообщения')
        openDialogButton.grid(row = 3, column = 1)
        openDialogButton.bind('<Button-1>', openChatWindow)
        openDialogButton.bind('<ButtonRelease-1>', lambda x: x.widget.config(relief = 'raised'))
        openInfoButton = Button(self, text = 'Инфо')
        openInfoButton.grid(row = 3, column = 2)
        if VKDialog['IsChat']:
            openInfoButton.bind('<Button-1>', openChatInfoWindow)
        else:
            openInfoButton.bind('<Button-1>', openUserInfoWindow)
        openInfoButton.bind('<ButtonRelease-1>', lambda x: x.widget.config(relief = 'raised'))
        self.grid(row = num, column = 1)
        if VKDialog['IsChat']:
            self.userID = VKDialog['ChatID']
            status.destroy()
        else:
            self.userID = VKDialog['UserID']
        self.isChat = VKDialog['IsChat']

dialogWindow = Tk()
dialogWindow.wm_title('VKMessenger')
refreshDialogsButton = Button(dialogWindow, text = 'Обновить диалоги')
refreshDialogsButton.grid(row = 1, column = 1)
dialogFramesList = []
def refreshDialogsList(event):
    event.widget.config(relief = 'sunken')
    for dialog in dialogFramesList:
        dialog.destroy()
        dialogFramesList.remove(dialog)
    VKdialogs = messenger.getVKdialogsList()
    i = 2
    for VKdialog in VKdialogs:
        dialogFramesList.append(Dialog(dialogWindow, VKdialog, i))
        i += 1
    
refreshDialogsButton.bind('<Button-1>', refreshDialogsList)
refreshDialogsButton.bind('<ButtonRelease-1>', lambda x: x.widget.config(relief = 'raised'))
dialogWindow.mainloop()
