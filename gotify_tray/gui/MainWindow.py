import getpass
import logging
import os
import tempfile
from typing import List

from gotify_tray import gotify
from gotify_tray.database import Downloader, Settings
from gotify_tray.tasks import (
    DeleteApplicationMessagesTask,
    DeleteMessageTask,
    DeleteAllMessagesTask,
    GetApplicationMessagesTask,
    GetApplicationsTask,
    GetMessagesTask,
)
from PyQt6 import QtCore, QtGui, QtWidgets

from ..__version__ import __title__
from .ApplicationModel import (
    ApplicationAllMessagesItem,
    ApplicationModel,
    ApplicationModelItem,
)
from .designs.widget_main import Ui_Form as Ui_Main
from .themes import set_theme
from .MessagesModel import MessagesModel, MessagesModelItem
from .MessageWidget import MessageWidget
from .SettingsDialog import SettingsDialog
from .Tray import Tray

settings = Settings("gotify-tray")
logger = logging.getLogger("logger")
downloader = Downloader()


class MainWidget(QtWidgets.QWidget, Ui_Main):
    def __init__(
        self, application_model: ApplicationModel, messages_model: MessagesModel
    ):
        super(MainWidget, self).__init__()
        self.setupUi(self)

        self.listView_messages.setModel(messages_model)
        self.listView_applications.setModel(application_model)
        self.listView_applications.setFixedWidth(180)
        icon_size = settings.value("ApplicationModelItem/icon/size", type=int)
        self.listView_applications.setIconSize(QtCore.QSize(icon_size, icon_size))

        label_size = settings.value("MainWidget/status_image/size", type=int)
        self.label_status.setFixedSize(QtCore.QSize(label_size, label_size))
        self.label_status_connecting()

    def label_status_active(self):
        self.label_status.setToolTip("Listening for new messages")
        self.label_status.setStyleSheet("QLabel {background-color: green;}")

    def label_status_connecting(self):
        self.label_status.setToolTip("Connecting...")
        self.label_status.setStyleSheet("QLabel {background-color: orange;}")

    def label_status_inactive(self):
        self.label_status.setToolTip("Listener inactive")
        self.label_status.setStyleSheet("QLabel {background-color: grey;}")

    def label_status_error(self):
        self.label_status.setToolTip("Listener error")
        self.label_status.setStyleSheet("QLabel {background-color: red;}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super(MainWindow, self).__init__()
        self.app = app
        self.shutting_down = False

    def init_ui(self):
        self.gotify_client = gotify.GotifyClient(
            settings.value("Server/url", type=str),
            settings.value("Server/client_token", type=str),
        )

        self.setWindowTitle(__title__)
        self.resize(800, 600)
        set_theme(self.app, settings.value("MainWindow/theme", type=str))

        self.application_model = ApplicationModel()
        self.messages_model = MessagesModel()

        self.main_widget = MainWidget(self.application_model, self.messages_model)
        self.setCentralWidget(self.main_widget)

        self.refresh_applications()

        self.tray = Tray()
        self.tray.show()

        self.restore_window_state()

        self.gotify_client.listen(
            new_message_callback=self.new_message_callback,
            opened_callback=self.listener_opened_callback,
            closed_callback=self.listener_closed_callback,
        )

        self.link_callbacks()

        self.show()
        self.window_state_to_restore = QtCore.Qt.WindowState.WindowNoState

        if settings.value("MainWindow/start_minimized", type=bool) and settings.value(
            "tray/show", type=bool
        ):
            self.tray_activated_callback(
                QtWidgets.QSystemTrayIcon.ActivationReason.Trigger
            )

    def refresh_applications(self):
        self.application_model.clear()
        self.messages_model.clear()

        self.main_widget.listView_applications.clearSelection()
        self.main_widget.listView_applications.setEnabled(False)
        self.application_model.setItem(0, 0, ApplicationAllMessagesItem())

        def get_applications_callback(
            applications: List[gotify.GotifyApplicationModel],
        ):
            for i, application in enumerate(applications):
                icon = (
                    QtGui.QIcon(
                        downloader.get_filename(
                            f"{self.gotify_client.url}/{application.image}"
                        )
                    )
                    if settings.value("ApplicationModelItem/icon/show", type=bool)
                    else None
                )
                self.application_model.setItem(
                    i + 1, 0, ApplicationModelItem(application, icon),
                )

        self.get_applications_task = GetApplicationsTask(self.gotify_client)
        self.get_applications_task.success.connect(get_applications_callback)
        self.get_applications_task.finished.connect(
            self.get_applications_finished_callback
        )
        self.get_applications_task.start()

    def get_applications_finished_callback(self):
        self.main_widget.listView_applications.setEnabled(True)
        self.main_widget.listView_applications.setCurrentIndex(
            self.application_model.index(0, 0)
        )

    def insert_message(
        self,
        row: int,
        message: gotify.GotifyMessageModel,
        application: gotify.GotifyApplicationModel,
    ):
        message_item = MessagesModelItem(message)
        self.messages_model.insertRow(row, message_item)

        message_widget = MessageWidget(
            message_item,
            image_path=downloader.get_filename(
                f"{self.gotify_client.url}/{application.image}"
            )
            if settings.value("MessageWidget/image/show", type=bool)
            else "",
        )
        self.main_widget.listView_messages.setIndexWidget(
            self.messages_model.indexFromItem(message_item), message_widget
        )
        message_widget.deletion_requested.connect(
            self.message_deletion_requested_callback
        )

    def listener_opened_callback(self):
        self.main_widget.label_status_active()
        self.tray.set_icon_ok()

    def listener_closed_callback(self, close_status_code: int, close_msg: str):
        self.main_widget.label_status_connecting()
        self.tray.set_icon_error()
        if not self.shutting_down:
            self.gotify_client.reconnect()

    def application_selection_changed(
        self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex
    ):
        if item := self.application_model.itemFromIndex(current):
            self.main_widget.label_selected.setText(item.text())
            self.messages_model.clear()

            if isinstance(item, ApplicationModelItem):

                def get_application_messages_callback(
                    page: gotify.GotifyPagedMessagesModel,
                ):
                    for i, message in enumerate(page.messages):
                        self.insert_message(i, message, item.application)

                self.get_application_messages_task = GetApplicationMessagesTask(
                    item.application.id, self.gotify_client
                )
                self.get_application_messages_task.success.connect(
                    get_application_messages_callback
                )
                self.get_application_messages_task.start()

            elif isinstance(item, ApplicationAllMessagesItem):

                def get_messages_callback(page: gotify.GotifyPagedMessagesModel):
                    for i, message in enumerate(page.messages):
                        if item := self.application_model.itemFromId(message.appid):
                            self.insert_message(i, message, item.application)

                self.get_messages_task = GetMessagesTask(self.gotify_client)
                self.get_messages_task.success.connect(get_messages_callback)
                self.get_messages_task.start()

    def refresh_callback(self):
        self.application_model.clear()
        self.messages_model.clear()

        self.refresh_applications()
        if not self.gotify_client.listener.running:
            self.gotify_client.listener.reset_wait_time()
        else:
            self.gotify_client.stop(reset_wait=True)
        self.gotify_client.reconnect(increase_wait_time=False)

    def delete_all_callback(self):
        selection_model = self.main_widget.listView_applications.selectionModel()
        if item := self.application_model.itemFromIndex(selection_model.currentIndex()):
            self.messages_model.clear()

            if isinstance(item, ApplicationModelItem):
                self.delete_application_messages_task = DeleteApplicationMessagesTask(
                    item.application.id, self.gotify_client
                )
                self.delete_application_messages_task.start()
            elif isinstance(item, ApplicationAllMessagesItem):
                self.delete_all_messages_task = DeleteAllMessagesTask(
                    self.gotify_client
                )
                self.delete_all_messages_task.start()

    def new_message_callback(self, message: gotify.GotifyMessageModel):
        # Show a notification
        application_item = self.application_model.itemFromId(message.appid)
        if not self.isActiveWindow() and message.priority >= settings.value(
            "tray/notifications/priority", type=int
        ):
            image_url = f"{self.gotify_client.url}/{application_item.application.image}"
            self.tray.showMessage(
                message.title,
                message.message,
                QtGui.QIcon(downloader.get_filename(image_url))
                if settings.value("tray/notifications/icon/show", type=bool)
                else QtWidgets.QSystemTrayIcon.Information,
                msecs=settings.value("tray/notifications/duration_ms", type=int),
            )

        # Add the message to the message_model, if its corresponding application is selected
        application_index = (
            self.main_widget.listView_applications.selectionModel().currentIndex()
        )
        if selected_application_item := self.application_model.itemFromIndex(
            application_index
        ):
            if isinstance(selected_application_item, ApplicationModelItem):
                # A single application is selected
                if message.appid == selected_application_item.application.id:
                    self.insert_message(0, message, application_item.application)
            elif isinstance(selected_application_item, ApplicationAllMessagesItem):
                # "All messages' is selected
                self.insert_message(0, message, application_item.application)

    def message_deletion_requested_callback(self, message_item: MessagesModelItem):
        self.messages_model.removeRow(message_item.row())
        self.delete_message_task = DeleteMessageTask(
            message_item.message.id, self.gotify_client
        )
        self.delete_message_task.start()

    def tray_activated_callback(
        self, reason: QtWidgets.QSystemTrayIcon.ActivationReason
    ):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            if self.windowState() & QtCore.Qt.WindowState.WindowMinimized or self.windowState() == (
                QtCore.Qt.WindowState.WindowMinimized
                | QtCore.Qt.WindowState.WindowMaximized
            ):
                self.show()
                self.setWindowState(
                    self.window_state_to_restore | QtCore.Qt.WindowState.WindowActive
                )  # Set the window to its normal state
            else:
                window_state_temp = self.windowState()
                self.setWindowState(QtCore.Qt.WindowState.WindowMinimized)
                self.hide()
                self.window_state_to_restore = window_state_temp

    def message_clicked_callback(self):
        self.main_widget.listView_messages.scrollToTop()
        self.setWindowState(
            self.window_state_to_restore | QtCore.Qt.WindowState.WindowActive
        )
        self.show()

    def settings_callback(self):
        settings_dialog = SettingsDialog(self.app)
        accepted = settings_dialog.exec()

        if accepted and settings_dialog.settings_changed:
            settings_dialog.apply_settings()

        if settings_dialog.server_changed:
            mb = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Icon.Information,
                "Restart",
                "Restart to apply server changes",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.Cancel,
                parent=self,
            )

            r = mb.exec()
            if r == QtWidgets.QMessageBox.StandardButton.Yes:
                self.close()

    def link_callbacks(self):
        self.main_widget.listView_applications.selectionModel().currentChanged.connect(
            self.application_selection_changed
        )
        self.main_widget.pb_refresh.clicked.connect(self.refresh_callback)
        self.main_widget.pb_delete_all.clicked.connect(self.delete_all_callback)

        self.tray.actionQuit.triggered.connect(self.close)
        self.tray.actionSettings.triggered.connect(self.settings_callback)
        self.tray.actionToggleWindow.triggered.connect(
            lambda: self.tray_activated_callback(
                QtWidgets.QSystemTrayIcon.ActivationReason.Trigger
            )
        )
        self.tray.messageClicked.connect(self.message_clicked_callback)
        self.tray.activated.connect(self.tray_activated_callback)

    def acquire_lock(self) -> bool:
        temp_dir = tempfile.gettempdir()
        lock_filename = os.path.join(
            temp_dir, __title__ + "-" + getpass.getuser() + ".lock"
        )
        self.lock_file = QtCore.QLockFile(lock_filename)
        self.lock_file.setStaleLockTime(0)
        return self.lock_file.tryLock()

    def restore_window_state(self):
        window_geometry = settings.value("MainWindow/geometry", type=QtCore.QByteArray)
        window_state = settings.value("MainWindow/state", type=QtCore.QByteArray)

        if window_geometry:
            self.restoreGeometry(window_geometry)
        if window_state:
            self.restoreState(window_state)

    def save_window_state(self):
        settings.setValue("MainWindow/geometry", self.saveGeometry())
        settings.setValue("MainWindow/state", self.saveState())

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if settings.value("tray/show", type=bool) and settings.value(
                "tray/minimize", type=bool
            ):
                if self.windowState() & QtCore.Qt.WindowState.WindowMinimized:
                    self.window_state_to_restore = (
                        self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                    )
                    self.hide()

        super(MainWindow, self).changeEvent(event)

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self.save_window_state()

        if settings.value("tray/show", type=bool):
            self.tray.hide()

        self.lock_file.unlock()

        self.shutting_down = True
        self.gotify_client.stop()
        super(MainWindow, self).closeEvent(e)
        self.app.quit()
