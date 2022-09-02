import os

from PyQt6 import QtCore, QtGui, QtWidgets

from ..models.MessagesModel import MessageItemDataRole, MessagesModelItem
from ..designs.widget_message import Ui_Form
from gotify_tray.database import Settings
from gotify_tray.utils import convert_links, get_abs_path


settings = Settings("gotify-tray")


class MessageWidget(QtWidgets.QWidget, Ui_Form):
    deletion_requested = QtCore.pyqtSignal(MessagesModelItem)
    image_popup = QtCore.pyqtSignal(str, QtCore.QPoint)

    def __init__(self, message_item: MessagesModelItem, image_path: str = ""):
        super(MessageWidget, self).__init__()
        self.setupUi(self)
        self.setAutoFillBackground(True)

        self.message_item = message_item
        message = message_item.data(MessageItemDataRole.MessageRole)

        # Fonts
        self.set_fonts()

        # Display message contents
        self.label_title.setText(message.title)
        self.label_date.setText(message.date.strftime("%Y-%m-%d, %H:%M"))

        if (
            markdown := message.get("extras", {})
            .get("client::display", {})
            .get("contentType")
        ) == "text/markdown":
            self.label_message.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)

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
        self.gridLayout_frame.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setContentsMargins(4, 5, 4, 0)
        self.adjustSize()
        size_hint = self.message_item.sizeHint()
        self.message_item.setSizeHint(QtCore.QSize(size_hint.width(), self.height()))

        self.pb_delete.setIcon(
            QtGui.QIcon(get_abs_path("gotify_tray/gui/images/trashcan.svg"))
        )
        self.pb_delete.setIconSize(QtCore.QSize(24, 24))

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
