from typing import Optional, Union
from PyQt6 import QtCore, QtGui
from gotify_tray import gotify


class ApplicationModelItem(QtGui.QStandardItem):
    def __init__(
        self,
        application: gotify.GotifyApplicationModel,
        icon: Optional[QtGui.QIcon] = None,
        *args,
        **kwargs
    ):
        super(ApplicationModelItem, self).__init__(application.name)
        self.application = application
        if icon:
            self.setIcon(icon)


class ApplicationAllMessagesItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super(ApplicationAllMessagesItem, self).__init__("ALL MESSAGES")


class ApplicationModel(QtGui.QStandardItemModel):
    def setItem(self, row: int, column: int, item: Union[ApplicationModelItem, ApplicationAllMessagesItem]) -> None:
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
            if item.application.id == appid:
                return item
        return None
