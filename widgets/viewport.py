from PySide.QtCore import *
from PySide.QtGui import *
import logging
from os import path
from emoji import Emoji
from gifsicle import GifSicle
from messages import *

from widgets import viewport_ui

DEFAULT_SCALE = 2
logger = logging.getLogger(__name__)


class Viewport(QWidget, viewport_ui.Ui_viewport_masterQW):

    TO_STATUS_BAR = Signal(str)

    def __init__(self, embedded):
        super(Viewport, self).__init__()

        self.setupUi(self)

        self.movie = QMovie()
        self.opened_image = None
        self.previous_scale = 1
        self.flag1 = False
        self.color_table = None
        self.embedded = not bool(embedded)                                               # Has NOT a parent widget?
        self.scroll_lock = False
        self.graphics_scene = QGraphicsScene()                                           # Create a scene
        self.graphicsView.setScene(self.graphics_scene)                                  # Start watching at the scene

        self.gif_player_widget = QWidget()                                               # Setup a QWidget
        self.gif_player = QLabel(self.gif_player_widget)                                 # Add QLabel to the QWidget
        self.gif_player.setAlignment(Qt.AlignCenter)                                     # Tell QLabel to center itself
        self.gif_player.setStyleSheet("background-color:transparent;");
        self.gif_player.setParent(None)
        self.gif_player_proxy_widget = self.graphics_scene.addWidget(self.gif_player)         # Add QWidget to scene

        self.graphicsView.PLAYPAUSE.connect(lambda: self.btn_playpause.toggle())
        self.TO_STATUS_BAR.connect(lambda x: print(x))

        self.load(r"icons\nofileloaded.png", zoom=1)

        @self.graphicsView.MOUSEWHEEL.connect
        def wheel_zoom(up):
            if up:
                self.change_zoom_by(1)
            else:
                self.change_zoom_by(-1)


        @self.graphicsView.TIME_OFFSET.connect
        def time_scroll(mouse_offset):
            if mouse_offset > 0:
                self.btn_ff.click()
            elif mouse_offset < 0:
                self.btn_fb.click()

        @self.graphicsView.TEMP_PAUSE.connect
        def pause_on_drag(state):
            if not self.btn_playpause.isChecked() and state:
                self.flag1 = True
                self.btn_playpause.toggle()
            if self.btn_playpause.isChecked() and not state and self.flag1:
                self.flag1 = False
                self.btn_playpause.toggle()

        @self.btn_fb.clicked.connect
        def btn_fb_clicked():
            current_frame = self.movie.currentFrameNumber()
            self.movie.jumpToFrame(0)
            for i in range(current_frame - 1):
                self.movie.jumpToNextFrame()

            frame_n = str(self.movie.currentFrameNumber())
            fps = '\tFPS: ' + str(round(1000 / self.movie.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie.nextFrameDelay())
            self.TO_STATUS_BAR.emit('px: Jumped to frame #' + frame_n + fps + delay)

        @self.btn_playpause.toggled.connect
        def btn_playpause_toggled(state):
            self.movie.setPaused(state)
            self.btn_playpause.setDown(state)
            if state:
                self.TO_STATUS_BAR.emit('px: Paused on frame #' + str(self.movie.currentFrameNumber()))
            else:
                self.TO_STATUS_BAR.emit('px: Playing')

        @self.btn_ff.clicked.connect
        def btn_ff_clicked():
            self.movie.jumpToNextFrame()
            fps = '\tFPS: ' + str(round(1000 / self.movie.nextFrameDelay(), 2))
            delay = '\tDelay: ' + str(self.movie.nextFrameDelay())
            frame_n = str(self.movie.currentFrameNumber())
            self.TO_STATUS_BAR.emit('px: Jumped to frame #' + frame_n + fps + delay)

        @self.slider_speed.valueChanged.connect
        def speed_slider_changed(value):
            self.TO_STATUS_BAR.emit('Speed of px changed to {}x'.format(value/100))
            self.spin_speed.blockSignals(True)
            self.spin_speed.setValue(value * 0.01)
            self.spin_speed.blockSignals(False)
            self.movie.setSpeed(value)

        @self.spin_speed.valueChanged.connect
        def speed_spinner_changed(value):
            value = round(value, 2)
            value *= 100
            self.slider_speed.setValue(value)
            self.movie.setSpeed(value)

        @self.spin_quality.valueChanged.connect
        def spin_quality_value_changed():
            if self.check_livepreview.isChecked():
                btn_update_clicked()

        def btn_update_clicked():
            if self.embedded or self.scroll_lock:
                f = QFileDialog.getOpenFileName(self, 'Select image to load', '.', "All Files (*.*)", "All Files (*.*)")
                if f:
                    self.load(f[0])
            else:
                if isinstance(self.opened_image, str):  # If we give a string it makes it to Emoji
                    self.opened_image = Emoji(self.opened_image)
                if isinstance(self.opened_image, Emoji):
                    working_file = self.opened_image.gif_path
                    output_file = self.opened_image.temp_path
                else:
                    raise ValueError('Update button received not Emoji or str')
                self.movie.stop()
                lossy_factor = self.spin_quality.text()
                # Instead of generating a txt file for a colortable
                # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
                color_table_path = path.join('.', 'current_act.txt')

                # Get a handle on color table QPlainTextEdit

                plaintext_act_readout = self.parentWidget().findChildren(QPlainTextEdit, 'plaintext_act_readout')[0]
                # We generate a colormap from the colormap viewer window
                with open(color_table_path, 'w') as txt:
                    txt.writelines(plaintext_act_readout.toPlainText())

                self.gc = GifSicle(self.opened_image, lossy_factor, color_table_path)
                print(self.gc, self.opened_image, lossy_factor, color_table_path)

                self.load(output_file)
                temp_file_size = path.getsize(output_file)/1024
                self.TO_STATUS_BAR.emit('Resulting filesize is: {:.2f} Kb'.format(temp_file_size))
        self.btn_update.clicked.connect(btn_update_clicked)
        self.check_embedded()

    def check_embedded(self):
        if self.embedded or self.scroll_lock:                                                                  # Override update button
            self.btn_update.setText('Load')
            # self.btn_update.clicked.connect(self.btn_update_clicked_load_override)
            # self.btn_update.clicked.disconnect(self.btn_update_clicked)
        else:
            self.btn_update.setText('Update')
            # self.btn_update.clicked.connect(self.btn_update_clicked)
            # self.btn_update.clicked.disconnect(self.btn_update_clicked_load_override)




    def change_zoom_by(self, value):
        self.TO_STATUS_BAR.emit('Zoom was {}'.format(self.previous_scale))
        self.graphicsView.scale(1/self.previous_scale, 1/self.previous_scale)
        self.previous_scale = max(self.previous_scale + value, 1)
        self.graphicsView.scale(self.previous_scale, self.previous_scale)
        self.TO_STATUS_BAR.emit('Zoom of px changed to {}x'.format(self.previous_scale))

    def reset_zoom(self):
        self.graphicsView.scale(1/self.previous_scale, 1/self.previous_scale)
        self.previous_scale = 1
        return self.previous_scale


    def open_image(self, input_):
        """
        This method opens image and sends it to loader

        :param input_: Emoji or str path to the image
        :return: Loaded image or None if error
        """
        self.opened_image = input_                              # Store the image as currently working with
        if isinstance(input_, Emoji):                           # If it is an Emoji object,
            input_ = input_.gif_path                            # then convert it to image path
        elif not isinstance(input_, str):                       # If it is also not a string, then raise an exception
            raise AttributeError('Trying to open image but it is not a Emoji and not a string')
        if path.exists(input_):                                 # If path exists
            self.load(input_)                                   # Load the image
            return input_
        else:                                                   # Or notify user that image does not exist
            error_msg = file_not_found(input_)
            QMessageBox.critical(QMessageBox(), *error_msg)
            # todo test this
            return False

    def load(self, file: str, zoom=DEFAULT_SCALE):
        """
        This method loads an image to the viewer based on str full path to it

        :param file: Image path
        :param zoom: If defined, sets the initial zoom
        :return: If loaded movie is valid and functional
        """
        image_dimensions = QImage(file).size()                      # Get image size
        self.graphics_scene.setSceneRect(image_dimensions.width()*-.5,image_dimensions.height()*-.5,image_dimensions.width(),image_dimensions.height())
        self.gif_player_proxy_widget.setMaximumSize(image_dimensions)     # Set widget's size to image's size
        self.gif_player.setFixedSize(image_dimensions)            # Set QLabel's size to image's size
        self.gif_player.move(image_dimensions.width()*-.5,image_dimensions.height()*-.5)
        self.change_zoom_by(zoom - self.reset_zoom())
        self.btn_playpause.setChecked(False)                    # Unpress the play-pause button
        self.btn_fb.setEnabled(True)                            # Enable back button
        self.btn_playpause.setEnabled(True)                     # Enable play-pause button
        self.btn_ff.setEnabled(True)                            # Enable forward button
        self.layout_viewport.setTitle(path.split(file)[1])      # Set name of the gif as the title
        self.movie.setFileName('')                              # Free (close) the previous loaded image
        self.movie = QMovie(file)                               # Create a QMovie instance
        self.gif_player.setMovie(self.movie)                    # And assign it to the player widget
        self.movie.setSpeed(self.spin_speed.value()*100)        # Automatically set speed using the speed spinner
        self.movie.start()
        self.graphicsView.updateGeometry()
        return self.movie.isValid()

    def unload_image(self):
        self.movie.stop()
        self.load(r"icons\nofileloaded.png")
        self.reset_zoom()


if __name__ == '__main__':
    app = QApplication([])
    vp = Viewport(embedded=False)
    vp.show()
    # vp.open_image(Emoji("C:\Python\Giftcher\BrandinCooksEmojiTest_01\BrandinCooksEmojiTest_01_280x280_30fps.gif"))
    app.exec_()
