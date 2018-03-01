from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QTextEdit, QMessageBox, QLabel
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sys
import worker

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Home Meet'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 640

        self.firstTxt = True

        # 1 - create Worker and Thread inside the Form
        self.obj = worker.Worker()  # no parent!
        self.thread = QThread()  # no parent!
        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.obj.txtReady.connect(self.onTxtReady)
        self.obj.newMsg.connect(self.updateMsg)
        # 3 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)
        # 4 - Connect Worker Signals to the Thread slots
        # self.obj.finished.connect(self.thread.quit)
        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj.getText)
        # * - Thread finished signal will close the app if you want!
        #self.thread.finished.connect(app.exit)
        # 6 - Start the thread
        self.thread.start()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setStyleSheet("QMainWindow {background-image: url(./cat.jpg) }");

        # textbox showing recognized test
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 300)
        ## TODO relative size
        self.textbox.resize(600, 300)
        self.textbox.setText('Text to be shown here...')
        self.textbox.moveCursor(QtGui.QTextCursor.End)

        # status bar showing current status
        self.statusBar().showMessage('Message in statusbar.')
        self.show()

    def onTxtReady(self, txt):
        ## TODO formatting
        if self.firstTxt:
            self.textbox.setText(txt)
            self.textbox.moveCursor(QtGui.QTextCursor.End)
            self.firstTxt = False
        else:
            self.textbox.append(txt)
            self.textbox.moveCursor(QtGui.QTextCursor.End)

    def updateMsg(self, msg):
        self.statusBar().showMessage(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

