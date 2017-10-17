# encoding: utf-8
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import act_reader
# import gifsicle
# import avi2gif
import time
import gif
import os

# ################################# CONFIG ################################### #
flag_convert_30_to_29dot97 = True
flag_show_message_bar_timer = False
act_folder = r'C:\Users\DayDreamer-i7\AppData\Roaming\Adobe\Adobe Photoshop CC 2017\Optimized Colors'
act_folder = './act'

# ############################### END CONFIG ################################# #
# ################################ CONSTANTS ################################# #
ITEM_EMOJI_OBJECT =  0x100
ITEM_NAME =          0x101
ITEM_VERSION =       0x102
ITEM_RESOLUTION =    0x103
ITEM_FPS =           0x104
ITEM_LOSSY =         0x105
ITEM_DAMAGED =       0x105
ITEM_FULL_PATH =     0x106
# ############################### END CONSTANTS ############################## #


def gifs_in_folder():
    return [os.path.join(os.path.abspath('./input'), gif) for gif in os.listdir('input') if '.gif' in gif]


def acts_in_folder():
    return [os.path.join(os.path.abspath(act_folder), act) for act in os.listdir('act') if '.act' in act]


def avis_in_folder():
    return [os.path.join(os.path.abspath('./input'), avi) for avi in os.listdir('input') if '.avi' in avi]


def emoji_list():
    emoji = []
    for item in gifs_in_folder():
        if len(item.split('-')) >= 4:
            item = Emoji(item)
            emoji.append(item)
    return emoji


