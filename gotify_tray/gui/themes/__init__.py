import logging
from PyQt6 import QtGui, QtWidgets
from gotify_tray.utils import get_abs_path
from . import default, dark_purple, light_purple
from gotify_tray.database import Settings


settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")


styles = {
    "default": default,
    "dark purple": dark_purple,
    "light purple": light_purple,
}


def set_theme(app: QtWidgets.QApplication, style: str = "default"):    
    if style not in styles.keys():
        logger.error(f"set_style: style {style} is unsupported.")
        return

    stylesheet = ""
    with open(get_abs_path(f"gotify_tray/gui/themes/{style.replace(' ', '_')}/style.qss"), "r") as f:
        stylesheet += f.read()

    app.setPalette(styles[style].get_palette())
    app.setStyleSheet(stylesheet)

def get_themes():
    return styles.keys()
    
def get_theme_file(file: str, theme: str = None) -> str:
    theme = settings.value("theme", type=str) if not theme else theme
    return get_abs_path(f"gotify_tray/gui/themes/{theme.replace(' ', '_')}/{file}")
