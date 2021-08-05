from gotify_tray.database import Settings
from gotify_tray.utils import verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from .designs.widget_settings import Ui_Dialog
from .themes import set_theme

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

        # Fonts
        self.set_font_labels()

        # Theme
        self.combo_theme.addItems(["default", "dark"])
        self.combo_theme.setCurrentText(settings.value("MainWindow/theme", type=str))

        # Icons
        self.cb_icons_application.setChecked(
            settings.value("ApplicationModelItem/icon/show", type=bool)
        )
        self.cb_icons_message.setChecked(
            settings.value("MessageWidget/image/show", type=bool)
        )
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

    def set_font_labels(self):
        self.label_font_message_title.setText(
            settings.value("MessageWidget/font/title", type=str)
        )
        self.label_font_message_date.setText(
            settings.value("MessageWidget/font/date", type=str)
        )
        self.label_font_message_content.setText(
            settings.value("MessageWidget/font/content", type=str)
        )

    def change_font_callback(self, key: str):
        font = QtGui.QFont()
        font.fromString(settings.value(key, type=str))
        font, accepted = QtWidgets.QFontDialog.getFont(font, self, "Select font")

        if not accepted:
            return

        self.settings_changed_callback()
        label: QtWidgets.QLabel = getattr(
            self, "label_font_message_" + key.split("/")[-1]
        )
        label.setText(font.toString())

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

        # Fonts
        self.pb_font_message_title.clicked.connect(
            lambda: self.change_font_callback("MessageWidget/font/title")
        )
        self.pb_font_message_date.clicked.connect(
            lambda: self.change_font_callback("MessageWidget/font/date")
        )
        self.pb_font_message_content.clicked.connect(
            lambda: self.change_font_callback("MessageWidget/font/content")
        )

        # Theme
        self.combo_theme.currentTextChanged.connect(self.settings_changed_callback)

        # Icons
        self.cb_icons_application.stateChanged.connect(self.settings_changed_callback)
        self.cb_icons_message.stateChanged.connect(self.settings_changed_callback)
        self.cb_icons_notification.stateChanged.connect(self.settings_changed_callback)

        # Notifications
        self.spin_priority.valueChanged.connect(self.settings_changed_callback)
        self.spin_duration.valueChanged.connect(self.settings_changed_callback)

        # Server info
        self.pb_change_server_info.clicked.connect(self.change_server_info_callback)

    def apply_settings(self):
        # Fonts
        settings.setValue(
            "MessageWidget/font/title", self.label_font_message_title.text()
        )
        settings.setValue(
            "MessageWidget/font/date", self.label_font_message_date.text()
        )
        settings.setValue(
            "MessageWidget/font/content", self.label_font_message_content.text()
        )

        # Theme
        settings.setValue("MainWindow/theme", self.combo_theme.currentText())
        set_theme(self.app, self.combo_theme.currentText())

        # Icons
        settings.setValue(
            "ApplicationModelItem/icon/show", self.cb_icons_application.isChecked()
        )
        settings.setValue("MessageWidget/image/show", self.cb_icons_message.isChecked())
        settings.setValue(
            "tray/notifications/icon/show", self.cb_icons_notification.isChecked()
        )

        # Priority
        settings.setValue("tray/notifications/priority", self.spin_priority.value())
        settings.setValue("tray/notifications/duration_ms", self.spin_duration.value())

        self.settings_changed = False
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

        self.changes_applied = True
