# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python\Vault_Of_Gifs\widgets\palette_editor.ui'
#
# Created: Sat Feb 10 06:02:29 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_palette_editor(object):
    def setupUi(self, palette_editor):
        palette_editor.setObjectName("palette_editor")
        palette_editor.resize(647, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(palette_editor)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gv_palette_editor = QtGui.QGraphicsView(palette_editor)
        self.gv_palette_editor.setObjectName("gv_palette_editor")
        self.horizontalLayout.addWidget(self.gv_palette_editor)

        self.retranslateUi(palette_editor)
        QtCore.QMetaObject.connectSlotsByName(palette_editor)

    def retranslateUi(self, palette_editor):
        palette_editor.setWindowTitle(QtGui.QApplication.translate("palette_editor", "Palette editor", None, QtGui.QApplication.UnicodeUTF8))