class DDgui(QtGui.QMainWindow, gif.Ui_MainWindow):

    def __init__(self):
        super(DDgui, self).__init__()
        self.setupUi(self)
        self.setGeometry(200, 200, 40, 40)

        self.graphics_scene = QtGui.QGraphicsScene(self.layout_colortable)
        self.graphicsView = QtGui.QGraphicsView(self.graphics_scene)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 150))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        self.list_videoslist.setIconSize(QtCore.QSize(32, 32))

        # self.btn_size1.clicked.connect(lambda: self.spin_width.setValue(dims[0][0]))
        # self.btn_size1.clicked.connect(lambda: self.spin_height.setValue(dims[0][1]))

        self.movie136 = QtGui.QMovie()
        self.movie280 = QtGui.QMovie()

        # ################################# TOP BAR ################################## #
        @self.actionExit.triggered.connect
        def exit_ui():
            exit(0)

        # ################################# TOP ROW ################################## #
        self.btn_top1.setText('Update Videos Available')
        @self.btn_top1.clicked.connect
        def wip1():
            self.update_video_list()
            self.update_gifs_list()

        @self.btn_top2.clicked.connect
        def wip2():
            minimal_window_size()

        self.btn_top3.setEnabled(True)
        @self.btn_top3.clicked.connect
        def btn3():
            self.load_palette('SteffonDiggsEmoji-02-280x280-15FPS.avi_palette.png')


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

        # ############################### LEFT COLUMN ################################ #
        @self.btn_input_folder.clicked.connect
        def input_folder():
            self.list_videoslist.clear()
            self.list_videoslist.addItems(avis_in_folder())
            # self.list_gifslist.clear()
            # self.list_gifslist.addItems(gifs_in_folder())
            # Add gifs from folder to list widget
            for i in emoji_list():
                print(i)
                self.list_gifslist.addItem(i.filename)

        @self.list_videoslist.itemActivated.connect
        def avi_double_clicked_decorated(video_list_item):
            avi_double_clicked(video_list_item)

        def avi_double_clicked(video_list_item):
            if not video_list_item.data(ITEM_EMOJI_OBJECT).has_raw_gif:
                self.statusbar.showMessage('Generating the gif')
                self.ffmpeg(video_list_item.data(ITEM_FULL_PATH), video_list_item.data(ITEM_FPS))
            else:
                gif_double_clicked('avi')

        @self.list_gifslist.itemActivated.connect
        def gif_double_clicked_decorated():
            gif_double_clicked('gif')

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
            if self.list_videoslist.selectedItems():
                list_duplicate = [i.data(ITEM_EMOJI_OBJECT) for i in self.list_videoslist.selectedItems()]
                for i in list_duplicate:
                # for i in self.list_videoslist.selectedItems():
                #     self.export(i.data(ITEM_EMOJI_OBJECT))
                    self.export(i)
            else:
                self.statusbar.showMessage('Nothing selected for export')

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
            selected_file = os.path.splitext(self.original_280_gif)[0] + '.gif'
            working_file = self.movie280.fileName()
            output_file = os.path.splitext(working_file)[0] + '.tmp'
            self.movie280.stop()
            lossy_factor = self.spin_quality280.text()
            color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            # self.btn_update280.setEnabled(False)
            if self.check_endless_lossy280.isChecked():
                self.gifsicle(
                    input_file=working_file,
                    lossy_factor=lossy_factor,
                    color_map=color_table,
                    output_file=output_file,
                    delay=3,
                    source=self.source)
            else:
                self.gifsicle(
                    input_file=selected_file,
                    lossy_factor=lossy_factor,
                    color_map=color_table,
                    output_file=output_file,
                    delay=3,
                    source=self.source)
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
            selected_file = os.path.splitext(self.original_136_gif)[0] + '.gif'
            working_file = self.movie136.fileName()
            output_file = os.path.splitext(working_file)[0] + '.tmp'
            self.movie136.stop()
            lossy_factor = self.spin_quality136.text()
            color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            # print(color_table)
            # self.btn_update136.setEnabled(False)
            if self.check_endless_lossy136.isChecked():
                self.gifsicle(
                    input_file=working_file,
                    lossy_factor=lossy_factor,
                    color_map=color_table,
                    output_file=output_file,
                    delay=3,
                    source=self.source)
            else:
                self.gifsicle(
                    input_file=selected_file,
                    lossy_factor=lossy_factor,
                    color_map=color_table,
                    output_file=output_file,
                    delay=3,
                    source=self.source)

        def minimal_window_size():
            self.resize(1, 1)

        # def lossy(input_file, lossy_factor, color_map, delay=3, output_file=None, program='gifsicle.exe', arg=''):
        #     if output_file is None:
        #         output_file = input_file
        #     if arg == '':
        #         arg = '-O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}' \
        #             .format(delay, lossy_factor, color_map, input_file, output_file)

                #     parent.process = QtCore.QProcess(self)
                #     parent.process.start(program, arg)
                #     parent.process.readyReadStandardOutput.connect(self.__read)
                #     parent.calc.start('ping.exe', ['127.0.0.1'])
                #
                # def __read(self):
                #     out = self.calc.readAllStandardOutput()
                #     print(out)
                #
                # lossy

        self.source = None
        self.update_video_list()
        self.update_gifs_list()
        # Add acts from folder to list widget
        self.dropdown_colortable.addItems(acts_in_folder())

    def update_video_list(self):
        self.list_videoslist.clear()
        # Add objects pre-created list items to the list
        for i in avis_in_folder():
            emoji_object = Emoji(i)
            # Get the video-list item out of the Emoji object
            item = emoji_object.video_list_item
            # Check if avi has gif counterpart
            gif_full_path = os.path.splitext(item.data(ITEM_FULL_PATH))[0]+'.gif'
            if os.path.exists(gif_full_path):
                item.setBackground(QtGui.QColor(0, 255, 0, 32))
                emoji_object.has_raw_gif = True
            else:
                item.setBackground(QtGui.QColor(255, 255, 255, 255))
                emoji_object.has_raw_gif = False
            self.list_videoslist.addItem(item)

    def update_gifs_list(self):
        self.list_gifslist.clear()
        # Add objects pre-created list items to the list
        for i in gifs_in_folder():
            emoji_object = Emoji(i)
            # Get the video-list item out of the Emoji object
            item = emoji_object.video_list_item
            # Check if avi has gif counterpart
            gif_full_path = os.path.splitext(item.data(ITEM_FULL_PATH))[0]+'.gif'
            if os.path.exists(gif_full_path):
                item.setBackground(QtGui.QColor(0, 255, 0, 32))
                emoji_object.has_raw_gif = True
            else:
                item.setBackground(QtGui.QColor(255, 255, 255, 255))
                emoji_object.has_raw_gif = False
            self.list_gifslist.addItem(item)
    # ################################# LOADERS ################################## #

    def load_act(self, act_file):
        # print(act_file)
        self.graphics_scene.clear()
        act = act_reader.act_to_list(act_file)
        self.graphics_scene.addText(''.join(act[0]))
        self.statusbar.showMessage(act[1])

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

    def launch_process(self, command, source=None, working_file=''):
        self.console_add('='*50+'\n' + 'Launched ' + command)
        # print('Launched', command)
        self.slider_quality136.setEnabled(False)
        self.slider_quality280.setEnabled(False)
        self.spin_quality136.setEnabled(False)
        self.spin_quality280.setEnabled(False)
        self.btn_update136.setEnabled(False)
        self.btn_update280.setEnabled(False)
        self.proc = QtCore.QProcess()
        self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        @self.proc.finished.connect
        def finished():
            self.slider_quality136.setEnabled(True)
            self.slider_quality280.setEnabled(True)
            self.spin_quality136.setEnabled(True)
            self.spin_quality280.setEnabled(True)
            self.btn_update136.setEnabled(True)
            self.btn_update280.setEnabled(True)
            recognize_source()
            time2 = time.time()
            timer = 'Last subroutine took {} msec'.format(str(round(((time2-time1)*1000), 2)))
            self.console_add(timer)
            if flag_show_message_bar_timer:
                self.statusbar.showMessage(timer)
            self.console_add('Finished ' + command + '\n'+'='*50)
            # print('Finished ' + command)

        @self.proc.readyRead.connect
        def read_out():
            out = self.proc.readAll()
            self.console.append(str(out))
            print('|', str(out), sep='', end='')

        def recognize_source():
            print(source)
            if source == 'btn_update280':
                self.load280(os.path.splitext(self.movie280.fileName())[0] + '.tmp')
                size = str(round(os.path.getsize(self.movie280.fileName()) / 1024, 2))
                message = '280px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality280.text(), size)
                self.statusbar.showMessage(message)
                self.console_add(message)
            if source == 'btn_update136':
                self.load136(os.path.splitext(self.movie136.fileName())[0] + '.tmp')
                size = str(round(os.path.getsize(self.movie136.fileName()) / 1024, 2))
                message = '136px: Lossy factor of {} results in {}Kb of size'.format(self.spin_quality136.text(), size)
                self.statusbar.showMessage(message)
                self.console_add(message)
            if source == 'ffmpeg280':
                self.load280(os.path.splitext(working_file)[0] + '.gif')
                self.update_video_list()
            if source == 'ffmpeg136':
                self.load136(os.path.splitext(working_file)[0] + '.gif')
                self.update_video_list()

        time1 = time.time()
        self.proc.start(command)
        # self.proc.startDetached(command)
        # self.proc.start('ffmpeg.exe')
        # self.proc.start('gifsicle.exe --help')
        # self.proc.start('ping.exe')
        # self.proc.waitForFinished()

    def gifsicle(self, delay, lossy_factor, color_map, input_file, source=None, output_file=None):
        """Converts string a gif to a lossy gif
        input_file is a full path
        Returns output_file, which by default is equal to input_file"""
        if output_file is None:
            output_file = input_file
        cmd = 'gifsicle.exe -O3 --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}' \
            .format(lossy_factor, color_map, input_file, output_file)
        self.launch_process(cmd, source)
        return output_file

    def ffmpeg(self, input_file, fps=30):
        """Converts any video file to a gif
        input_file is a full path
        Returns input_file with .gif extension"""
        if flag_convert_30_to_29dot97 and fps == 30:
            fps = 29.97
        cmd = 'video2gif.bat {} -y -f {}'.format(input_file, fps)
        if '280' in input_file:
            self.launch_process(cmd, 'ffmpeg280', input_file)

        elif '136' in input_file:
            self.launch_process(cmd, 'ffmpeg136', input_file)

        return os.path.splitext(input_file)[0] + '.gif'

    def export(self, emoji):
        self.btn_export.setText('Exporting')
        self.console_add('Exporting: {}'.format(emoji.name))

        # Avi to uncompressed gif
        if not emoji.has_raw_gif:
            raw_gif = self.ffmpeg(emoji.full_path)
            self.proc.waitForFinished()
            print('Launching ffmpeg')
        else:
            raw_gif = os.path.splitext(emoji.full_path)[0]+'.gif'
            print('No ffmpeg needed')

        # Uncompressed gif to lossy gif
        if emoji.resolution == '280x280':
            lossy_factor = self.spin_quality280.value()
        elif emoji.resolution == '136x136':
            lossy_factor = self.spin_quality136.value()

        color_map = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
        output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy.gif'
                                   .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
        self.console_add('output file = ' + output_file)
        self.gifsicle(delay=int(100/int(''.join((digit for digit in emoji.fps if digit.isdigit())))),
                      lossy_factor=lossy_factor,
                      color_map=color_map,
                      input_file=raw_gif,
                      output_file=output_file)

        self.proc.waitForFinished()
        # self.task_x.add_task(cmd)

        if os.path.exists(output_file):
            self.console_add(output_file + ' exists')
        else:
            self.console_add(output_file + ' doesnt exist')

        # Uncompressed gif to damaged gif
        # if emoji.resolution == '280x280':
        lossy_file_size = os.path.getsize(output_file)
        output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS-lossy-damaged.gif'
                                   .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))


        while lossy_file_size > 500*1024:

            lossy_factor += 1

            self.console_add('***\nTrying to write '+ output_file + '\n lossy factor is ' + str(lossy_factor))
            self.console_add('Trying lossy factor of {}'.format(lossy_factor))

            self.gifsicle(delay=int(100/int(''.join((digit for digit in emoji.fps if digit.isdigit())))),
                          lossy_factor=lossy_factor,
                          color_map=color_map,
                          input_file=raw_gif,
                          output_file=output_file)
            self.proc.waitForFinished()
            lossy_file_size = os.path.getsize(output_file)

            print('{} ver-{} {} {}fps with lossy of {} was compressed to {}Kb'.format(emoji.name,
                                                                                      emoji.version,
                                                                                      emoji.resolution,
                                                                                      emoji.fps,
                                                                                      lossy_factor,
                                                                                      round(lossy_file_size/1024, 2)))
            self.console_add('({}Kb)'.format(round(lossy_file_size/1024, 2)))
            if lossy_file_size > 600*1024:
                lossy_factor += 100-1
            if lossy_file_size > 550*1024:
                lossy_factor += 50-1
            if lossy_file_size > 505*1024:
                lossy_factor += 10-1

        self.btn_export.setText('Export')


