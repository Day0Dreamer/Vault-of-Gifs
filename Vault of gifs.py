# encoding: utf-8
import os
from gifsicle import GifSicle
from ffmpeg import FFmpeg
from emoji import Emoji
from export import Conversion
from shutil import copy2

import sys

from config import Config
import time
# from threads import Launcher

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from os import path

import act_reader
from widgets import MainWindow_UI
from widgets import settings
from widgets import stylesheet

from Tasks_pool3 import TasksPool


# ################################# CONFIG ################################### #
config = Config()
fps_delays = config()['fps_delays']
flag_show_message_bar_timer = config()['flag_show_message_bar_timer']
act_folder = config()['act_folder']
damaged_filesize = int(config()['damaged_filesize'])
icons_folder_name = 'icons'
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

def gifs_in_folder(folder='input'):
    return [os.path.join(os.path.abspath(folder), gif) for gif in os.listdir(folder) if '.gif' in gif]


def acts_in_folder():
    return [os.path.join(os.path.abspath(act_folder), act) for act in os.listdir('act') if '.act' in act]


def avis_in_folder(folder):
    return [os.path.join(os.path.abspath(folder), avi) for avi in os.listdir(folder) if '.avi' in avi]


def files_in_folder(folder, ext):
    return [os.path.join(os.path.abspath(folder), file) for file in os.listdir(folder) if '.'+str(ext) in file]


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
            return str(emoji)
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

