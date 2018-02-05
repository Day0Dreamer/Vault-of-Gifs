# encoding: utf-8
import os  # todo убрать этот импорт
# todo Добавить нахождение файлов gif если нет avi
# todo Вынести with open(self.color_table, 'w') as txt: в отдельную функцию

# todo При выборе папки во вьюверы должны автоматически конвевртироваться из avi и загружаться версии с максимальным FPS
# todo (это не обязательно 30FPS) готовые для кручения Lossy.
# todo При выборе видео/гиф с другим фпс он должна загружаться в соответсвующий вьювер.
# todo При нажатии кнопки экспорт должна производится конвертация ВСЕХ avi в выбранной папке (с соответсвующими
# todo настройками Lossy для 136x136 и 280x280), далее конвертация DAMAGED-версий, затем конвертация файла с именем
# todo [NameofComposition[Version]].mov в h264 с настройками кодека на 100%.
# todo При повторном выборе папки, с уже произведённым экспортом повевдение программы меняться не должно - при любом
# todo совпадении по именам - овверайдить без диалоговых окон.
# todo Сборка проекта:
# todo При нажатии на кнопку "Collect and Send Project Files" долже запускаться отдельный скрипт.
# todo Кнопка должна быть активна только при выбранной папке.
#
# todo 0. Зум по умолчанию 2x, ограничить шкалу от 1x до 4x у обоих вьюверов.
# todo 1. Дебаг автоподгрузки 136х136 при выборе папки.
# todo 2. Конвертация в мп4 пока не работает.
# todo 3. Переименовываем Collect Project в Clean Project Folder. При нажатии на кнопку должно проихсодить следующее:
# todo а. Удаляться все временные файлы (палитры)
# todo б. Удаляться все avi файлы из которых делались гифки.
# todo в. Удаляться NameOfFile_Version.mov при успешной конвертации в mp4,
# todo г. act таблицу импортрованную из папки ps удалять не нужно!
#
# todo Примерный функционал БУДЕТ выглядеть так
# todo а. Найти месторасположение выбранной папки.
# todo б. Удалить в выбранной папке все avi файлы, др. файлы не
# todo б. Перейти на уровень выше и загрузить выбранную папку с именем
# todo [NameofComposition[Version]] и папку с именем [NameofComposition[Version]]_sources на сервер.

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide.QtGui import QDialog

from handbrake import Handbrake
from widgets import MainWindow_UI, about
from widgets import settings
from widgets import stylesheet

from os import path, listdir, walk, remove, rmdir, makedirs
import subprocess
from shutil import copy2
from time import sleep
import winreg
from send2trash import send2trash

import logging  # Logging is configured inside config module
from config import Config
from TasksPool import TasksPool
from gifsicle import GifSicle
from ffmpeg import FFmpeg
from emoji import Emoji
from export import Conversion
import act_reader
import updater

# ################################# CONFIG ################################### #
config = Config()
fps_delays = config()['fps_delays']
damaged_filesize = int(config()['damaged_filesize'])
logging_level = config()['logging_level']
console_flag = config()['console_enabled']
default_project_folder = config()['default_folder']
preload_files = config()['preload_files']
icons_folder_name = 'icons'

# ################################ LOGGING ################################### #
# # todo сделать так, чтобы логгер писал имя файла откуда лог


class PsFolder(object):
    def __init__(self):
        self.ps_paths = PsFolder.parse_versions(PsFolder.versions())

    def __getitem__(self, index):
        return self.ps_paths[index]

    def __repr__(self):
        return str(self.ps_paths)

    @staticmethod
    def versions() -> list:
        installed_versions = []
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Adobe\Photoshop') as hKey:
            # Get the information about the key.
            subkey_count, values_count, modtime = winreg.QueryInfoKey(hKey)
            installed_versions_count = subkey_count
            for version in range(installed_versions_count):
                installed_versions.append(winreg.EnumKey(hKey, version))
            return installed_versions

    @staticmethod
    def parse_versions(versions: list) -> list:
        """

        :type versions: list
        """
        ps_paths = []
        for version in versions:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Adobe\Photoshop\{}'.format(version)) as hKey:
                subkey_count, values_count, modtime = winreg.QueryInfoKey(hKey)
                for value in range(values_count):
                    if winreg.EnumValue(hKey, value)[0] == 'SettingsFilePath':
                        adobe_ps_roaming_settings_dir = winreg.EnumValue(hKey, value)[1]
                        adobe_ps_roaming = path.dirname(path.dirname(adobe_ps_roaming_settings_dir))
                        adobe_ps_roaming_act = path.join(adobe_ps_roaming,'Optimized Colors')
                        ps_paths.append(adobe_ps_roaming_act)
                        break
        return ps_paths


