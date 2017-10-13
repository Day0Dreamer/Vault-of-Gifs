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
# ############################### END CONFIG ################################# #


def gifs_in_folder():
    return [os.path.join(os.path.abspath(os.path.curdir), gif) for gif in os.listdir() if '.gif' in gif]


def acts_in_folder():
    return [os.path.join(os.path.abspath(os.path.curdir), act) for act in os.listdir() if '.act' in act]


def avis_in_folder():
    return [os.path.join(os.path.abspath(os.path.curdir), avi) for avi in os.listdir() if '.avi' in avi]


def emoji_list():
    emoji = []
    for item in gifs_in_folder():
        if len(item.split('-')) >= 4:
            item = Emoji(item)
            emoji.append(item)
    return emoji


def update_video_list(qt_window):
    qt_window.list_videoslist.clear()
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
        qt_window.list_videoslist.addItem(item)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{} function took {} ms'.format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap




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
            update_video_list(self)

        @self.btn_top2.clicked.connect
        def wip2():
            minimal_window_size()

        self.btn_top3.setEnabled(True)
        # self.btn_top3.clicked.connect(self.test)

        self.console = QtGui.QTextBrowser(self)
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

        @self.list_videoslist.itemDoubleClicked.connect
        def avi_double_clicked(item):
            if not item.data(ITEM_EMOJI_OBJECT).has_raw_gif:
                self.statusbar.showMessage('Generating the gif')
                self.ffmpeg(item.data(ITEM_FULL_PATH))
            gif_double_clicked(item)
            update_video_list(self)
            # print(item.data(ITEM_FULL_PATH))

        @self.list_gifslist.itemDoubleClicked.connect
        def gif_double_clicked_decorated(value):
            gif_double_clicked(value)

        self.original_280_gif = None
        self.original_136_gif = None

        def gif_double_clicked(value):
            value = value.data(ITEM_FULL_PATH)
            # Launch avi's gif counterparts
            if os.path.splitext(value)[1] != 'gif':
                value = os.path.splitext(value)[0] + '.gif'
            if '136' in value:
                load136(value)
                self.original_136_gif = value
            elif '280' in value:
                vid280 = load280(value)
                self.original_280_gif = value
                if vid280:
                    self.statusbar.showMessage('280px: Gif is loaded')

        @self.dropdown_colortable.currentIndexChanged.connect
        def dropdown_colortable_selected(index_of_selected_item):
            load_act(acts_in_folder()[index_of_selected_item])

        @self.btn_export.clicked.connect
        def btn_export_clicked():
            if self.list_videoslist.selectedItems():
                for i in self.list_videoslist.selectedItems():
                    self.export(i.data(ITEM_EMOJI_OBJECT))
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

        @self.slider_quality280.sliderReleased.connect
        def slider_quality280_slider_released():
            # self.spin_quality280.blockSignals(True)
            self.spin_quality280.setValue(self.slider_quality280.value())
            # self.spin_quality280.blockSignals(False)

        @self.slider_quality280.valueChanged.connect
        def slider_quality280_value_changed():
            if self.check_livepreview280.isChecked():
                pass
            else:
                self.spin_quality280.setValue(self.slider_quality280.value())
                # self.spin_quality280.blockSignals(True)
                # self.spin_quality280.blockSignals(False)

        @self.spin_quality280.valueChanged.connect
        def spin_quality280_value_changed():
            if self.check_livepreview280.isChecked():
                btn_update280_clicked()

        @self.btn_update280.clicked.connect
        def btn_update280_clicked_decorated():
            btn_update280_clicked()

        def btn_update280_clicked():
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
                    delay=3)
            else:
                self.gifsicle(
                    input_file=selected_file,
                    lossy_factor=lossy_factor,
                    color_map=color_table,
                    output_file=output_file,
                    delay=3)
            # @self.worker.finish_signal.connect
            # def load280_decorated():
            #     print('Finish signal received:', time.time())
            load280(os.path.splitext(working_file)[0] + '.tmp')


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

        # ################################# LOADERS ################################## #
        def load280(file280):
            self.btn_playpause280.setChecked(False)
            self.btn_fb280.setEnabled(True)
            self.btn_playpause280.setEnabled(True)
            self.btn_ff280.setEnabled(True)
            self.layout_gif280.setTitle(file280)
            self.movie280 = QtGui.QMovie(file280)
            self.gifplayer280.setMovie(self.movie280)
            self.movie280.setSpeed(self.spin_speed280.value()*100)
            self.movie280.start()
            return self.movie280.isValid()

        def load136(file136):
            self.btn_playpause136.setChecked(False)
            self.btn_fb136.setEnabled(True)
            self.btn_playpause136.setEnabled(True)
            self.btn_ff136.setEnabled(True)
            self.layout_gif136.setTitle(file136)
            self.movie136 = QtGui.QMovie(file136)
            self.gifplayer136.setMovie(self.movie136)
            self.movie136.setSpeed(self.spin_speed136.value()*100)
            self.movie136.start()
            return self.movie136.isValid()

        def load_act(act_file):
            # print(act_file)
            self.graphics_scene.clear()
            act = act_reader.act_to_list(act_file)
            self.graphics_scene.addText(''.join(act[0]))
            self.statusbar.showMessage(act[1])

        def minimal_window_size():
            self.resize(1, 1)

        def lossy(input_file, lossy_factor, color_map, delay=3, output_file=None, program='gifsicle.exe', arg=''):
            if output_file is None:
                output_file = input_file
            if arg == '':
                arg = '-O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}' \
                    .format(delay, lossy_factor, color_map, input_file, output_file)

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

    def console_add(self, log_input):
        self.console.append(str(log_input).rstrip())

    def launch_process(self, command='ping.exe'):
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
            self.console_add('Me finished')

        @self.proc.readyRead.connect
        def read_out():
            out = self.proc.readAll()
            self.console.append(str(out))
        time1 = time.time()
        self.proc.start(command)
        # self.proc.startDetached(command)
        # self.proc.start('ffmpeg.exe')
        # self.proc.start('gifsicle.exe --help')
        # self.proc.start('ping.exe')
        # self.proc.waitForFinished()
        time2 = time.time()
        timer = 'Last subroutine took {} msec'.format(str(round(((time2-time1)*1000),2)))
        self.console_add(timer)
        self.statusbar.showMessage(timer)

    def gifsicle(self, delay, lossy_factor, color_map, input_file, output_file=None):
        if output_file is None:
            output_file = input_file
        cmd = 'gifsicle.exe -O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}'\
            .format(delay, lossy_factor, color_map, input_file, output_file)
        self.launch_process(cmd)

    def ffmpeg(self, video, fps=30):
        cmd = 'video2gif.bat {} -y -f {}'.format(video, fps)
        self.launch_process(cmd)
        return os.path.splitext(video)[0]+'.gif'

    def export(self, emoji):
        if flag_convert_30_to_29dot97:
            pass
        self.console_add('Exporting: {}'.format(emoji.name))

        # Avi to uncompressed gif
        if not emoji.has_raw_gif:
            raw_gif = self.ffmpeg(emoji.full_path)
        else:
            raw_gif = os.path.splitext(emoji.full_path)[0]+'.gif'

        # Uncompressed gif to lossy gif
        if emoji.resolution == '280x280':
            lossy_factor = self.spin_quality280.value()
        elif emoji.resolution == '136x136':
            lossy_factor = self.spin_quality136.value()

        color_map = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
        output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS_lossy.gif'
                                   .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
        self.console_add(output_file)
        self.gifsicle(delay=int(100/int(''.join((digit for digit in emoji.fps if digit.isdigit())))),
                      lossy_factor=lossy_factor,
                      color_map=color_map,
                      input_file=raw_gif,
                      output_file=output_file)

        # Uncompressed gif to damaged gif
        if emoji.resolution == '280x280':
            lossy_file_size = os.path.getsize(output_file)
            output_file = os.path.join(emoji.path, '{}-{}-{}-{}FPS_lossy_damaged.gif'
                                       .format(emoji.name, emoji.version, emoji.resolution, emoji.fps))
            while lossy_file_size > 500*1024:
                lossy_factor += 1
                self.console_add('Trying lossy factor of {}'.format(lossy_factor))

                self.gifsicle(delay=int(100/int(''.join((digit for digit in emoji.fps if digit.isdigit())))),
                              lossy_factor=lossy_factor,
                              color_map=color_map,
                              input_file=raw_gif,
                              output_file=output_file)
                lossy_file_size = os.path.getsize(output_file)
                self.console_add('({}Kb)'.format(round(lossy_file_size/1024,2)))

        self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        @self.proc.readyRead.connect
        def read_out():
            out = self.proc.readAll()
            w.console.append(str(out))
            print(out)
        self.proc.start(command)
        # self.proc.waitForFinished()
        # self.finish_signal.emit()
        self.proc.finished.connect(lambda *a: self.finish_signal.emit())



