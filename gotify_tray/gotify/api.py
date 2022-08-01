import logging
from typing import Callable, List, Optional, Union

import requests

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


class GotifySession(object):
    def __init__(self, url: str, token: str):
        self.session = requests.Session()
        self.update_auth(url.rstrip("/"), token)

    def update_auth(self, url: str = None, token: str = None):
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
    def __init__(self, url: str, application_token: str):
        super(GotifyApplication, self).__init__(url, application_token)

    def push(
        self, title: str = "", message: str = "", priority: int = 0, extras: dict = None
    ) -> Union[GotifyMessageModel, GotifyErrorModel]:
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

    """
    Application
    """

    def get_applications(self) -> Union[List[GotifyApplicationModel], GotifyErrorModel]:
        response = self._get("/application")
        return (
            [GotifyApplicationModel(x) for x in response.json()]
            if response.ok
            else GotifyErrorModel(response)
        )

    def create_application(
        self, name: str, description: str = ""
    ) -> Union[GotifyApplicationModel, GotifyErrorModel]:
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
    ) -> Union[GotifyApplicationModel, GotifyErrorModel]:
        response = self._put(
            f"/application/{application_id}",
            json={"name": name, "description": description},
        )
        return (
            GotifyApplicationModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )

    def delete_application(self, application_id: int) -> bool:
        return self._delete(f"/application/{application_id}").ok

    def upload_application_image(
        self, application_id: int, img_path: str
    ) -> Optional[Union[GotifyApplicationModel, GotifyErrorModel]]:
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

    """
    Message
    """

    def get_application_messages(
        self, application_id: int, limit: int = 100, since: int = None
    ) -> Union[GotifyPagedMessagesModel, GotifyErrorModel]:
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

    def delete_application_messages(self, application_id: int) -> bool:
        return self._delete(f"/application/{application_id}/message").ok

    def get_messages(
        self, limit: int = 100, since: int = None
    ) -> Union[GotifyPagedMessagesModel, GotifyErrorModel]:
        response = self._get("/message", params={"limit": limit, "since": since})
        if not response.ok:
            return GotifyErrorModel(response)
        j = response.json()
        return GotifyPagedMessagesModel(
            messages=[GotifyMessageModel(m) for m in j["messages"]],
            paging=GotifyPagingModel(j["paging"]),
        )

    def delete_messages(self) -> bool:
        return self._delete("/message").ok

    def delete_message(self, message_id: int) -> bool:
        return self._delete(f"/message/{message_id}").ok

    def listen(
        self,
        opened_callback: Callable[[], None] = None,
        closed_callback: Callable[[int, str], None] = None,
        new_message_callback: Callable[[GotifyMessageModel], None] = None,
        error_callback: Callable[[Exception], None] = None,
    ):
        def dummy(*args):
            ...

        self.listener = Listener(self.url, self.token)
        self.listener.opened.connect(lambda: self.opened_callback(opened_callback))
        self.listener.closed.connect(closed_callback or dummy)
        self.listener.new_message.connect(new_message_callback or dummy)
        self.listener.error.connect(error_callback or dummy)
        self.listener.start()

    def opened_callback(self, user_callback: Callable[[], None] = None):
        self.reset_wait_time()
        if user_callback:
            user_callback()

    def reconnect(self):
        if not self.is_listening():
            self.listener.start()

    def stop_final(self):
        self.listener.stop_final()

    def stop(self, reset_wait: bool = False):
        if reset_wait:
            self.reset_wait_time()
        self.listener.stop()

    def is_listening(self) -> bool:
        return self.listener.running

    def increase_wait_time(self):
        self.listener.increase_wait_time()

    def get_wait_time(self) -> int:
        return self.listener.wait_time

    def reset_wait_time(self):
        self.listener.reset_wait_time()

    """
    Health
    """

    def health(self) -> Union[GotifyHealthModel, GotifyErrorModel]:
        response = self._get("/health")
        return (
            GotifyHealthModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )

    """
    Version
    """

    def version(self) -> Union[GotifyVersionModel, GotifyErrorModel]:
        response = self._get("/version")
        return (
            GotifyVersionModel(response.json())
            if response.ok
            else GotifyErrorModel(response)
        )
