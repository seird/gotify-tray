import platform
from PyQt6 import QtCore, QtGui, QtWidgets

from gotify_tray.database import Settings


settings = Settings("gotify-tray")


class ImagePopup(QtWidgets.QLabel):
    def __init__(self, filename: str, pos: QtCore.QPoint, link: str = None):
        """Create and show a pop-up image under the cursor

        Args:
            filename (str): The path to the image to display
            pos (QtCore.QPoint): The location at which the image should be displayed
            link (str, optional): The URL of the image. Defaults to None.
        """
        super(ImagePopup, self).__init__()
        self.link = link

        self.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.installEventFilter(self)

        # Prevent leaving the pop-up open when moving quickly out of the widget
        self.popup_timer = QtCore.QTimer()
        self.popup_timer.timeout.connect(self.check_mouse)

        pixmap = QtGui.QPixmap(filename)
        W = settings.value("ImagePopup/w", type=int)
        H = settings.value("ImagePopup/h", type=int)
        if pixmap.height() > H or pixmap.width() > W:
            pixmap = pixmap.scaled(
                W,
                H,
                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        self.setPixmap(pixmap)

        self.move(pos - QtCore.QPoint(15, 15))

        self.popup_timer.start(500)

    def check_mouse(self):
        if not self.underMouse():
            self.close()

    def close(self):
        self.popup_timer.stop()
        super(ImagePopup, self).close()

    def eventFilter(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if platform.system() != "Darwin" and event.type() == QtCore.QEvent.Type.Leave:
            # Close the pop-up on mouse leave
            self.close()
        elif (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.button() == QtCore.Qt.MouseButton.LeftButton
            and self.link
        ):
            # Open the image URL on left click
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.link))

        return super().eventFilter(object, event)
