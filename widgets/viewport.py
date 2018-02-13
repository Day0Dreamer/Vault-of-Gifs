from PySide.QtCore import *
from PySide.QtGui import *
from os import path

from widgets import viewport_ui

DEFAULT_SCALE = 2


class Viewport(QWidget, viewport_ui.Ui_Form):

    TO_STATUS_BAR = Signal(str)

    def __init__(self):
        super(Viewport, self).__init__()
        self.setupUi(self)

        self.movie = QMovie()
        self.previous_scale = DEFAULT_SCALE

        self.graphics_scene = QGraphicsScene()                                           # Create a scene
        self.graphicsView.setScene(self.graphics_scene)                                  # Start watching at the scene

        self.gif_player_widget = QWidget()                                               # Setup a QWidget
        self.gif_player = QLabel(self.gif_player_widget)                                 # Add QLabel to the QWidget
        gif_player_proxy_widget = self.graphics_scene.addWidget(self.gif_player_widget)  # Add QWidget to scene
        self.gif_player_widget = gif_player_proxy_widget.widget()                        # Get new handle to QWidget
        self.gif_player = self.gif_player_widget.children()[0]                           # Get new handle to QLabel

        self.graphicsView.PLAYPAUSE.connect(lambda: self.btn_playpause.toggle())
        self.TO_STATUS_BAR.connect(lambda x: print(x))

        @self.graphicsView.MOUSEWHEEL.connect
        def wheel_zoom(up):
            if up:
                change_zoom_by(1)
            else:
                change_zoom_by(-1)

        def change_zoom_by(value):
            self.TO_STATUS_BAR.emit('Zoom of px changed to {}x'.format(value))
            self.graphicsView.scale(1/self.previous_scale, 1/self.previous_scale)
            self.previous_scale = max(self.previous_scale + value, 1)
            self.graphicsView.scale(self.previous_scale, self.previous_scale)

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
            working_file = self.loaded_.gif_path
            output_file = path.splitext(working_file)[0] + '.tmp'
            self.movie.stop()
            lossy_factor = self.spin_quality.text()
            # Instead of generating a txt file for a colortable
            # color_table = act_reader.create_gifsicle_colormap(self.dropdown_colortable.currentText())
            self.color_table = path.join('.\\temp', 'current_act.txt')
            # We generate a colormap from the colormap viewer window
            with open(self.color_table, 'w') as txt:
                txt.writelines(self.plaintext_act_readout.toPlainText())
            color_table = self.color_table

            self.gc = GifSicle(self.loaded_, lossy_factor, color_table)

            self.load_gif(output_file)
            temp_file_size = path.getsize(output_file)/1024
            self.TO_STATUS_BAR.emit('Resulting filesize is: {:.2f} Kb'.format(temp_file_size))
        self.btn_update.clicked.connect(btn_update_clicked)

        # self.graphicsView.scale(2, 2)
        
    def load(self, file):
        image_dimensions = QImage(file).size()                          # Get image size
        self.gif_player_widget.setMinimumSize(image_dimensions)         # Set widget's size to image's size
        self.gif_player.setMinimumSize(image_dimensions)                # Set QLabel's size to image's size
        self.btn_playpause.setChecked(False)                   # Unpress the play-pause button
        self.btn_fb.setEnabled(True)                           # Enable back button
        self.btn_playpause.setEnabled(True)                    # Enable play-pause button
        self.btn_ff.setEnabled(True)                           # Enable forward button
        self.layout_viewport.setTitle(path.split(file)[1])     # Set name of the gif as the title
        self.movie.setFileName('')                             # Free (close) the previous loaded image
        self.movie = QMovie(file)                              # Create a QMovie instance
        self.gif_player.setMovie(self.movie)                   # And assign it to the player widget
        self.movie.setSpeed(self.spin_speed.value()*100)       # Automatically set speed using the speed spinner
        self.movie.start()
        return self.movie.isValid()


if __name__ == '__main__':
    app = QApplication([])
    vp = Viewport()
    vp.show()
    vp.load("C:\Python\Vault_Of_Gifs\Fanatics-animated-emoji-07\Fanatics-animated-emoji-07_280x280_15fps_LOSSY.gif")
    app.exec_()
