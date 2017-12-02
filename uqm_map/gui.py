#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:
#
# UQM Starmap Viewer
# Copyright (C) 2009-2017 CJ Kucera
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from PyQt5 import QtWidgets, QtGui, QtCore

from uqm_map import app_version
from uqm_map.data import *

class Constants(object):
    """
    Just a convenience class to hold a bunch of constants for us.
    """

    # Initialize a bunch of Colors that we'll use
    c_background_out_of_scene = QtGui.QColor(200, 200, 200)

class CoordinateToolBar(QtWidgets.QToolBar):
    """
    Toolbar whose job it is to show the current mouse coordinates to the user
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFloatable(False)
        self.setMovable(False)

class ControlToolBar(QtWidgets.QToolBar):
    """
    Toolbar whose job it is to hold all the user-defineable filtering parameters
    (and show some other information to the user as well)
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFloatable(False)
        self.setMovable(False)

class MapScene(QtWidgets.QGraphicsScene):
    """
    Main scene which holds our map and does all the necessary graphics stuff.
    """

    def __init__(self, parent, mainwindow):

        super().__init__(parent)
        self.mainwindow = mainwindow
        self.systems = mainwindow.systems

        # Keep track of what's currently hovering in the scene
        self.hover_current = None

        # Keep track of whether we're currently dragging
        self.dragging = False
        self.dragged = False

        # Populate with all our starmap information
        self.populate()

    def mousePressEvent(self, event):
        """
        Handle a mouse press event
        """
        if self.hover_current:
            super().mousePressEvent(event)
        else:
            self.start_dragging()

    def mouseReleaseEvent(self, event):
        """
        Handle a mouse release event
        """
        if self.hover_current:
            super().mouseReleaseEvent(event)
        else:
            self.stop_dragging()

    def start_dragging(self):
        """
        Start dragging around the scene
        """
        self.dragging = True
        self.dragged = False
        self.parent().setCursor(QtCore.Qt.ClosedHandCursor)

    def stop_dragging(self):
        """
        Stop dragging the scene around
        """
        self.dragging = False
        self.parent().unsetCursor()
        if not self.dragged:
            # TODO: clear current selection
            pass
        self.dragged = False

    def mouseMoveEvent(self, event):
        """
        Mouse movement
        """
        if self.dragging:
            last = event.lastScreenPos()
            pos = event.screenPos()
            delta_x = last.x() - pos.x()
            delta_y = last.y() - pos.y()
            if delta_x != 0:
                self.dragged = True
                sb = self.parent().horizontalScrollBar()
                new_x = sb.value() + delta_x
                if new_x >= sb.minimum() and new_x <= sb.maximum():
                    sb.setValue(new_x)
            if delta_y != 0:
                self.dragged = True
                sb = self.parent().verticalScrollBar()
                new_y = sb.value() + delta_y
                if new_y >= sb.minimum() and new_y <= sb.maximum():
                    sb.setValue(new_y)
        else:
            super().mouseMoveEvent(event)

    def populate(self):
        """
        Populates ourselves with all the information stored in our Systems
        object.
        """

class MapArea(QtWidgets.QGraphicsView):
    """
    Class which holds the viewport into our scene.  Not much happens
    in this class.
    """

    def __init__(self, parent):
        
        super().__init__(parent)

        self.setRenderHints(QtGui.QPainter.Antialiasing)
        self.scene = MapScene(self, parent)
        self.setScene(self.scene)
        self.setBackgroundBrush(QtGui.QBrush(Constants.c_background_out_of_scene))
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

class GUI(QtWidgets.QMainWindow):
    """
    Main application window
    """

    def __init__(self, systems):
        super().__init__()

        self.systems = systems

        # First set up a scene attribute to prevent possible AttributeErrors
        self.scene = None

        # Create our coordinate-reporting toolbar
        self.toolbar_coord = CoordinateToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar_coord)

        # Create our command/filtering toolbar
        self.toolbar_control = ControlToolBar(self)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar_control)

        # Set up our main widgets
        self.maparea = MapArea(self)
        self.scene = self.maparea.scene
        self.setCentralWidget(self.maparea)

        # Set up our main attributes
        self.setMinimumSize(800, 800)
        self.resize(800, 800)
        self.setWindowTitle('Ur-Quan Masters / Star Control II Starmap Viewer')

        # Show ourselves
        self.show()

class Application(QtWidgets.QApplication):
    """
    Main application GUI class
    """

    def __init__(self, datafile):
        """
        Initialization
        """

        super().__init__([])
        systems = Systems.load_from_file(datafile)
        self.app = GUI(systems)
