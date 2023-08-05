import logging

import requests

from PyQt6 import QtCore

from .listener import Listener
from .models import (
    GotifyApplicationModel,
    GotifyErrorModel,
    GotifyHealthModel,
    GotifyMessageModel,
    GotifyPagedMessagesModel,
    GotifyPagingModel,
    GotifyVersionModel,
)

logger = logging.getLogger("gotify-tray")


class GotifySession(QtCore.QObject):
    def __init__(self, url: str, token: str):
        super(GotifySession, self).__init__()
        self.session = requests.Session()
        self.update_auth(url.rstrip("/"), token)

    def update_auth(self, url: str | None = None, token: str | None = None):
        if url:
            self.url = url
        if token:
            self.token = token
            self.session.headers.update({"X-Gotify-Key": token})

    def _get(self, endpoint: str = "/", **kwargs) -> requests.Response:
        return self.session.get(self.url + endpoint, **kwargs)

    def _post(self, endpoint: str = "/", **kwargs) -> requests.Response:
        return self.session.post(self.url + endpoint, **kwargs)

    def _put(self, endpoint: str = "/", **kwargs) -> requests.Response:
        return self.session.put(self.url + endpoint, **kwargs)

    def _delete(self, endpoint: str = "/", **kwargs) -> requests.Response:
        return self.session.delete(self.url + endpoint, **kwargs)


# For sending messages


class GotifyApplication(GotifySession):
    def push(
        self, title: str = "", message: str = "", priority: int = 0, extras: dict | None = None
    ) -> GotifyMessageModel | GotifyErrorModel:
        response = self._post(
            "/message",
            json={
                "title": title,
                "message": message,
                "priority": priority,
                "extras": extras,
            },
        )
        return (
            GotifyMessageModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )


# For everything else


class GotifyClient(GotifySession):
    new_message = QtCore.pyqtSignal(GotifyMessageModel)
    opened = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal()

    def __init__(self, url: str, client_token: str):
        self.listener = Listener(url, client_token)

        super(GotifyClient, self).__init__(url, client_token)

        self.listener.opened.connect(self.opened.emit)
        self.listener.closed.connect(self.closed.emit)
        self.listener.new_message.connect(self.new_message.emit)

    def update_auth(self, url: str | None = None, token: str | None = None):
        super().update_auth(url, token)
        self.listener.update_auth(url, token)


    """
    Application
    """

    def get_applications(self) -> list[GotifyApplicationModel] | GotifyErrorModel:
        response = self._get("/application")
        return (
            [GotifyApplicationModel(x) for x in response.json()]
            if response.ok
            else GotifyErrorModel(response)
        )

    def create_application(
        self, name: str, description: str = ""
    ) -> GotifyApplicationModel | GotifyErrorModel:
        response = self._post(
            "/application", json={"name": name, "description": description}
        )
        return (
            GotifyApplicationModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )

    def update_application(
        self, application_id: int, name: str, description: str = ""
    ) -> GotifyApplicationModel | GotifyErrorModel:
        response = self._put(
            f"/application/{application_id}",
            json={"name": name, "description": description},
        )
        return (
            GotifyApplicationModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )

    def delete_application(self, application_id: int) -> None | GotifyErrorModel:
        response = self._delete(f"/application/{application_id}")
        return None if response.ok else GotifyErrorModel(response)

    def upload_application_image(
        self, application_id: int, img_path: str
    ) -> GotifyApplicationModel | GotifyErrorModel | None:
        try:
            with open(img_path, "rb") as f:
                response = self._post(
                    f"/application/{application_id}/image", files={"file": f}
                )
            return (
                GotifyApplicationModel(response.json())
                if response.ok
                else GotifyErrorModel(response)
            )
        except FileNotFoundError:
            logger.error(
                f"GotifyClient.upload_application_image: image '{img_path}' not found."
            )
            return None

    def delete_application_image(self, application_id: int) -> None | GotifyErrorModel:
        response = self._delete(f"/application/{application_id}/image")
        return None if response.ok else GotifyErrorModel(response)

    """
    Message
    """

    def get_application_messages(
        self, application_id: int, limit: int = 100, since: int | None = None
    ) -> GotifyPagedMessagesModel | GotifyErrorModel:
        response = self._get(
            f"/application/{application_id}/message",
            params={"limit": limit, "since": since},
        )
        if not response.ok:
            return GotifyErrorModel(response)
        j = response.json()
        return GotifyPagedMessagesModel(
            messages=[GotifyMessageModel(m) for m in j["messages"]],
            paging=GotifyPagingModel(j["paging"]),
        )

    def delete_application_messages(self, application_id: int) -> None | GotifyErrorModel:
        response = self._delete(f"/application/{application_id}/message")
        return None if response.ok else GotifyErrorModel(response)

    def get_messages(
        self, limit: int = 100, since: int | None = None
    ) -> GotifyPagedMessagesModel | GotifyErrorModel:
        response = self._get("/message", params={"limit": limit, "since": since})
        if not response.ok:
            return GotifyErrorModel(response)
        j = response.json()
        return GotifyPagedMessagesModel(
            messages=[GotifyMessageModel(m) for m in j["messages"]],
            paging=GotifyPagingModel(j["paging"]),
        )

    def delete_messages(self) -> None | GotifyErrorModel:
        response = self._delete("/message")
        return None if response.ok else GotifyErrorModel(response)

    def delete_message(self, message_id: int) -> None | GotifyErrorModel:
        response = self._delete(f"/message/{message_id}")
        return None if response.ok else GotifyErrorModel(response)

    def listen(self):
        self.listener.start()

    def reconnect(self):
        self.listener.reconnect()

    def quit(self):
        """Close the listener and disconnect from the closed signal so it doesn't get reopened
        """
        try:
            self.listener.closed.disconnect()
        except TypeError:
            logger.error(f"listener.closed was already disconnected.")
        self.listener.close()

    def stop(self):
        self.listener.close()

    def is_listening(self) -> bool:
        return self.listener.is_connected()

    def reset_wait_time(self):
        self.listener.reset_wait_time()

    """
    Health
    """

    def health(self) -> GotifyHealthModel | GotifyErrorModel:
        response = self._get("/health")
        return (
            GotifyHealthModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )

    """
    Version
    """

    def version(self) -> GotifyVersionModel | GotifyErrorModel:
        response = self._get("/version")
        return (
            GotifyVersionModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )
