import logging
import webbrowser

from gotify_tray.database import Settings
from gotify_tray.gotify import GotifyMessageModel
from gotify_tray.gui.models import MessagesModelItem
from . import MessageWidget
from gotify_tray.utils import verify_server
from PyQt6 import QtCore, QtGui, QtWidgets

from ..designs.widget_settings import Ui_Dialog


logger = logging.getLogger("gotify-tray")
settings = Settings("gotify-tray")


class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Settings")

        self.settings_changed = False
        self.changes_applied = False
        self.server_changed = False

        self.initUI()

        self.link_callbacks()

    def initUI(self):
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

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

        # Fonts
        self.message_widget = MessageWidget(
            MessagesModelItem(
                GotifyMessageModel(
                    {
                        "date": "2021-01-01T11:11:00.928224+01:00",
                        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin luctus.",
                        "title": "Title",
                    }
                )
            )
        )
        self.layout_fonts_message.addWidget(self.message_widget)

    def change_server_info_callback(self):
        self.server_changed = verify_server(force_new=True)

    def settings_changed_callback(self, *args, **kwargs):
        self.settings_changed = True
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(True)

    def change_font_callback(self, name: str):
        label: QtWidgets.QLabel = getattr(self.message_widget, "label_" + name)

        font, accepted = QtWidgets.QFontDialog.getFont(
            label.font(), self, f"Select a {name} font"
        )

        if accepted:
            self.settings_changed_callback()
            label.setFont(font)

    def link_callbacks(self):
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).clicked.connect(self.apply_settings)

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

        # Fonts
        self.pb_font_message_title.clicked.connect(
            lambda: self.change_font_callback("title")
        )
        self.pb_font_message_date.clicked.connect(
            lambda: self.change_font_callback("date")
        )
        self.pb_font_message_content.clicked.connect(
            lambda: self.change_font_callback("message")
        )

    def apply_settings(self):
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

        # Fonts
        settings.setValue(
            "MessageWidget/font/title",
            self.message_widget.label_title.font().toString(),
        )
        settings.setValue(
            "MessageWidget/font/date", self.message_widget.label_date.font().toString()
        )
        settings.setValue(
            "MessageWidget/font/message",
            self.message_widget.label_message.font().toString(),
        )

        self.settings_changed = False
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

        self.changes_applied = True
