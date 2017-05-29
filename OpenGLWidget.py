# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtWidgets import QOpenGLWidget
from math import pi, sin, cos

# размеры окна
MINIMUM_SIZE = QSize(200, 200)
SIZE = QSize(400, 400)

# позиции источников света
FIRST_LIGHT_POSITION  = [1, 1, 1, 0]
SECOND_LIGHT_POSITION = [1, 1, 0, 0]

# скорость вращения фигуры
ROTATION_SPEED = 4
# удаленность фигуры при параллельной проекции
DISTANCE = 4

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
        glShadeModel(GL_FLAT)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, FIRST_LIGHT_POSITION)
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, SECOND_LIGHT_POSITION)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10.0)
        glRotatef(self.__xRotation / ROTATION_SPEED, 1.0, 0.0, 0.0)
        glRotatef(self.__yRotation / ROTATION_SPEED, 0.0, 1.0, 0.0)
        glRotatef(self.__zRotation / ROTATION_SPEED, 0.0, 0.0, 1.0)
        self.draw()

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / height
        glViewport(0, 0, width, height)
        if aspect > 1:
            glOrtho(-DISTANCE * aspect, DISTANCE * aspect, -DISTANCE, DISTANCE, 1, 16)
        else:
            glOrtho(-DISTANCE, DISTANCE, -DISTANCE / aspect, DISTANCE / aspect, 1, 16)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, _event):
        self.__lastPoint = _event.pos()

    def mouseMoveEvent(self, _event):
        dx = _event.x() - self.__lastPoint.x()
        dy = _event.y() - self.__lastPoint.y()
        if _event.buttons() & Qt.LeftButton or _event.buttons & Qt.RightButton:
            self.set_xRotation(self.__xRotation + dy)
            self.set_yRotation(self.__yRotation + dx)

    def set_quality(self, quality):
        self.__quality = quality
        self.update()

    def set_radius(self, radius):
        self.__radius = radius
        self.update()
    
    def normalize_angle(self, angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360

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
        radius = self.__radius
        quality = self.__quality
        y_multiplier = pi / quality
        x_multiplier = 2.0 * y_multiplier
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUAD_STRIP)
        for y_index in range(quality):
            # theta is the latitude, ranging from 0 to pi
            theta = y_index * y_multiplier
            tex_Y = y_index / quality
            for x_index in range(quality):
                # phi is the longitude, ranging from 0 to 2*pi
                phi = x_index * x_multiplier
                tex_X = x_index / quality
                x = radius * sin(theta) * cos(phi)
                y = radius * sin(theta) * sin(phi)
                z = radius * cos(theta)
                glNormal3f(x, y, z)
                glTexCoord2f(tex_X, tex_Y)
                glVertex3f(x, y, z)
                theta_new = theta + y_multiplier
                x = radius * sin(theta_new) * cos(phi)
                y = radius * sin(theta_new) * sin(phi)
                z = radius * cos(theta_new)
                glNormal3f(x, y, z)
                glTexCoord2f(tex_X, tex_Y + 1 / self.__quality)
                glVertex3f(x, y, z)
        glEnd()
        glFlush()
