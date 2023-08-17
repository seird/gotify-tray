import enum

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
        icon: QtGui.QIcon | None = None,
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
        self.setItemPrototype(ApplicationModelItem(gotify.GotifyApplicationModel({"name": ""}), None))

    def setItem(
        self,
        row: int,
        column: int,
        item: ApplicationModelItem | ApplicationAllMessagesItem,
    ) -> None:
        super(ApplicationModel, self).setItem(row, column, item)

    def itemFromIndex(
        self, index: QtCore.QModelIndex
    ) -> ApplicationModelItem | ApplicationAllMessagesItem:
        return super(ApplicationModel, self).itemFromIndex(index)

    def itemFromId(self, appid: int) -> ApplicationModelItem | None:
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if not isinstance(item, ApplicationModelItem):
                continue
            if item.data(ApplicationItemDataRole.ApplicationRole).id == appid:
                return item
        return None


class ApplicationProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, application_model: ApplicationModel) -> None:
        super(ApplicationProxyModel, self).__init__()
        self.setSourceModel(application_model)
        self.setSortCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        if settings.value("ApplicationModel/sort", type=bool):
            self.sort(0, QtCore.Qt.SortOrder.AscendingOrder)

    def lessThan(self, left: QtCore.QModelIndex, right: QtCore.QModelIndex) -> bool:
        """Make sure ApplicationAllMessagesItem remains at the top of the model -- ApplicationAllMessagesItem doesn't have any ApplicationRole data
        """
        if not self.sourceModel().data(left, ApplicationItemDataRole.ApplicationRole):
            return True
        elif not self.sourceModel().data(right, ApplicationItemDataRole.ApplicationRole):
            return False

        return super().lessThan(left, right)
