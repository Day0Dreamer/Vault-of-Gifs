# encoding: utf-8
import os  # todo убрать этот импорт

from TasksPool import TasksPool
from gifsicle import GifSicle
from ffmpeg import FFmpeg
from emoji import Emoji
from export import Conversion
from config import Config

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from os import path, listdir, walk, remove, rmdir, makedirs
from shutil import copy2
from time import sleep
import logging
import winreg

import act_reader
from widgets import MainWindow_UI
from widgets import settings
from widgets import stylesheet




# ################################# CONFIG ################################### #
config = Config()
fps_delays = config()['fps_delays']
flag_show_message_bar_timer = config()['flag_show_message_bar_timer']
act_folder = config()['act_folder']
damaged_filesize = int(config()['damaged_filesize'])
warning_level = config()['warning_level']
console_flag = config()['console_enabled']
icons_folder_name = 'icons'

# ################################ LOGGING ################################### #
logging.basicConfig(format='%(levelname)s:%(message)s', level=warning_level)
# todo сделать так, чтобы логгер писал имя файла откуда лог

# ############################### END CONFIG ################################# #

# # ################################ CONSTANTS ################################# #
# ITEM_EMOJI_OBJECT =  0x100
# ITEM_NAME =          0x101
# ITEM_VERSION =       0x102
# ITEM_RESOLUTION =    0x103
# ITEM_FPS =           0x104
# ITEM_LOSSY =         0x105
# ITEM_DAMAGED =       0x105
# ITEM_FULL_PATH =     0x106
# # ############################### END CONSTANTS ############################## #


def files_in_folder(folder, ext):
    return [path.join(path.abspath(folder), file) for file in listdir(folder) if '.'+str(ext) == path.splitext(file)[1]]


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

    def update(self):
        pass


class ActListModel(QtCore.QAbstractListModel):

    def __init__(self, act_list):
        super(ActListModel, self).__init__()
        self.act_list = act_list

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

    def update(self):
        pass


