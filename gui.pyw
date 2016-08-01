import messenger
#import webbrowser
import sys
from PyQt4 import QtCore, QtGui

# элемент-диалог
class Dialog(QtGui.QFrame):
	def __init__(self, vkDialog):
		QtGui.QFrame.__init__(self)
		self.setFrameStyle(QtGui.QFrame.Box)
		if vkDialog['IsChat']: # диалог чата выделен жёлтым цветом
			self.setStyleSheet('QFrame {background-color : yellow;}')
		name = QtGui.QLabel(vkDialog['UserName']) # имя собеседника
		status = QtGui.QLabel(vkDialog['Status']) # статус Он/Оффлайн собеседника
		if len(vkDialog['Status']) == 6: # Онлайн
			status.setStyleSheet('background-color : green')
		elif len(vkDialog['Status']) == 7: # Оффлайн
			status.setStyleSheet('background-color : red')
		unread = QtGui.QLabel('Непрочитанных сообщений: ' + str(vkDialog['UnreadCount']))
		messageButton = QtGui.QPushButton('', parent = self)
		messageButton.setIcon(QtGui.QIcon('dialog.png'))
		infoButton = QtGui.QPushButton('', parent = self)
		infoButton.setIcon(QtGui.QIcon('info.png'))
		grid = QtGui.QGridLayout(self)
		grid.addWidget(name, 0, 0, QtCore.Qt.AlignLeft)
		grid.addWidget(status, 0, 1, QtCore.Qt.AlignRight)
		grid.addWidget(messageButton, 0, 2)
		grid.addWidget(unread, 1, 0, 1, 2, QtCore.Qt.AlignHCenter)
		grid.addWidget(infoButton, 1, 2)

# обновление диалогов. Диалоги получаются из модуля messenger методом getVKdialogsList. Далее в виджет dialogsWindow.dialogsTab в столбец вставляются элементы-диалоги. 
def refreshDialogs():
	vkDialogsList = messenger.getVKdialogsList()
	if dialogsWindow.dialogsTab.layout(): # если менеджер размещений уже есть, переназначаем его на временный QWidget, который удаляется сборщиком мусора. В результате менеджер также удаляется
		QtGui.QWidget().setLayout(dialogsWindow.dialogsTab.layout())
	grid = QtGui.QGridLayout(dialogsWindow.dialogsTab)
	for i in range(len(vkDialogsList)):
		grid.addWidget(Dialog(vkDialogsList[i]), i, 0)
	if not len(vkDialogsList): # нет диалогов
		label = QtGui.QLabel('Нет диалогов!')
		grid.addWidget(label, 0, 0)
	dialogsWindow.dialogsTab.setLayout(grid)
	dialogsWindow.dialogsTab.show()

# основное окно с диалогами
class DialogsWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setWindowTitle('Диалоги') # окно с диалогами
		formWidget = QtGui.QWidget(self) # центральный виджет окна с диалогами, где будут все элементы
		self.setCentralWidget(formWidget)
		self.dialogsTab = QtGui.QWidget(formWidget) # виджет с элементами-диалогами
		self.dialogsTab.hide()
		refreshDialogsButton = QtGui.QPushButton('Обновить диалоги', parent = formWidget) # получить и изменить в окне имеющиеся диалоги пользователя
		QtCore.QObject.connect(refreshDialogsButton, QtCore.SIGNAL('clicked()'), refreshDialogs)
		searchCompanionButton = QtGui.QPushButton('Написать...', parent = formWidget) # написать первое сообщение новому собеседнику
		grid = QtGui.QGridLayout(formWidget) # менеджер размещений для центрального виджета окна с диалогами
		grid.addWidget(self.dialogsTab, 0, 0) # ставим в менеджер виджет с диалогами и две кнопки
		grid.addWidget(refreshDialogsButton, 1, 0)
		grid.addWidget(searchCompanionButton, 2, 0)
		formWidget.setLayout(grid)
		self.show()

# запуск основного окна приложения
app = QtGui.QApplication(sys.argv)
dialogsWindow = DialogsWindow()
sys.exit(app.exec_())
