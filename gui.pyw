import tkinter as tk
import messenger
import webbrowser

#sys.stdout = open('logs.txt', 'w')

def setSunken(event):
    event.widget.config(relief = 'sunken')

def setRaised(event):
    event.widget.config(relief = 'raised')

def sendMessage(event):
    if event.widget.master.isChat:
        messenger.sendChatMessage(event.widget.master.ID, event.widget.master.chat.get(1.0, tk.END))
        event.widget.master.chat.delete(1.0, tk.END)
    else:
        messenger.sendMessage(event.widget.master.ID, event.widget.master.chat.get(1.0, tk.END))
        event.widget.master.chat.delete(1.0, tk.END)

def refreshHistoryWindow(event):
    event.widget.master.history.destroy()
    historyFrame = tk.Frame(event.widget.master)
    historyFrame.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W + tk.E)
    event.widget.master.history = historyFrame
    historyCanvas = tk.Canvas(historyFrame)
    tk.Grid.columnconfigure(historyFrame, 0, weight = 1)
    tk.Grid.rowconfigure(historyFrame, 0, weight = 1)
    historyScroll = tk.Scrollbar(historyFrame, command = historyCanvas.yview)
    frame = tk.Frame(historyCanvas)
    tk.Grid.columnconfigure(frame, 0, weight = 1)
    historyCanvas.configure(yscrollcommand = historyScroll.set, bg = 'yellow')
    historyScroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
    historyCanvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W)
    if event.widget.master.isChat:
        VKhistory = messenger.getChatHistory(event.widget.master.ID)
    else:
        VKhistory = messenger.getUserHistory(event.widget.master.ID)
        userInfo = messenger.getUserInfo(event.widget.master.ID)
        event.widget.master.userStatus.config(text = userInfo['IsOnline'])
    for i in range(len(VKhistory)):
        mesFrame = MsgHistFrame(frame, VKhistory[i])
        mesFrame.grid(row = i, column = 0)
    historyCanvas.create_window((0, 0), window = frame, anchor = 'nw')
    def configureHistory(event):
        historyCanvas.config(scrollregion = historyCanvas.bbox('all'), width = frame.winfo_width(), height = min(4 * mesFrame.winfo_height(), frame.winfo_height()))
    frame.bind('<Configure>', configureHistory)

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
    refreshButton.bind('<Button-1>', setSunken, '+')
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
    historyCanvas = tk.Canvas(historyFrame)
    tk.Grid.columnconfigure(historyFrame, 0, weight = 1)
    tk.Grid.rowconfigure(historyFrame, 0, weight = 1)
    historyScroll = tk.Scrollbar(historyFrame, command = historyCanvas.yview)
    frame = tk.Frame(historyCanvas)
    tk.Grid.columnconfigure(frame, 0, weight = 1)
    historyCanvas.configure(yscrollcommand = historyScroll.set, bg = 'yellow')
    historyScroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
    historyCanvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W)
    if historyWindow.isChat:
        VKhistory = messenger.getChatHistory(historyWindow.ID)
    else:
        VKhistory = messenger.getUserHistory(historyWindow.ID)
        userInfo = messenger.getUserInfo(historyWindow.ID)
        historyWindow.userStatus.config(text = userInfo['IsOnline'])
    for i in range(len(VKhistory)):
        mesFrame = MsgHistFrame(frame, VKhistory[i])
        mesFrame.grid(row = i, column = 0, sticky = tk.W + tk.E)
    historyCanvas.create_window((0, 0), window = frame, anchor = 'nw')
    def configureHistory(event):
        historyCanvas.config(scrollregion = historyCanvas.bbox('all'), width = frame.winfo_width(), height = min(4 * mesFrame.winfo_height(), frame.winfo_height()))
    frame.bind('<Configure>', configureHistory)

    chatMemo = tk.Text(historyWindow, wrap = tk.WORD, height = 3)
    chatMemo.grid(row = 2, column = 0, sticky = tk.W + tk.S + tk.E)
    chatMemo.bind('<Control-Return>', refreshHistoryWindow)
    chatMemo.bind('<Control-Return>', sendMessage, '+')
    historyWindow.chat = chatMemo

    sendButton = tk.Button(historyWindow, text = 'Отправить')
    sendButton.grid(row = 2, column = 1, sticky = tk.E + tk.N + tk.S)
    sendButton.bind('<Button-1>', refreshHistoryWindow)
    sendButton.bind('<Button-1>', sendMessage, '+')
    sendButton.bind('<Button-1>', setSunken, '+')
    sendButton.bind('<ButtonRelease-1>', setRaised)

    tk.Grid.rowconfigure(historyWindow, 1, weight = 1)
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