class VideoListModel(QtCore.QAbstractListModel):

    def __init__(self, emojis={}):
        super(VideoListModel, self).__init__()
        self.emoji_dict = emojis
        # Convert dict to list and sort it
        self.emoji_list = sorted(list(emojis.keys()), key=lambda x: (emojis[x].resolution, emojis[x].fps))

    def rowCount(self, parent):
        return len(self.emoji_dict)

    def data(self, index, role):
        # For each parse through get the emoji using the index int
        emoji = self.emoji_dict[self.emoji_list[index.row()]]
        # Use first UserRole as a handle to the Emoji object
        if role == 32:
            return emoji
        # Setup the text we see in the list
        if role == QtCore.Qt.DisplayRole:
            return str(emoji.name)
        # Setup the icon we see in the list
        if role == QtCore.Qt.DecorationRole:
            icon_path = path.join(path.curdir, icons_folder_name, "{}_{}.png".format(emoji.resolution, emoji.fps))
            if path.exists(icon_path):
                icon = QtGui.QIcon(icon_path)
            else:
                icon = QtGui.QPixmap(32, 32)
            return icon
        # Setup the tooltip
        if role == QtCore.Qt.ToolTipRole:
            return emoji.full_info().replace(' | ', '\n')
        if role == QtCore.Qt.BackgroundRole:
            if emoji.has_gif:
                return QtGui.QBrush(QtGui.QColor(50, 60, 50, 255))

    def update(self, folder):
        pass
        self.rowsAboutToBeInserted.emit(self,0,0)
        self.act_list = files_in_folder(folder, 'act')
        self.rowsInserted.emit(self,0,0)


class ActListModel(QtCore.QAbstractListModel):

    def __init__(self, act_list):
        super(ActListModel, self).__init__()
        self.act_list = []
        self.update(act_list)

    def rowCount(self, parent):
        return len(self.act_list)

    def data(self, index, role):
        # For each parse through get the emoji using the index int
        act_file = self.act_list[index.row()]
        # Use first UserRole as a handle to the Emoji object
        if role == 32:
            return act_file
        # Setup the text we see in the list
        if role == QtCore.Qt.DisplayRole:
            return path.splitext(path.split(act_file)[-1])[0]
        # Setup the icon we see in the list
        if role == QtCore.Qt.DecorationRole:
            icon_path = r"icons\ps.png"
            if path.exists(icon_path):
                icon = QtGui.QIcon(icon_path)
            else:
                icon = QtGui.QPixmap(16, 16)
            return icon
        # Setup the tooltip
        if role == QtCore.Qt.ToolTipRole:
            return act_file
            # return emoji.full_info().replace(' | ', '\n')
        # if role == QtCore.Qt.BackgroundRole:
        #     if emoji.has_gif:
        #         return QtGui.QBrush(QtGui.QColor(50, 60, 50, 255))

    def update(self, folder):
        self.reset()
        self.rowsAboutToBeInserted.emit(self,0,0)
        self.beginInsertRows(self.index(0),0,0)
        try:
            self.act_list = files_in_folder(folder, 'act')
        except FileNotFoundError:
            logging.warning("Ye, there an error, but we don't care")
        self.endInsertRows()
        self.rowsInserted.emit(self,0,0)
        # if len(self.act_list) == 0:
        #     error_message = 'Please import one color_palette.act inside \n{}'.format(path.abspath(folder))
        #     logging.warning(error_message.replace('\n',''))
        #     error_box = QtGui.QMessageBox()
        #     error_box.setStyleSheet(stylesheet.houdini)
        #     error_box.setWindowTitle('File error')
        #     error_box.setText('There is .act file missing'+' '*50)
        #     error_box.setInformativeText(error_message)
        #     error_box.exec_()


def files_in_folder(folder, ext):
    try:
        result = [path.join(path.abspath(folder), file) for file in listdir(folder) if '.'+str(ext) == path.splitext(file)[1]]
    except FileNotFoundError as e:
        logging.warning(e)
        result = ''
    return result


def make_folder_structure():
    makedirs('temp', exist_ok=True)
#     makedirs('bin', exist_ok=True)
make_folder_structure()


def clean_folder(folder: str):
    for root, dirs, files in walk(folder, topdown=False):
        for name in files:
            try:
                remove(path.join(root, name))
            except Exception as e:
                return e
        sleep(.01)
        for name in dirs:
            rmdir(path.join(root, name))


