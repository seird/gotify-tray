import json
import logging

from PyQt6 import QtCore
from PyQt6 import QtNetwork, QtWebSockets

from .models import GotifyMessageModel


logger = logging.getLogger("gotify-tray")


class Listener(QtWebSockets.QWebSocket):
    new_message = QtCore.pyqtSignal(GotifyMessageModel)
    opened = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal()

    def __init__(self, url: str, client_token: str):
        super(Listener, self).__init__()

        self.update_auth(url, client_token)

        self.connected.connect(self._on_connect)
        self.disconnected.connect(self._on_disconnect)
        self.error.connect(self._on_error)
        self.textMessageReceived.connect(self._on_message)

        self.reset_wait_time()

    def update_auth(self, url: str, client_token: str):
        self.qurl = QtCore.QUrl(url.rstrip("/") + "/")
        self.qurl.setScheme("wss" if self.qurl.scheme() == "https" else "ws")
        self.qurl.setPath(self.qurl.path() + "stream")
        self.qurl.setQuery(f"token={client_token}")

    def start(self):
        logger.debug("Opening connection.")
        self.open(self.qurl)

    def stop(self):
        logger.debug("Stopping listener.")
        self.close()

    def reconnect(self):
        self.increase_wait_time()
        QtCore.QTimer.singleShot(self.wait_time * 1000, self.start)

    def is_connected(self) -> bool:
        return self.state() == QtNetwork.QAbstractSocket.SocketState.ConnectedState

    def reset_wait_time(self):
        self.wait_time = 0

    def increase_wait_time(self):
        if self.wait_time == 0:
            self.wait_time = 1
        else:
            self.wait_time = min(self.wait_time * 2, 10 * 60)

    def _on_connect(self):
        logger.debug("Connection established.")
        self.reset_wait_time()
        self.opened.emit()

    def _on_disconnect(self):
        logger.debug(f"Connection was closed: {self.closeCode()}.")
        self.closed.emit()

    def _on_message(self, message: str):
        self.new_message.emit(GotifyMessageModel(json.loads(message)))

    def _on_error(self):
        logger.error(f"Listener socket error: {self.errorString()}")
