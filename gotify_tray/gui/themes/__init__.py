from PyQt6 import QtWidgets


def set_theme(app: QtWidgets.QApplication, theme: str = "default"):
    if theme == "default":
        from . import default

        app.setPalette(default.palette())
    elif theme == "dark":
        from . import dark

        app.setPalette(dark.palette())
