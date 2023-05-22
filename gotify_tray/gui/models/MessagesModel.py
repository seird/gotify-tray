import enum

from typing import cast
from PyQt6 import QtCore, QtGui
from gotify_tray import gotify
from gotify_tray.database import Settings


settings = Settings("gotify-tray")


class MessageItemDataRole(enum.IntEnum):
    MessageRole = QtCore.Qt.ItemDataRole.UserRole + 1


class MessagesModelItem(QtGui.QStandardItem):
    def __init__(self, message: gotify.GotifyMessageModel, *args, **kwargs):
        super(MessagesModelItem, self).__init__()
        self.setData(message, MessageItemDataRole.MessageRole)


class MessagesModel(QtGui.QStandardItemModel):
    def update_last_id(self, i: int):
        if i > settings.value("message/last", type=int):
            settings.setValue("message/last", i)

    def insert_message(self, row: int, message: gotify.GotifyMessageModel):
        self.update_last_id(message.id)
        message_item = MessagesModelItem(message)
        self.insertRow(row, message_item)
    
    def append_message(self, message: gotify.GotifyMessageModel):
        self.update_last_id(message.id)
        message_item = MessagesModelItem(message)
        self.appendRow(message_item)

    def setItem(self, row: int, column: int, item: MessagesModelItem) -> None:
        super(MessagesModel, self).setItem(row, column, item)

    def itemFromIndex(self, index: QtCore.QModelIndex) -> MessagesModelItem:
        return cast(MessagesModelItem, super(MessagesModel, self).itemFromIndex(index))
