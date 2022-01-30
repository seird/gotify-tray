from PyQt6 import QtGui, QtWidgets
from gotify_tray.__version__ import __title__


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super(Tray, self).__init__()

        self.set_icon_error()
        self.setToolTip(__title__)

        # Tray menu items
        menu = QtWidgets.QMenu()

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
        self.setIcon(QtGui.QIcon("gotify_tray/gui/images/gotify-small.png"))

    def set_icon_error(self):
        self.setIcon(QtGui.QIcon("gotify_tray/gui/images/gotify-small-error.png"))
