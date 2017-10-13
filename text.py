from PySide.QtCore import *
from PySide.QtGui import *


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(411, 79)
        self.ly = QHBoxLayout(self)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.ly.addWidget(self.slider)
        self.spin = QDoubleSpinBox(self)
        self.ly.addWidget(self.spin)
        self.spin.setMaximum(100)
        self.spin.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setMinimum(0)
        self.spin.setSingleStep(0.01)

        @self.spin.valueChanged.connect
        def spinchanged(value):
            self.slider.blockSignals(True)
            self.slider.setValue(value*100)
            self.slider.blockSignals(False)

        @self.slider.valueChanged.connect
        def sliderchanged(value):
            self.spin.blockSignals(True)
            self.spin.setValue(value*0.01)
            self.spin.blockSignals(False)


if __name__ == '__main__':
    app = QApplication([])
    w = Window()
    w.show()
    app.exec_()