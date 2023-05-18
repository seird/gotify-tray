import logging
from PyQt6 import QtCore, QtGui, QtWidgets
from gotify_tray.utils import get_abs_path
from . import default, dark_purple, light_purple
from gotify_tray.database import Settings


settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")


styles = {
    "default": default,
    "automatic": None,
    "dark purple": dark_purple,
    "light purple": light_purple,
}


def automatic_to_theme(app: QtWidgets.QApplication) -> str:
    if app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark:
        return "dark purple"
    else:
        return "light purple"


def set_theme(app: QtWidgets.QApplication, style: str = "automatic"):
    if style not in styles.keys():
        logger.error(f"set_style: style {style} is unsupported.")
        return
    
    if style == "automatic":
        style = automatic_to_theme(app)        

    stylesheet = ""
    with open(get_abs_path(f"gotify_tray/gui/themes/{style.replace(' ', '_')}/style.qss"), "r") as f:
        stylesheet += f.read()

    app.setPalette(styles[style].get_palette())
    app.setStyleSheet(stylesheet)

def get_themes():
    return styles.keys()
    
def get_theme_file(app: QtWidgets.QApplication, file: str, theme: str = None) -> str:
    theme = settings.value("theme", type=str) if not theme else theme
    if theme in ("automatic", "default"):
        theme = automatic_to_theme(app)
    return get_abs_path(f"gotify_tray/gui/themes/{theme.replace(' ', '_')}/{file}")
