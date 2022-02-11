import getpass
import logging
import os
import sys
import tempfile
from typing import List, Union

from gotify_tray import gotify
from gotify_tray.__version__ import __title__
from gotify_tray.database import Downloader, Settings
from gotify_tray.tasks import (
    DeleteApplicationMessagesTask,
    DeleteAllMessagesTask,
    DeleteMessageTask,
    GetApplicationsTask,
    GetApplicationMessagesTask,
    GetMessagesTask,
    ServerConnectionWatchdogTask,
)
from gotify_tray.utils import get_abs_path, verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from ..__version__ import __title__
from .models import (
    ApplicationAllMessagesItem,
    ApplicationItemDataRole,
    ApplicationModel,
    ApplicationModelItem,
    MessagesModel,
    MessagesModelItem,
    MessageItemDataRole,
)
from .widgets import MainWindow, SettingsDialog, Tray


settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")


title = __title__.replace(" ", "-")


def init_logger(logger: logging.Logger):
    if (level := settings.value("logging/level", type=str)) != "Disabled":
        logger.setLevel(level)
    else:
        logging.disable()

    logdir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.StandardLocation.AppDataLocation
    )[0]
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.basicConfig(
        filename=os.path.join(logdir, f"{title}.log"),
        format="%(levelname)s > %(name)s > %(asctime)s > %(message)s",
    )