class QtMainWindow(QtGui.QMainWindow, MainWindow_UI.Ui_MainWindow):

    def __init__(self):
        super(QtMainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet.houdini)

        os.makedirs('temp', exist_ok=True)
        os.makedirs('bin', exist_ok=True)
        os.makedirs('input', exist_ok=True)
        os.makedirs('act', exist_ok=True)
        self.working_directory = 'input'

        self.videolist_model = None
        self.ffmpeg = None
        self.gifsicle = None
        self.launcher = Launcher()
        self.main_task_pool = TasksPool()

        # ############################ MODIFY INTERFACE ############################## #
        # self.setGeometry(200, 200, 40, 40)

        self.list_videoslist.setIconSize(QtCore.QSize(32, 32))

        self.movie136 = QtGui.QMovie()
        self.movie280 = QtGui.QMovie()

        # Add acts from folder to list widget
        self.dropdown_colortable.addItems(acts_in_folder())

        self.source = None
        self.working_emoji = None
        self.lossy_file_size = None
        self.lossy_factor = None
        self.output_file = None
        self.file_watch = QtCore.QFileSystemWatcher()

        # Update the video list on initial program start
        self.update_video_list(self.working_directory)
        self.update_gifs_list(self.working_directory)

        ################################### ??? ###################################### #

        # self.main_task_pool.allTasksCompleteSignal.connect(self.selector)

        # ################################# TOP BAR ################################## #
        @self.actionExit.triggered.connect
        def exit_ui():
            exit(0)

        @self.actionConfig.triggered.connect
        def call_settings():
            self.dial = settings.QtSettings()
            self.dial.exec_()

        @self.actionDelete_temp_files.triggered.connect
        def clear_temp_folder():
            for file in os.listdir('temp'):
                os.remove(os.path.join('temp', file))

        # ################################# TOP ROW ################################## #
        @self.btn_top1.clicked.connect
        def convert_mov_to_mp4():
            print(QtGui.QFileDialog())
            files, filtr = QtGui.QFileDialog.getOpenFileNames(self,
                                                              "QFileDialog.getOpenFileNames()", '.',
                                                              "All Files (*);;MOV (*.mov)", "MOV (*.mov)")
            print(files, filtr)
            for input_file in files:
                self.launch_process('bin\\ffmpeg.exe -i "{}" -c:a copy -c:v libx264 -profile:v high '
                                    '-crf 21 -preset fast "{}.mp4"'.format(input_file, input_file))

        @self.btn_top2.clicked.connect
        def wip2():
            minimal_window_size()

        self.btn_top3.setEnabled(True)
        # self.btn_top3.hide()
        @self.btn_top3.clicked.connect
        def btn3():
            # self.load_palette('SteffonDiggsEmoji-02-280x280-15FPS.avi_palette.png')
            # main_task_pool.add_task('bin/fake_renderer.exe')
            # self.signal_update280.emit()
            pass

        self.console = QtGui.QTextBrowser(self)
        self.console.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.layout3in1.addWidget(self.console)
        self.console.setMinimumWidth(500)
        self.console.setVisible(False)
        self.btn_top4.setText('Toggle console')
        self.btn_top4.setCheckable(True)
        self.btn_top4.setEnabled(True)
        @self.btn_top4.clicked.connect
        def toggle_console():
            self.console.setVisible(self.btn_top4.isChecked())
            self.resize(0,0)


        # ############################### LEFT COLUMN ################################ #
        @self.btn_input_folder.clicked.connect
        def input_folder():
            # self.list_videoslist.clear()
            # self.list_videoslist.addItems(avis_in_folder())

            # Add gifs from folder to list widget
            # for i in emoji_list():
            #     print(i)
            #     self.list_gifslist.addItem(i.filename)

            # options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
            directory = QtGui.QFileDialog.getExistingDirectory()
            if directory:
                self.working_directory = directory
                self.update_video_list(self.working_directory)
                self.update_gifs_list(self.working_directory)

        # self.list_videoslist.activated.connect(lambda x: self.load280(x.data(32).gif_path))
        @self.list_videoslist.activated.connect
        def avi_activated_decorated(video_list_item):
            avi_activated(video_list_item)

        def avi_activated(video_list_item):
            self.working_emoji = video_list_item.data(32)
            if not self.working_emoji.has_gif:
                self.statusbar.showMessage('Generating the gif')
                self.ffmpeg = FFmpeg()
                self.ffmpeg.add(self.working_emoji.full_path, self.working_emoji.fps)
                self.ffmpeg.run()
                self.working_file = self.working_emoji.full_path
                self.load_gif(self.working_emoji.gif_path)
                self.update_video_list(self.working_directory)
            else:
                self.load_gif(self.working_emoji.gif_path)



        # @self.list_gifslist.itemActivated.connect
        # def gif_double_clicked_decorated():
        #     gif_double_clicked('gif')

        self.original_280_gif = None
        self.original_136_gif = None

        def gif_double_clicked(avi_or_gif):
            """Takes an item of videos list, reads ITEM_FULL_PATH,
            replaces extension with .gif and loads it to viewport"""

            if avi_or_gif == 'avi':
                if len(self.list_videoslist.selectedItems()) > 2:
                    selected_items = [self.list_videoslist.selectedItems()[0], self.list_videoslist.selectedItems()[-1]]
                else:
                    selected_items = self.list_videoslist.selectedItems()
            if avi_or_gif == 'gif':
                if len(self.list_gifslist.selectedItems()) > 2:
                    selected_items = [self.list_gifslist.selectedItems()[0], self.list_gifslist.selectedItems()[-1]]
                else:
                    selected_items = self.list_gifslist.selectedItems()

            for item in selected_items:
                video_file_path = item.data(ITEM_FULL_PATH)
                # Launch avi's gif counterparts
                if os.path.splitext(video_file_path)[1] != 'gif':
                    video_file_path = os.path.splitext(video_file_path)[0] + '.gif'

                # If it is 136 file > load it to 136 viewport
                if '136' in video_file_path:
                    self.load136(video_file_path)
                    self.original_136_gif = video_file_path
                # If it is 280 file > load it to 280 viewport
                elif '280' in video_file_path:
                    vid280 = self.load280(video_file_path)
                    self.original_280_gif = video_file_path
                    if vid280:
                        self.statusbar.showMessage('280px: Gif is loaded' + video_file_path)
            # video_file_path = video_list_item.data(ITEM_FULL_PATH)
            # # Launch avi's gif counterparts
            # if os.path.splitext(video_file_path)[1] != 'gif':
            #     video_file_path = os.path.splitext(video_file_path)[0] + '.gif'
            # # If it is 136 file > load it to 136 viewport
            # if '136' in video_file_path:
            #     load136(video_file_path)
            #     self.original_136_gif = video_file_path
            # # If it is 280 file > load it to 280 viewport
            # elif '280' in video_file_path:
            #     vid280 = self.load280(video_file_path)
            #     self.original_280_gif = video_file_path
            #     if vid280:
            #         self.statusbar.showMessage('280px: Gif is loaded')

        @self.dropdown_colortable.currentIndexChanged.connect
        def dropdown_colortable_selected(index_of_selected_item):
            self.load_act(acts_in_folder()[index_of_selected_item])

        @self.btn_export.clicked.connect
        def btn_export_clicked():
            # print(self.working_directory, self.spin_quality280.text())
            self.conversion = Conversion(self.working_directory, self.spin_quality280.text())

        #     if self.list_videoslist.selectedItems():
        #         list_duplicate = [i.data(ITEM_EMOJI_OBJECT) for i in self.list_videoslist.selectedItems()]
        #         for i in list_duplicate:
        #         # for i in self.list_videoslist.selectedItems():
        #         #     self.export(i.data(ITEM_EMOJI_OBJECT))
        #             self.working_emoji = i
        #             self.export(self.working_emoji)
        #     else:
        #         self.statusbar.showMessage('Nothing selected for export')
        #
        # self.groupb_preset.hide()

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
            self.statusbar.showMessage('Speed of 280px changed to ' + str(value / 100) + 'x')
            self.spin_speed280.blockSignals(True)
            self.spin_speed280.setValue(value * 0.01)
            self.spin_speed280.blockSignals(False)
            self.movie280.setSpeed(value)

        @self.spin_speed280.valueChanged.connect
        def speed280_spinner_changed(value):
            # value = round(value, 2)
            self.statusbar.showMessage('Speed of 280px changed to ' + str(value) + 'x')
            value *= 100
            self.slider_speed280.setValue(value)
            self.movie280.setSpeed(value)

        @self.spin_scale280.valueChanged.connect
        def spin_scale280_value_changed(value):
            self.statusbar.showMessage('Zoom of 280px changed to ' + str(value) + 'x')
            self.gifplayer280.setScaledContents(True)
            self.gifplayer280.setFixedHeight(280 * value)
            self.gifplayer280.setFixedWidth(280 * value)
            self.slider_scale280.setValue(value)
            minimal_window_size()

        # @self.slider_quality280.sliderReleased.connect
        # def slider_quality280_slider_released():
        #     # self.spin_quality280.blockSignals(True)
        #     self.spin_quality280.setValue(self.slider_quality280.value())
        #     # self.spin_quality280.blockSignals(False)
        #
        # @self.slider_quality280.valueChanged.connect
        # def slider_quality280_value_changed():
        #     if self.check_livepreview280.isChecked():
        #         pass
        #     else:
        #         self.spin_quality280.setValue(self.slider_quality280.value())
        #         # self.spin_quality280.blockSignals(True)
        #         # self.spin_quality280.blockSignals(False)

        @self.spin_quality280.valueChanged.connect
        def spin_quality280_value_changed():
            if self.check_livepreview280.isChecked():
                btn_update280_clicked()

        @self.btn_update280.clicked.connect
        def btn_update280_clicked_decorated():
            btn_update280_clicked()

        def btn_update280_clicked():
            self.source = 'btn_update280'
            # selected_file = self.list_videoslist.selectedItems()[0].text().replace('avi', 'gif')
            # selected_file = path.splitext(self.original_280_gif)[0] + '.gif'
            selected_file = path.splitext(self.movie280.fileName())[0] + '.gif'
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
            # self.gifsicle = GifSicle()
            # if self.check_endless_lossy280.isChecked():
            #     self.gifsicle(
            #         input_file=working_file,
            #         lossy_factor=lossy_factor,
            #         color_map=color_table,
            #         output_file=output_file,
            #         delay=3)
            # else:
                # self.gifsicle(
                #     input_file=selected_file,
                #     lossy_factor=lossy_factor,
                #     color_map=color_table,
                #     output_file=output_file,
                #     delay=3)
            GifSicle(self.working_emoji, lossy_factor, color_table)
            self.load_gif(output_file)
            # COMMENTED AS OF GIFSICLE METHOD
            # self.proc.waitForFinished()

                # @self.worker.finish_signal.connect
                # def load280_decorated():
                #     print('Finish signal received:', time.time())
                # load280(os.path.splitext(working_file)[0] + '.tmp')


                # self.gifsicle(
                #     input_file=selected_file,
                #     lossy_factor=lossy_factor,
                #     color_map=color_table,
                #     output_file=output_file,
                #     delay=3)
                # size = str(round(os.path.getsize(output_file) / 1024, 2))
                # self.statusbar.showMessage('280px: Lossy factor of {} results in {}Kb of size'.format(lossy_factor, size))

                # load280(os.path.splitext(working_file)[0] + '.tmp')
                # self.btn_update280.setEnabled(True)

        # ############################### RIGHT COLUMN ############################### #

        self.load_act(acts_in_folder()[0])

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
            self.statusbar.showMessage('Speed of 136px changed to ' + str(value / 100) + 'x')
            self.spin_speed136.blockSignals(True)
            self.spin_speed136.setValue(value * 0.01)
            self.spin_speed136.blockSignals(False)
            self.movie136.setSpeed(value)

        @self.spin_speed136.valueChanged.connect
        def speed136_spinner_changed(value):
            # value = round(value, 2)
            self.statusbar.showMessage('Speed of 136px changed to ' + str(value) + 'x')
            value *= 100
            self.slider_speed136.setValue(value)
            self.movie136.setSpeed(value)

        @self.spin_scale136.valueChanged.connect
        def spin_scale136_value_changed(value):
            self.statusbar.showMessage('Zoom of 136px changed to ' + str(value) + 'x')
            self.gifplayer136.setScaledContents(True)
            self.gifplayer136.setFixedHeight(136 * value)
            self.gifplayer136.setFixedWidth(136 * value)
            self.slider_scale136.setValue(value)
            minimal_window_size()

        # @self.slider_quality136.sliderReleased.connect
        # def slider_quality136_slider_released():
        #     # self.spin_quality136.blockSignals(True)
        #     self.spin_quality136.setValue(self.slider_quality136.value())
        #     # self.spin_quality136.blockSignals(False)

        # @self.slider_quality136.valueChanged.connect
        # def slider_quality136_value_changed():
        #     if self.check_livepreview136.isChecked():
        #         pass
        #     else:
        #         self.spin_quality136.setValue(self.slider_quality136.value())
        #         # self.spin_quality136.blockSignals(True)
        #         # self.spin_quality136.blockSignals(False)

        @self.spin_quality136.valueChanged.connect
        def spin_quality136_value_changed():
            if self.check_livepreview136.isChecked():
                btn_update136_clicked()

        @self.btn_update136.clicked.connect
        def btn_update136_clicked_decorated():
            btn_update136_clicked()

        def btn_update136_clicked():
            self.source = 'btn_update136'
            # selected_file = self.list_videoslist.selectedItems()[0].text().replace('avi', 'gif')
            # selected_file = os.path.splitext(self.original_136_gif)[0] + '.gif'
            selected_file = path.splitext(self.movie136.fileName())[0] + '.gif'
            working_file = self.movie136.fileName()
            output_file = os.path.splitext(working_file)[0] + '.tmp'
            self.movie136.stop()
            lossy_factor = self.spin_quality136.text()
            color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            # print(color_table)
            # self.btn_update136.setEnabled(False)
            # if self.check_endless_lossy136.isChecked():
            #     self.gifsicle(
            #         input_file=working_file,
            #         lossy_factor=lossy_factor,
            #         color_map=color_table,
            #         output_file=output_file,
            #         delay=3)
            # else:
            #     self.gifsicle(
            #         input_file=selected_file,
            #         lossy_factor=lossy_factor,
            #         color_map=color_table,
            #         output_file=output_file,
            #         delay=3)
            GifSicle(self.working_emoji, lossy_factor, color_table)
            self.load_gif(output_file)

        def minimal_window_size():
            self.resize(1, 1)

    def update_video_list(self, folder='input', ext='avi'):
        emoji_dict = {Emoji(emoji).filename: Emoji(emoji) for emoji in files_in_folder(folder, ext)}

        self.videolist_model = VideoListModel(emoji_dict)
        self.list_videoslist.setModel(self.videolist_model)

        # self.list_videoslist.clear()
        # # Add objects pre-created list items to the list
        # for i in files_in_folder(folder, ext):
        #     emoji_object = Emoji(i)
        #     # Get the video-list item out of the Emoji object
        #     item = emoji_object.video_list_item
        #     # Check if avi has gif counterpart
        #     gif_full_path = os.path.splitext(item.data(ITEM_FULL_PATH))[0]+'.gif'
        #     if os.path.exists(gif_full_path):
        #         item.setBackground(QtGui.QColor(0, 255, 0, 32))
        #         emoji_object.has_raw_gif = True
        #     else:
        #         item.setBackground(QtGui.QColor(255, 255, 255, 255))
        #         emoji_object.has_raw_gif = False
        #     self.list_videoslist.addItem(item)

    def update_gifs_list(self, folder='input', ext='gif'):
        pass
        # self.list_gifslist.clear()
        # # Add objects pre-created list items to the list
        # for i in files_in_folder(folder, ext):
        #     emoji_object = Emoji(i)
        #     # Get the video-list item out of the Emoji object
        #     item = emoji_object.video_list_item
        #     # Check if avi has gif counterpart
        #     gif_full_path = os.path.splitext(item.data(ITEM_FULL_PATH))[0]+'.gif'
        #     if os.path.exists(gif_full_path):
        #         item.setBackground(QtGui.QColor(0, 255, 0, 32))
        #         emoji_object.has_raw_gif = True
        #     else:
        #         item.setBackground(QtGui.QColor(255, 255, 255, 255))
        #         emoji_object.has_raw_gif = False
        #     self.list_gifslist.addItem(item)

    # ################################# LOADERS ################################## #

    def load_act(self, act_file):
        # print(act_file)
        self.plaintext_act_readout.clear()
        act = act_reader.act_to_list(act_file)
        # self.graphics_scene.addText(''.join(act[0]))
        self.plaintext_act_readout.setPlainText(''.join(act[0]))
        self.statusbar.showMessage(act[1])

    def load_gif(self, gif_path):
        if '280' in gif_path:
            self.load280(gif_path)
        elif '136' in gif_path:
            self.load136(gif_path)
        else:
            print('load_gif function encountered a weird gif_path')

    def load280(self, file280):
        self.btn_playpause280.setChecked(False)
        self.btn_fb280.setEnabled(True)
        self.btn_playpause280.setEnabled(True)
        self.btn_ff280.setEnabled(True)
        self.layout_gif280.setTitle(os.path.split(file280)[1])
        self.movie280 = QtGui.QMovie(file280)
        self.gifplayer280.setMovie(self.movie280)
        self.movie280.setSpeed(self.spin_speed280.value()*100)
        self.movie280.start()
        return self.movie280.isValid()

    def load136(self, file136):
        self.btn_playpause136.setChecked(False)
        self.btn_fb136.setEnabled(True)
        self.btn_playpause136.setEnabled(True)
        self.btn_ff136.setEnabled(True)
        print(file136)
        self.layout_gif136.setTitle(os.path.split(file136)[1])
        self.movie136 = QtGui.QMovie(file136)
        self.gifplayer136.setMovie(self.movie136)
        self.movie136.setSpeed(self.spin_speed136.value()*100)
        self.movie136.start()
        return self.movie136.isValid()

    def load_palette(self, palette):
        pixmap = QtGui.QPixmap(palette)
        pixmap = pixmap.scaled(136,136,mode=QtCore.Qt.FastTransformation)
        self.gifplayer136.setPixmap(pixmap)
        # self.gifplayer136.scaled
        # self.gifplayer136.setScaledContents(True)

    def console_add(self, log_input):
        self.console.append(str(log_input).rstrip())

    # def launch_process(self, command, source=None, working_file=''):
    #     self.console_add('='*50+'\n' + 'Launched ' + command)
    #     # print('Launched', command)
    #     self.slider_quality136.setEnabled(False)
    #     self.slider_quality280.setEnabled(False)
    #     self.spin_quality136.setEnabled(False)
    #     self.spin_quality280.setEnabled(False)
    #     self.btn_update136.setEnabled(False)
    #     self.btn_update280.setEnabled(False)
    #     self.proc = QtCore.QProcess()
    #     self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
    #     # self.proc.waitForFinished()
    #
    #     @self.proc.finished.connect
    #     def finished():
    #         self.slider_quality136.setEnabled(True)
    #         self.slider_quality280.setEnabled(True)
    #         self.spin_quality136.setEnabled(True)
    #         self.spin_quality280.setEnabled(True)
    #         self.btn_update136.setEnabled(True)
    #         self.btn_update280.setEnabled(True)
    #         recognize_source()
    #         time2 = time.time()
    #         timer = 'Last subroutine took {} msec'.format(str(round(((time2-time1)*1000), 2)))
    #         self.console_add(timer)
    #         if flag_show_message_bar_timer:
    #             self.statusbar.showMessage(timer)
    #         self.console_add('Finished ' + command + '\n'+'='*50)
    #         # print('Finished ' + command)
    #
    #     @self.proc.readyRead.connect
    #     def read_out():
    #         out = self.proc.readAll()
    #         self.console.append(str(out))
    #         print('|', str(out), sep='', end='')
    #
    #     def recognize_source():
    #         print(source)
    #         if source == 'btn_update280':
    #             self.load280(os.path.splitext(self.movie280.fileName())[0] + '.tmp')
    #             size = str(round(os.path.getsize(self.movie280.fileName()) / 1024, 2))
    #             message = '280px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality280.text(), size)
    #             self.statusbar.showMessage(message)
    #             self.console_add(message)
    #         if source == 'btn_update136':
    #             self.load136(os.path.splitext(self.movie136.fileName())[0] + '.tmp')
    #             size = str(round(os.path.getsize(self.movie136.fileName()) / 1024, 2))
    #             message = '136px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality136.text(), size)
    #             self.statusbar.showMessage(message)
    #             self.console_add(message)
    #         if source == 'ffmpeg280':
    #             self.load280(os.path.splitext(working_file)[0] + '.gif')
    #             self.original_280_gif = os.path.splitext(working_file)[0] + '.gif'
    #             self.update_video_list(self.working_directory)
    #         if source == 'ffmpeg136':
    #             self.load136(os.path.splitext(working_file)[0] + '.gif')
    #             self.original_136_gif = os.path.splitext(working_file)[0] + '.gif'
    #             self.update_video_list(self.working_directory)
    #
    #     time1 = time.time()
    #     self.proc.start(command)
    #     # self.proc.startDetached(command)
    #     # self.proc.start('ffmpeg.exe')
    #     # self.proc.start('gifsicle.exe --help')
    #     # self.proc.start('ping.exe')
    #     # self.proc.waitForFinished()
    #
    # def selector(self):
    #     print('Selector has been called')
    #     if self.source == 'btn_update280':
    #         self.load280(os.path.splitext(self.movie280.fileName())[0] + '.tmp')
    #         size = str(round(os.path.getsize(self.movie280.fileName()) / 1024, 2))
    #         message = '280px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality280.text(), size)
    #         self.statusbar.showMessage(message)
    #         self.console_add(message)
    #     elif self.source == 'btn_update136':
    #         self.load136(os.path.splitext(self.movie136.fileName())[0] + '.tmp')
    #         size = str(round(os.path.getsize(self.movie136.fileName()) / 1024, 2))
    #         message = '136px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality136.text(), size)
    #         self.statusbar.showMessage(message)
    #         self.console_add(message)
    #     elif self.source == 'ffmpeg280':
    #         if self.isVisible():
    #             self.load280(os.path.splitext(self.working_file)[0] + '.gif')
    #             self.original_280_gif = os.path.splitext(self.working_file)[0] + '.gif'
    #             self.update_video_list(self.working_directory)
    #     elif self.source == 'ffmpeg136':
    #         if self.isVisible():
    #             self.load136(os.path.splitext(self.working_file)[0] + '.gif')
    #             self.original_136_gif = os.path.splitext(self.working_file)[0] + '.gif'
    #             self.update_video_list(self.working_directory)
    #     elif self.source == 'export_stage1':
    #         if os.path.exists(self.output_file):
    #             self.console_add(self.output_file + ' exists')
    #         else:
    #             self.console_add(self.output_file + ' doesnt exist')
    #
    #         # Uncompressed gif to damaged gif
    #         # if emoji.resolution == '280x280':
    #         try:
    #             self.lossy_file_size = os.path.getsize(self.output_file)
    #         except FileNotFoundError:
    #             self.lossy_file_size = True
    #         # Get the size of the lossy (not damaged) file
    #         # If lossy is over 500kb start export stage 2
    #         while self.lossy_file_size > 500*1024:
    #             try:
    #                 self.lossy_file_size = os.path.getsize(self.output_file)
    #             except FileNotFoundError:
    #                 self.lossy_file_size = True
    #             self.export_stage2_signal.emit()
    #     elif self.source == 'export_stage2':
    #         print('export_stage2_end_signal_received')
    #
    #
    #     self.source = None
    #
    # def gifsicle_old(self, delay, lossy_factor, color_map, input_file, source=None, output_file=None):
    #     """Converts string a gif to a lossy gif
    #     input_file is a full path
    #     Returns output_file, which by default is equal to input_file"""
    #     if output_file is None:
    #         output_file = input_file
    #     cmd = 'bin\\gifsicle.exe -O3 --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}' \
    #         .format(lossy_factor, color_map, input_file, output_file)
    #     self.launch_process(cmd, source)
    #     return output_file
    #
    # def gifsicle(self, fps, lossy_factor, color_map, input_file, output_file=None):
    #     if output_file is None:
    #         output_file = input_file
    #
    #     delay = fps_delays[''.join((digit for digit in fps if digit.isdigit()))]
    #     cmd = r'bin\gifsicle.exe -O3 --no-comments --no-names --no-extensions -d{} --lossy={} ' \
    #           '--use-colormap "{}" {} -o {}'.format(delay, lossy_factor, color_map, input_file, output_file)
    #     self.main_task_pool.add_task(cmd)
    #
    #     return output_file
    #
    # def ffmpeg_old(self, input_file, fps=30):
    #     """Converts any video file to a gif
    #     input_file is a full path
    #     Returns input_file with .gif extension"""
    #     # if flag_convert_30_to_29dot97 and fps == 30:
    #     #     fps = 29.97
    #     cmd = 'bin\\video2gif.bat {} -y -f {}'.format(input_file, fps)
    #     if '280' in input_file:
    #         self.source = 'ffmpeg280'
    #     elif '136' in input_file:
    #         self.source = 'ffmpeg136'
    #     self.main_task_pool.add_task(cmd)
    #
    #     return os.path.splitext(input_file)[0] + '.gif'
    #
    # def export_folder(self, folder='input', ext='avi', lossy280=200, lossy136=200, color_map=r"C:\Python\Vault_Of_Gifs\act\perc.act"):
    #     emojis = []
    #     for i in files_in_folder(folder, ext):
    #         emoji_object = Emoji(i)
    #         emojis.append(emoji_object)
    #
    #     # Generate missing gifs
    #     for emoji_object in emojis:
    #         # Check if avi has gif counterpart
    #         gif_full_path = os.path.splitext(emoji_object.full_path)[0]+'.gif'
    #         # Make a gif if none exists
    #         if not os.path.exists(gif_full_path):
    #             self.ffmpeg(emoji_object.full_path)
    #
    #     # Save lossy factor from input to object's variable
    #     self.lossy_factor280 = lossy280
    #     self.lossy_factor136 = lossy136
    #     # If colormap is act, then convert it to txt
    #     if color_map[-3:] == 'act':
    #         color_map = act_reader.create_gifsicle_colormap(color_map)
    #     # Generate lossy versions
    #     for emoji in emojis:
    #         raw_gif = os.path.splitext(emoji.full_path)[0]+'.gif'
    #         output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy.gif'
    #                                    .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
    #         if '280' in emoji.resolution:
    #             self.lossy_factor = self.lossy_factor280
    #         elif '136' in emoji.resolution:
    #             self.lossy_factor = self.lossy_factor136
    #         self.gifsicle(fps=emoji.fps,
    #                       lossy_factor=self.lossy_factor,
    #                       color_map=color_map,
    #                       input_file=raw_gif,
    #                       output_file=output_file)
    #
    #     # Generate damaged versions
    #     for emoji in emojis:
    #         raw_gif = os.path.splitext(emoji.full_path)[0]+'-lossy.gif'
    #         output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy-damaged.gif'
    #                                    .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
    #         # If lossy gif is over 500Kb then:
    #         while not os.path.exists(raw_gif):
    #             time.sleep(.5)
    #         size = path.getsize(raw_gif)
    #
    #         if size > damaged_filesize*1024:
    #             print('lossy file is over {}kb'.format(damaged_filesize))
    #             copy2(raw_gif, output_file)
    #             # Add current file to the file watcher
    #             self.file_watch.addPath(output_file)
    #             def damaged_is_changed(output_file):
    #                 actual_damaged_filesize = path.getsize(output_file)
    #                 if actual_damaged_filesize/1024 > damaged_filesize:
    #                     size_difference = actual_damaged_filesize/1024-damaged_filesize
    #                     print(size_difference)
    #                     if size_difference > 50:
    #                         self.lossy_factor += 50
    #                     elif size_difference > 25:
    #                         self.lossy_factor += 10
    #                     elif size_difference > 10:
    #                         self.lossy_factor += 5
    #                     elif size_difference <= 10:
    #                         self.lossy_factor += 1
    #                     self.gifsicle(fps=emoji.fps,
    #                                   lossy_factor=self.lossy_factor,
    #                                   color_map=color_map,
    #                                   input_file=raw_gif,
    #                                   output_file=output_file)
    #
    #
    #                 else:
    #                     print('damaged file is now {}kb'.format(actual_damaged_filesize/1024))
    #                     self.file_watch.removePath(output_file)
    #
    #             self.file_watch.fileChanged.connect(damaged_is_changed)
    #             damaged_is_changed(output_file)
    #
    #         else:
    #             print('lossy file is under {}kb'.format(damaged_filesize))
    #
    # def export(self, emoji):
    #     self.btn_export.setText('Exporting')
    #     self.console_add('Exporting: {}'.format(emoji.name))
    #
    #     # Avi to uncompressed gif
    #     if not emoji.has_raw_gif:
    #         raw_gif = self.ffmpeg(emoji.full_path, emoji.fps)
    #         print('Launching ffmpeg')
    #     else:
    #         raw_gif = os.path.splitext(emoji.full_path)[0]+'.gif'
    #         print('No ffmpeg needed')
    #
    #     # Uncompressed gif to lossy gif
    #     if emoji.resolution == '280x280':
    #         lossy_factor = self.spin_quality280.value()
    #     elif emoji.resolution == '136x136':
    #         lossy_factor = self.spin_quality136.value()
    #
    #     color_map = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
    #     output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy.gif'
    #                                .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
    #     self.console_add('output file = ' + output_file)
    #
    #     self.output_file = output_file
    #     self.lossy_factor = lossy_factor
    #     self.source = "export_stage1"
    #
    #     self.gifsicle(fps=emoji.fps,
    #                   lossy_factor=lossy_factor,
    #                   color_map=color_map,
    #                   input_file=raw_gif,
    #                   output_file=output_file)
    #
    #     # self.proc.waitForFinished()
    #     # self.task_x.add_task(cmd)
    #
    # @QtCore.Slot()
    # def export_stage2(self):
    #     self.source = 'export_stage2'
    #     emoji = self.working_emoji
    #     self.output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy-damaged.gif'
    #                                     .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
    #
    #     self.lossy_factor += 1
    #
    #     self.console_add('***\nTrying to write '+ self.output_file + '\n lossy factor is ' + str(self.lossy_factor))
    #     self.console_add('Trying lossy factor of {}'.format(self.lossy_factor))
    #     color_map = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
    #     raw_gif = os.path.splitext(emoji.full_path)[0]+'.gif'
    #
    #     self.gifsicle(fps=emoji.fps,
    #                   lossy_factor=self.lossy_factor,
    #                   color_map=color_map,
    #                   input_file=raw_gif,
    #                   output_file=self.output_file)
    #     print('export_stage2 ended')


