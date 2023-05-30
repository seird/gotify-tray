from PyQt6 import QtCore, QtGui, QtWidgets

from gotify_tray.database import Settings
from gotify_tray.gui.themes import get_theme_file


settings = Settings("gotify-tray")


class StatusWidget(QtWidgets.QLabel):
    def __init__(self):
        super(StatusWidget, self).__init__()
        self.setFixedSize(QtCore.QSize(20, 20))
        self.setScaledContents(True)
        self.set_connecting()
        self.image = None

    def set_status(self, image: str):
        self.image = image
        self.setPixmap(QtGui.QPixmap(get_theme_file(image)))

    def set_active(self):
        self.setToolTip("Listening for new messages")
        self.set_status("status_active.svg")

    def set_connecting(self):
        self.setToolTip("Connecting...")
        self.set_status("status_connecting.svg")

    def set_inactive(self):
        self.setToolTip("Listener inactive")
        self.set_status("status_inactive.svg")

    def set_error(self):
        self.setToolTip("Listener error")
        self.set_status("status_error.svg")

    def refresh(self):
        # refresh on theme change
        if self.image:
            self.set_status(self.image)
