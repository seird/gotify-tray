# Form implementation generated from reading ui file 'gotify_tray/gui/designs\widget_settings.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 392)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_general = QtWidgets.QWidget()
        self.tab_general.setObjectName("tab_general")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_general)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_notifications = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_notifications.setObjectName("groupBox_notifications")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_notifications)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_notification_duration = QtWidgets.QLabel(self.groupBox_notifications)
        self.label_notification_duration.setObjectName("label_notification_duration")
        self.gridLayout_4.addWidget(self.label_notification_duration, 1, 0, 1, 1)
        self.spin_duration = QtWidgets.QSpinBox(self.groupBox_notifications)
        self.spin_duration.setMinimum(500)
        self.spin_duration.setMaximum(30000)
        self.spin_duration.setSingleStep(100)
        self.spin_duration.setObjectName("spin_duration")
        self.gridLayout_4.addWidget(self.spin_duration, 1, 1, 1, 1)
        self.cb_notification_click = QtWidgets.QCheckBox(self.groupBox_notifications)
        self.cb_notification_click.setObjectName("cb_notification_click")
        self.gridLayout_4.addWidget(self.cb_notification_click, 3, 0, 1, 3)
        self.label_notification_duration_ms = QtWidgets.QLabel(self.groupBox_notifications)
        self.label_notification_duration_ms.setObjectName("label_notification_duration_ms")
        self.gridLayout_4.addWidget(self.label_notification_duration_ms, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.cb_notify = QtWidgets.QCheckBox(self.groupBox_notifications)
        self.cb_notify.setObjectName("cb_notify")
        self.gridLayout_4.addWidget(self.cb_notify, 2, 0, 1, 3)
        self.spin_priority = QtWidgets.QSpinBox(self.groupBox_notifications)
        self.spin_priority.setMinimum(1)
        self.spin_priority.setMaximum(10)
        self.spin_priority.setProperty("value", 5)
        self.spin_priority.setObjectName("spin_priority")
        self.gridLayout_4.addWidget(self.spin_priority, 0, 1, 1, 1)
        self.label_notification_priority = QtWidgets.QLabel(self.groupBox_notifications)
        self.label_notification_priority.setObjectName("label_notification_priority")
        self.gridLayout_4.addWidget(self.label_notification_priority, 0, 0, 1, 1)
        self.cb_tray_icon_unread = QtWidgets.QCheckBox(self.groupBox_notifications)
        self.cb_tray_icon_unread.setObjectName("cb_tray_icon_unread")
        self.gridLayout_4.addWidget(self.cb_tray_icon_unread, 4, 0, 1, 3)
        self.verticalLayout_4.addWidget(self.groupBox_notifications)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_theme = QtWidgets.QLabel(self.groupBox_2)
        self.label_theme.setObjectName("label_theme")
        self.horizontalLayout_3.addWidget(self.label_theme)
        self.combo_theme = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_theme.setObjectName("combo_theme")
        self.horizontalLayout_3.addWidget(self.combo_theme)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.cb_priority_colors = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_priority_colors.setObjectName("cb_priority_colors")
        self.verticalLayout_2.addWidget(self.cb_priority_colors)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_server_info = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_server_info.setObjectName("groupBox_server_info")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_server_info)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pb_change_server_info = QtWidgets.QPushButton(self.groupBox_server_info)
        self.pb_change_server_info.setObjectName("pb_change_server_info")
        self.gridLayout_3.addWidget(self.pb_change_server_info, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_server_info)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.tabWidget.addTab(self.tab_general, "")
        self.tab_fonts = QtWidgets.QWidget()
        self.tab_fonts.setObjectName("tab_fonts")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_fonts)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pb_reset_fonts = QtWidgets.QPushButton(self.tab_fonts)
        self.pb_reset_fonts.setObjectName("pb_reset_fonts")
        self.horizontalLayout_5.addWidget(self.pb_reset_fonts)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.groupBox_fonts_message = QtWidgets.QGroupBox(self.tab_fonts)
        self.groupBox_fonts_message.setObjectName("groupBox_fonts_message")
        self.layout_fonts_message = QtWidgets.QVBoxLayout(self.groupBox_fonts_message)
        self.layout_fonts_message.setContentsMargins(4, 4, 4, 4)
        self.layout_fonts_message.setSpacing(6)
        self.layout_fonts_message.setObjectName("layout_fonts_message")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_font_message_title = QtWidgets.QPushButton(self.groupBox_fonts_message)
        self.pb_font_message_title.setObjectName("pb_font_message_title")
        self.horizontalLayout.addWidget(self.pb_font_message_title)
        self.pb_font_message_date = QtWidgets.QPushButton(self.groupBox_fonts_message)
        self.pb_font_message_date.setObjectName("pb_font_message_date")
        self.horizontalLayout.addWidget(self.pb_font_message_date)
        self.pb_font_message_content = QtWidgets.QPushButton(self.groupBox_fonts_message)
        self.pb_font_message_content.setObjectName("pb_font_message_content")
        self.horizontalLayout.addWidget(self.pb_font_message_content)
        self.layout_fonts_message.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.groupBox_fonts_message)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.tabWidget.addTab(self.tab_fonts, "")
        self.tab_advanced = QtWidgets.QWidget()
        self.tab_advanced.setObjectName("tab_advanced")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_advanced)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_reset = QtWidgets.QPushButton(self.groupBox)
        self.pb_reset.setObjectName("pb_reset")
        self.horizontalLayout_2.addWidget(self.pb_reset)
        self.pb_import = QtWidgets.QPushButton(self.groupBox)
        self.pb_import.setObjectName("pb_import")
        self.horizontalLayout_2.addWidget(self.pb_import)
        self.pb_export = QtWidgets.QPushButton(self.groupBox)
        self.pb_export.setObjectName("pb_export")
        self.horizontalLayout_2.addWidget(self.pb_export)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupbox_image_popup = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupbox_image_popup.setCheckable(True)
        self.groupbox_image_popup.setObjectName("groupbox_image_popup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupbox_image_popup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.groupbox_image_popup)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.spin_popup_w = QtWidgets.QSpinBox(self.groupbox_image_popup)
        self.spin_popup_w.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spin_popup_w.setMinimum(100)
        self.spin_popup_w.setMaximum(10000)
        self.spin_popup_w.setObjectName("spin_popup_w")
        self.horizontalLayout_4.addWidget(self.spin_popup_w)
        self.label_2 = QtWidgets.QLabel(self.groupbox_image_popup)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.spin_popup_h = QtWidgets.QSpinBox(self.groupbox_image_popup)
        self.spin_popup_h.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spin_popup_h.setMinimum(100)
        self.spin_popup_h.setMaximum(10000)
        self.spin_popup_h.setObjectName("spin_popup_h")
        self.horizontalLayout_4.addWidget(self.spin_popup_h)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupbox_image_popup)
        self.groupBox_cache = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupBox_cache.setObjectName("groupBox_cache")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_cache)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pb_clear_cache = QtWidgets.QPushButton(self.groupBox_cache)
        self.pb_clear_cache.setObjectName("pb_clear_cache")
        self.horizontalLayout_6.addWidget(self.pb_clear_cache)
        self.pb_open_cache_dir = QtWidgets.QPushButton(self.groupBox_cache)
        self.pb_open_cache_dir.setObjectName("pb_open_cache_dir")
        self.horizontalLayout_6.addWidget(self.pb_open_cache_dir)
        self.label_cache = QtWidgets.QLabel(self.groupBox_cache)
        self.label_cache.setObjectName("label_cache")
        self.horizontalLayout_6.addWidget(self.label_cache)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout.addWidget(self.groupBox_cache)
        self.groupBox_logging = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupBox_logging.setObjectName("groupBox_logging")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_logging)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.combo_logging = QtWidgets.QComboBox(self.groupBox_logging)
        self.combo_logging.setObjectName("combo_logging")
        self.gridLayout_6.addWidget(self.combo_logging, 0, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(190, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_6.addItem(spacerItem7, 0, 3, 1, 1)
        self.pb_open_log = QtWidgets.QPushButton(self.groupBox_logging)
        self.pb_open_log.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pb_open_log.setObjectName("pb_open_log")
        self.gridLayout_6.addWidget(self.pb_open_log, 0, 2, 1, 1)
        self.label_logging = QtWidgets.QLabel(self.groupBox_logging)
        self.label_logging.setObjectName("label_logging")
        self.gridLayout_6.addWidget(self.label_logging, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_logging)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.tabWidget.addTab(self.tab_advanced, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.tabWidget, self.spin_priority)
        Dialog.setTabOrder(self.spin_priority, self.spin_duration)
        Dialog.setTabOrder(self.spin_duration, self.cb_notify)
        Dialog.setTabOrder(self.cb_notify, self.pb_change_server_info)
        Dialog.setTabOrder(self.pb_change_server_info, self.pb_font_message_title)
        Dialog.setTabOrder(self.pb_font_message_title, self.pb_font_message_date)
        Dialog.setTabOrder(self.pb_font_message_date, self.pb_font_message_content)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_notifications.setTitle(_translate("Dialog", "Notifications"))
        self.label_notification_duration.setText(_translate("Dialog", "Notification duration:"))
        self.cb_notification_click.setText(_translate("Dialog", "Clicking the notification pop-up opens the main window"))
        self.label_notification_duration_ms.setText(_translate("Dialog", "ms"))
        self.cb_notify.setText(_translate("Dialog", "Show a notification for missed messages after reconnecting"))
        self.label_notification_priority.setText(_translate("Dialog", "Minimum priority to show notifications:"))
        self.cb_tray_icon_unread.setText(_translate("Dialog", "Change the tray icon color when there are unread notifications"))
        self.groupBox_2.setTitle(_translate("Dialog", "Interface"))
        self.label_theme.setText(_translate("Dialog", "Theme:"))
        self.cb_priority_colors.setToolTip(_translate("Dialog", "4..7   -> medium\n"
"8..10 -> high"))
        self.cb_priority_colors.setText(_translate("Dialog", "Show message priority colors"))
        self.groupBox_server_info.setTitle(_translate("Dialog", "Server info"))
        self.pb_change_server_info.setText(_translate("Dialog", "Change server info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_general), _translate("Dialog", "General"))
        self.pb_reset_fonts.setText(_translate("Dialog", "Reset all fonts"))
        self.groupBox_fonts_message.setTitle(_translate("Dialog", "Message"))
        self.pb_font_message_title.setText(_translate("Dialog", "Title"))
        self.pb_font_message_date.setText(_translate("Dialog", "Date"))
        self.pb_font_message_content.setText(_translate("Dialog", "Message"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fonts), _translate("Dialog", "Fonts"))
        self.groupBox.setTitle(_translate("Dialog", "Settings"))
        self.pb_reset.setText(_translate("Dialog", "Reset"))
        self.pb_import.setText(_translate("Dialog", "Import"))
        self.pb_export.setText(_translate("Dialog", "Export"))
        self.groupbox_image_popup.setTitle(_translate("Dialog", "Image pop-up for URLs"))
        self.label.setToolTip(_translate("Dialog", "Maximum pop-up width"))
        self.label.setText(_translate("Dialog", "Width"))
        self.spin_popup_w.setToolTip(_translate("Dialog", "Maximum pop-up width"))
        self.label_2.setToolTip(_translate("Dialog", "Maximum pop-up height"))
        self.label_2.setText(_translate("Dialog", "Height"))
        self.spin_popup_h.setToolTip(_translate("Dialog", "Maximum pop-up height"))
        self.groupBox_cache.setTitle(_translate("Dialog", "Cache"))
        self.pb_clear_cache.setText(_translate("Dialog", "Clear"))
        self.pb_open_cache_dir.setText(_translate("Dialog", "Open"))
        self.label_cache.setText(_translate("Dialog", "TextLabel"))
        self.groupBox_logging.setTitle(_translate("Dialog", "Logging"))
        self.pb_open_log.setToolTip(_translate("Dialog", "Open logfile"))
        self.pb_open_log.setText(_translate("Dialog", "..."))
        self.label_logging.setText(_translate("Dialog", "Level"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_advanced), _translate("Dialog", "Advanced"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
