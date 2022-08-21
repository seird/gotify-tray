import enum

from typing import Optional, Union
from PyQt6 import QtCore, QtGui
from gotify_tray import gotify
from gotify_tray.database import Settings


settings = Settings("gotify-tray")


class ApplicationItemDataRole(enum.IntEnum):
    ApplicationRole = QtCore.Qt.ItemDataRole.UserRole + 1
    IconRole = QtCore.Qt.ItemDataRole.UserRole + 2


class ApplicationModelItem(QtGui.QStandardItem):
    def __init__(
        self,
        application: gotify.GotifyApplicationModel,
        icon: Optional[QtGui.QIcon] = None,
        *args,
        **kwargs,
    ):
        super(ApplicationModelItem, self).__init__(application.name)
        self.setDropEnabled(False)
        self.setData(application, ApplicationItemDataRole.ApplicationRole)
        self.setData(icon, ApplicationItemDataRole.IconRole)

        if s := settings.value("ApplicationItem/font", type=str):
            font = QtGui.QFont()
            font.fromString(s)
            self.setFont(font)
        if icon:
            self.setIcon(icon)

    def clone(self):
        return ApplicationModelItem(
            self.data(ApplicationItemDataRole.ApplicationRole),
            self.data(ApplicationItemDataRole.IconRole),
        )


class ApplicationAllMessagesItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super(ApplicationAllMessagesItem, self).__init__("ALL MESSAGES")
        self.setDropEnabled(False)
        self.setDragEnabled(False)
        if s := settings.value("ApplicationItem/font", type=str):
            font = QtGui.QFont()
            font.fromString(s)
            self.setFont(font)


class ApplicationModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(ApplicationModel, self).__init__()
        self.setItemPrototype(
            ApplicationModelItem(gotify.GotifyApplicationModel({"name": ""}), None)
        )

    def setItem(
        self,
        row: int,
        column: int,
        item: Union[ApplicationModelItem, ApplicationAllMessagesItem],
    ) -> None:
        super(ApplicationModel, self).setItem(row, column, item)

    def itemFromIndex(
        self, index: QtCore.QModelIndex
    ) -> Union[ApplicationModelItem, ApplicationAllMessagesItem]:
        return super(ApplicationModel, self).itemFromIndex(index)

    def itemFromId(self, appid: int) -> Optional[ApplicationModelItem]:
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if not isinstance(item, ApplicationModelItem):
                continue
            if item.data(ApplicationItemDataRole.ApplicationRole).id == appid:
                return item
        return None
