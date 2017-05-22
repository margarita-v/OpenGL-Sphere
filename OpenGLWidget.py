# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtWidgets import QOpenGLWidget

MINIMUM_SIZE = QSize(50, 50)
SIZE = QSize(400, 400)

FIRST_LIGHT_POSITION  = [1, 1, 1, 0]
SECOND_LIGHT_POSITION = [0, 1, 0, 0]

class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.__radius = 1
        self.__xRotation = 0
        self.__yRotation = 0
        self.__zRotation = 0
        self.__lastPoint = QPoint()

    def sizeHint(self):
        return SIZE

    def minimumSizeHint(self):
        return MINIMUM_SIZE

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, FIRST_LIGHT_POSITION)
        glLightfv(GL_LIGHT0, GL_POSITION, SECOND_LIGHT_POSITION)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.draw()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2, 2, -2, 2, 1.0, 16.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, _event):
        self.__lastPoint = _event.pos()

    def mouseMoveEvent(self, _event):
        dx = _event.x() - self.__lastPoint.x()
        dy = _event.y() - self.__lastPoint.y()
        if _event.buttons() & LeftButton or _event.buttons & RightButton:
            self.set_xRotation(self.__xRotation + 8*dy)
            self.set_yRotation(self.__yRotation + 8*dx)

    def get_radius(self):
        return self.__radius

    def set_radius(self, radius):
        self.__radius = radius
        self.updateGL()
    
    def normalize_angle(self, angle):
        while angle < 0:
            angle += 360*16
        while angle > 360:
            angle -= 360*16

    def set_xRotation(self, angle):
        normalize_angle(angle)
        if angle != self.__xRotation:
            self.__xRotation = angle
            self.updateGL()
    
    def set_yRotation(self, angle):
        normalize_angle(angle)
        if angle != self.__yRotation:
            self.__yRotation = angle
            self.updateGL()
    
    def set_zRotation(self, angle):
        normalize_angle(angle)
        if angle != self.__zRotation:
            self.__zRotation = angle
            self.updateGL()

    def draw(self):
        pass