class MainApplication(QtWidgets.QApplication):
    def __init__(self, argv: List):
        super(MainApplication, self).__init__(argv)
        self.shutting_down = False

    def init_ui(self):
        self.gotify_client = gotify.GotifyClient(
            settings.value("Server/url", type=str),
            settings.value("Server/client_token", type=str),
        )

        self.downloader = Downloader()

        self.messages_model = MessagesModel()
        self.application_model = ApplicationModel()

        self.main_window = MainWindow(self.application_model, self.messages_model)

        self.refresh_applications()

        self.tray = Tray()
        self.tray.show()

        self.gotify_client.listen(
            new_message_callback=self.new_message_callback,
            opened_callback=self.listener_opened_callback,
            closed_callback=self.listener_closed_callback,
        )

        self.watchdog = ServerConnectionWatchdogTask(self.gotify_client)

        self.link_callbacks()

        self.watchdog.start()

    def refresh_applications(self):
        self.messages_model.clear()
        self.application_model.clear()

        self.application_model.setItem(0, 0, ApplicationAllMessagesItem())

        self.get_applications_task = GetApplicationsTask(self.gotify_client)
        self.get_applications_task.success.connect(
            self.get_applications_success_callback
        )
        self.get_applications_task.started.connect(
            self.main_window.disable_applications
        )
        self.get_applications_task.finished.connect(
            self.main_window.enable_applications
        )
        self.get_applications_task.start()

    def get_applications_success_callback(
        self, applications: List[gotify.GotifyApplicationModel],
    ):
        for i, application in enumerate(applications):
            icon = QtGui.QIcon(
                self.downloader.get_filename(
                    f"{self.gotify_client.url}/{application.image}"
                )
            )
            self.application_model.setItem(
                i + 1, 0, ApplicationModelItem(application, icon),
            )

    def listener_opened_callback(self):
        self.main_window.set_active()
        self.tray.set_icon_ok()

    def listener_closed_callback(self, close_status_code: int, close_msg: str):
        self.main_window.set_connecting()
        self.tray.set_icon_error()
        if not self.shutting_down:
            self.gotify_client.reconnect()

    def reconnect_callback(self):
        if not self.gotify_client.is_listening():
            self.gotify_client.listener.reset_wait_time()
        else:
            self.gotify_client.stop(reset_wait=True)
        self.gotify_client.reconnect(increase_wait_time=False)

    def insert_message(
        self,
        row: int,
        message: gotify.GotifyMessageModel,
        application: gotify.GotifyApplicationModel,
    ):
        message_item = MessagesModelItem(message)
        self.messages_model.insertRow(row, message_item)
        self.main_window.insert_message_widget(
            message_item,
            self.downloader.get_filename(
                f"{self.gotify_client.url}/{application.image}"
            ),
        )

    def application_selection_changed_callback(
        self, item: Union[ApplicationModelItem, ApplicationAllMessagesItem]
    ):
        self.messages_model.clear()

        if isinstance(item, ApplicationModelItem):

            def get_application_messages_callback(
                page: gotify.GotifyPagedMessagesModel,
            ):
                for i, message in enumerate(page.messages):
                    self.insert_message(
                        i, message, item.data(ApplicationItemDataRole.ApplicationRole),
                    )

            self.get_application_messages_task = GetApplicationMessagesTask(
                item.data(ApplicationItemDataRole.ApplicationRole).id,
                self.gotify_client,
            )
            self.get_application_messages_task.success.connect(
                get_application_messages_callback
            )
            self.get_application_messages_task.start()

        elif isinstance(item, ApplicationAllMessagesItem):

            def get_messages_callback(page: gotify.GotifyPagedMessagesModel):
                for i, message in enumerate(page.messages):
                    if item := self.application_model.itemFromId(message.appid):
                        self.insert_message(
                            i,
                            message,
                            item.data(ApplicationItemDataRole.ApplicationRole),
                        )

            self.get_messages_task = GetMessagesTask(self.gotify_client)
            self.get_messages_task.success.connect(get_messages_callback)
            self.get_messages_task.start()

    def add_message_to_model(self, message: gotify.GotifyMessageModel):
        if application_item := self.application_model.itemFromId(message.appid):
            application_index = self.main_window.currentApplicationIndex()
            if selected_application_item := self.application_model.itemFromIndex(
                application_index
            ):
                if isinstance(selected_application_item, ApplicationModelItem):
                    # A single application is selected
                    if (
                        message.appid
                        == selected_application_item.data(
                            ApplicationItemDataRole.ApplicationRole
                        ).id
                    ):
                        self.insert_message(
                            0,
                            message,
                            application_item.data(
                                ApplicationItemDataRole.ApplicationRole
                            ),
                        )
                elif isinstance(selected_application_item, ApplicationAllMessagesItem):
                    # "All messages' is selected
                    self.insert_message(
                        0,
                        message,
                        application_item.data(ApplicationItemDataRole.ApplicationRole),
                    )

    def new_message_callback(self, message: gotify.GotifyMessageModel):
        self.add_message_to_model(message)

        # Show a notification
        if (
            message.priority < settings.value("tray/notifications/priority", type=int)
            or self.main_window.isActiveWindow()
        ):
            return

        if settings.value("tray/notifications/icon/show", type=bool):
            if application_item := self.application_model.itemFromId(message.appid):
                image_url = f"{self.gotify_client.url}/{application_item.data(ApplicationItemDataRole.ApplicationRole).image}"
                icon = QtGui.QIcon(self.downloader.get_filename(image_url))
            else:
                logger.error(
                    f"MainWindow.new_message_callback: App id {message.appid} could not be found. Refreshing applications."
                )
                self.refresh_applications()
                icon = QtWidgets.QSystemTrayIcon.MessageIcon.Information
        else:
            icon = QtWidgets.QSystemTrayIcon.MessageIcon.Information

        self.tray.showMessage(
            message.title,
            message.message,
            icon,
            msecs=settings.value("tray/notifications/duration_ms", type=int),
        )

    def delete_message_callback(self, message_item: MessagesModelItem):
        self.delete_message_task = DeleteMessageTask(
            message_item.data(MessageItemDataRole.MessageRole).id, self.gotify_client
        )
        self.messages_model.removeRow(message_item.row())
        self.delete_message_task.start()

    def delete_all_messages_callback(
        self, item: Union[ApplicationModelItem, ApplicationAllMessagesItem]
    ):
        if isinstance(item, ApplicationModelItem):
            self.delete_application_messages_task = DeleteApplicationMessagesTask(
                item.data(ApplicationItemDataRole.ApplicationRole).id,
                self.gotify_client,
            )
            self.delete_application_messages_task.start()
        elif isinstance(item, ApplicationAllMessagesItem):
            self.delete_all_messages_task = DeleteAllMessagesTask(self.gotify_client)
            self.delete_all_messages_task.start()
        else:
            return

        self.messages_model.clear()

    def settings_callback(self):
        settings_dialog = SettingsDialog()
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
            )

            r = mb.exec()
            if r == QtWidgets.QMessageBox.StandardButton.Yes:
                self.quit()

    def tray_activated_callback(
        self, reason: QtWidgets.QSystemTrayIcon.ActivationReason
    ):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.main_window.bring_to_front()

    def link_callbacks(self):
        self.tray.actionQuit.triggered.connect(self.quit)
        self.tray.actionSettings.triggered.connect(self.settings_callback)
        self.tray.actionShowWindow.triggered.connect(self.main_window.bring_to_front)
        self.tray.actionReconnect.triggered.connect(self.reconnect_callback)
        self.tray.messageClicked.connect(self.main_window.bring_to_front)
        self.tray.activated.connect(self.tray_activated_callback)

        self.main_window.refresh.connect(self.refresh_applications)
        self.main_window.delete_all.connect(self.delete_all_messages_callback)
        self.main_window.application_selection_changed.connect(
            self.application_selection_changed_callback
        )
        self.main_window.delete_message.connect(self.delete_message_callback)

        self.watchdog.closed.connect(lambda: self.listener_closed_callback(None, None))

    def acquire_lock(self) -> bool:
        temp_dir = tempfile.gettempdir()
        lock_filename = os.path.join(
            temp_dir, __title__ + "-" + getpass.getuser() + ".lock"
        )
        self.lock_file = QtCore.QLockFile(lock_filename)
        self.lock_file.setStaleLockTime(0)
        return self.lock_file.tryLock()

    def quit(self) -> None:
        self.main_window.store_state()

        self.tray.hide()

        self.lock_file.unlock()

        self.shutting_down = True
        self.gotify_client.stop()
        super(MainApplication, self).quit()


def start_gui():
    app = MainApplication(sys.argv)
    app.setApplicationName(title)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(
        QtGui.QIcon(get_abs_path("gotify_tray/gui/images/gotify-small.png"))
    )
    app.setStyle("fusion")

    init_logger(logger)

    # prevent multiple instances
    if (app.acquire_lock() or "--no-lock" in sys.argv) and verify_server():
        app.init_ui()
        sys.exit(app.exec())
