#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Imgreveal 
    ~~~~~~~~~~~~~~

    A simple PySlide based GUI application for overlaying two
    images ontop of each other and selectively displaying a 
    percentage of the top image at a time.  

    Usefull for doing before and after comparisons

    :copyright: (c) Copyright 2013 by Bob
    :license: BSD, see LICENSE for more details.
"""


import sys
import os
import argparse

from PySide import QtGui, QtCore

class ImgReveal(QtGui.QWidget):

    def __init__(self, bottom_image_path, top_image_path):
        super(ImgReveal, self).__init__()

        self.setWindowTitle("ImgReveal")

        self.mouse_down = False
        self.width_mode = True

        bottom_image = QtGui.QPixmap(bottom_image_path)
        self.bottom_image = bottom_image
        top_image = QtGui.QPixmap(top_image_path)

        x,y,w,h = 0,0, bottom_image.size().width(), \
                        bottom_image.size().height() 
        self.setGeometry(x, y, w, h)

        self.bottom_image_label = QtGui.QLabel('', self)
        self.bottom_image_label.setPixmap(bottom_image)
        
        self.top_image_label = QtGui.QLabel('', self)
        self.top_image_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.top_image_label.setPixmap(top_image)
        self.top_image_label.setFixedWidth(bottom_image.size().width()/2.0)

    def mousePressEvent(self, evt):
        if evt.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse_down = True
            if self.width_mode:
                self.top_image_label.setFixedWidth(evt.pos().x())
            else:
                self.top_image_label.setFixedHeight(evt.pos().y())
        elif evt.button() == QtCore.Qt.MouseButton.RightButton:
            self.width_mode = not self.width_mode

            if self.width_mode:
                self.top_image_label.setFixedWidth(self.bottom_image.size().width()/2.0)
                self.top_image_label.setFixedHeight(self.bottom_image.size().height())
            else:
                self.top_image_label.setFixedWidth(self.bottom_image.size().width())
                self.top_image_label.setFixedHeight(self.bottom_image.size().height()/2.0)


    def mouseMoveEvent(self, evt):
        if self.mouse_down:
            if self.width_mode:
                self.top_image_label.setFixedWidth(evt.pos().x())
            else:
                self.top_image_label.setFixedHeight(evt.pos().y())

    def mouseReleaseEvent(self, evt):
        if evt.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse_down = False 



    def show_and_raise(self):
        self.show()
        self.raise_()


def parse_args(argv=sys.argv[1:]):
    description = """
    Display one image ontop of another with the ability to reveal part of the 
    image below for comparison puroposes
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('files', metavar='image_path', nargs=2,
                     help='image files to be displayed')

    return parser.parse_args(argv)

if __name__ == "__main__":

    arguments = parse_args()

    files = arguments.files

    for file in files:
        if not os.path.exists(file):
            print("File %s does not exist" % (file,))
            sys.exit(1)

    app = QtGui.QApplication(sys.argv)

    imgReveal = ImgReveal(files[0], files[1])
    imgReveal.show_and_raise()

    sys.exit(app.exec_())




