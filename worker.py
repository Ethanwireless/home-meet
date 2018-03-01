from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from microphone_recognition import audioToText

class Worker(QObject):
    txtReady = pyqtSignal(str)
    newMsg = pyqtSignal(str)

    @pyqtSlot()
    def getText(self): # A slot takes no params
        ## TODO msg formatting
        # store last 2 msg
        msgBuffer = []

        def addMsg(msg):
            if len(msgBuffer)<2:
                msgBuffer.append(msg)
            else:
                msgBuffer[0] = msgBuffer[1]
                msgBuffer[1] = msg

        def genMsg():
            msg = ''
            if (len(msgBuffer)>0):
                msg += (msgBuffer[0] + '\n')
            if (len(msgBuffer)>1):
                msg += (msgBuffer[1] + '\n')
            return msg

        def getAbstract(txt):
            if len(txt) <= 15:
                return txt
            else:
                return txt[0:7] + '...' + txt[-7:-1]+txt[-1]

        while(1):
            addMsg('Listening...')
            self.newMsg.emit(genMsg())

            txt = audioToText()
            if txt is not None:
                print('Worker get: ',txt)
                self.txtReady.emit(txt)
                abs = getAbstract(txt)
                addMsg('Text Generated: ' + abs)
                self.newMsg.emit(genMsg())
            else:
                addMsg('Google Speech Recognition could not understand audio.')
                self.newMsg.emit(genMsg())

