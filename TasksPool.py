# encoding: utf-8
"""
This module allows you to queue and launch processes using PySide's QProcess
"""
from PySide.QtCore import QObject, QProcess, Signal, QEventLoop
from PySide.QtGui import QApplication


class TasksPool(QObject):
    """
    This class allows you to add_task() for execution queue. Launch_list() starts the queue.
    """
    task_done = Signal()

    def __init__(self):

        super(TasksPool, self).__init__()
        self.tasks_pool = []
        self.process = None
        if not QApplication.instance():
            self.qapp = QApplication([])


    def add_task(self, command):
        """
        :type command: str
        :param command: A console command with arguments
        Adds a task to the pool for later execution
        """
        self.tasks_pool.append(command)

    def __execute_task(self, task):
        """
        :param task: Is a string used to start a process
        """
        process = QProcess(self)
        process.finished.connect(lambda *x: print(task, 'reports done'))
        process.finished.connect(self.task_done)
        process.readyRead.connect(lambda *x: print(str(process.readAll())))
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.start(task)

    def launch_list(self):
        """
        Starts the execution of the queue in consecutive order, waiting for previous process to finish
        """
        for task in self.tasks_pool:
            loop = QEventLoop()
            self.task_done.connect(loop.quit)
            self.__execute_task(task)
            loop.exec_()
