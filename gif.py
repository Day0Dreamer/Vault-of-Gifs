# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python\Vault_Of_Gifs\gif.ui'
#
# Created: Tue Oct 10 20:06:57 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(926, 880)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_topshelf = QtGui.QHBoxLayout()
        self.layout_topshelf.setObjectName("layout_topshelf")
        self.btn_top1 = QtGui.QPushButton(self.centralwidget)
        self.btn_top1.setEnabled(True)
        self.btn_top1.setObjectName("btn_top1")
        self.layout_topshelf.addWidget(self.btn_top1)
        self.btn_top2 = QtGui.QPushButton(self.centralwidget)
        self.btn_top2.setObjectName("btn_top2")
        self.layout_topshelf.addWidget(self.btn_top2)
        self.btn_top3 = QtGui.QPushButton(self.centralwidget)
        self.btn_top3.setEnabled(False)
        self.btn_top3.setObjectName("btn_top3")
        self.layout_topshelf.addWidget(self.btn_top3)
        self.btn_top4 = QtGui.QPushButton(self.centralwidget)
        self.btn_top4.setEnabled(False)
        self.btn_top4.setObjectName("btn_top4")
        self.layout_topshelf.addWidget(self.btn_top4)
        self.verticalLayout_2.addLayout(self.layout_topshelf)
        self.separator_topshelf = QtGui.QFrame(self.centralwidget)
        self.separator_topshelf.setFrameShape(QtGui.QFrame.HLine)
        self.separator_topshelf.setFrameShadow(QtGui.QFrame.Sunken)
        self.separator_topshelf.setObjectName("separator_topshelf")
        self.verticalLayout_2.addWidget(self.separator_topshelf)
        self.layout3in1 = QtGui.QHBoxLayout()
        self.layout3in1.setObjectName("layout3in1")
        self.layout_fileops = QtGui.QVBoxLayout()
        self.layout_fileops.setObjectName("layout_fileops")
        self.btn_input_folder = QtGui.QPushButton(self.centralwidget)
        self.btn_input_folder.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_input_folder.setObjectName("btn_input_folder")
        self.layout_fileops.addWidget(self.btn_input_folder)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_videos = QtGui.QWidget()
        self.tab_videos.setObjectName("tab_videos")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_videos)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.list_videoslist = QtGui.QListWidget(self.tab_videos)
        self.list_videoslist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.list_videoslist.setObjectName("list_videoslist")
        self.verticalLayout_4.addWidget(self.list_videoslist)
        self.tabWidget.addTab(self.tab_videos, "")
        self.tab_gifs = QtGui.QWidget()
        self.tab_gifs.setObjectName("tab_gifs")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_gifs)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.list_gifslist = QtGui.QListWidget(self.tab_gifs)
        self.list_gifslist.setObjectName("list_gifslist")
        self.verticalLayout_5.addWidget(self.list_gifslist)
        self.tabWidget.addTab(self.tab_gifs, "")
        self.layout_fileops.addWidget(self.tabWidget)
        self.groupb_colortable = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupb_colortable.sizePolicy().hasHeightForWidth())
        self.groupb_colortable.setSizePolicy(sizePolicy)
        self.groupb_colortable.setObjectName("groupb_colortable")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupb_colortable)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.dropdown_colortable = QtGui.QComboBox(self.groupb_colortable)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dropdown_colortable.sizePolicy().hasHeightForWidth())
        self.dropdown_colortable.setSizePolicy(sizePolicy)
        self.dropdown_colortable.setObjectName("dropdown_colortable")
        self.verticalLayout_6.addWidget(self.dropdown_colortable)
        self.layout_fileops.addWidget(self.groupb_colortable)
        self.groupb_preset = QtGui.QGroupBox(self.centralwidget)
        self.groupb_preset.setObjectName("groupb_preset")
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.groupb_preset)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.btn_savepreset = QtGui.QPushButton(self.groupb_preset)
        self.btn_savepreset.setEnabled(False)
        self.btn_savepreset.setObjectName("btn_savepreset")
        self.horizontalLayout_8.addWidget(self.btn_savepreset)
        self.btn_loadpreset = QtGui.QPushButton(self.groupb_preset)
        self.btn_loadpreset.setEnabled(False)
        self.btn_loadpreset.setObjectName("btn_loadpreset")
        self.horizontalLayout_8.addWidget(self.btn_loadpreset)
        self.layout_fileops.addWidget(self.groupb_preset)
        self.btn_export = QtGui.QPushButton(self.centralwidget)
        self.btn_export.setMinimumSize(QtCore.QSize(0, 49))
        self.btn_export.setObjectName("btn_export")
        self.layout_fileops.addWidget(self.btn_export)
        self.layout3in1.addLayout(self.layout_fileops)
        self.layout_280 = QtGui.QVBoxLayout()
        self.layout_280.setObjectName("layout_280")
        self.layout_gif280 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layout_gif280.sizePolicy().hasHeightForWidth())
        self.layout_gif280.setSizePolicy(sizePolicy)
        self.layout_gif280.setObjectName("layout_gif280")
        self.verticalLayout = QtGui.QVBoxLayout(self.layout_gif280)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gifplayer280 = QtGui.QLabel(self.layout_gif280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gifplayer280.sizePolicy().hasHeightForWidth())
        self.gifplayer280.setSizePolicy(sizePolicy)
        self.gifplayer280.setMinimumSize(QtCore.QSize(280, 280))
        self.gifplayer280.setAlignment(QtCore.Qt.AlignCenter)
        self.gifplayer280.setObjectName("gifplayer280")
        self.gridLayout.addWidget(self.gifplayer280, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.line = QtGui.QFrame(self.layout_gif280)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.layout_playback280 = QtGui.QHBoxLayout()
        self.layout_playback280.setObjectName("layout_playback280")
        self.btn_fb280 = QtGui.QPushButton(self.layout_gif280)
        self.btn_fb280.setEnabled(False)
        self.btn_fb280.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        self.btn_fb280.setFont(font)
        self.btn_fb280.setObjectName("btn_fb280")
        self.layout_playback280.addWidget(self.btn_fb280)
        self.btn_playpause280 = QtGui.QPushButton(self.layout_gif280)
        self.btn_playpause280.setEnabled(False)
        self.btn_playpause280.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        self.btn_playpause280.setFont(font)
        self.btn_playpause280.setCheckable(True)
        self.btn_playpause280.setObjectName("btn_playpause280")
        self.layout_playback280.addWidget(self.btn_playpause280)
        self.btn_ff280 = QtGui.QPushButton(self.layout_gif280)
        self.btn_ff280.setEnabled(False)
        self.btn_ff280.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        self.btn_ff280.setFont(font)
        self.btn_ff280.setObjectName("btn_ff280")
        self.layout_playback280.addWidget(self.btn_ff280)
        self.verticalLayout.addLayout(self.layout_playback280)
        self.layout_speed280 = QtGui.QHBoxLayout()
        self.layout_speed280.setContentsMargins(-1, 0, -1, -1)
        self.layout_speed280.setObjectName("layout_speed280")
        self.lbl_speed280 = QtGui.QLabel(self.layout_gif280)
        self.lbl_speed280.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_speed280.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_speed280.setAutoFillBackground(False)
        self.lbl_speed280.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_speed280.setObjectName("lbl_speed280")
        self.layout_speed280.addWidget(self.lbl_speed280)
        self.spin_speed280 = QtGui.QDoubleSpinBox(self.layout_gif280)
        self.spin_speed280.setWrapping(False)
        self.spin_speed280.setFrame(True)
        self.spin_speed280.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.spin_speed280.setMinimum(0.1)
        self.spin_speed280.setMaximum(4.0)
        self.spin_speed280.setSingleStep(0.01)
        self.spin_speed280.setProperty("value", 1.0)
        self.spin_speed280.setObjectName("spin_speed280")
        self.layout_speed280.addWidget(self.spin_speed280)
        self.slider_speed280 = QtGui.QSlider(self.layout_gif280)
        self.slider_speed280.setMinimum(10)
        self.slider_speed280.setMaximum(400)
        self.slider_speed280.setSingleStep(1)
        self.slider_speed280.setProperty("value", 100)
        self.slider_speed280.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed280.setInvertedAppearance(False)
        self.slider_speed280.setTickPosition(QtGui.QSlider.NoTicks)
        self.slider_speed280.setObjectName("slider_speed280")
        self.layout_speed280.addWidget(self.slider_speed280)
        self.verticalLayout.addLayout(self.layout_speed280)
        self.layout_scale280 = QtGui.QHBoxLayout()
        self.layout_scale280.setObjectName("layout_scale280")
        self.lbl_scale280 = QtGui.QLabel(self.layout_gif280)
        self.lbl_scale280.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_scale280.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_scale280.setAutoFillBackground(False)
        self.lbl_scale280.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_scale280.setObjectName("lbl_scale280")
        self.layout_scale280.addWidget(self.lbl_scale280)
        self.spin_scale280 = QtGui.QSpinBox(self.layout_gif280)
        self.spin_scale280.setMinimumSize(QtCore.QSize(45, 0))
        self.spin_scale280.setMinimum(1)
        self.spin_scale280.setMaximum(7)
        self.spin_scale280.setObjectName("spin_scale280")
        self.layout_scale280.addWidget(self.spin_scale280)
        self.slider_scale280 = QtGui.QSlider(self.layout_gif280)
        self.slider_scale280.setMinimum(1)
        self.slider_scale280.setMaximum(7)
        self.slider_scale280.setOrientation(QtCore.Qt.Horizontal)
        self.slider_scale280.setObjectName("slider_scale280")
        self.layout_scale280.addWidget(self.slider_scale280)
        self.verticalLayout.addLayout(self.layout_scale280)
        self.layout_quality280 = QtGui.QHBoxLayout()
        self.layout_quality280.setObjectName("layout_quality280")
        self.lbl_quality280 = QtGui.QLabel(self.layout_gif280)
        self.lbl_quality280.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_quality280.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbl_quality280.setFrameShadow(QtGui.QFrame.Plain)
        self.lbl_quality280.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_quality280.setObjectName("lbl_quality280")
        self.layout_quality280.addWidget(self.lbl_quality280)
        self.spin_quality280 = QtGui.QSpinBox(self.layout_gif280)
        self.spin_quality280.setMaximum(1024)
        self.spin_quality280.setObjectName("spin_quality280")
        self.layout_quality280.addWidget(self.spin_quality280)
        self.slider_quality280 = QtGui.QSlider(self.layout_gif280)
        self.slider_quality280.setMaximum(400)
        self.slider_quality280.setPageStep(20)
        self.slider_quality280.setOrientation(QtCore.Qt.Horizontal)
        self.slider_quality280.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_quality280.setTickInterval(20)
        self.slider_quality280.setObjectName("slider_quality280")
        self.layout_quality280.addWidget(self.slider_quality280)
        self.verticalLayout.addLayout(self.layout_quality280)
        self.layout_preview280 = QtGui.QVBoxLayout()
        self.layout_preview280.setObjectName("layout_preview280")
        self.btn_update280 = QtGui.QPushButton(self.layout_gif280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_update280.sizePolicy().hasHeightForWidth())
        self.btn_update280.setSizePolicy(sizePolicy)
        self.btn_update280.setObjectName("btn_update280")
        self.layout_preview280.addWidget(self.btn_update280)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.check_livepreview280 = QtGui.QCheckBox(self.layout_gif280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_livepreview280.sizePolicy().hasHeightForWidth())
        self.check_livepreview280.setSizePolicy(sizePolicy)
        self.check_livepreview280.setObjectName("check_livepreview280")
        self.horizontalLayout_3.addWidget(self.check_livepreview280)
        self.check_endless_lossy280 = QtGui.QCheckBox(self.layout_gif280)
        self.check_endless_lossy280.setObjectName("check_endless_lossy280")
        self.horizontalLayout_3.addWidget(self.check_endless_lossy280)
        self.layout_preview280.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.layout_preview280)
        self.layout_280.addWidget(self.layout_gif280)
        self.layout3in1.addLayout(self.layout_280)
        self.layout_136 = QtGui.QVBoxLayout()
        self.layout_136.setObjectName("layout_136")
        self.layout_colortable = QtGui.QGroupBox(self.centralwidget)
        self.layout_colortable.setObjectName("layout_colortable")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layout_colortable)
        self.horizontalLayout.setContentsMargins(-1, 4, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_136.addWidget(self.layout_colortable)
        self.layout_gif136 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layout_gif136.sizePolicy().hasHeightForWidth())
        self.layout_gif136.setSizePolicy(sizePolicy)
        self.layout_gif136.setObjectName("layout_gif136")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layout_gif136)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gifplayer136 = QtGui.QLabel(self.layout_gif136)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gifplayer136.sizePolicy().hasHeightForWidth())
        self.gifplayer136.setSizePolicy(sizePolicy)
        self.gifplayer136.setMinimumSize(QtCore.QSize(136, 136))
        self.gifplayer136.setAlignment(QtCore.Qt.AlignCenter)
        self.gifplayer136.setObjectName("gifplayer136")
        self.gridLayout_3.addWidget(self.gifplayer136, 0, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.line_2 = QtGui.QFrame(self.layout_gif136)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.layout_playback136 = QtGui.QHBoxLayout()
        self.layout_playback136.setObjectName("layout_playback136")
        self.btn_fb136 = QtGui.QPushButton(self.layout_gif136)
        self.btn_fb136.setEnabled(False)
        self.btn_fb136.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        self.btn_fb136.setFont(font)
        self.btn_fb136.setObjectName("btn_fb136")
        self.layout_playback136.addWidget(self.btn_fb136)
        self.btn_playpause136 = QtGui.QPushButton(self.layout_gif136)
        self.btn_playpause136.setEnabled(False)
        self.btn_playpause136.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        font.setPointSize(8)
        font.setItalic(False)
        font.setUnderline(False)
        self.btn_playpause136.setFont(font)
        self.btn_playpause136.setCheckable(True)
        self.btn_playpause136.setFlat(False)
        self.btn_playpause136.setObjectName("btn_playpause136")
        self.layout_playback136.addWidget(self.btn_playpause136)
        self.btn_ff136 = QtGui.QPushButton(self.layout_gif136)
        self.btn_ff136.setEnabled(False)
        self.btn_ff136.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        self.btn_ff136.setFont(font)
        self.btn_ff136.setObjectName("btn_ff136")
        self.layout_playback136.addWidget(self.btn_ff136)
        self.verticalLayout_3.addLayout(self.layout_playback136)
        self.layout_speed136 = QtGui.QHBoxLayout()
        self.layout_speed136.setContentsMargins(-1, 0, -1, -1)
        self.layout_speed136.setObjectName("layout_speed136")
        self.lbl_speed136 = QtGui.QLabel(self.layout_gif136)
        self.lbl_speed136.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_speed136.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_speed136.setObjectName("lbl_speed136")
        self.layout_speed136.addWidget(self.lbl_speed136)
        self.spin_speed136 = QtGui.QDoubleSpinBox(self.layout_gif136)
        self.spin_speed136.setMinimum(0.1)
        self.spin_speed136.setMaximum(4.0)
        self.spin_speed136.setSingleStep(0.01)
        self.spin_speed136.setProperty("value", 1.0)
        self.spin_speed136.setObjectName("spin_speed136")
        self.layout_speed136.addWidget(self.spin_speed136)
        self.slider_speed136 = QtGui.QSlider(self.layout_gif136)
        self.slider_speed136.setEnabled(True)
        self.slider_speed136.setMinimum(10)
        self.slider_speed136.setMaximum(400)
        self.slider_speed136.setProperty("value", 100)
        self.slider_speed136.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed136.setObjectName("slider_speed136")
        self.layout_speed136.addWidget(self.slider_speed136)
        self.verticalLayout_3.addLayout(self.layout_speed136)
        self.layout_scale136 = QtGui.QHBoxLayout()
        self.layout_scale136.setObjectName("layout_scale136")
        self.lbl_scale136 = QtGui.QLabel(self.layout_gif136)
        self.lbl_scale136.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_scale136.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_scale136.setObjectName("lbl_scale136")
        self.layout_scale136.addWidget(self.lbl_scale136)
        self.spin_scale136 = QtGui.QSpinBox(self.layout_gif136)
        self.spin_scale136.setMinimumSize(QtCore.QSize(45, 0))
        self.spin_scale136.setMinimum(1)
        self.spin_scale136.setMaximum(7)
        self.spin_scale136.setObjectName("spin_scale136")
        self.layout_scale136.addWidget(self.spin_scale136)
        self.slider_scale136 = QtGui.QSlider(self.layout_gif136)
        self.slider_scale136.setMinimum(1)
        self.slider_scale136.setMaximum(7)
        self.slider_scale136.setProperty("value", 1)
        self.slider_scale136.setOrientation(QtCore.Qt.Horizontal)
        self.slider_scale136.setObjectName("slider_scale136")
        self.layout_scale136.addWidget(self.slider_scale136)
        self.verticalLayout_3.addLayout(self.layout_scale136)
        self.layout_quality136 = QtGui.QHBoxLayout()
        self.layout_quality136.setObjectName("layout_quality136")
        self.lbl_quality136 = QtGui.QLabel(self.layout_gif136)
        self.lbl_quality136.setMinimumSize(QtCore.QSize(40, 0))
        self.lbl_quality136.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_quality136.setObjectName("lbl_quality136")
        self.layout_quality136.addWidget(self.lbl_quality136)
        self.spin_quality136 = QtGui.QSpinBox(self.layout_gif136)
        self.spin_quality136.setMaximum(1024)
        self.spin_quality136.setObjectName("spin_quality136")
        self.layout_quality136.addWidget(self.spin_quality136)
        self.slider_quality136 = QtGui.QSlider(self.layout_gif136)
        self.slider_quality136.setMaximum(400)
        self.slider_quality136.setPageStep(20)
        self.slider_quality136.setOrientation(QtCore.Qt.Horizontal)
        self.slider_quality136.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_quality136.setTickInterval(20)
        self.slider_quality136.setObjectName("slider_quality136")
        self.layout_quality136.addWidget(self.slider_quality136)
        self.verticalLayout_3.addLayout(self.layout_quality136)
        self.layout_preview136 = QtGui.QVBoxLayout()
        self.layout_preview136.setObjectName("layout_preview136")
        self.btn_update136 = QtGui.QPushButton(self.layout_gif136)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_update136.sizePolicy().hasHeightForWidth())
        self.btn_update136.setSizePolicy(sizePolicy)
        self.btn_update136.setObjectName("btn_update136")
        self.layout_preview136.addWidget(self.btn_update136)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.check_livepreview136 = QtGui.QCheckBox(self.layout_gif136)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_livepreview136.sizePolicy().hasHeightForWidth())
        self.check_livepreview136.setSizePolicy(sizePolicy)
        self.check_livepreview136.setObjectName("check_livepreview136")
        self.horizontalLayout_2.addWidget(self.check_livepreview136)
        self.check_endless_lossy136 = QtGui.QCheckBox(self.layout_gif136)
        self.check_endless_lossy136.setObjectName("check_endless_lossy136")
        self.horizontalLayout_2.addWidget(self.check_endless_lossy136)
        self.layout_preview136.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.layout_preview136)
        self.layout_136.addWidget(self.layout_gif136)
        self.layout3in1.addLayout(self.layout_136)
        self.verticalLayout_2.addLayout(self.layout3in1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 926, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionConfig = QtGui.QAction(MainWindow)
        self.actionConfig.setObjectName("actionConfig")
        self.actionDelete_temp_files = QtGui.QAction(MainWindow)
        self.actionDelete_temp_files.setObjectName("actionDelete_temp_files")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuOptions.addAction(self.actionConfig)
        self.menuOptions.addAction(self.actionDelete_temp_files)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.spin_scale280, QtCore.SIGNAL("valueChanged(int)"), self.slider_scale280.setValue)
        QtCore.QObject.connect(self.spin_quality280, QtCore.SIGNAL("valueChanged(int)"), self.slider_quality280.setValue)
        QtCore.QObject.connect(self.slider_scale280, QtCore.SIGNAL("valueChanged(int)"), self.spin_scale280.setValue)
        QtCore.QObject.connect(self.spin_quality136, QtCore.SIGNAL("valueChanged(int)"), self.slider_quality136.setValue)
        QtCore.QObject.connect(self.spin_scale136, QtCore.SIGNAL("valueChanged(int)"), self.slider_scale136.setValue)
        QtCore.QObject.connect(self.slider_scale136, QtCore.SIGNAL("valueChanged(int)"), self.spin_scale136.setValue)
        QtCore.QObject.connect(self.slider_quality136, QtCore.SIGNAL("valueChanged(int)"), self.spin_quality136.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_top1.setText(QtGui.QApplication.translate("MainWindow", "Convert AVI > GIF", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_top2.setText(QtGui.QApplication.translate("MainWindow", "W.I.P.", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_top3.setText(QtGui.QApplication.translate("MainWindow", "W.I.P.", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_top4.setText(QtGui.QApplication.translate("MainWindow", "W.I.P.", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_input_folder.setText(QtGui.QApplication.translate("MainWindow", "Select project folder", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_videos), QtGui.QApplication.translate("MainWindow", "Videos available", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_gifs), QtGui.QApplication.translate("MainWindow", "Gifs available", None, QtGui.QApplication.UnicodeUTF8))
        self.groupb_colortable.setTitle(QtGui.QApplication.translate("MainWindow", "Color table (.act file)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupb_preset.setTitle(QtGui.QApplication.translate("MainWindow", "Preset", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_savepreset.setText(QtGui.QApplication.translate("MainWindow", "W.I.P.", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_loadpreset.setText(QtGui.QApplication.translate("MainWindow", "W.I.P.", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export.setText(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.layout_gif280.setTitle(QtGui.QApplication.translate("MainWindow", "280x280 px", None, QtGui.QApplication.UnicodeUTF8))
        self.gifplayer280.setText(QtGui.QApplication.translate("MainWindow", "280 px picture", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_fb280.setText(QtGui.QApplication.translate("MainWindow", "", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_playpause280.setText(QtGui.QApplication.translate("MainWindow", "⏵/⏸", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ff280.setText(QtGui.QApplication.translate("MainWindow", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_speed280.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_scale280.setText(QtGui.QApplication.translate("MainWindow", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_quality280.setText(QtGui.QApplication.translate("MainWindow", "Lossy", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_update280.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.check_livepreview280.setText(QtGui.QApplication.translate("MainWindow", "Auto update", None, QtGui.QApplication.UnicodeUTF8))
        self.check_endless_lossy280.setText(QtGui.QApplication.translate("MainWindow", "Additive madness", None, QtGui.QApplication.UnicodeUTF8))
        self.layout_colortable.setTitle(QtGui.QApplication.translate("MainWindow", "Color table", None, QtGui.QApplication.UnicodeUTF8))
        self.layout_gif136.setTitle(QtGui.QApplication.translate("MainWindow", "136x136 px", None, QtGui.QApplication.UnicodeUTF8))
        self.gifplayer136.setText(QtGui.QApplication.translate("MainWindow", "136 px picture", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_fb136.setText(QtGui.QApplication.translate("MainWindow", "", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_playpause136.setText(QtGui.QApplication.translate("MainWindow", "⏵/⏸", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ff136.setText(QtGui.QApplication.translate("MainWindow", "", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_speed136.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_scale136.setText(QtGui.QApplication.translate("MainWindow", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_quality136.setText(QtGui.QApplication.translate("MainWindow", "Lossy", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_update136.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.check_livepreview136.setText(QtGui.QApplication.translate("MainWindow", "Auto update", None, QtGui.QApplication.UnicodeUTF8))
        self.check_endless_lossy136.setText(QtGui.QApplication.translate("MainWindow", "Additive madness", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("MainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfig.setText(QtGui.QApplication.translate("MainWindow", "C&onfig", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_temp_files.setText(QtGui.QApplication.translate("MainWindow", "&Clean temp files", None, QtGui.QApplication.UnicodeUTF8))