def openAttach(event):
    if event.widget.attach['Type'] == 'Photo':
        webbrowser.open(event.widget.attach['URL'])
    elif event.widget.attach['Type'] == 'Video':
        window = tk.Toplevel(event.widget.master)
        label = tk.Label(window, text = event.widget.attach['Descr'])
        label.pack()
    elif event.widget.attach['Type'] == 'Audio':
        webbrowser.open(event.widget.attach['URL'])
    elif event.widget.attach['Type'] == 'Doc':
        webbrowser.open(event.widget.attach['URL'])
    elif event.widget.attach['Type'] == 'Wall':
        pass
    elif event.widget.attach['Type'] == 'WallComm':
        pass
    elif event.widget.attach['Type'] == 'Stick':
        webbrowser.open(event.widget.attach['URL'])
    elif event.widget.attach['Type'] == 'Link':
        window = tk.Toplevel(event.widget.master)
        text = tk.Text(window, height = 2)
        text.insert(tk.END, event.widget.attach['URL'])
        text.config(state = 'disabled')
        text.pack(side = 'top')
        button = tk.Button(window, text = 'Открыть ссылку')
        button.pack(side = 'bottom')
        button.bind('<Button-1>', lambda x: webbrowser.open(event.widget.attach['URL']))
        button.bind('<Button-1>', setSunken, '+')
        button.bind('<ButtonRelease-1>', setRaised)

def showAttachList(event):
    window = tk.Toplevel(event.widget.master)

    canvas = tk.Canvas(window)
    scroll = tk.Scrollbar(window, command = canvas.yview)
    frame = tk.Frame(canvas)
    canvas.configure(yscrollcommand = scroll.set)
    scroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
    canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W)
    for i in range(len(event.widget.master.msgAttach)):
        button = tk.Button(frame, text = event.widget.master.msgAttach[i]['Name'])
        button.grid(row = i, column = 0)
        button.attach = event.widget.master.msgAttach[i]
        button.bind('<Button-1>', openAttach)
        button.bind('<Button-1>', setSunken, '+')
        button.bind('<ButtonRelease-1>', setRaised)
    canvas.create_window((0, 0), window = frame, anchor = 'nw')
    def configureFrame(event):
        canvas.config(scrollregion = canvas.bbox('all'), width = frame.winfo_width(), height = min(frame.winfo_height(), 5 * button.winfo_height()))
    frame.bind('<Configure>', configureFrame)

    window.mainloop()

def openFwd(event):
    window = tk.Toplevel(event.widget.master)

    name = tk.Label(window, text = event.widget.fwd['Sender'])
    name.grid(row = 0, column = 0, sticky = tk.W + tk.N)
    date = tk.Label(window, text = event.widget.fwd['Date'])
    date.grid(row = 0, column = 1, sticky = tk.E + tk.N)
    if event.widget.fwd['Text'] or event.widget.fwd['Title']:
        text = tk.Text(window, wrap = tk.WORD)
        text.grid(row = 1, column = 0, columnspan = 2, sticky = tk.E + tk.W + tk.N + tk.S)
        if event.widget.fwd['Text'] and event.widget.fwd['Title']:
            text.insert(tk.END, event.widget.fwd['Title'] + '\n' + event.widget.fwd['Text'])
        else:
            text.insert(tk.END, event.widget.fwd['Title'] + event.widget.fwd['Text'])
        text.config(state = 'disabled')
        attach = tk.Button(window, text = '{} медиавложений'.format(str(len(event.widget.fwd['Attach']))))
        attach.grid(row = 2, column = 0, sticky = tk.W + tk.S)
        window.msgAttach = event.widget.fwd['Attach']
        if not event.widget.fwd['Attach']:
            attach.config(state = 'disabled')
        attach.bind('<Button-1>', showAttachList)
        attach.bind('<Button-1>', setSunken, '+')
        attach.bind('<ButtonRelease-1>', setRaised)
        fwd = tk.Button(window, text = '{} вложенных сообщений'.format(str(len(event.widget.fwd['Fwd']))))
        fwd.grid(row = 2, column = 1, sticky = tk.S + tk.E)
        window.msgFwd = event.widget.fwd['Fwd']
        if not event.widget.fwd['Fwd']:
            fwd.config(state = 'disabled')
        fwd.bind('<Button-1>', showFwdList)
        fwd.bind('<Button-1>', setSunken, '+')
        fwd.bind('<ButtonRelease-1>', setRaised)
    else:
        attach = tk.Button(window, text = '{} медиавложений'.format(str(len(event.widget.fwd['Attach']))))
        attach.grid(row = 1, column = 0, sticky = tk.W + tk.S)
        window.msgAttach = event.widget.fwd['Attach']
        if not event.widget.fwd['Attach']:
            attach.config(state = 'disabled')
        attach.bind('<Button-1>', showAttachList)
        attach.bind('<Button-1>', setSunken, '+')
        attach.bind('<ButtonRelease-1>', setRaised)
        fwd = tk.Button(window, text = '{} вложенных сообщений'.format(str(len(event.widget.fwd['Fwd']))))
        fwd.grid(row = 1, column = 1, sticky = tk.S + tk.E)
        window.msgFwd = event.widget.fwd['Fwd']
        if not event.widget.fwd['Fwd']:
            fwd.config(state = 'disabled')
        fwd.bind('<Button-1>', showFwdList)
        fwd.bind('<Button-1>', setSunken, '+')
        fwd.bind('<ButtonRelease-1>', setRaised)

    window.mainloop()

