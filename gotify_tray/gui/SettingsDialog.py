import logging
import webbrowser

from gotify_tray.database import Settings
from gotify_tray.utils import verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from .designs.widget_settings import Ui_Dialog
from .themes import set_theme


logger = logging.getLogger("gotify-tray")
settings = Settings("gotify-tray")


class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, app: QtWidgets.QApplication):
        super(SettingsDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Settings")

        self.app = app

        self.settings_changed = False
        self.changes_applied = False
        self.server_changed = False

        self.initUI()

        self.link_callbacks()

    def initUI(self):
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

        # Theme
        self.combo_theme.addItems(["default", "dark"])
        self.combo_theme.setCurrentText(
            settings.value("MainApplication/theme", type=str)
        )

        # Icons
        self.cb_icons_notification.setChecked(
            settings.value("tray/notifications/icon/show", type=bool)
        )

        # Notifications
        self.spin_priority.setValue(
            settings.value("tray/notifications/priority", type=int)
        )

        self.spin_duration.setValue(
            settings.value("tray/notifications/duration_ms", type=int)
        )

        # Logging
        self.combo_logging.addItems(
            [
                logging.getLevelName(logging.ERROR),
                logging.getLevelName(logging.WARNING),
                logging.getLevelName(logging.INFO),
                logging.getLevelName(logging.DEBUG),
                "Disabled",
            ]
        )
        self.combo_logging.setCurrentText(settings.value("logging/level", type=str))

    def change_server_info_callback(self):
        self.server_changed = verify_server(force_new=True)

    def settings_changed_callback(self, *args, **kwargs):
        self.settings_changed = True
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(True)

    def reset_settings_callback(self):
        response = QtWidgets.QMessageBox.warning(
            self,
            "Are you sure?",
            "Reset all settings?",
            QtWidgets.QMessageBox.StandardButton.Ok
            | QtWidgets.QMessageBox.StandardButton.Cancel,
            defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel,
        )
        if response == QtWidgets.QMessageBox.StandardButton.Ok:
            settings.clear()

    def link_callbacks(self):
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).clicked.connect(self.apply_settings)

        # Theme
        self.combo_theme.currentTextChanged.connect(self.settings_changed_callback)

        # Icons
        self.cb_icons_notification.stateChanged.connect(self.settings_changed_callback)

        # Notifications
        self.spin_priority.valueChanged.connect(self.settings_changed_callback)
        self.spin_duration.valueChanged.connect(self.settings_changed_callback)

        # Server info
        self.pb_change_server_info.clicked.connect(self.change_server_info_callback)

        # Logging
        self.combo_logging.currentTextChanged.connect(self.settings_changed_callback)
        self.pb_open_log.clicked.connect(
            lambda: webbrowser.open(logger.root.handlers[0].baseFilename)
        )

    def apply_settings(self):
        # Theme
        settings.setValue("MainApplication/theme", self.combo_theme.currentText())
        set_theme(self.app, self.combo_theme.currentText())

        # Icons
        settings.setValue(
            "tray/notifications/icon/show", self.cb_icons_notification.isChecked()
        )

        # Priority
        settings.setValue("tray/notifications/priority", self.spin_priority.value())
        settings.setValue("tray/notifications/duration_ms", self.spin_duration.value())

        # Logging
        selected_level = self.combo_logging.currentText()
        settings.setValue("logging/level", selected_level)
        if selected_level == "Disabled":
            logging.disable(logging.CRITICAL)
        else:
            logging.disable(logging.NOTSET)
            logger.setLevel(selected_level)

        self.settings_changed = False
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

        self.changes_applied = True
