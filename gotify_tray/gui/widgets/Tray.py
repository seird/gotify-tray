import logging

from PyQt6 import QtGui, QtWidgets
from gotify_tray.__version__ import __title__
from gotify_tray.utils import get_icon


logger = logging.getLogger("gotify-tray")


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super(Tray, self).__init__()

        if not self.isSystemTrayAvailable():
            logger.warning("系统托盘不可用")
        if not self.supportsMessages():
            logger.warning("系统不支持通知")

        self.set_icon_error()
        self.setToolTip(__title__)

        # Tray menu items
        menu = QtWidgets.QMenu()

        self.actionShowWindow = QtGui.QAction("显示窗口", self)
        menu.addAction(self.actionShowWindow)

        menu.addSeparator()

        self.actionSettings = QtGui.QAction("设置", self)
        menu.addAction(self.actionSettings)

        menu.addSeparator()

        self.actionReconnect = QtGui.QAction("重新连接", self)
        menu.addAction(self.actionReconnect)

        menu.addSeparator()

        self.actionQuit = QtGui.QAction("退出", self)
        menu.addAction(self.actionQuit)

        self.setContextMenu(menu)

    def set_icon_ok(self):
        self.icon_error = False
        self.setIcon(QtGui.QIcon(get_icon("tray")))

    def set_icon_error(self):
        self.icon_error = True
        self.setIcon(QtGui.QIcon(get_icon("tray-error")))

    def set_icon_unread(self):
        self.setIcon(QtGui.QIcon(get_icon("tray-unread")))

    def revert_icon(self):
        if self.icon_error:
            self.set_icon_error()
        else:
            self.set_icon_ok()
