import logging
import platform
import os

from gotify_tray.database import Cache, Settings
from gotify_tray.gotify import GotifyMessageModel
from gotify_tray.gui.models import MessagesModelItem
from . import MessageWidget
from gotify_tray.utils import get_icon, verify_server, open_file
from gotify_tray.tasks import (
    ExportSettingsTask,
    ImportSettingsTask,
    CacheSizeTask,
    ClearCacheTask,
)
from gotify_tray.gui.themes import get_themes
from PyQt6 import QtCore, QtGui, QtWidgets

from ..designs.widget_settings import Ui_Dialog


logger = logging.getLogger("gotify-tray")
settings = Settings("gotify-tray")


class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):
    quit_requested = QtCore.pyqtSignal()
    theme_change_requested = QtCore.pyqtSignal(str)

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
        if platform.system() == "Windows":
            # The notification duration setting is ignored by windows
            self.label_notification_duration.hide()
            self.spin_duration.hide()
            self.label_notification_duration_ms.hide()

        self.cb_notify.setChecked(
            settings.value("message/check_missed/notify", type=bool)
        )

        self.cb_notification_click.setChecked(
            settings.value("tray/notifications/click", type=bool)
        )

        self.cb_tray_icon_unread.setChecked(
            settings.value("tray/icon/unread", type=bool)
        )

        # Interface
        self.combo_theme.addItems(get_themes())
        self.combo_theme.setCurrentText(settings.value("theme", type=str))
        self.cb_priority_colors.setChecked(
            settings.value("MessageWidget/priority_color", type=bool)
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
        self.add_message_widget()

        # Advanced
        self.groupbox_image_popup.setChecked(
            settings.value("ImagePopup/enabled", type=bool)
        )
        self.spin_popup_w.setValue(settings.value("ImagePopup/w", type=int))
        self.spin_popup_h.setValue(settings.value("ImagePopup/h", type=int))
        self.label_cache.setText("0 MB")
        self.compute_cache_size()

    def add_message_widget(self):
        self.message_widget = MessageWidget(
            self,
            MessagesModelItem(
                GotifyMessageModel(
                    {
                        "date": "2021-01-01T11:11:00.928224+01:00",
                        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin luctus.",
                        "title": "Title",
                        "priority": 4,
                    }
                )
            ),
            get_icon("gotify-small"),
        )
        self.layout_fonts_message.addWidget(self.message_widget)

    def compute_cache_size(self):
        self.cache_size_task = CacheSizeTask()
        self.cache_size_task.size.connect(lambda size: self.label_cache.setText(f"{round(size/1e6, 1)} MB"))
        self.cache_size_task.start()

    def change_server_info_callback(self):
        self.server_changed = verify_server(force_new=True, enable_import=False)

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

    def export_callback(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Settings", settings.value("export/path", type=str), "*",
        )[0]
        if fname and os.path.exists(os.path.dirname(fname)):
            self.export_settings_task = ExportSettingsTask(fname)
            self.export_settings_task.start()
            settings.setValue("export/path", fname)

    def import_success_callback(self):
        response = QtWidgets.QMessageBox.information(
            self, "Restart to apply settings", "Restart to apply settings"
        )
        if response == QtWidgets.QMessageBox.StandardButton.Ok:
            self.quit_requested.emit()

    def import_callback(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import Settings", settings.value("export/path", type=str), "*",
        )[0]
        if fname and os.path.exists(fname):
            self.import_settings_task = ImportSettingsTask(fname)
            self.import_settings_task.success.connect(self.import_success_callback)
            self.import_settings_task.start()

    def reset_fonts_callback(self):
        response = QtWidgets.QMessageBox.warning(
            self,
            "Are you sure?",
            "Reset all fonts?",
            QtWidgets.QMessageBox.StandardButton.Ok
            | QtWidgets.QMessageBox.StandardButton.Cancel,
            defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel,
        )
        if response == QtWidgets.QMessageBox.StandardButton.Ok:
            settings.remove("MessageWidget/font")
            self.message_widget.deleteLater()
            self.add_message_widget()

    def reset_callback(self):
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
            self.quit_requested.emit()

    def clear_cache_callback(self):
        self.clear_cache_task = ClearCacheTask()
        self.clear_cache_task.start()
        self.label_cache.setText("0 MB")

    def link_callbacks(self):
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).clicked.connect(self.apply_settings)

        # Notifications
        self.spin_priority.valueChanged.connect(self.settings_changed_callback)
        self.spin_duration.valueChanged.connect(self.settings_changed_callback)
        self.cb_notify.stateChanged.connect(self.settings_changed_callback)
        self.cb_notification_click.stateChanged.connect(self.settings_changed_callback)
        self.cb_tray_icon_unread.stateChanged.connect(self.settings_changed_callback)

        # Interface
        self.combo_theme.currentTextChanged.connect(self.settings_changed_callback)
        self.cb_priority_colors.stateChanged.connect(self.settings_changed_callback)

        # Server info
        self.pb_change_server_info.clicked.connect(self.change_server_info_callback)

        # Logging
        self.combo_logging.currentTextChanged.connect(self.settings_changed_callback)
        self.pb_open_log.clicked.connect(
            lambda: open_file(logger.root.handlers[0].baseFilename)
        )

        # Fonts
        self.pb_reset_fonts.clicked.connect(self.reset_fonts_callback)

        self.pb_font_message_title.clicked.connect(
            lambda: self.change_font_callback("title")
        )
        self.pb_font_message_date.clicked.connect(
            lambda: self.change_font_callback("date")
        )
        self.pb_font_message_content.clicked.connect(
            lambda: self.change_font_callback("message")
        )

        # Advanced
        self.pb_export.clicked.connect(self.export_callback)
        self.pb_import.clicked.connect(self.import_callback)
        self.pb_reset.clicked.connect(self.reset_callback)
        self.groupbox_image_popup.toggled.connect(self.settings_changed_callback)
        self.spin_popup_w.valueChanged.connect(self.settings_changed_callback)
        self.spin_popup_h.valueChanged.connect(self.settings_changed_callback)
        self.pb_clear_cache.clicked.connect(self.clear_cache_callback)
        self.pb_open_cache_dir.clicked.connect(lambda: open_file(Cache().directory()))

    def apply_settings(self):
        # Priority
        settings.setValue("tray/notifications/priority", self.spin_priority.value())
        settings.setValue("tray/notifications/duration_ms", self.spin_duration.value())
        settings.setValue("message/check_missed/notify", self.cb_notify.isChecked())
        settings.setValue(
            "tray/notifications/click", self.cb_notification_click.isChecked()
        )
        settings.setValue("tray/icon/unread", self.cb_tray_icon_unread.isChecked())

        # Interface
        current_theme = settings.value("theme", type=str)
        selected_theme = self.combo_theme.currentText()
        if current_theme != selected_theme:
            settings.setValue("theme", selected_theme)
            self.theme_change_requested.emit(selected_theme)

        settings.setValue(
            "MessageWidget/priority_color", self.cb_priority_colors.isChecked()
        )

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

        # Advanced
        settings.setValue("ImagePopup/enabled", self.groupbox_image_popup.isChecked())
        settings.setValue("ImagePopup/w", self.spin_popup_w.value())
        settings.setValue("ImagePopup/h", self.spin_popup_h.value())

        self.settings_changed = False
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Apply
        ).setEnabled(False)

        self.changes_applied = True
