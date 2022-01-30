import getpass
import logging
import os
import sys
import tempfile
from typing import List

from gotify_tray import gotify
from gotify_tray.__version__ import __title__
from gotify_tray.database import Downloader, Settings
from gotify_tray.tasks import GetApplicationsTask, ServerConnectionWatchdogTask
from gotify_tray.utils import verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from ..__version__ import __title__
from .ApplicationModel import (
    ApplicationItemDataRole,
    ApplicationModel,
    ApplicationModelItem,
)
from .SettingsDialog import SettingsDialog
from .Tray import Tray

settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")
downloader = Downloader()

if (level := settings.value("logging/level", type=str)) != "Disabled":
    logger.setLevel(level)
else:
    logging.disable()


title = __title__.replace(" ", "-")


def init_logger():
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
        self.setApplicationName(title)
        self.setQuitOnLastWindowClosed(False)
        self.setWindowIcon(QtGui.QIcon("gotify_tray/gui/images/gotify-small.png"))
        self.setStyle("fusion")

        init_logger()

        self.gotify_client = gotify.GotifyClient(
            settings.value("Server/url", type=str),
            settings.value("Server/client_token", type=str),
        )

        self.application_model = ApplicationModel()
        self.refresh_applications()

        self.tray = Tray()
        self.tray.show()

        self.gotify_client.listen(
            new_message_callback=self.new_message_callback,
            opened_callback=self.listener_opened_callback,
            closed_callback=self.listener_closed_callback,
        )

        self.watchdog = ServerConnectionWatchdogTask(self.gotify_client)
        self.watchdog.closed.connect(lambda: self.listener_closed_callback(None, None))
        self.watchdog.start()

        self.link_callbacks()

    def refresh_applications(self):
        self.application_model.clear()

        def get_applications_callback(
            applications: List[gotify.GotifyApplicationModel],
        ):
            for i, application in enumerate(applications):
                icon = QtGui.QIcon(
                    downloader.get_filename(
                        f"{self.gotify_client.url}/{application.image}"
                    )
                )
                self.application_model.setItem(
                    i, 0, ApplicationModelItem(application, icon),
                )

        self.get_applications_task = GetApplicationsTask(self.gotify_client)
        self.get_applications_task.success.connect(get_applications_callback)
        self.get_applications_task.start()

    def listener_opened_callback(self):
        self.tray.set_icon_ok()
        # self.tray.actionReconnect.setEnabled(True)

    def listener_closed_callback(self, close_status_code: int, close_msg: str):
        self.tray.set_icon_error()
        if not self.shutting_down:
            self.gotify_client.reconnect()

    def refresh_callback(self):
        # self.tray.actionReconnect.setDisabled(True)
        if not self.gotify_client.is_listening():
            self.gotify_client.listener.reset_wait_time()
        else:
            self.gotify_client.stop(reset_wait=True)
        self.gotify_client.reconnect(increase_wait_time=False)

    def new_message_callback(self, message: gotify.GotifyMessageModel):
        # Show a notification
        if not (application_item := self.application_model.itemFromId(message.appid)):
            logger.error(
                f"MainWindow.new_message_callback: App id {message.appid} could not be found. Refreshing applications."
            )
            self.refresh_applications()
            return

        if message.priority >= settings.value("tray/notifications/priority", type=int):
            image_url = f"{self.gotify_client.url}/{application_item.data(ApplicationItemDataRole.ApplicationRole).image}"
            self.tray.showMessage(
                message.title,
                message.message,
                QtGui.QIcon(downloader.get_filename(image_url))
                if settings.value("tray/notifications/icon/show", type=bool)
                else QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                msecs=settings.value("tray/notifications/duration_ms", type=int),
            )

    def settings_callback(self):
        settings_dialog = SettingsDialog(self)
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

    def link_callbacks(self):
        self.tray.actionQuit.triggered.connect(self.quit)
        self.tray.actionSettings.triggered.connect(self.settings_callback)
        self.tray.actionReconnect.triggered.connect(self.refresh_callback)

    def acquire_lock(self) -> bool:
        temp_dir = tempfile.gettempdir()
        lock_filename = os.path.join(
            temp_dir, __title__ + "-" + getpass.getuser() + ".lock"
        )
        self.lock_file = QtCore.QLockFile(lock_filename)
        self.lock_file.setStaleLockTime(0)
        return self.lock_file.tryLock()

    def quit(self) -> None:
        self.tray.hide()

        self.lock_file.unlock()

        self.shutting_down = True
        self.gotify_client.stop()
        super(MainApplication, self).quit()


def start_gui():
    app = MainApplication(sys.argv)

    # prevent multiple instances
    if (app.acquire_lock() or "--no-lock" in sys.argv) and verify_server():
        app.init_ui()
        sys.exit(app.exec())
