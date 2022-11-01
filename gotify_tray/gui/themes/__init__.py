import logging
from PyQt6 import QtGui, QtWidgets
from gotify_tray.utils import get_abs_path
from . import default, dark_purple, light_purple


logger = logging.getLogger("gotify-tray")


styles = {
    "default": default,
    "dark_purple": dark_purple,
    "light_purple": light_purple,
}


def set_theme(app: QtWidgets.QApplication, style: str = "default"):
    app.setStyle("fusion")
    
    if style not in styles.keys():
        logger.error(f"set_style: style {style} is unsupported.")
        return

    stylesheet = ""
    with open(get_abs_path(f"gotify_tray/gui/themes/{style}/style.qss"), "r") as f:
        stylesheet += f.read()
    # with open(get_abs_path(f"gotify_tray/gui/themes/{style}/MainWindow.css"), "r") as f:
    #     s = f.read()
    #     s = s.replace("gotify_tray", get_abs_path("gotify_tray"))
    #     stylesheet += s

    app.setPalette(styles[style].get_palette())
    app.setStyleSheet(stylesheet)
    
def get_theme_file(file: str, theme: str) -> str:
    return get_abs_path(f"gotify_tray/gui/themes/{theme}/{file}")
