import re

from PyQt6 import QtCore, QtGui, QtWidgets

from .MessagesModel import MessageItemDataRole, MessagesModelItem
from .designs.widget_message import Ui_Form
from gotify_tray.database import Settings


settings = Settings("gotify-tray")


def convert_links(text):
    _link = re.compile(
        r'(?:(https://|http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)',
        re.I,
    )

    def replace(match):
        groups = match.groups()
        protocol = groups[0] or ""  # may be None
        www_lead = groups[1] or ""  # may be None
        return '<a href="http://{1}{2}" rel="nofollow">{0}{1}{2}</a>{3}{4}'.format(
            protocol, www_lead, *groups[2:]
        )

    return _link.sub(replace, text)


class MessageWidget(QtWidgets.QWidget, Ui_Form):
    deletion_requested = QtCore.pyqtSignal(MessagesModelItem)

    def __init__(self, message_item: MessagesModelItem, image_path: str = ""):
        super(MessageWidget, self).__init__()
        self.setupUi(self)
        self.setAutoFillBackground(True)

        self.message_item = message_item
        message = message_item.data(MessageItemDataRole.MessageRole)

        # Fonts
        font_title = QtGui.QFont()
        font_date = QtGui.QFont()
        font_content = QtGui.QFont()
        font_title.fromString(settings.value("MessageWidget/font/title", type=str))
        font_date.fromString(settings.value("MessageWidget/font/date", type=str))
        font_content.fromString(settings.value("MessageWidget/font/content", type=str))
        self.label_title.setFont(font_title)
        self.label_date.setFont(font_date)
        self.text_message.setFont(font_content)

        self.label_title.setText(message.title)
        self.label_date.setText(message.date.strftime("%Y-%m-%d, %H:%M"))

        if markdown := message.get("extras", {}).get("client::display", {}).get("contentType") == "text/markdown":
            self.text_message.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)
        self.text_message.setText(convert_links(message.message))

        if image_path:
            image_size = settings.value("MessageWidget/image/size", type=int)
            self.label_image.setFixedSize(QtCore.QSize(image_size, image_size))
            pixmap = QtGui.QPixmap(image_path).scaled(image_size, image_size, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.label_image.setPixmap(pixmap)
        else:
            self.label_image.hide()

        # Set MessagesModelItem's size hint based on the size of this widget
        self.gridLayout_frame.setContentsMargins(10, 5, 10, 5)
        self.gridLayout.setContentsMargins(5, 15, 5, 15)
        self.adjustSize()
        size_hint = self.message_item.sizeHint()
        self.message_item.setSizeHint(
            QtCore.QSize(
                size_hint.width(),
                self.height()
            )
        )
        self.pb_delete.setIcon(QtGui.QIcon("gotify_tray/gui/images/trashcan.svg"))
        self.pb_delete.setIconSize(QtCore.QSize(24, 24))

        self.link_callbacks()

    def link_callbacks(self):
        self.pb_delete.clicked.connect(lambda: self.deletion_requested.emit(self.message_item))