class QtMainWindow(QtGui.QMainWindow, MainWindow_UI.Ui_MainWindow):
    # todo прикрутить ПКМ меню в списке видосов
    # todo сделать сортировку в меню списка видосов
    def __init__(self, input_folder=default_project_folder):
        super(QtMainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet.houdini)

        self.working_directory = input_folder
        self.videolist_model = None
        self.ffmpeg = None
        self.gifsicle = None
        self.movie136 = QtGui.QMovie()
        self.movie280 = QtGui.QMovie()
        self.working_emoji = None
        self.lossy_file_size = None
        self.lossy_factor = None
        self.output_file = None
        self.original_280_gif = None
        self.original_136_gif = None
        self.loaded_280 = None
        self.loaded_136 = None
        self.tp = None
        self.color_table = None
        # todo разобраться с self.launcher self.launcher = Launcher()
        # todo разобраться с self.main_task_pool self.main_task_pool = TasksPool()

        # ############################ MODIFY INTERFACE ############################## #
        # todo исправить размер интерфейса self.setGeometry(200, 200, 40, 40)

        self.setWindowTitle('Vault of Gifs | v 0.1')
        # Modify relationship between main interface columns
        self.splitter_main.setStretchFactor(0, 1)
        self.splitter_main.setStretchFactor(2, 2)
        self.splitter_main.setStretchFactor(1, 3)

        # Max size of icons in video list
        self.list_videoslist.setIconSize(QtCore.QSize(32, 32))

        # Update the video list on initial program start
        if len(self.working_directory):
            self.make_video_list()

        # ################################# TOP BAR ################################## #
        # File menu
        # Connect "Open folder" to other Open folder button
        self.actionChooseFolder.triggered.connect(self.btn_input_folder.clicked)

        @self.actionExit.triggered.connect
        def exit_ui():
            exit(0)

        # Options menu
        @self.actionConfig.triggered.connect
        def call_settings():
            self.dial = settings.QtSettings()
            self.dial.exec_()
        # todo доработать окно settings

        @self.actionDelete_temp_files.triggered.connect
        def clear_temp_folder():
            if len(listdir('temp')) != 0:
                cleaning_result = clean_folder('temp')
                if cleaning_result:
                    self.console_add(cleaning_result)
                sleep(.1)
                if len(listdir('temp')) == 0:
                    self.statusbar.showMessage('Temp folder is cleaned')
                else:
                    self.statusbar.showMessage('Trying to clean temp folder, but failed')

        # todo вынести добавление консоли в другое место
        self.console = QtGui.QTextBrowser(self)
        self.console.setWordWrapMode(QtGui.QTextOption.NoWrap)
        # self.layout3in1.addWidget(self.console)
        self.console.setMinimumWidth(500)
        self.console.setVisible(console_flag)
        @self.actionShow_console.triggered.connect
        def show_console():
            self.console.setVisible(not self.console.isVisible())
            if self.console.isVisible():
                self.statusbar.showMessage('Console is enabled')
            else:
                self.statusbar.showMessage('Console is disabled')

        # Button for deleting gif files in the working directory
        self.actionDelete_gif_files = QtGui.QAction(self)
        self.actionDelete_gif_files.setObjectName("actionDelete_temp_files")
        self.menuOptions.addAction(self.actionDelete_gif_files)
        self.actionDelete_gif_files.setText(QtGui.QApplication.translate("MainWindow", "&Clean generated gifs", None, QtGui.QApplication.UnicodeUTF8))
        @self.actionDelete_gif_files.triggered.connect
        def clean_gifs():
            self.actionUnloadGifs.triggered.emit()  # Stop and unload playing gifs
            for i in files_in_folder(self.working_directory, 'gif'):
                remove(i)
            # self.update_video_list()
            self.make_video_list()

        # Button for unloading running gifs in the viewports
        self.actionUnloadGifs = QtGui.QAction(self)
        self.actionUnloadGifs.setObjectName("actionDelete_temp_files")
        self.menuOptions.addAction(self.actionUnloadGifs)
        self.actionUnloadGifs.setText(QtGui.QApplication.translate("MainWindow", "&Unload gifs", None, QtGui.QApplication.UnicodeUTF8))
        @self.actionUnloadGifs.triggered.connect
        def unload_gifs():
            self.movie136.setFileName('')
            self.movie280.setFileName('')

        self.actionmov2mp4.triggered.connect(self.convert_mov_to_mp4)

        # About menu
        @self.actionAbout.triggered.connect
        def call_about():
            # self.dial = settings.QtSettings() # Изменить
            # self.dial.exec_()
            print(self.size())
            self.dial = about.QtAbout()
            self.dial.exec_()
        # todo доработать окно about

        # ############################### LEFT COLUMN ################################ #
        @self.btn_input_folder.clicked.connect
        def input_folder():
            # options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
            directory = QtGui.QFileDialog.getExistingDirectory(self)
            if directory:
                self.working_directory = directory
                # self.update_video_list()
                self.make_video_list()
                self.actlist_model.update(directory)
                self.dropdown_colortable.setCurrentIndex(0)
                # load the most fps image
                if preload_files:
                    self.movie136.setFileName('')
                    self.movie136.stop()
                    self.movie280.setFileName('')
                    self.movie280.stop()
                    # get count of how many items are in the video list
                    items_count = self.videolist_model.rowCount(self.videolist_model)
                    res136 = {}  # Dict for only 136 entries
                    res280 = {}  # Dict for only 280 entries
                    # Walk through the model and separate entries by resolution
                    for item in range(items_count):
                        emoji = self.videolist_model.data(self.actlist_model.index(item), 32)
                        print(emoji)
                        if emoji.resolution == '136x136':
                            res136.update({str(emoji.fps): item})
                        elif emoji.resolution == '280x280':
                            res280.update({str(emoji.fps): item})
                    # Sort entries by highest FPS
                    fps_136 = sorted(res136.keys(), reverse=True)
                    fps_280 = sorted(res280.keys(), reverse=True)
                    # print(res136.keys())
                    if len(fps_136):
                        top_fps_136 = sorted(res136.keys(), reverse=True)[0]
                        # Click on the appropriate items in the ModelViewer
                        avi_activated(self.videolist_model.index(res136[top_fps_136]))
                        avi_activated(self.videolist_model.index(res136[top_fps_136]))
                    if len(fps_280):
                        top_fps_280 = sorted(res280.keys(), reverse=True)[0]
                        # Click on the appropriate items in the ModelViewer
                        avi_activated(self.videolist_model.index(res280[top_fps_280]))
                        avi_activated(self.videolist_model.index(res280[top_fps_280]))
        self.btn_input_folder.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        @self.btn_input_folder.customContextMenuRequested.connect
        def btn_input_folder_open_menu(pos):
            subprocess.Popen(r'explorer "{}"'.format(self.working_directory))

        def avi_activated(video_list_item):
            self.working_emoji = video_list_item.data(32)
            # Calling FFmpeg if there is no gif created
            print(type(settings.overwrite_gifs))
            if not self.working_emoji.has_gif or settings.overwrite_gifs:
                self.statusbar.showMessage('Generating the gif')
                self.ffmpeg = FFmpeg()
                self.ffmpeg.return_signal.connect(self.console_add)
                self.ffmpeg.add(self.working_emoji.full_path, self.working_emoji.fps)
                self.console_add('='*50)
                self.console_add('Converting {} using ffmpeg'.format(self.working_emoji.full_path))
                self.ffmpeg.run()
                self.console_add('='*50+'\n')
                self.ffmpeg.return_signal.disconnect(self.console_add)
                self.working_file = self.working_emoji.full_path
                # self.load_gif(self.working_emoji.gif_path)
                # self.update_video_list()
                self.make_video_list()
                self.load_gif(self.working_emoji.gif_path)
            else:
                self.load_gif(self.working_emoji.gif_path)
            if self.working_emoji.resolution == '136x136':
                self.loaded_136 = self.working_emoji
            elif self.working_emoji.resolution == '280x280':
                self.loaded_280 = self.working_emoji
        self.list_videoslist.activated.connect(avi_activated)

        # Add acts from folder to list widget
        # todo if len(self.working_directory):
        if True:
            self.actlist_model = ActListModel(self.working_directory)
            # self.actlist_model.no_act_files_found.connect(QtError())
            # QtError()
            # todo 000
            self.dropdown_colortable.setModel(self.actlist_model)

        @self.dropdown_colortable.currentIndexChanged.connect
        def dropdown_colortable_selected(index_of_selected_item):
            act_file_path = self.dropdown_colortable.itemData(index_of_selected_item, 32)
            self.current_act = self.load_act(act_file_path)

        @self.btn_import_act.clicked.connect
        def import_act_clicked():
            photoshop_paths = PsFolder().ps_paths
            # print(photoshop_paths[0])
            if len(photoshop_paths) > 1:
                logging.warning('Multiple Photoshop paths found, using {}'.format(photoshop_paths[0]))
            files, filtr = QtGui.QFileDialog.getOpenFileNames(self,
                                                              "Choose your color table",
                                                              '{}'.format(photoshop_paths[0]),
                                                              "All Files (*.*);;A color table (*.act)",
                                                              "A color table (*.act)"
                                                              )

            def copy_act(act_file):  # Compact repeating function
                copy2(act_file, path.join(self.working_directory, path.basename(act_file)))

            user_choice = None
            for file in files:
                # If there is a file existing and if user has NOT clicked YesToAll ask him
                if path.exists(path.join(path.abspath(self.working_directory), path.basename(file))) and user_choice != QtGui.QMessageBox.YesToAll:
                    error_box = QtGui.QMessageBox()
                    error_box.setStyleSheet(self.styleSheet())
                    error_box.setWindowTitle('File error')
                    error_box.setText('The file {} exists in {}'.format(path.basename(file),
                                                                        path.abspath(self.working_directory)))
                    error_box.setInformativeText('Do you want to overwrite it?')
                    error_box.setStandardButtons(QtGui.QMessageBox.YesToAll | QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    error_box.setDefaultButton(QtGui.QMessageBox.No)
                    user_choice = error_box.exec_()
                    if user_choice == QtGui.QMessageBox.Yes or user_choice == QtGui.QMessageBox.YesToAll:
                        copy_act(file)
                else:
                    copy_act(file)

            self.actlist_model.update(self.working_directory)
            # Select the first of selected files in the dropdown menu
            first_file = files[0]
            first_file_stripped = path.splitext(path.basename(first_file))[0]
            index = self.actlist_model.index(0)
            index_of_first_item = self.actlist_model.match(index, QtCore.Qt.DisplayRole, first_file_stripped)
            if len(index_of_first_item):
                index_of_first_item = index_of_first_item[0].row()
                self.dropdown_colortable.setCurrentIndex(index_of_first_item)
            else:
                raise FileNotFoundError

                # todo update the act file model

        @self.btn_export.clicked.connect
        def btn_export_clicked():

            if self.actlist_model.rowCount(self) == 0:
                if self.working_directory == '':
                    error_message = 'There is no project directory specified'
                else:
                    error_message = 'Please import one color_palette.act inside \n{}'.format(self.working_directory)
                logging.warning(error_message.replace('\n', ''))
                error_box = QtGui.QMessageBox()
                error_box.setStyleSheet(stylesheet.houdini)
                error_box.setWindowTitle('File error')
                error_box.setText('There is .act file missing'+' '*50)
                error_box.setInformativeText(error_message)
                error_box.exec_()
                return 1

            # Dictionary two lossy values from their interface spinners
            lossy_dict = {'136': self.spin_quality136.text(), '280': self.spin_quality280.text()}
            self.color_table = path.join('.\\temp', 'current_act.txt')
            # We generate a colormap from the colormap viewer window
            with open(self.color_table, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self.color_table
            self.actionUnloadGifs.triggered.emit()  # Stop and unload playing gifs
            # Start export conversion using dir user selected and lossy dict
            self.conversion = Conversion(self.working_directory, lossy_dict, color_table)
            self.conversion.conversion5_done.connect(self.make_video_list(self.working_directory))

        @self.btn_clean.clicked.connect
        def clean():
            self.console_add('Cleaning process has started')
            self.statusbar.showMessage('Cleaning process has started')
            files_to_delete = files_in_folder(self.working_directory, 'avi')
            files_to_delete.extend(files_in_folder(self.working_directory, 'tmp'))
            files_to_delete_names = [path.basename(file) for file in files_to_delete]
            box = QtGui.QMessageBox()
            box.setStyleSheet(self.styleSheet())
            # box_layout = box.layout()
            # box_layout.setColumnMinimumWidth(1,500)
            # QtGui.QGridLayout.set
            box.setWindowTitle('Clean up')
            box.setText('You are about to delete: \n{}'.format('\n'.join(str(x) for x in files_to_delete_names)))
            box.setInformativeText('Are you sure?')
            box.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            box.setDefaultButton(QtGui.QMessageBox.No)
            user_choice = box.exec_()
            if user_choice == QtGui.QMessageBox.Yes:
                [send2trash(file) for file in files_to_delete]

        self.btn_export.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        @self.btn_export.customContextMenuRequested.connect
        def btn_input_folder_open_menu(pos):
            self.slider_scale136.setValue(1)
            self.slider_scale280.setValue(1)
            self.minimal_size()

        # ############################## MIDDLE COLUMN ############################### #

        @self.btn_fb280.clicked.connect
        def btn_fb280_clicked():
            current_frame = self.movie280.currentFrameNumber()
            self.movie280.jumpToFrame(0)
            for i in range(current_frame - 1):
                self.movie280.jumpToNextFrame()
            fps = '\tFPS: ' + str(round(1000 / self.movie280.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie280.nextFrameDelay())
            frame_n = str(self.movie280.currentFrameNumber())
            self.statusbar.showMessage('280px: Jumped to frame #' + frame_n + fps + delay)

        @self.btn_playpause280.clicked.connect
        def btn_playpause280_clicked():
            if self.btn_playpause280.isChecked():
                self.movie280.setPaused(True)
                self.statusbar.showMessage('280px: Paused on frame #' + str(self.movie280.currentFrameNumber()))
            else:
                self.movie280.setPaused(False)
                self.statusbar.showMessage('280px: Playing')

        @self.btn_ff280.clicked.connect
        def btn_ff280_clicked():
            self.movie280.jumpToNextFrame()
            fps = '\tFPS: ' + str(round(1000 / self.movie280.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie280.nextFrameDelay())
            frame_n = str(self.movie280.currentFrameNumber())
            self.statusbar.showMessage('280px: Jumped to frame #' + frame_n + fps + delay)

        @self.slider_speed280.valueChanged.connect
        def speed280_slider_changed(value):
            self.statusbar.showMessage('Speed of 280px changed to {}x'.format(value/100))
            self.spin_speed280.blockSignals(True)
            self.spin_speed280.setValue(value * 0.01)
            self.spin_speed280.blockSignals(False)
            self.movie280.setSpeed(value)

        @self.spin_speed280.valueChanged.connect
        def speed280_spinner_changed(value):
            value = round(value, 2)
            self.statusbar.showMessage('Speed of 280px changed to {}x'.format(value))
            value *= 100
            self.slider_speed280.setValue(value)
            self.movie280.setSpeed(value)

        self.previous_scale280 = self.spin_scale280.value()
        @self.spin_scale280.valueChanged.connect
        def spin_scale280_value_changed(value):
            self.statusbar.showMessage('Zoom of 280px changed to {}x'.format(value))
            self.graphicsView_280.scale(1/self.previous_scale280, 1/self.previous_scale280)
            self.graphicsView_280.scale(value, value)
            self.slider_scale280.setValue(value)
            self.previous_scale280 = self.spin_scale280.value()

        self.spin_scale280.valueChanged.emit(self.spin_scale280.value())

        @self.spin_quality280.valueChanged.connect
        def spin_quality280_value_changed():
            if self.check_livepreview280.isChecked():
                btn_update280_clicked()

        def btn_update280_clicked():
            # working_file = self.movie280.fileName()
            working_file = self.loaded_280.gif_path
            print(working_file)
            output_file = path.splitext(working_file)[0] + '.tmp'
            self.movie280.stop()
            lossy_factor = self.spin_quality280.text()
            # Instead of generating a txt file for a colortable
            # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            self.color_table = path.join('.\\temp', 'current_act.txt')
            # We generate a colormap from the colormap viewer window
            with open(self.color_table, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self.color_table

            # self.btn_update280.setEnabled(False)
            self.gc = GifSicle(self.loaded_280, lossy_factor, color_table)
            # self.gc = GifSicle() todo разобраться что происходит тут
            # self.gc.return_signal.connect(lambda x: print(x))
            # self.gc.add(self.working_emoji, lossy_factor, color_table)
            # self.gc.run()
            # .return_signal.connect(self.console_add)

            self.load_gif(output_file)
            temp_file_size = path.getsize(output_file)/1024
            self.statusbar.showMessage('Resulting filesize is: {:.2f} Kb'.format(temp_file_size))
        self.btn_update280.clicked.connect(btn_update280_clicked)

        # ############################### RIGHT COLUMN ############################### #

        # Load the color table viewer
        if len(default_project_folder):
            files = files_in_folder(self.working_directory, 'act')
            if len(files):
                self.load_act(files[self.dropdown_colortable.currentIndex()])

        @self.btn_fb136.clicked.connect
        def btn_fb136_clicked():
            current_frame = self.movie136.currentFrameNumber()
            self.movie136.jumpToFrame(0)
            for i in range(current_frame - 1):
                self.movie136.jumpToNextFrame()
            fps = '\tFPS: ' + str(round(1000 / self.movie136.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie136.nextFrameDelay())
            frame_n = str(self.movie136.currentFrameNumber())
            self.statusbar.showMessage('136px: Jumped to frame #' + frame_n + fps + delay)

        @self.btn_playpause136.clicked.connect
        def btn_playpause136_clicked():
            if self.btn_playpause136.isChecked():
                self.movie136.setPaused(True)
                self.statusbar.showMessage('136px: Paused on frame #' + str(self.movie136.currentFrameNumber()))
            else:
                self.movie136.setPaused(False)
                self.statusbar.showMessage('136px: Playing')

        @self.btn_ff136.clicked.connect
        def btn_ff136_clicked():
            self.movie136.jumpToNextFrame()
            fps = '\tFPS: ' + str(round(1000 / self.movie136.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie136.nextFrameDelay())
            frame_n = str(self.movie136.currentFrameNumber())
            self.statusbar.showMessage('136px: Jumped to frame #' + frame_n + fps + delay)

        @self.slider_speed136.valueChanged.connect
        def speed136_slider_changed(value):
            self.statusbar.showMessage('Speed of 136px changed to {}x'.format(value/100))
            self.spin_speed136.blockSignals(True)
            self.spin_speed136.setValue(value * 0.01)
            self.spin_speed136.blockSignals(False)
            self.movie136.setSpeed(value)

        @self.spin_speed136.valueChanged.connect
        def speed136_spinner_changed(value):
            value = round(value, 2)
            self.statusbar.showMessage('Speed of 136px changed to {}x'.format(value))
            value *= 100
            self.slider_speed136.setValue(value)
            self.movie136.setSpeed(value)

        self.previous_scale136 = self.spin_scale136.value()
        @self.spin_scale136.valueChanged.connect
        def spin_scale136_value_changed(value):
            self.statusbar.showMessage('Zoom of 136px changed to {}x'.format(value))
            self.graphicsView_136.scale(1/self.previous_scale136, 1/self.previous_scale136)
            self.graphicsView_136.scale(value, value)
            self.slider_scale136.setValue(value)
            self.previous_scale136 = self.spin_scale136.value()
        self.spin_scale136.valueChanged.emit(self.spin_scale136.value())

        @self.spin_quality136.valueChanged.connect
        def spin_quality136_value_changed():
            if self.check_livepreview136.isChecked():
                btn_update136_clicked()

        def btn_update136_clicked():
            # working_file = self.movie136.fileName()
            working_file = self.loaded_136.gif_path
            output_file = path.splitext(working_file)[0] + '.tmp'
            self.movie136.stop()
            lossy_factor = self.spin_quality136.text()
            # Instead of generating a txt file for a colortable
            # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            self.color_table = path.join('.\\temp', 'current_act.txt')
            # We generate a colormap from the colormap viewer window
            with open(self.color_table, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self.color_table

            GifSicle(self.loaded_136, lossy_factor, color_table)
            self.load_gif(output_file)
            temp_file_size = path.getsize(output_file)/1024
            self.statusbar.showMessage('Resulting filesize is: {:.2f} Kb'.format(temp_file_size))
        self.btn_update136.clicked.connect(btn_update136_clicked)

        self.gifplayer136_widget = QtGui.QWidget()
        self.gifplayer136 = QtGui.QLabel(self.gifplayer136_widget)
        self.gifplayer136.setMinimumSize(QtCore.QSize(136, 136))

        self.graphics_scene_136 = QtGui.QGraphicsScene()
        self.graphicsView_136.setScene(self.graphics_scene_136)
        self.graphicsView_136.setInteractive(1)

        self.graphics_scene_136.addWidget(self.gifplayer136_widget)
        self.graphicsView_136.scale(2, 2)

        self.gifplayer280_widget = QtGui.QWidget()
        self.gifplayer280 = QtGui.QLabel(self.gifplayer280_widget)
        self.gifplayer280.setMinimumSize(QtCore.QSize(280, 280))

        self.graphics_scene_280 = QtGui.QGraphicsScene()
        self.graphicsView_280.setScene(self.graphics_scene_280)
        self.graphicsView_280.setInteractive(1)

        self.graphics_scene_280.addWidget(self.gifplayer280_widget)
        self.graphicsView_280.scale(2, 2)


    def make_video_list(self, folder=None, ext='avi'):
        # If no folder specified, update the current working directory
        if not folder:
            folder = self.working_directory
        if len(files_in_folder(folder, ext)) > 0:
            # Make a dictionary out of emojis, when emoji object is not none (has been successfully created)
            emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in files_in_folder(folder, ext) if Emoji(emoji)}
            # Make a model
            self.videolist_model = VideoListModel(emoji_dict)
            # Assign the model to the list view
            self.list_videoslist.setModel(self.videolist_model)
            # Enable the collect button
            self.btn_clean.setEnabled(True)

    # def update_video_list(self, folder=None, ext='avi'):
    #     # If no folder specified, update the current working directory
    #     if not folder:
    #         folder = self.working_directory
    #     if len(files_in_folder(folder, ext)) > 0:
    #         # Make a dictionary out of emojis, when emoji object is not none (has been successfully created)
    #         emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in files_in_folder(folder, ext) if Emoji(emoji)}
    #         # Make a model
    #         self.videolist_model = VideoListModel(emoji_dict)
    #         # Assign the model to the list view
    #         self.list_videoslist.setModel(self.videolist_model)
    #         # Enable the collect button
    #         self.btn_collect.setEnabled(True)

    # ################################# LOADERS ################################## #

    def load_act(self, act_file):
        self.plaintext_act_readout.setToolTip('{} is loaded.\n\n'
                                              'You can see and edit the color map here.\n'
                                              'Those changes appear on update and export.'.format(act_file))
        self.plaintext_act_readout.clear()
        act = act_reader.act_to_list(act_file)
        # self.graphics_scene.addText(''.join(act[0]))
        self.plaintext_act_readout.setPlainText(''.join(act[0]))
        self.statusbar.showMessage(act[1])
        return act

    def load_gif(self, gif_path: str) -> None:
        """
        This method chooses, and loads, in which viewport to load the gif, 280 or 136 one.

        :type gif_path: str
        :param gif_path: Full path to the gif, you want to load.
        """
        if '280' in gif_path:
            self.load280(gif_path)
        elif '136' in gif_path:
            self.load136(gif_path)
        else:
            logging.error('load_gif function encountered a weird gif_path: {}'.format(gif_path))

    def load280(self, file280):
        self.btn_playpause280.setChecked(False)  # Unpress the play-pause button
        self.btn_fb280.setEnabled(True)          # Enable back button
        self.btn_playpause280.setEnabled(True)   # Enable play-pause button
        self.btn_ff280.setEnabled(True)          # Enable forward button
        self.layout_gif280.setTitle(path.split(file280)[1])  # Set name of the gif as the title
        self.movie280.setFileName('')  # Free (close) the previous loaded image
        self.movie280 = QtGui.QMovie(file280)  # Create a QMovie instance
        self.gifplayer280.setMovie(self.movie280)  # And assign it to the player widget
        self.movie280.setSpeed(self.spin_speed280.value()*100)  # Automatically set speed using the speed spinner
        self.movie280.start()
        return self.movie280.isValid()

    def load136(self, file136):
        self.btn_playpause136.setChecked(False)  # Unpress the play-pause button
        self.btn_fb136.setEnabled(True)          # Enable back button
        self.btn_playpause136.setEnabled(True)   # Enable play-pause button
        self.btn_ff136.setEnabled(True)          # Enable forward button
        self.layout_gif136.setTitle(path.split(file136)[1])  # Set name of the gif as the title
        self.movie136.setFileName('')  # Free (close) the previous loaded image
        self.movie136 = QtGui.QMovie(file136)  # Create a QMovie instance
        self.gifplayer136.setMovie(self.movie136)  # And assign it to the player widget
        self.movie136.setSpeed(self.spin_speed136.value()*100)  # Automatically set speed using the speed spinner
        self.movie136.start()
        return self.movie136.isValid()


    def load_palette(self, palette: str) -> None:
        """
        This method chooses loads a palette image to 136 viewport.

        :type palette: str
        :param palette: Full path to the image, you want to load.
        """
        pixmap = QtGui.QPixmap(palette)
        pixmap = pixmap.scaled(136, 136, mode=QtCore.Qt.FastTransformation)
        self.gifplayer136.setPixmap(pixmap)
        # self.gifplayer136.scaled todo
        # self.gifplayer136.setScaledContents(True) todo

    def console_add(self, log_input):
        self.console.append(str(log_input))#.rstrip())

    def convert_mov_to_mp4(self):
        print(QtGui.QFileDialog())
        files, filtr = QtGui.QFileDialog.getOpenFileNames(self,
                                                          "Choose your files for conversion", '.',
                                                          "All Files (*.*);;MOV (*.mov)", "MOV (*.mov)")
        print(files, filtr)
        for input_file in files:
            Handbrake(input_file)


    def minimal_size(self):
        self.resize(0, 0)


if __name__ == '__main__':

    app = QtGui.QApplication([])
    MainWindowObj = QtMainWindow()
    MainWindowObj.show()

    app.exec_()
