import logging
import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets

from gotify_tray.__version__ import __title__
from gotify_tray.utils import verify_server


if __name__ == "__main__":
    title = __title__.replace(" ", "-")

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(title)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QtGui.QIcon("gotify_tray/gui/images/gotify-small.png"))
    app.setStyle("fusion")

    logdir = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.StandardLocation.AppDataLocation
    )[0]
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.basicConfig(
        filename=os.path.join(logdir, f"{title}.log"),
        format="%(levelname)s > %(name)s > %(asctime)s > %(message)s",
        level=logging.ERROR,
    )

    # import from gui has to happen after 'setApplicationName' to make sure the correct cache directory is created
    from gotify_tray.gui import MainWindow

    window = MainWindow(app)

    # prevent multiple instances
    if (window.acquire_lock() or "--no-lock" in sys.argv) and verify_server():
        window.init_ui()
        sys.exit(app.exec())
