# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from OpenGLWidget import OpenGLWidget

import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("mainwindow.ui", self)
        self.openGLWidget = OpenGLWidget(self, 
                self.dsbRadius.value(), self.hsQuality.value())
        self.horizontalLayout.addWidget(self.openGLWidget)

        self.dsbRadius.valueChanged.connect(self.radiusChanged)
        self.hsQuality.sliderMoved.connect(self.qualityChanged)
        self.show()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            result = QMessageBox.question(self, "Подтверждение выхода", 
                    "Вы действительно хотите выйти?")
            if result == QMessageBox.Yes:
                self.close()

    def radiusChanged(self):
        self.openGLWidget.set_radius(self.dsbRadius.value())

    def qualityChanged(self):
        self.openGLWidget.set_quality(self.hsQuality.value())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