# class Emoji(object):
#     def __init__(self, filename):
#         self.name = self.version = self.resolution = self.fps = self.lossy = self.damaged = self.has_raw_gif = False
#         self.full_path = filename
#         # [Наименование-анимации]-[02]-[280х280]-[30FPS]-[LOSSY]-[DAMAGED].[ext]
#         self.path, self.name = os.path.split(filename)
#         self.ext = os.path.splitext(self.name)[1]
#         self.name = os.path.splitext(self.name)[0]
#         self.split_properties = self.name.split('-')
#         if len(self.split_properties) >= 4:
#             self.name, self.version, self.resolution, self.fps = self.split_properties[:4]
#             self.fps = self.fps.upper().rstrip('FPS')
#             if 'LOSSY' in (tag.upper() for tag in self.split_properties[4:]):
#                 self.lossy = True
#             if 'DAMAGED' in (tag.upper() for tag in self.split_properties[4:]):
#                 self.damaged = True
#
#             self.video_list_item = QtGui.QListWidgetItem()
#             self.video_list_item.setText(self.name + ' | ' + self.version)
#
#             if self.lossy: lossy_icon = '_L'
#             else: lossy_icon = ''
#             if self.damaged: damaged_icon = '_D'
#             else: damaged_icon = ''
#             self.video_list_item.setIcon(QtGui.QIcon("icons\\{}_{}{}{}.png".
#                                                      format(self.resolution, self.fps, lossy_icon, damaged_icon)))
#
#             self.video_list_item.setToolTip\
#                 ('Name: {} \nversion: {} \nresolution: {} \nfps: {} \nlossy: {} \ndamaged: {}'
#                  .format(self.name, self.version, self.resolution, self.fps, self.lossy, self.damaged))
#
#             self.video_list_item.setData(ITEM_EMOJI_OBJECT, self)
#             self.video_list_item.setData(ITEM_NAME        , self.name)
#             self.video_list_item.setData(ITEM_VERSION     , self.version)
#             self.video_list_item.setData(ITEM_RESOLUTION  , self.resolution)
#             self.video_list_item.setData(ITEM_FPS         , self.fps)
#             self.video_list_item.setData(ITEM_LOSSY       , self.lossy)
#             self.video_list_item.setData(ITEM_DAMAGED     , self.damaged)
#             self.video_list_item.setData(ITEM_FULL_PATH   , self.full_path)
#         else:
#             raise ValueError('Wrong File detected: ' + self.full_path)
#
#     def get_info(self):
#         return 'Name: {} \nversion: {} \nresolution: {} \nfps: {} \nlossy: {} \ndamaged: {}' \
#             .format(self.name, self.version, self.resolution, self.fps, self.lossy, self.damaged)


if __name__ == '__main__':

    app = QtGui.QApplication([])
    MainWindowObj = QtMainWindow()
    MainWindowObj.show()

    app.exec_()
