import logging

from PyQt6 import QtGui, QtWidgets
from gotify_tray.__version__ import __title__
from gotify_tray.utils import get_icon


logger = logging.getLogger("gotify-tray")


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super(Tray, self).__init__()

        if not self.isSystemTrayAvailable():
            logger.warning("System tray is not available.")
        if not self.supportsMessages():
            logger.warning("System does not support notifications.")

        self.set_icon_error()
        self.setToolTip(__title__)

        # Tray menu items
        menu = QtWidgets.QMenu()

        self.actionShowWindow = QtGui.QAction("Show Window", self)
        menu.addAction(self.actionShowWindow)

        menu.addSeparator()

        self.actionSettings = QtGui.QAction("Settings", self)
        menu.addAction(self.actionSettings)

        menu.addSeparator()

        self.actionReconnect = QtGui.QAction("Reconnect", self)
        menu.addAction(self.actionReconnect)

        menu.addSeparator()

        self.actionQuit = QtGui.QAction("Quit", self)
        menu.addAction(self.actionQuit)

        self.setContextMenu(menu)

    def set_icon_ok(self):
        self.setIcon(QtGui.QIcon(get_icon("tray")))

    def set_icon_error(self):
        self.setIcon(QtGui.QIcon(get_icon("tray-error")))
