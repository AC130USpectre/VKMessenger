import tkinter as tk
import messenger
#import webbrowser

#sys.stdout = open('logs.txt', 'w')

def setSunken(event):
    event.widget.config(relief = 'sunken')

def setRaised(event):
    event.widget.config(relief = 'raised')

def sendMessage(event):
    if event.widget.master.isChat:
        messenger.sendChatMessage(event.widget.master.ID, event.widget.master.chat.get(1.0, END))
        event.widget.master.chat.delete(1.0, END)
    else:
        messenger.sendMessage(event.widget.master.ID, event.widget.master.chat.get(1.0, END))
        event.widget.master.chat.delete(1.0, END)

def refreshHistoryWindow(event):
    event.widget.master.history.destroy()
    historyFrame = tk.Frame(event.widget.master)
    event.widget.master.history = historyFrame

def refreshDialogsList(event): # что здесь происходит?!
    global dialogsList
    dialogsList = []
    for dialog in dialogsList:
        dialogsList.remove(dialog)
    VKdialogs = messenger.getVKdialogsList()
    global framesListCanvas
    framesListCanvas = tk.Canvas(dialogsFrame)
    tk.Grid.columnconfigure(dialogsFrame, 0, weight = 1)
    tk.Grid.rowconfigure(dialogsFrame, 0, weight = 1)
    global framesListScroll
    framesListScroll = tk.Scrollbar(dialogsFrame, command = framesListCanvas.yview)
    framesList = tk.Frame(framesListCanvas)
    tk.Grid.columnconfigure(framesList, 0, weight = 1)
    framesListCanvas.configure(yscrollcommand = framesListScroll.set)
    framesListScroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
    framesListCanvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W)
    for VKdialog in VKdialogs:
        dialogFrame = Dialog(framesList, VKdialog)
        dialogFrame.grid(row = len(dialogsList), column = 0, sticky = tk.W + tk.E)
        dialogsList.append(dialogFrame)
    framesListCanvas.create_window((0, 0), window = framesList, anchor = 'nw')
    def configureFramesList(event):
        framesListCanvas.config(scrollregion = framesListCanvas.bbox('all'), width = framesList.winfo_width(), height = min(framesList.winfo_height(), mainWindow.winfo_screenheight() * 2 // 3))
    framesList.bind('<Configure>', configureFramesList)

def openChatWindow(event):
    historyWindow = tk.Toplevel(mainWindow)
    historyWindow.minsize(width = mainWindow.winfo_screenwidth() // 2, height = mainWindow.winfo_screenheight() // 2)
    historyWindow.maxsize(width = mainWindow.winfo_screenwidth() * 5 // 6, height = mainWindow.winfo_screenheight() * 5 // 6)

    refreshButton = tk.Button(historyWindow, text = 'Обновить')
    refreshButton.bind('<Button-1>', refreshHistoryWindow, setSunken)
    refreshButton.bind('<ButtonRelease-1>', setRaised)
    refreshButton.grid(row = 0, column = 1, sticky = tk.E + tk.N)

    historyWindow.ID = event.widget.master.ID
    historyWindow.isChat = event.widget.master.isChat
    if historyWindow.isChat:
        (info, title) = messenger.getChatInfo(historyWindow.ID)
        historyWindow.title(title)
    else:
        userInfo = messenger.getUserInfo(historyWindow.ID)
        historyWindow.title(userInfo['Name'])
        status = tk.Label(historyWindow, text = userInfo['IsOnline'])
        status.grid(row = 0, column = 0, sticky = tk.W + tk.N)
        historyWindow.userStatus = status

    historyFrame = tk.Frame(historyWindow)
    historyFrame.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W + tk.E)
    historyWindow.history = historyFrame

    chatMemo = tk.Text(historyWindow, wrap = tk.WORD)
    chatMemo.grid(row = 2, column = 0, sticky = tk.W + tk.S + tk.E)
    chatMemo.bind('<Control-Enter>', refreshHistoryWindow, sendMessage)
    historyWindow.chat = chatMemo

    sendButton = tk.Button(historyWindow, text = 'Отправить')
    sendButton.grid(row = 2, column = 1, sticky = tk.E + tk.N + tk.S)
    sendButton.bind('<Button-1>', refreshHistoryWindow, sendMessage) # !!! много биндов !!!
    sendButton.bind('<ButtonRelease-1>', setRaised)

    tk.Grid.columnconfigure(historyWindow, 0, weight = 1)
    historyWindow.mainloop()

def openInfoWindow(event):
    infoWindow = tk.Toplevel(mainWindow)
    if event.widget.master.isChat:
        (chatInfo, chatTitle) = messenger.getChatInfo(event.widget.master.ID)
        infoWindow.title(chatTitle)
        for i in range(len(chatInfo)):
            tk.Label(infoWindow, text = chatInfo[i]['Name']).grid(row = (i + 1), column = 1)
            tk.Label(infoWindow, text = chatInfo[i]['Status']).grid(row = (i + 1), column = 2)
            tk.Label(infoWindow, text = chatInfo[i]['LastSeenTime']).grid(row = (i + 1), column = 3)
    else:
        userInfo = messenger.getUserInfo(event.widget.master.ID)
        infoWindow.title(userInfo['ID'])
        name = tk.Label(infoWindow, text = userInfo['Name'])
        name.grid(row = 1, column = 1)
        sex = tk.Label(infoWindow, text = 'Пол: ' + userInfo['Sex'])
        sex.grid(row = 2, column = 1)
        isOnline = tk.Label(infoWindow, text = userInfo['IsOnline'])
        isOnline.grid(row = 1, column = 2)
        lastSeenDate = tk.Label(infoWindow, text = userInfo['LastSeenDate'])
        lastSeenDate.grid(row = 2, column = 2)
        friendStatus = tk.Label(infoWindow, text = userInfo['FriendStatus'])
        friendStatus.grid(row = 3, column = 1, columnspan = 2)
        status = tk.Label(infoWindow, text = userInfo['Status'])
        status.grid(row = 4, column = 1, columnspan = 2)
        birthDate = tk.Label(infoWindow, text = 'Дата рождения: ' + userInfo['BirthDate'])
        birthDate.grid(row = 5, column = 1, columnspan = 2)
        relation = tk.Label(infoWindow, text = userInfo['Relation'])
        relation.grid(row = 6, column = 1, columnspan = 2)
    infoWindow.mainloop()

class Dialog(tk.Frame):
    def __init__(self, window, VKDialog):
        super(Dialog, self).__init__(window, relief = 'solid', bd = 2)
        self.isChat = VKDialog['IsChat']
        self.ID = VKDialog[{True : 'ChatID', False : 'UserID'}[self.isChat]]
        bgColor = {True : 'yellow', False : 'white'}[self.isChat]
        self.config(bg = bgColor)
        self.infoImage = tk.PhotoImage(file = 'info.png')
        self.messImage = tk.PhotoImage(file = 'dialog.png')

        mCountLabel = tk.Label(self, text = VKDialog['UnreadCount'], bg = bgColor)
        mCountLabel.grid(row = 0, column = 0)
        statusLabel = tk.Label(self, text = VKDialog['Status'], bg = bgColor)
        statusLabel.grid(row = 0, column = 1, columnspan = 2, sticky = tk.W + tk.E)
        infoButton = tk.Button(self, image = self.infoImage)
        infoButton.grid(row = 0, column = 3, sticky = tk.E)
        infoButton.bind('<Button-1>', openInfoWindow, setSunken)
        infoButton.bind('<ButtonRelease-1>', setRaised)
        userNameLabel = tk.Label(self, text = VKDialog['UserName'], bg = bgColor)
        userNameLabel.grid(row = 1, column = 0, columnspan = 3, sticky = tk.W + tk.E)
        messButton = tk.Button(self, image = self.messImage)
        messButton.grid(row = 1, column = 3, sticky = tk.E)
        messButton.bind('<Button-1>', openChatWindow, setSunken)
        messButton.bind('<ButtonRelease-1>', setRaised)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)

mainWindow = tk.Tk()
mainWindow.wm_title('VKMessenger')

refreshDialogsButton = tk.Button(mainWindow, text = 'Обновить диалоги')
refreshDialogsButton.grid(row = 0, column = 0, sticky = tk.W + tk.E)
refreshDialogsButton.bind('<Button-1>', refreshDialogsList, setSunken)
refreshDialogsButton.bind('<ButtonRelease-1>', setRaised)

dialogsFrame = tk.Frame(mainWindow, bg = 'yellow')
dialogsFrame.grid(row = 1, column = 0)

tk.Grid.columnconfigure(mainWindow, 0, weight = 1)
tk.Grid.rowconfigure(mainWindow, 1, weight = 1)

mainWindow.mainloop()

#sys.stdout.close()

#############################################################################################################################################################
##def sendMessage(event):
##    if event.widget.master.isChat:
##        messenger.sendChatMessage(event.widget.master.userID, event.widget.master.chat.get(1.0, END))
##        event.widget.master.chat.delete(1.0, END)
##    else:
##        messenger.sendMessage(event.widget.master.userID, event.widget.master.chat.get(1.0, END))
##        event.widget.master.chat.delete(1.0, END)
##
##def refreshHistoryWindow(event):
##    event.widget.config(relief = 'sunken')
##    if event.widget.master.isChat:
##        history = messenger.getChatHistory(event.widget.master.userID)
##        event.widget.master.history.config(state = 'normal')
##        event.widget.master.history.delete(1.0, END)
##        event.widget.master.history.insert(END, '\n'.join(history))
##        event.widget.master.history.see(END)
##        event.widget.master.history.config(state = 'disabled')
##    else:
##        history = messenger.getUserHistory(event.widget.master.userID)
##        event.widget.master.history.config(state = 'normal')
##        event.widget.master.history.delete(1.0, END)
##        event.widget.master.history.insert(END, '\n'.join(history))
##        event.widget.master.history.see(END)
##        event.widget.master.history.config(state = 'disabled')
##        userInfo = messenger.getUserInfo(event.widget.master.userID)
##        event.widget.master.userStatus.config(text = userInfo['IsOnline'])
