import json
import logging
import platform
import ssl

import websocket
from PyQt6 import QtCore

from .models import GotifyMessageModel, GotifyErrorModel


logger = logging.getLogger("gotify-tray")


class Listener(QtCore.QThread):
    new_message = QtCore.pyqtSignal(GotifyMessageModel)
    error = QtCore.pyqtSignal(Exception)
    opened = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal(int, str)

    def __init__(self, url: str, client_token: str):
        super(Listener, self).__init__()

        qurl = QtCore.QUrl(url.rstrip("/") + "/")
        qurl.setScheme("wss" if qurl.scheme() == "https" else "ws")
        qurl.setPath(qurl.path() + "stream")
        qurl.setQuery(f"token={client_token}")

        self.ws = websocket.WebSocketApp(
            qurl.toString(),
            on_message=self._on_message,
            on_error=self._on_error,
            on_open=self._on_open,
            on_close=self._on_close,
        )

        self.wait_time = 0

        self.running = False

    def reset_wait_time(self):
        self.wait_time = 0

    def increase_wait_time(self):
        if self.wait_time == 0:
            self.wait_time = 1
        else:
            self.wait_time = min(self.wait_time * 2, 10 * 60)

    def _on_message(self, ws: websocket.WebSocketApp, message: str):
        self.new_message.emit(GotifyMessageModel(json.loads(message)))

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception):
        logger.error(f"websocket error: {error}")
        self.error.emit(error)

    def _on_open(self, ws: websocket.WebSocketApp):
        self.opened.emit()
        self.reset_wait_time()

    def _on_close(
        self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str
    ):
        self.closed.emit(close_status_code, close_msg)

    def stop_final(self):
        def dummy(*args):
            ...

        self.ws.on_close = dummy
        self.ws.close()
        self.running = False

    def stop(self):
        logger.debug("Listener: stopping.")
        self.ws.close()
        self.running = False

    def run(self):
        self.running = True
        try:
            if platform.system() == "Darwin":
                self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            else:
                self.ws.run_forever()
        finally:
            logger.debug("Listener: stopped.")
            self.running = False
