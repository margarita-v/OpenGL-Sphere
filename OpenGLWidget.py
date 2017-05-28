# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtWidgets import QOpenGLWidget
from Vertex import Vertex

import numpy as np

MINIMUM_SIZE = QSize(200, 200)
SIZE = QSize(400, 400)

FIRST_LIGHT_POSITION  = [1, 1, 0, 0]
SECOND_LIGHT_POSITION = [-1, -1, 0, 0]

class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent, radius, quality):
        QOpenGLWidget.__init__(self, parent)
        self.__radius = radius
        self.__quality = quality
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
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, SECOND_LIGHT_POSITION)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10.0);
        glRotatef(self.__xRotation / 16, 1.0, 0.0, 0.0);
        glRotatef(self.__yRotation / 16, 0.0, 1.0, 0.0);
        glRotatef(self.__zRotation / 16, 0.0, 0.0, 1.0);
        self.draw()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-4, 4, -4, 4, 1.0, 16.0)
        glMatrixMode(GL_MODELVIEW)


    def mousePressEvent(self, _event):
        self.__lastPoint = _event.pos()

    def mouseMoveEvent(self, _event):
        dx = _event.x() - self.__lastPoint.x()
        dy = _event.y() - self.__lastPoint.y()
        if _event.buttons() & Qt.LeftButton or _event.buttons & Qt.RightButton:
            self.set_xRotation(self.__xRotation + 8*dy)
            self.set_yRotation(self.__yRotation + 8*dx)

    def set_quality(self, quality):
        self.__quality = quality
        self.update()

    def set_radius(self, radius):
        self.__radius = radius
        self.update()
    
    def normalize_angle(self, angle):
        while angle < 0:
            angle += 360*16
        while angle > 360:
            angle -= 360*16

    def set_xRotation(self, angle):
        self.normalize_angle(angle)
        if angle != self.__xRotation:
            self.__xRotation = angle
            self.update()
    
    def set_yRotation(self, angle):
        self.normalize_angle(angle)
        if angle != self.__yRotation:
            self.__yRotation = angle
            self.update()
    
    def set_zRotation(self, angle):
        self.normalize_angle(angle)
        if angle != self.__zRotation:
            self.__zRotation = angle
            self.update()

    def draw(self):
        multiplier = 1 / self.__quality
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUAD_STRIP)
        for y_index in range(self.__quality):
            piy = np.pi * multiplier
            ay = y_index * piy
            sy = np.sin(ay)
            cy = np.cos(ay)
            ty = y_index * multiplier
            ay1 = ay + piy
            sy1 = np.sin(ay1)
            cy1 = np.cos(ay1)
            ty1 = ty + multiplier
            for x_index in range(self.__quality):
                pix = np.pi * multiplier
                ax = 2.0 * x_index * pix
                sx = np.sin(ax)
                cx = np.cos(ax)
                x = self.__radius * sy * cx
                y = self.__radius * sy * sx
                z = self.__radius * cy
                tx = x_index * multiplier
                glNormal3f(x, y, z)
                glTexCoord2f(tx, ty)
                glVertex3f(x, y, z)
                x = self.__radius * sy1 * cx
                y = self.__radius * sy1 * sx
                z = self.__radius * cy1
                glNormal3f(x, y, z)
                glTexCoord2f(tx, ty1)
                glVertex3f(x, y, z)
        glEnd()
        glFlush()
