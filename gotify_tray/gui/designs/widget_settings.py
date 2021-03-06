# Form implementation generated from reading ui file 'gotify_tray/gui/designs\widget_settings.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(384, 274)
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
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.spin_duration = QtWidgets.QSpinBox(self.groupBox_5)
        self.spin_duration.setMinimum(500)
        self.spin_duration.setMaximum(30000)
        self.spin_duration.setSingleStep(100)
        self.spin_duration.setObjectName("spin_duration")
        self.gridLayout_4.addWidget(self.spin_duration, 1, 1, 1, 1)
        self.spin_priority = QtWidgets.QSpinBox(self.groupBox_5)
        self.spin_priority.setMinimum(1)
        self.spin_priority.setMaximum(10)
        self.spin_priority.setProperty("value", 5)
        self.spin_priority.setObjectName("spin_priority")
        self.gridLayout_4.addWidget(self.spin_priority, 0, 1, 1, 1)
        self.cb_notify = QtWidgets.QCheckBox(self.groupBox_5)
        self.cb_notify.setObjectName("cb_notify")
        self.gridLayout_4.addWidget(self.cb_notify, 2, 0, 1, 3)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pb_change_server_info = QtWidgets.QPushButton(self.groupBox_4)
        self.pb_change_server_info.setObjectName("pb_change_server_info")
        self.gridLayout_3.addWidget(self.pb_change_server_info, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_general, "")
        self.tab_fonts = QtWidgets.QWidget()
        self.tab_fonts.setObjectName("tab_fonts")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_fonts)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_fonts)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layout_fonts_message = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.layout_fonts_message.setContentsMargins(4, 4, 4, 4)
        self.layout_fonts_message.setSpacing(6)
        self.layout_fonts_message.setObjectName("layout_fonts_message")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_font_message_title = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_font_message_title.setObjectName("pb_font_message_title")
        self.horizontalLayout.addWidget(self.pb_font_message_title)
        self.pb_font_message_date = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_font_message_date.setObjectName("pb_font_message_date")
        self.horizontalLayout.addWidget(self.pb_font_message_date)
        self.pb_font_message_content = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_font_message_content.setObjectName("pb_font_message_content")
        self.horizontalLayout.addWidget(self.pb_font_message_content)
        self.layout_fonts_message.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.tabWidget.addTab(self.tab_fonts, "")
        self.tab_advanced = QtWidgets.QWidget()
        self.tab_advanced.setObjectName("tab_advanced")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_advanced)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pb_export = QtWidgets.QPushButton(self.groupBox)
        self.pb_export.setObjectName("pb_export")
        self.verticalLayout_2.addWidget(self.pb_export)
        self.pb_import = QtWidgets.QPushButton(self.groupBox)
        self.pb_import.setObjectName("pb_import")
        self.verticalLayout_2.addWidget(self.pb_import)
        self.pb_reset = QtWidgets.QPushButton(self.groupBox)
        self.pb_reset.setObjectName("pb_reset")
        self.verticalLayout_2.addWidget(self.pb_reset)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_advanced)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_7)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 0, 0, 1, 1)
        self.combo_logging = QtWidgets.QComboBox(self.groupBox_7)
        self.combo_logging.setObjectName("combo_logging")
        self.gridLayout_6.addWidget(self.combo_logging, 0, 1, 1, 1)
        self.pb_open_log = QtWidgets.QPushButton(self.groupBox_7)
        self.pb_open_log.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pb_open_log.setObjectName("pb_open_log")
        self.gridLayout_6.addWidget(self.pb_open_log, 0, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(190, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_6.addItem(spacerItem4, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_7)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
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
        self.groupBox_5.setTitle(_translate("Dialog", "Notifications"))
        self.label_6.setText(_translate("Dialog", "ms"))
        self.label_4.setText(_translate("Dialog", "Minimum priority to show notifications:"))
        self.label_5.setText(_translate("Dialog", "Notification duration:"))
        self.cb_notify.setText(_translate("Dialog", "Show a notification for missed messages after reconnecting"))
        self.groupBox_4.setTitle(_translate("Dialog", "Server info"))
        self.pb_change_server_info.setText(_translate("Dialog", "Change server info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_general), _translate("Dialog", "General"))
        self.groupBox_2.setTitle(_translate("Dialog", "Message"))
        self.pb_font_message_title.setText(_translate("Dialog", "Title"))
        self.pb_font_message_date.setText(_translate("Dialog", "Date"))
        self.pb_font_message_content.setText(_translate("Dialog", "Message"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fonts), _translate("Dialog", "Fonts"))
        self.groupBox.setTitle(_translate("Dialog", "Settings"))
        self.pb_export.setText(_translate("Dialog", "Export"))
        self.pb_import.setText(_translate("Dialog", "Import"))
        self.pb_reset.setText(_translate("Dialog", "Reset"))
        self.groupBox_7.setTitle(_translate("Dialog", "Logging"))
        self.label_7.setText(_translate("Dialog", "Level"))
        self.pb_open_log.setToolTip(_translate("Dialog", "Open logfile"))
        self.pb_open_log.setText(_translate("Dialog", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_advanced), _translate("Dialog", "Advanced"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
