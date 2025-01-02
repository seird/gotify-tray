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
        msg = GotifyMessageModel(json.loads(message))
        logger.debug(f"Full message: {msg}")
        
        # Get application filter settings
        from gotify_tray.database import Settings
        settings = Settings("gotify-tray")
        enabled = settings.value("ids_filter/enabled", False, type=bool)
        app_ids = settings.value("ids_filter/ids", [])
        
        logger.debug(f"Application filtering enabled: {enabled}")
        logger.debug(f"Configured application IDs: {app_ids}")
        
        # Check if message should be filtered
        if enabled and app_ids:
            msg_app_id = msg.get("appid")
            logger.debug(f"Message application ID: {msg_app_id}")
            
            # Convert configured app IDs to integers for comparison
            app_ids_int = [int(app_id) for app_id in app_ids]
            
            if msg_app_id in app_ids_int:
                logger.debug(f"Message from appid {msg_app_id} is in blacklist - filtering out")
                return
            logger.debug(f"Message from appid {msg_app_id} is not in blacklist - allowing through")
                
        self.new_message.emit(msg)

    def _on_error(self):
        logger.error(f"Listener socket error: {self.errorString()}")
