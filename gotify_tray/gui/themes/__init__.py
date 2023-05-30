from PyQt6 import QtCore, QtGui, QtWidgets
from gotify_tray.utils import get_abs_path


themes = {
    QtCore.Qt.ColorScheme.Dark: "dark",
    QtCore.Qt.ColorScheme.Light: "light",
    QtCore.Qt.ColorScheme.Unknown: "light",
}


def set_theme(app: QtWidgets.QApplication):
    theme = themes.get(app.styleHints().colorScheme(), "light")

    stylesheet = ""
    with open(get_abs_path(f"gotify_tray/gui/themes/base.qss"), "r") as f:
        stylesheet += f.read()
    with open(get_abs_path(f"gotify_tray/gui/themes/{theme}/style.qss"), "r") as f:
        stylesheet += f.read()

    app.setPalette(QtGui.QPalette())
    app.setStyleSheet(stylesheet)


def get_theme_file(file: str) -> str:
    app = QtCore.QCoreApplication.instance()
    theme = themes.get(app.styleHints().colorScheme(), "light")
    return get_abs_path(f"gotify_tray/gui/themes/{theme}/{file}")
