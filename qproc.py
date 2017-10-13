from PySide import QtCore
from PySide import QtGui


# def calc(parent, program='calc.exe',arg=''):
#     calc = QtCore.QProcess(parent)
#     return calc.start(program, arg)

class MyW(QtGui.QWidget):
    def __init__(self):
        super(MyW, self).__init__()
        w = QtGui.QMainWindow()
        l = QtGui.QVBoxLayout()

        self.calc = QtCore.QProcess(self)
        self.calc.readyReadStandardOutput.connect(self.__read)
        # # self.calc.start('ping.exe',['127.0.0.1'])
        self.calc.start('gifsicle.exe',['C:\\Python\\Vault_Of_Gifs\\SteffonDiggsEmoji-02-280x280-30FPS.gif', '-o C:/Python/Vault_Of_Gifs/SteffonDiggsEmoji-02-280x280-30FPS.tmp'])

    def __read(self):
        out = self.calc.readAllStandardOutput()
        print(out)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = MyW()
    w.show()
    app.exec_()