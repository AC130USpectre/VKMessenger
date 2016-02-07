from tkinter import *
import messenger

def openChatWindow(event):
    ID = event.widget.master.userID
    print(ID)

def openInfoWindow(event):
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

class Dialog(Frame):
    def __init__(self, window, VKDialog, num):
        super(Dialog, self).__init__(window, bd = 2, bg = {False: 'white', True : 'yellow'}[VKDialog['IsChat']], relief = 'solid')
        status = Label(self, text = VKDialog['Status'], bg = 'white')
        status.grid(row = 1, column = 2)
        name = Label(self, text = VKDialog['UserName'], bg = 'white')
        name.grid(row = 2, column = 1, columnspan = 2)
        openDialogButton = Button(self, text = 'Сообщения')
        openDialogButton.grid(row = 3, column = 1)
        openDialogButton.bind('<Button-1>', openChatWindow)
        openInfoButton = Button(self, text = 'Инфо')
        openInfoButton.grid(row = 3, column = 2)
        openInfoButton.bind('<Button-1>', openInfoWindow)
        self.grid(row = num, column = 1)
        self.userID = VKDialog['UserID']

dialogWindow = Tk()
dialogWindow.wm_title('VKMessenger')
refreshDialogsButton = Button(dialogWindow, text = 'Обновить диалоги')
refreshDialogsButton.grid(row = 1, column = 1)
dialogFramesList = []
def refreshDialogsList(event):
    for dialog in dialogFramesList:
        dialog.destroy()
        dialogFramesList.remove(dialog)
    VKdialogs = messenger.getVKdialogsList()
    i = 2
    for VKdialog in VKdialogs:
        dialogFramesList.append(Dialog(dialogWindow, VKdialog, i))
        i += 1
    
refreshDialogsButton.bind('<Button-1>', refreshDialogsList)
dialogWindow.mainloop()
