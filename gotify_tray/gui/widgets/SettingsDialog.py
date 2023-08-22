import logging
import platform
import os

from gotify_tray.__version__ import __version__
from gotify_tray.database import Cache, Settings
from gotify_tray.gotify import GotifyMessageModel
from gotify_tray.gui.models import MessagesModelItem
from . import MessageWidget
from gotify_tray.utils import get_image, get_icon, verify_server, open_file
from gotify_tray.tasks import (
    ExportSettingsTask,
    ImportSettingsTask,
    CacheSizeTask,
    ClearCacheTask,
)
from typing import Any
from PyQt6 import QtCore, QtGui, QtWidgets

from ..designs.widget_settings import Ui_Dialog


logger = logging.getLogger("gotify-tray")
settings = Settings("gotify-tray")


class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):
    quit_requested = QtCore.pyqtSignal()

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
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).setEnabled(False)

        # Notifications
        self.spin_priority.setValue(settings.value("tray/notifications/priority", type=int))

        self.spin_duration.setValue(settings.value("tray/notifications/duration_ms", type=int))
        if platform.system() == "Windows":
            # The notification duration setting is ignored by windows
            self.label_notification_duration.hide()
            self.spin_duration.hide()
            self.label_notification_duration_ms.hide()

        self.cb_notify.setChecked(settings.value("message/check_missed/notify", type=bool))

        self.cb_notification_click.setChecked(settings.value("tray/notifications/click", type=bool))

        self.cb_tray_icon_unread.setChecked(settings.value("tray/icon/unread", type=bool))

        # Interface
        self.cb_priority_colors.setChecked(settings.value("MessageWidget/priority_color", type=bool))
        self.cb_locale.setChecked(settings.value("locale", type=bool))
        self.cb_sort_applications.setChecked(settings.value("ApplicationModel/sort", type=bool))

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
        self.groupbox_image_popup.setChecked(settings.value("ImagePopup/enabled", type=bool))
        self.spin_popup_w.setValue(settings.value("ImagePopup/w", type=int))
        self.spin_popup_h.setValue(settings.value("ImagePopup/h", type=int))
        self.label_cache.setText("0 MB")
        self.compute_cache_size()
        self.groupbox_watchdog.setChecked(settings.value("watchdog/enabled", type=bool))
        self.spin_watchdog_interval.setValue(settings.value("watchdog/interval/s", type=int))

        self.label_app_version.setText(__version__)
        self.label_qt_version.setText(QtCore.QT_VERSION_STR)
        self.label_app_icon.setPixmap(QtGui.QIcon(get_image("logo.ico")).pixmap(22,22))
        self.label_qt_icon.setPixmap(QtGui.QIcon(get_image("qt.png")).pixmap(22,22))

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
            QtGui.QIcon(get_icon("gotify-small")),
        )
        self.layout_fonts_message.addWidget(self.message_widget)

    def compute_cache_size(self):
        self.cache_size_task = CacheSizeTask()
        self.cache_size_task.size.connect(lambda size: self.label_cache.setText(f"{round(size/1e6, 1)} MB"))
        self.cache_size_task.start()

    def set_value(self, key: str, value: Any, widget: QtWidgets.QWidget):
        """Set a Settings value, only if the widget's value_changed attribute has been set
        """
        if hasattr(widget, "value_changed"):
            settings.setValue(key, value)

    def connect_signal(self, signal: QtCore.pyqtBoundSignal, widget: QtWidgets.QWidget):
        """Connect to a signal and set the value_changed attribute for a widget on trigger
        """
        signal.connect(lambda *args: self.setting_changed_callback(widget))

    def change_server_info_callback(self):
        self.server_changed = verify_server(force_new=True, enable_import=False)

    def setting_changed_callback(self, widget: QtWidgets.QWidget):
        self.settings_changed = True
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).setEnabled(True)
        setattr(widget, "value_changed", True)

    def change_font_callback(self, name: str):
        label: QtWidgets.QLabel = getattr(self.message_widget, "label_" + name)

        font, accepted = QtWidgets.QFontDialog.getFont(label.font(), self, f"Select a {name} font")

        if accepted:
            self.setting_changed_callback(label)
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
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)

        # Notifications
        self.connect_signal(self.spin_priority.valueChanged, self.spin_priority)
        self.connect_signal(self.spin_duration.valueChanged, self.spin_duration)
        self.connect_signal(self.cb_notify.stateChanged, self.cb_notify)
        self.connect_signal(self.cb_notification_click.stateChanged, self.cb_notification_click)
        self.connect_signal(self.cb_tray_icon_unread.stateChanged, self.cb_tray_icon_unread)

        # Interface
        self.connect_signal(self.cb_priority_colors.stateChanged, self.cb_priority_colors)
        self.connect_signal(self.cb_locale.stateChanged, self.cb_locale)
        self.connect_signal(self.cb_sort_applications.stateChanged, self.cb_sort_applications)

        # Server info
        self.pb_change_server_info.clicked.connect(self.change_server_info_callback)

        # Logging
        self.connect_signal(self.combo_logging.currentTextChanged, self.combo_logging)
        self.pb_open_log.clicked.connect(lambda: open_file(logger.root.handlers[0].baseFilename))

        # Fonts
        self.pb_reset_fonts.clicked.connect(self.reset_fonts_callback)

        self.pb_font_message_title.clicked.connect(lambda: self.change_font_callback("title"))
        self.pb_font_message_date.clicked.connect(lambda: self.change_font_callback("date"))
        self.pb_font_message_content.clicked.connect(lambda: self.change_font_callback("message"))

        # Advanced
        self.pb_export.clicked.connect(self.export_callback)
        self.pb_import.clicked.connect(self.import_callback)
        self.pb_reset.clicked.connect(self.reset_callback)
        self.connect_signal(self.groupbox_image_popup.toggled, self.groupbox_image_popup)
        self.connect_signal(self.spin_popup_w.valueChanged, self.spin_popup_w)
        self.connect_signal(self.spin_popup_h.valueChanged, self.spin_popup_h)
        self.pb_clear_cache.clicked.connect(self.clear_cache_callback)
        self.pb_open_cache_dir.clicked.connect(lambda: open_file(Cache().directory()))
        self.connect_signal(self.groupbox_watchdog.toggled, self.groupbox_watchdog)
        self.connect_signal(self.spin_watchdog_interval.valueChanged, self.spin_watchdog_interval)

    def apply_settings(self):
        # Priority
        self.set_value("tray/notifications/priority", self.spin_priority.value(), self.spin_priority)
        self.set_value("tray/notifications/duration_ms", self.spin_duration.value(), self.spin_duration)
        self.set_value("message/check_missed/notify", self.cb_notify.isChecked(), self.cb_notify)
        self.set_value("tray/notifications/click", self.cb_notification_click.isChecked(), self.cb_notification_click)
        self.set_value("tray/icon/unread", self.cb_tray_icon_unread.isChecked(), self.cb_tray_icon_unread)

        # Interface
        self.set_value("MessageWidget/priority_color", self.cb_priority_colors.isChecked(), self.cb_priority_colors)
        self.set_value("locale", self.cb_locale.isChecked(), self.cb_locale)
        self.set_value("ApplicationModel/sort", self.cb_sort_applications.isChecked(), self.cb_sort_applications)

        # Logging
        selected_level = self.combo_logging.currentText()
        self.set_value("logging/level", selected_level, self.combo_logging)
        if selected_level == "Disabled":
            logging.disable(logging.CRITICAL)
        else:
            logging.disable(logging.NOTSET)
            logger.setLevel(selected_level)

        # Fonts
        self.set_value("MessageWidget/font/title", self.message_widget.label_title.font().toString(), self.message_widget.label_title)
        self.set_value("MessageWidget/font/date", self.message_widget.label_date.font().toString(), self.message_widget.label_date)
        self.set_value("MessageWidget/font/message", self.message_widget.label_message.font().toString(), self.message_widget.label_message)

        # Advanced
        self.set_value("ImagePopup/enabled", self.groupbox_image_popup.isChecked(), self.groupbox_image_popup)
        self.set_value("ImagePopup/w", self.spin_popup_w.value(), self.spin_popup_w)
        self.set_value("ImagePopup/h", self.spin_popup_h.value(), self.spin_popup_h)
        self.set_value("watchdog/enabled", self.groupbox_watchdog.isChecked(), self.groupbox_watchdog)
        self.set_value("watchdog/interval/s", self.spin_watchdog_interval.value(), self.spin_watchdog_interval)

        self.settings_changed = False
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).setEnabled(False)

        self.changes_applied = True
