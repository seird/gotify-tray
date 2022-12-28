import os

from PyQt6 import QtCore, QtGui, QtWidgets

from ..models.MessagesModel import MessageItemDataRole, MessagesModelItem
from ..designs.widget_message import Ui_Form
from gotify_tray.database import Downloader
from gotify_tray.database import Settings
from gotify_tray.utils import convert_links, get_image
from gotify_tray.gui.themes import get_theme_file
from gotify_tray.gotify.models import GotifyMessageModel


settings = Settings("gotify-tray")


class MessageWidget(QtWidgets.QWidget, Ui_Form):
    deletion_requested = QtCore.pyqtSignal(MessagesModelItem)
    image_popup = QtCore.pyqtSignal(str, QtCore.QPoint)

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        message_item: MessagesModelItem,
        image_path: str = "",
    ):
        super(MessageWidget, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.message_item = message_item
        message: GotifyMessageModel = message_item.data(MessageItemDataRole.MessageRole)

        # Fonts
        self.set_fonts()

        # Display the message priority as a color
        self.set_priority_color(message.priority)

        # Display message contents
        self.label_title.setText(message.title)
        self.label_date.setText(message.date.strftime("%Y-%m-%d, %H:%M"))

        if markdown := (
            message.get("extras", {}).get("client::display", {}).get("contentType")
            == "text/markdown"
        ):
            self.label_message.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)

        # If the message is only an image URL, then instead of showing the message,
        # download the image and show it in the message label
        if image_url := get_image(message.message):
            downloader = Downloader()
            filename = downloader.get_filename(image_url)
            self.set_message_image(filename)
        else:
            self.label_message.setText(convert_links(message.message))

        # Show the application icon
        if image_path:
            image_size = settings.value("MessageWidget/image/size", type=int)
            self.label_image.setFixedSize(QtCore.QSize(image_size, image_size))
            pixmap = QtGui.QPixmap(image_path).scaled(
                image_size,
                image_size,
                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                transformMode=QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self.label_image.setPixmap(pixmap)
        else:
            self.label_image.hide()

        # Set MessagesModelItem's size hint based on the size of this widget
        self.gridLayout_frame.setContentsMargins(0, 0, 5, 0)
        self.gridLayout.setContentsMargins(4, 5, 4, 0)
        self.adjustSize()
        size_hint = self.message_item.sizeHint()
        self.message_item.setSizeHint(QtCore.QSize(size_hint.width(), self.height()))

        self.set_icons()

        self.link_callbacks()

    def set_fonts(self):
        font_title = QtGui.QFont()
        font_date = QtGui.QFont()
        font_content = QtGui.QFont()

        if s := settings.value("MessageWidget/font/title", type=str):
            font_title.fromString(s)
        else:
            font_title.setBold(True)

        if s := settings.value("MessageWidget/font/date", type=str):
            font_date.fromString(s)
        else:
            font_date.setItalic(True)

        if s := settings.value("MessageWidget/font/message", type=str):
            font_content.fromString(s)

        self.label_title.setFont(font_title)
        self.label_date.setFont(font_date)
        self.label_message.setFont(font_content)

    def set_icons(self):
        self.pb_delete.setIcon(QtGui.QIcon(get_theme_file("trashcan.svg")))
        self.pb_delete.setIconSize(QtCore.QSize(24, 24))

    def set_message_image(self, filename: str):
        pixmap = QtGui.QPixmap(filename)

        # Make sure the image fits within the listView
        W = settings.value("MessageWidget/content_image/W_percentage", type=float) * (
            self.parent.width() - self.label_image.width()
        )
        H = (
            settings.value("MessageWidget/content_image/H_percentage", type=float)
            * self.parent.height()
        )

        if pixmap.width() > W or pixmap.height() > H:
            pixmap = pixmap.scaled(
                QtCore.QSize(int(W), int(H)),
                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=QtCore.Qt.TransformationMode.SmoothTransformation,
            )

        self.label_message.setPixmap(pixmap)

    def set_priority_color(self, priority: int):
        if not settings.value("MessageWidget/priority_color", type=bool):
            self.label_priority.setFixedWidth(0) # set width to 0 instead of hiding, so we still get the content margins
            return

        if priority >= 4 and priority <= 7:
                self.label_priority.setStyleSheet("background-color: rgba(230, 126, 34, 0.7);")
        elif priority > 7:
            self.label_priority.setStyleSheet("background-color: #e74c3c;")

    def link_hovered_callback(self, link: str):
        if not settings.value("ImagePopup/enabled", type=bool):
            return

        qurl = QtCore.QUrl(link)
        _, ext = os.path.splitext(qurl.fileName())
        if ext in settings.value("ImagePopup/extensions", type=list):
            self.image_popup.emit(link, QtGui.QCursor.pos())

    def link_callbacks(self):
        self.pb_delete.clicked.connect(
            lambda: self.deletion_requested.emit(self.message_item)
        )
        self.label_message.linkHovered.connect(self.link_hovered_callback)
