import getpass
import logging
import os
import platform
import sys
import tempfile
from typing import List, Union

from gotify_tray import gotify
from gotify_tray.__version__ import __title__
from gotify_tray.database import Cache, Downloader, Settings
from gotify_tray.tasks import (
    DeleteApplicationMessagesTask,
    DeleteAllMessagesTask,
    DeleteMessageTask,
    GetApplicationsTask,
    GetApplicationMessagesTask,
    GetMessagesTask,
    ServerConnectionWatchdogTask,
)
from gotify_tray.utils import get_icon, verify_server
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
from .widgets import ImagePopup, MainWindow, SettingsDialog, Tray


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
        format="%(levelname)s > %(name)s > %(asctime)s > %(filename)20s:%(lineno)3s - %(funcName)20s() > %(message)s",
    )


class MainApplication(QtWidgets.QApplication):
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

        self.first_connect = True

        self.gotify_client.listen(
            new_message_callback=self.new_message_callback,
            opened_callback=self.listener_opened_callback,
            closed_callback=self.listener_closed_callback,
        )

        self.watchdog = ServerConnectionWatchdogTask(self.gotify_client)

        self.link_callbacks()
        self.init_shortcuts()

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

    def update_last_id(self, i: int):
        if i > settings.value("message/last", type=int):
            settings.setValue("message/last", i)

    def listener_opened_callback(self):
        self.main_window.set_active()
        self.tray.set_icon_ok()

        if self.first_connect:
            # Do not check for missed messages on launch
            self.first_connect = False
            return

        def get_missed_messages_callback(page: gotify.GotifyPagedMessagesModel):
            last_id = settings.value("message/last", type=int)
            ids = []

            page.messages.reverse()
            for message in page.messages:
                if message.id > last_id:
                    if settings.value("message/check_missed/notify", type=bool):
                        self.new_message_callback(message)
                    else:
                        self.add_message_to_model(message)
                    ids.append(message.id)

            if ids:
                self.update_last_id(max(ids))

        self.get_missed_messages_task = GetMessagesTask(self.gotify_client)
        self.get_missed_messages_task.success.connect(get_missed_messages_callback)
        self.get_missed_messages_task.start()

    def listener_closed_callback(self, close_status_code: int, close_msg: str):
        self.main_window.set_connecting()
        self.tray.set_icon_error()
        self.gotify_client.increase_wait_time()
        QtCore.QTimer.singleShot(
            self.gotify_client.get_wait_time() * 1000, self.gotify_client.reconnect
        )

    def reconnect_callback(self):
        if not self.gotify_client.is_listening():
            self.gotify_client.listener.reset_wait_time()
            self.gotify_client.reconnect()
        else:
            self.gotify_client.stop(reset_wait=True)

    def insert_message(
        self,
        row: int,
        message: gotify.GotifyMessageModel,
        application: gotify.GotifyApplicationModel,
    ):
        self.update_last_id(message.id)
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

    def image_popup_callback(self, link: str, pos: QtCore.QPoint):
        if filename := self.downloader.get_filename(link):
            self.image_popup = ImagePopup(filename, pos, link)
            self.image_popup.show()
        else:
            logger.warning(f"Image {link} is not in the cache")

    def main_window_hidden_callback(self):
        if image_popup := getattr(self, "image_popup", None):
            image_popup.close()

    def refresh_callback(self):
        # Manual refresh -> also reset the image cache
        Cache().clear()
        self.refresh_applications()

    def settings_callback(self):
        settings_dialog = SettingsDialog()
        settings_dialog.quit_requested.connect(self.quit)
        accepted = settings_dialog.exec()

        if accepted and settings_dialog.settings_changed:
            settings_dialog.apply_settings()

        if settings_dialog.server_changed:
            # Restart the listener
            self.gotify_client.stop_final()
            self.gotify_client.update_auth(
                settings.value("Server/url", type=str),
                settings.value("Server/client_token", type=str),
            )
            self.gotify_client.listen(
                new_message_callback=self.new_message_callback,
                opened_callback=self.listener_opened_callback,
                closed_callback=self.listener_closed_callback,
            )

    def tray_notification_clicked_callback(self):
        if settings.value("tray/notifications/click", type=bool):
            self.main_window.bring_to_front()

    def tray_activated_callback(
        self, reason: QtWidgets.QSystemTrayIcon.ActivationReason
    ):
        if (
            reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger
            and platform.system() != "Darwin"
        ):
            self.main_window.bring_to_front()

    def link_callbacks(self):
        self.tray.actionQuit.triggered.connect(self.quit)
        self.tray.actionSettings.triggered.connect(self.settings_callback)
        self.tray.actionShowWindow.triggered.connect(self.main_window.bring_to_front)
        self.tray.actionReconnect.triggered.connect(self.reconnect_callback)
        self.tray.messageClicked.connect(self.tray_notification_clicked_callback)
        self.tray.activated.connect(self.tray_activated_callback)

        self.main_window.refresh.connect(self.refresh_callback)
        self.main_window.delete_all.connect(self.delete_all_messages_callback)
        self.main_window.application_selection_changed.connect(
            self.application_selection_changed_callback
        )
        self.main_window.delete_message.connect(self.delete_message_callback)
        self.main_window.image_popup.connect(self.image_popup_callback)
        self.main_window.hidden.connect(self.main_window_hidden_callback)

        self.watchdog.closed.connect(lambda: self.listener_closed_callback(None, None))

    def init_shortcuts(self):
        self.shortcut_quit = QtGui.QShortcut(
            QtGui.QKeySequence.fromString(settings.value("shortcuts/quit", type=str)),
            self.main_window,
        )
        self.shortcut_quit.activated.connect(self.quit)

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

        self.gotify_client.stop_final()
        super(MainApplication, self).quit()
        sys.exit(0)


def start_gui():
    app = MainApplication(sys.argv)
    app.setApplicationName(title)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QtGui.QIcon(get_icon("gotify-small")))
    app.setStyle("fusion")

    init_logger(logger)

    # prevent multiple instances
    if (app.acquire_lock() or "--no-lock" in sys.argv) and verify_server():
        app.init_ui()
        sys.exit(app.exec())