def showFwdList(event):
    window = tk.Toplevel(event.widget.master)

    canvas = tk.Canvas(window)
    scroll = tk.Scrollbar(window, command = canvas.yview)
    frame = tk.Frame(canvas)
    canvas.configure(yscrollcommand = scroll.set)
    scroll.grid(row = 0, column = 1, sticky = tk.N + tk.S)
    canvas.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W)
    for i in range(len(event.widget.master.msgFwd)):
        button = tk.Button(frame, text = event.widget.master.msgFwd[i]['Sender'])
        button.grid(row = i, column = 0)
        button.fwd = event.widget.master.msgFwd[i]
        button.bind('<Button-1>', openFwd)
        button.bind('<Button-1>', setSunken, '+')
        button.bind('<ButtonRelease-1>', setRaised)
    canvas.create_window((0, 0), window = frame, anchor = 'nw')
    def configureFrame(event):
        canvas.config(scrollregion = canvas.bbox('all'), width = frame.winfo_width(), height = min(frame.winfo_height(), 5 * button.winfo_height()))
    frame.bind('<Configure>', configureFrame)

    window.mainloop()

class MsgHistFrame(tk.Frame):
    def __init__(self, window, VKmsg):
        super(MsgHistFrame, self).__init__(window, relief = 'solid', bd = 2)

        sender = tk.Label(self, text = VKmsg['Sender'])
        sender.grid(row = 0, column = 0, sticky = tk.N + tk.W)
        title = tk.Label(self, text = VKmsg['Title'])
        title.grid(row = 0, column = 1, sticky = tk.N)
        date = tk.Label(self, text = VKmsg['Date'])
        date.grid(row = 0, column = 2, sticky = tk.N + tk.E)
        text = tk.Text(self, wrap = tk.WORD, height = 3)
        text.insert(tk.END, VKmsg['Text'])
        text.config(state = 'disabled')
        text.grid(row = 1, column = 0, columnspan = 3, sticky = tk.N + tk.E + tk.S + tk.W)
        status = tk.Label(self, text = VKmsg['Status'])
        status.grid(row = 2, column = 0, sticky = tk.S + tk.W)
        attach = tk.Button(self, text = '{} медиавложений'.format(str(len(VKmsg['Attach']))))
        attach.grid(row = 2, column = 1, sticky = tk.S)
        self.msgAttach = VKmsg['Attach']
        if not VKmsg['Attach']:
            attach.config(state = 'disabled')
        attach.bind('<Button-1>', showAttachList)
        attach.bind('<Button-1>', setSunken, '+')
        attach.bind('<ButtonRelease-1>', setRaised)
        fwd = tk.Button(self, text = '{} вложенных сообщений'.format(str(len(VKmsg['Fwd']))))
        fwd.grid(row = 2, column = 2, sticky = tk.S + tk.E)
        self.msgFwd = VKmsg['Fwd']
        if not VKmsg['Fwd']:
            fwd.config(state = 'disabled')
        fwd.bind('<Button-1>', showFwdList)
        fwd.bind('<Button-1>', setSunken, '+')
        fwd.bind('<ButtonRelease-1>', setRaised)

        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)

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
        infoButton.bind('<Button-1>', openInfoWindow)
        infoButton.bind('<Button-1>', setSunken, '+')
        infoButton.bind('<ButtonRelease-1>', setRaised)
        userNameLabel = tk.Label(self, text = VKDialog['UserName'], bg = bgColor)
        userNameLabel.grid(row = 1, column = 0, columnspan = 3, sticky = tk.W + tk.E)
        messButton = tk.Button(self, image = self.messImage)
        messButton.grid(row = 1, column = 3, sticky = tk.E)
        messButton.bind('<Button-1>', openChatWindow)
        messButton.bind('<Button-1>', setSunken, '+')
        messButton.bind('<ButtonRelease-1>', setRaised)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)

mainWindow = tk.Tk()
mainWindow.wm_title('VKMessenger')

refreshDialogsButton = tk.Button(mainWindow, text = 'Обновить диалоги')
refreshDialogsButton.grid(row = 0, column = 0, sticky = tk.W + tk.E)
refreshDialogsButton.bind('<Button-1>', refreshDialogsList)
refreshDialogsButton.bind('<Button-1>', setSunken, '+')
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
##   
