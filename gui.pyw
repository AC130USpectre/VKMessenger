#import messenger
#import webbrowser
import sys
from PyQt4 import QtGui

class DialogsWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Диалоги') # окно с диалогами
        formWidget = QtGui.QWidget(self)
        self.setCentralWidget(formWidget)
        refreshDialogsButton = QtGui.QPushButton('Обновить диалоги', parent = formWidget)
        searchCompanionButton = QtGui.QPushButton('Написать...', parent = formWidget)
        grid = QtGui.QGridLayout(formWidget) # выстраиваем две кнопки по сетке
        grid.addWidget(refreshDialogsButton, 0, 0)
        grid.addWidget(searchCompanionButton, 1, 0)
        formWidget.setLayout(grid)
        self.show()

app = QtGui.QApplication(sys.argv)
dialogsWindow = DialogsWindow()
sys.exit(app.exec_())
