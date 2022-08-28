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

        self.setWindowFlags(QtCore.Qt.WindowType.ToolTip)
        self.installEventFilter(self)

        pixmap = QtGui.QPixmap(filename).scaled(
                settings.value("ImagePopup/w", type=int),
                settings.value("ImagePopup/h", type=int),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            )
        self.setPixmap(pixmap)
        
        self.move(pos - QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        self.show()

    def eventFilter(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Type.Leave:
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