class TasksPool(QtCore.QObject):
    startNextTaskSignal = QtCore.Signal()
    allTasksCompleteSignal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.tasks_pool = []
        self.process = QtCore.QProcess()

        self.startNextTaskSignal.connect(self.execute_task)
        self.allTasksCompleteSignal.connect(self.tasks_copmlete)

    def add_task(self, cmd):
        self.tasks_pool.append(cmd)
        self.startNextTaskSignal.emit()

    def execute_task(self):
        print ('Start next?')
        if self.process.isOpen():
            self.process.waitForFinished()
        if not self.tasks_pool:
            self.allTasksCompleteSignal.emit()
            return
        self.process = QtCore.QProcess()
        # self.process.finished.connect(lambda *x: self.startNextTaskSignal.emit)
        self.process.finished.connect(lambda *x: QtCore.QTimer.singleShot(1000, self.startNextTaskSignal.emit))
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyRead.connect(self.process_output)
        next_task = self.tasks_pool.pop(0)
        print ('NEXT TASK', next_task)
        self.process.start(next_task)

    def process_output(self):
        output = self.process.readAll()
        output = str(output).strip()
        if output:
            print (output)

    def tasks_copmlete(self):
        print ('ALL TASKS COMPLETE')
        # sys.exit()


class Emoji(object):
    def __init__(self, filename):
        self.name = self.version = self.resolution = self.fps = self.lossy = self.damaged = self.has_raw_gif = False
        self.full_path = filename
        # [Наименование-анимации]-[02]]-[280х280]-[30FPS]-[LOSSY]-[DAMAGED].[ext]
        self.path, self.name = os.path.split(filename)
        self.ext = os.path.splitext(self.name)[1]
        self.name = os.path.splitext(self.name)[0]
        self.split_properties = self.name.split('-')
        if len(self.split_properties) >= 4:
            self.name, self.version, self.resolution, self.fps = self.split_properties[:4]
            self.fps = self.fps.upper().rstrip('FPS')
            if 'LOSSY' in (tag.upper() for tag in self.split_properties[4:]):
                self.lossy = True
            if 'DAMAGED' in (tag.upper() for tag in self.split_properties[4:]):
                self.damaged = True

            self.video_list_item = QtGui.QListWidgetItem()
            self.video_list_item.setText(self.name + ' | ' + self.version)

            if self.lossy: lossy_icon = '_L'
            else: lossy_icon = ''
            if self.damaged: damaged_icon = '_D'
            else: damaged_icon = ''
            self.video_list_item.setIcon(QtGui.QIcon("icons\\{}_{}{}{}.png".
                                                     format(self.resolution, self.fps, lossy_icon, damaged_icon)))

            self.video_list_item.setToolTip\
                ('Name: {} \nversion: {} \nresolution: {} \nfps: {} \nlossy: {} \ndamaged: {}'
                 .format(self.name, self.version, self.resolution, self.fps, self.lossy, self.damaged))


            self.video_list_item.setData(ITEM_EMOJI_OBJECT, self)
            self.video_list_item.setData(ITEM_NAME        , self.name)
            self.video_list_item.setData(ITEM_VERSION     , self.version)
            self.video_list_item.setData(ITEM_RESOLUTION  , self.resolution)
            self.video_list_item.setData(ITEM_FPS         , self.fps)
            self.video_list_item.setData(ITEM_LOSSY       , self.lossy)
            self.video_list_item.setData(ITEM_DAMAGED     , self.damaged)
            self.video_list_item.setData(ITEM_FULL_PATH   , self.full_path)
        else:
            raise ValueError('Wrong File detected: ' + self.full_path)

    def get_info(self):
        return 'Name: {} \nversion: {} \nresolution: {} \nfps: {} \nlossy: {} \ndamaged: {}' \
            .format(self.name, self.version, self.resolution, self.fps, self.lossy, self.damaged)


if __name__ == '__main__':
    # [ print('\n' + i.get_info()) for i in emojis_list]

    app = QtGui.QApplication([])
    w = DDgui()

    w.show()
    app.exec_()

