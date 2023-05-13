import logging
from PyQt6 import QtCore, QtGui, QtWidgets
from gotify_tray.utils import get_abs_path
from . import default, dark_purple, light_purple
from gotify_tray.database import Settings


settings = Settings("gotify-tray")
logger = logging.getLogger("gotify-tray")


themes = {
    "default": default,
    "automatic": None,
    "dark purple": dark_purple,
    "light purple": light_purple,
}


def get_themes():
    return themes.keys()


def is_dark_mode(app: QtWidgets.QApplication) -> bool:
    return app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark


def is_valid_theme(theme: str) -> bool:
    return theme in get_themes()


def set_theme(app: QtWidgets.QApplication, theme: str = "automatic"):
    if not is_valid_theme(theme):
        logger.warning(f"set_theme: theme {theme} is unsupported.")
        theme = "automatic"

    if theme == "automatic":
        theme = "dark purple" if is_dark_mode(app) else "light purple"

    stylesheet = ""
    with open(get_abs_path(f"gotify_tray/gui/themes/{theme.replace(' ', '_')}/style.qss"), "r") as f:
        stylesheet += f.read()

    app.setPalette(themes[theme].get_palette())
    app.setStyleSheet(stylesheet)


def get_theme_file(app: QtWidgets.QApplication, file: str, theme: str | None = None) -> str:
    theme = settings.value("theme", type=str) if not theme else theme

    if not is_valid_theme(theme):
        logger.warning(f"set_theme: theme {theme} is unsupported.")
        theme = "automatic"

    if theme in ("automatic", "default"):
        theme = "dark purple" if is_dark_mode(app) else "light purple"

    return get_abs_path(f"gotify_tray/gui/themes/{theme.replace(' ', '_')}/{file}")
