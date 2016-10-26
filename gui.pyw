import messenger
import sys
from PyQt4 import QtCore, QtGui

# элемент-диалог
class Dialog(QtGui.QFrame):
	def __init__(self, vkDialog):
		QtGui.QFrame.__init__(self)
		self.setFrameStyle(QtGui.QFrame.Box)
		if vkDialog['IsChat']: # диалог чата выделен жёлтым цветом
			self.setStyleSheet('QFrame {background-color : yellow;}')
		if len(vkDialog['UserName']) > 25: # имя собеседника
			name = QtGui.QLabel(vkDialog['UserName'][0:22] + "...")
		else:
			name = QtGui.QLabel(vkDialog['UserName'])
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
		self.adjustSize()

# обновление диалогов. Диалоги получаются из модуля messenger методом getVKdialogsList. Далее в виджет dialogsWindow.dialogsTab в столбец вставляются элементы-диалоги.
def refreshDialogs():
	vkDialogsList = messenger.getVKdialogsList()
	grid = dialogsWindow.dialogsTab.layout() # получаем менеджер виджета с диалогами
	while grid.itemAt(0): # удаляем из него элементы-диалоги
		grid.itemAt(0).widget().setParent(None)
	for i in range(len(vkDialogsList)): # добавляем новые элементы
		grid.addWidget(Dialog(vkDialogsList[i]), i, 0)
	if not len(vkDialogsList): # нет диалогов
		label = QtGui.QLabel('Нет диалогов!')
		grid.addWidget(label, 0, 0)
	dialogsWindow.scroll.setMinimumWidth(grid.itemAt(0).widget().width() + 55)
	dialogsWindow.scroll.setMinimumHeight(grid.itemAt(0).widget().height() * 3)

# основное окно с диалогами
class DialogsWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setWindowTitle('Диалоги') # окно с диалогами
		centralWidget = QtGui.QWidget(self) # центральный виджет окна с диалогами, где будут все элементы
		self.setCentralWidget(centralWidget)
		self.scroll = QtGui.QScrollArea(centralWidget) # scroll для виджета с элементами-диалогами
		self.dialogsTab = QtGui.QWidget(centralWidget) # виджет с элементами-диалогами
		label = QtGui.QLabel('Обновите диалоги!') # добавляем на виджет с элементами-диалогами менеджер с этикеткой-предупреждением. Согласно документации, добавление менеджера размещений необходимо сделать ДО вызова scroll.setWidget()
		grid = QtGui.QGridLayout(self.dialogsTab)
		grid.addWidget(label, 0, 0, QtCore.Qt.AlignHCenter)
		self.dialogsTab.setLayout(grid)
		self.scroll.setWidget(self.dialogsTab) # добавили менеджер размещений и теперь можем назначить виджет с диалогами на scrollArea
		self.scroll.setWidgetResizable(True)
		self.scroll.setAlignment(QtCore.Qt.AlignHCenter)
		refreshDialogsButton = QtGui.QPushButton('Обновить диалоги', parent = centralWidget) # получить и изменить в окне имеющиеся диалоги пользователя
		QtCore.QObject.connect(refreshDialogsButton, QtCore.SIGNAL('clicked()'), refreshDialogs)
		#searchCompanionButton = QtGui.QPushButton('Написать...', parent = centralWidget) # написать первое сообщение новому собеседнику
		grid = QtGui.QGridLayout(centralWidget) # менеджер размещений для центрального виджета окна с диалогами
		grid.addWidget(self.scroll, 0, 0) # ставим в менеджер виджет с диалогами и две кнопки
		grid.addWidget(refreshDialogsButton, 1, 0)
		#grid.addWidget(searchCompanionButton, 2, 0)
		centralWidget.setLayout(grid)
		self.show()

# запуск основного окна приложения
app = QtGui.QApplication(sys.argv)
dialogsWindow = DialogsWindow()
sys.exit(app.exec_())
