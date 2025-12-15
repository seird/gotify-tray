import os
import platform
from PyQt6 import QtCore, QtWidgets
from gotify_tray.utils import get_abs_path
from gotify_tray.database import Settings


settings = Settings("gotify-tray")


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

    app.setStyleSheet(stylesheet)

    if platform.system() == "Linux" and os.path.isdir("/usr/lib/qt6/plugins"):
        app.addLibraryPath("/usr/lib/qt6/plugins")

    if style_override := settings.value("StyleOverride", type=str):
        app.setStyle(style_override)
    elif platform.system() == "Linux" and "Breeze" in QtWidgets.QStyleFactory.keys():
        app.setStyle("Breeze")
    else:
        app.setStyle("Fusion")

            
def get_theme_file(file: str) -> str:
    app = QtCore.QCoreApplication.instance()
    theme = themes.get(app.styleHints().colorScheme(), "light")
    return get_abs_path(f"gotify_tray/gui/themes/{theme}/{file}")
