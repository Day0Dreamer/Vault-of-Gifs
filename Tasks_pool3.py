from PySide.QtCore import QObject, Signal, QProcess, QTimer
from PySide.QtGui import QApplication


cmd = 'bin/fake_renderer.exe'


class TasksPool(QObject):
    startNextTaskSignal = Signal()
    allTasksCompleteSignal = Signal()

    def __init__(self):
        super(TasksPool, self).__init__()
        self.tasks_pool = []
        self.process = QProcess()

        self.startNextTaskSignal.connect(self.execute_task)
        self.allTasksCompleteSignal.connect(self.tasks_complete)

        self.source = ''

    def add_task(self, command):
        self.tasks_pool.append(command)
        self.startNextTaskSignal.emit()

    def execute_task(self):
        print('Start next?')
        if self.process.isOpen():
            self.process.waitForFinished()
        if not self.tasks_pool:
            self.allTasksCompleteSignal.emit()
            return
        self.process = QProcess()
        self.process.finished.connect(lambda *x: QTimer.singleShot(1000, self.startNextTaskSignal.emit))
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.process_output)
        next_task = self.tasks_pool.pop(0)
        print('NEXT TASK', next_task)
        self.process.start(next_task)

    def process_output(self):
        output = self.process.readAll()
        output = str(output).strip()
        if output:
            print(output)

    def tasks_complete(self):
        print('ALL TASKS COMPLETE')


if __name__ == '__main__':
    qapp = QApplication([])
    inst = TasksPool()
    inst.add_task('bin/fake_renderer.exe')
    inst.add_task('bin/ffmpeg.exe')
    inst.add_task('bin/gifsicle.exe -h')
    inst.add_task('bin/gifsicle.exe -h')
    qapp.exec_()