def make_folder_structure():
    makedirs('temp', exist_ok=True)
    makedirs('bin', exist_ok=True)
    makedirs('input', exist_ok=True)
    makedirs('act', exist_ok=True)
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
    def __init__(self):
        super(QtMainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet.houdini)

        self.working_directory = 'input'  # todo Вынести это в конфиг
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
        self.tp = None
        # todo разобраться с self.launcher self.launcher = Launcher()
        # todo разобраться с self.main_task_pool self.main_task_pool = TasksPool()

        # ############################ MODIFY INTERFACE ############################## #
        # todo исправить размер интерфейса self.setGeometry(200, 200, 40, 40)

        # Max size of icons in video list
        self.list_videoslist.setIconSize(QtCore.QSize(32, 32))

        # Update the video list on initial program start
        self.update_video_list()

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
        self.layout3in1.addWidget(self.console)
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
                self.update_video_list()

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
            self.dial = settings.QtSettings() # Изменить
            self.dial.exec_()
        # todo доработать окно about

        # ############################### LEFT COLUMN ################################ #
        @self.btn_input_folder.clicked.connect
        def input_folder():
            # options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
            directory = QtGui.QFileDialog.getExistingDirectory(self)
            if directory:
                self.working_directory = directory
                self.update_video_list()

        @self.list_videoslist.activated.connect
        def avi_activated_decorated(video_list_item):
            self.working_emoji = video_list_item.data(32)
            # Calling FFmpeg if there is no gif created
            if not self.working_emoji.has_gif:
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
                self.load_gif(self.working_emoji.gif_path)
                self.update_video_list()
            else:
                self.load_gif(self.working_emoji.gif_path)

        # Add acts from folder to list widget
        self.actlist_model = ActListModel(files_in_folder(self.working_directory, 'act'))
        self.dropdown_colortable.setModel(self.actlist_model)

        @self.dropdown_colortable.currentIndexChanged.connect
        def dropdown_colortable_selected(index_of_selected_item):
            act_file_path = self.dropdown_colortable.itemData(index_of_selected_item, 32)
            self.load_act(act_file_path)

        @self.btn_import_act.clicked.connect
        def import_act_clicked():
            photoshop_paths = PsFolder().ps_paths
            print(photoshop_paths[0])
            if len(photoshop_paths) > 1:
                logging.warning('Multiple Photoshop paths found, using {}'.format(photoshop_paths[0]))
            files, filtr = QtGui.QFileDialog.getOpenFileNames(self,
                                                              "Choose your color table",
                                                              '{}'.format(photoshop_paths[0]),
                                                              "All Files (*.*);;A color table (*.act)",
                                                              "A color table (*.act)"
                                                              )
            print(files, filtr)
            for file in files:
                if path.exists(path.join(self.working_directory, file)):
                    raise ZeroDivisionError
                copy2(file, self.working_directory)

        @self.btn_export.clicked.connect
        def btn_export_clicked():
            # Dictionary two lossy values from their interface spinners
            lossy_dict = {'136': self.spin_quality136.text(), '280': self.spin_quality280.text()}
            # Start export conversion using dir user selected and lossy dict
            self.conversion = Conversion(self.working_directory, lossy_dict)
            # todo сделать обработку экспорта пустой папки

        @self.btn_collect.clicked.connect
        def collect():
            self.console_add('Collecting process has started')
            self.statusbar.showMessage('Collecting process has started')
            # todo сделать коллект проекта с загрузкой

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

        @self.spin_scale280.valueChanged.connect
        def spin_scale280_value_changed(value):
            self.statusbar.showMessage('Zoom of 280px changed to {}x'.format(value))
            self.gifplayer280.setScaledContents(True)
            self.gifplayer280.setFixedHeight(280 * value)
            self.gifplayer280.setFixedWidth(280 * value)
            self.slider_scale280.setValue(value)
            self.minimal_size()

        @self.spin_quality280.valueChanged.connect
        def spin_quality280_value_changed():
            if self.check_livepreview280.isChecked():
                btn_update280_clicked()

        def btn_update280_clicked():
            working_file = self.movie280.fileName()
            output_file = path.splitext(working_file)[0] + '.tmp'
            self.movie280.stop()
            lossy_factor = self.spin_quality280.text()
            # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            self_act_as_txt = path.join('.\\temp',
                                        path.splitext(
                                            path.split(
                                                self.dropdown_colortable.currentText())[1])[0]+'.txt')
            with open(self_act_as_txt, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self_act_as_txt

            # self.btn_update280.setEnabled(False)
            self.gc = GifSicle(self.working_emoji, lossy_factor, color_table)
            # self.gc = GifSicle() todo разобраться что происходит тут
            # self.gc.return_signal.connect(lambda x: print(x))
            # self.gc.add(self.working_emoji, lossy_factor, color_table)
            # self.gc.run()
            # .return_signal.connect(self.console_add)

            self.load_gif(output_file)
            # self.btn_update280.setEnabled(True)
        self.btn_update280.clicked.connect(btn_update280_clicked)

        # ############################### RIGHT COLUMN ############################### #

        # Load the color table viewer
        self.load_act(files_in_folder(self.working_directory, 'act')[self.dropdown_colortable.currentIndex()])


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

        @self.spin_scale136.valueChanged.connect
        def spin_scale136_value_changed(value):
            self.statusbar.showMessage('Zoom of 136px changed to {}x'.format(value))
            self.gifplayer136.setScaledContents(True)
            self.gifplayer136.setFixedHeight(136 * value)
            self.gifplayer136.setFixedWidth(136 * value)
            self.slider_scale136.setValue(value)
            self.minimal_size()

        @self.spin_quality136.valueChanged.connect
        def spin_quality136_value_changed():
            if self.check_livepreview136.isChecked():
                btn_update136_clicked()

        def btn_update136_clicked():
            working_file = self.movie136.fileName()
            output_file = path.splitext(working_file)[0] + '.tmp'
            self.movie136.stop()
            lossy_factor = self.spin_quality136.text()
            # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            self_act_as_txt = path.join('.\\temp',
                                        path.splitext(
                                            path.split(
                                                self.dropdown_colortable.currentText())[1])[0]+'.txt')
            with open(self_act_as_txt, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self_act_as_txt

            GifSicle(self.working_emoji, lossy_factor, color_table)
            self.load_gif(output_file)
        self.btn_update136.clicked.connect(btn_update136_clicked)

    def update_video_list(self, folder=None, ext='avi'):
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
            self.btn_collect.setEnabled(True)

    # ################################# LOADERS ################################## #

    def load_act(self, act_file):
        # print(act_file)
        self.plaintext_act_readout.clear()
        act = act_reader.act_to_list(act_file)
        # self.graphics_scene.addText(''.join(act[0]))
        self.plaintext_act_readout.setPlainText(''.join(act[0]))
        self.statusbar.showMessage(act[1])

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
            self.tp = TasksPool()
            self.tp.return_signal.connect(self.console_add)
            self.tp.add_task('bin\\ffmpeg.exe -i "{}" -c:a copy -c:v libx264 -profile:v high '
                             '-crf 21 -preset fast "{}.mp4"'.format(input_file, input_file))
            self.tp.launch_list()

    def minimal_size(self):
        self.resize(0, 0)


if __name__ == '__main__':

    app = QtGui.QApplication([])
    MainWindowObj = QtMainWindow()
    MainWindowObj.show()

    app.exec_()

# Замечания по автоматизации:
# 2.
# a. При выборе папки во вьюверы должны автоматически конвевртироваться из avi и загружаться версии с максимальным FPS
    # (это не обязательно 30FPS) готовые для кручения Lossy.
# б. При выборе видео/гиф с другим фпс он должна загружаться в соответсвующий вьювер.
# в. При нажатии кнопки экспорт должна производится конвертация ВСЕХ avi в выбранной папке (с соответсвующими
    # настройками Lossy для 136x136 и 280x280), далее конвертация DAMAGED-версий, затем конвертация файла с именем
    # [NameofComposition[Version]].mov в h264 с настройками кодека на 100%.
# г.При повторном выборе папки, с уже произведённым экспортом повевдение программы меняться не должно - при любом
    # совпадении по именам - овверайдить без диалоговых окон.
# Сборка проекта:
# 3. При нажатии на кнопку "Collect and Send Project Files" долже запускаться отдельный скрипт.
# Кнопка должна быть активна только при выбранной папке.
#
# Примерный функционал БУДЕТ выглядеть так
# а. Найти месторасположение выбранной папки.
# б. Удалить в выбранной папке все avi файлы, др. файлы не
# б. Перейти на уровень выше и загрузить выбранную папку с именем [NameofComposition[Version]] и папку с именем [NameofComposition[Version]]_sources на сервер.