ITEM_EMOJI_OBJECT =  0x100
ITEM_NAME =          0x101
ITEM_VERSION =       0x102
ITEM_RESOLUTION =    0x103
ITEM_FPS =           0x104
ITEM_LOSSY =         0x105
ITEM_DAMAGED =       0x105
ITEM_FULL_PATH =     0x106

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

class worker(QtCore.QObject):
    finish_signal = QtCore.Signal()
    def __init__(self):
        super(worker, self).__init__()
        self.proc = QtCore.QProcess()

    def gifsicle(self, delay, lossy_factor, color_map, input_file, output_file=None):
        print('Thread run (gifsicle)')
        if output_file is None:
            output_file = input_file
        cmd = 'gifsicle.exe -O3 -d={} --no-comments --no-names --no-extensions --lossy={} --use-colormap "{}" {} -o {}' \
            .format(delay, lossy_factor, color_map, input_file, output_file)
        self.launch_process(cmd)


        # self.finish_signal.emit()

if __name__ == '__main__':
    # [ print('\n' + i.get_info()) for i in emojis_list]

    app = QtGui.QApplication([])
    w = DDgui()

    # item = QtGui.QListWidgetItem('qwe')
    # item.setBackground(QtGui.QColor(255, 0, 0, 16))
    # item.setData(0x100,'asdasd')
    # print(item.data(0x100))
    # w.list_videoslist.addItem(item)

    update_video_list(w)

    # Add acts from folder to list widget
    # w.dropdown_colortable.clear()
    w.dropdown_colortable.addItems(acts_in_folder())

    w.show()
    app.exec_()
