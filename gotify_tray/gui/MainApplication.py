import getpass
import logging
import os
import platform
import sys
import tempfile

from gotify_tray import gotify
from gotify_tray.__version__ import __title__
from gotify_tray.database import Downloader, Settings
from gotify_tray.tasks import (
    ClearCacheTask,
    DeleteApplicationMessagesTask,
    DeleteAllMessagesTask,
    DeleteMessageTask,
    GetApplicationsTask,
    GetApplicationMessagesTask,
    GetMessagesTask,
    ProcessMessageTask,
    ServerConnectionWatchdogTask,
)
from gotify_tray.gui.themes import set_theme
from gotify_tray.utils import get_icon, verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from ..__version__ import __title__
from .models import (
    ApplicationAllMessagesItem,
    ApplicationItemDataRole,
    ApplicationModel,
    ApplicationModelItem,
    ApplicationProxyModel,
    MessagesModel,
    MessagesModelItem,
    MessageItemDataRole,
)
from .widgets import ImagePopup, MainWindow, MessageWidget, SettingsDialog, Tray


settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")


def init_logger(logger: logging.Logger):
    if (level := settings.value("logging/level", type=str)) != "Disabled":
        logger.setLevel(level)
    else:
        logging.disable()

    logdir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.AppDataLocation)[0]
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.basicConfig(
        filename=os.path.join(logdir, f"{__title__}.log"),
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
        self.application_proxy_model = ApplicationProxyModel(self.application_model)

        self.main_window = MainWindow(self.application_model, self.application_proxy_model, self.messages_model)
        self.main_window.show()  # The initial .show() is necessary to get the correct sizes when adding MessageWigets
        QtCore.QTimer.singleShot(0, self.main_window.hide)

        self.refresh_applications()

        self.tray = Tray()
        self.tray.show()

        self.first_connect = True

        self.watchdog = ServerConnectionWatchdogTask(self.gotify_client)

        self.link_callbacks()
        self.init_shortcuts()

        self.gotify_client.listen()

        if settings.value("watchdog/enabled", type=bool):
            self.watchdog.start()

    def set_theme(self):
        set_theme(self)

    def refresh_applications(self):
        self.messages_model.clear()
        self.application_model.clear()

        self.application_model.setItem(0, 0, ApplicationAllMessagesItem())

        self.get_applications_task = GetApplicationsTask(self.gotify_client)
        self.get_applications_task.success.connect(self.get_applications_success_callback)
        self.get_applications_task.started.connect(self.main_window.disable_applications)
        self.get_applications_task.finished.connect(self.main_window.enable_applications)
        self.get_applications_task.start()

    def get_applications_success_callback(
        self, applications: list[gotify.GotifyApplicationModel],
    ):
        for i, application in enumerate(applications):
            icon = QtGui.QIcon(self.downloader.get_filename(f"{self.gotify_client.url}/{application.image}"))
            self.application_model.setItem(i + 1, 0, ApplicationModelItem(application, icon))

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
                        self.new_message_callback(message, process=False)
                    else:
                        self.add_message_to_model(message, process=False)
                    ids.append(message.id)

            if ids:
                self.update_last_id(max(ids))

        self.get_missed_messages_task = GetMessagesTask(self.gotify_client)
        self.get_missed_messages_task.success.connect(get_missed_messages_callback)
        self.get_missed_messages_task.start()

    def listener_closed_callback(self):
        self.main_window.set_connecting()
        self.tray.set_icon_error()
        self.gotify_client.reconnect()

    def reconnect_callback(self):
        self.gotify_client.reset_wait_time()
        if not self.gotify_client.is_listening():
            self.gotify_client.reconnect()
        else:
            self.gotify_client.stop()

    def abort_get_messages_task(self):
        """
        Abort any tasks that will result in new messages getting appended to messages_model
        """
        aborted_tasks = []
        for s in ["get_application_messages_task", "get_messages_task"]:
            if task := getattr(self, s, None):
                task.abort()
                aborted_tasks.append(task)
                try:
                    task.message.disconnect()
                except TypeError:
                    pass
        
        for task in aborted_tasks:
            task.wait()

    def application_selection_changed_callback(self, item: ApplicationModelItem | ApplicationAllMessagesItem):
        self.main_window.disable_buttons()
        self.abort_get_messages_task()
        self.messages_model.clear()

        if isinstance(item, ApplicationModelItem):
            self.get_application_messages_task = GetApplicationMessagesTask(item.data(ApplicationItemDataRole.ApplicationRole).id, self.gotify_client)
            self.get_application_messages_task.message.connect(self.messages_model.append_message)
            self.get_application_messages_task.finished.connect(self.main_window.enable_buttons)
            self.get_application_messages_task.start()

        elif isinstance(item, ApplicationAllMessagesItem):
            self.get_messages_task = GetMessagesTask(self.gotify_client)
            self.get_messages_task.message.connect(self.messages_model.append_message)
            self.get_messages_task.finished.connect(self.main_window.enable_buttons)
            self.get_messages_task.start()

    def add_message_to_model(self, message: gotify.GotifyMessageModel, process: bool = True):
        if self.application_model.itemFromId(message.appid):
            application_index = self.main_window.currentApplicationIndex()
            if selected_application_item := self.application_model.itemFromIndex(self.application_proxy_model.mapToSource(application_index)):

                def insert_message_helper():
                    if isinstance(selected_application_item, ApplicationModelItem):
                        # A single application is selected
                        # -> Only insert the message if the appid matches the selected appid
                        if (
                            message.appid 
                            == selected_application_item.data(ApplicationItemDataRole.ApplicationRole).id
                        ):
                            self.messages_model.insert_message(0, message)
                    elif isinstance(selected_application_item, ApplicationAllMessagesItem):
                        # "All messages' is selected
                        self.messages_model.insert_message(0, message)

                if process:
                    self.process_message_task = ProcessMessageTask(message)
                    self.process_message_task.finished.connect(insert_message_helper)
                    self.process_message_task.start()
                else:
                    insert_message_helper()
        else:
            logger.error(f"App id {message.appid} could not be found. Refreshing applications.")
            self.refresh_applications()

    def new_message_callback(self, message: gotify.GotifyMessageModel, process: bool = True):
        self.add_message_to_model(message, process=process)

        # Don't show a notification if it's low priority or the window is active
        if (
            message.priority < settings.value("tray/notifications/priority", type=int)
            or self.main_window.isActiveWindow()
        ):
            return

        # Change the tray icon to show there are unread notifications
        if (
            settings.value("tray/icon/unread", type=bool)
            and not self.main_window.isActiveWindow()
        ):
            self.tray.set_icon_unread()

        # Get the application icon
        if (
            settings.value("tray/notifications/icon/show", type=bool)
            and (application_item := self.application_model.itemFromId(message.appid))
        ):
            icon = application_item.icon()
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
        self, item: ApplicationModelItem | ApplicationAllMessagesItem
    ):
        if isinstance(item, ApplicationModelItem):
            self.delete_application_messages_task = DeleteApplicationMessagesTask(
                item.data(ApplicationItemDataRole.ApplicationRole).id,
                self.gotify_client,
            )
            self.delete_application_messages_task.start()
        elif isinstance(item, ApplicationAllMessagesItem):
            self.clear_cache_task = ClearCacheTask()        
            self.clear_cache_task.start()
        
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

    def theme_change_requested_callback(self, *args):
        # Set the theme
        self.set_theme()

        # Update the main window icons
        self.main_window.set_icons()

        # Update the message widget icons
        for r in range(self.messages_model.rowCount()):
            message_widget: MessageWidget = self.main_window.listView_messages.indexWidget(self.messages_model.index(r, 0))
            message_widget.set_icons()

    def settings_callback(self):
        settings_dialog = SettingsDialog()
        settings_dialog.quit_requested.connect(self.quit)
        accepted = settings_dialog.exec()

        if accepted and settings_dialog.settings_changed:
            settings_dialog.apply_settings()

        if settings_dialog.server_changed:
            # Update the server parameters and trigger a listener restart
            self.gotify_client.update_auth(
                settings.value("Server/url", type=str),
                settings.value("Server/client_token", type=str),
            )
            self.gotify_client.stop()

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

        self.main_window.refresh.connect(self.refresh_applications)
        self.main_window.delete_all.connect(self.delete_all_messages_callback)
        self.main_window.application_selection_changed.connect(self.application_selection_changed_callback)
        self.main_window.delete_message.connect(self.delete_message_callback)
        self.main_window.image_popup.connect(self.image_popup_callback)
        self.main_window.hidden.connect(self.main_window_hidden_callback)
        self.main_window.activated.connect(self.tray.revert_icon)
        
        self.styleHints().colorSchemeChanged.connect(self.theme_change_requested_callback)

        self.messages_model.rowsInserted.connect(self.main_window.display_message_widgets)

        self.gotify_client.opened.connect(self.listener_opened_callback)
        self.gotify_client.closed.connect(self.listener_closed_callback)
        self.gotify_client.new_message.connect(self.new_message_callback)

        self.watchdog.closed.connect(self.listener_closed_callback)

    def init_shortcuts(self):
        self.shortcut_quit = QtGui.QShortcut(
            QtGui.QKeySequence.fromString(settings.value("shortcuts/quit", type=str)),
            self.main_window,
        )
        self.shortcut_quit.activated.connect(self.quit)

    def acquire_lock(self) -> bool:
        temp_dir = tempfile.gettempdir()
        lock_filename = os.path.join(temp_dir, __title__ + "-" + getpass.getuser() + ".lock")
        self.lock_file = QtCore.QLockFile(lock_filename)
        self.lock_file.setStaleLockTime(0)
        return self.lock_file.tryLock()

    def quit(self):
        logger.debug("Quit requested.")

        self.main_window.store_state()

        self.tray.hide()

        self.lock_file.unlock()

        self.gotify_client.quit()
        super(MainApplication, self).quit()
        sys.exit(0)


def start_gui():
    app = MainApplication(sys.argv)
    app.setApplicationName(__title__)
    app.setDesktopFileName("gotifytray.desktop")
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QtGui.QIcon(get_icon("gotify-small")))
    app.setStyle("fusion")
    app.set_theme()

    init_logger(logger)

    # prevent multiple instances
    if (app.acquire_lock() or "--no-lock" in sys.argv) and verify_server():
        app.init_ui()
        sys.exit(app.exec())
