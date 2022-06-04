import datetime
from dateutil.parser import isoparse
import logging
from typing import List, Optional

import requests


logger = logging.getLogger("gotify-tray")


try:
    local_timezone = datetime.datetime.utcnow().astimezone().tzinfo
except Exception as e:
    logger.error(f"gotify.models.local_timezone error: {e}")
    local_timezone = None


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class GotifyApplicationModel(AttributeDict):
    description: str
    id: int
    image: str
    internal: bool
    name: str
    token: str


class GotifyPagingModel(AttributeDict):
    limit: int
    next: Optional[str] = None
    since: int
    size: int


class GotifyMessageModel(AttributeDict):
    appid: int
    date: datetime.datetime
    extras: Optional[dict] = None
    id: int
    message: str
    priority: Optional[int] = None
    title: Optional[str] = None

    def __init__(self, d: dict, *args, **kwargs):
        d.update(
            {"date": isoparse(d["date"]).astimezone(local_timezone)}
        )
        super(GotifyMessageModel, self).__init__(d, *args, **kwargs)


class GotifyPagedMessagesModel(AttributeDict):
    messages: List[GotifyMessageModel]
    paging: GotifyPagingModel


class GotifyHealthModel(AttributeDict):
    database: str
    health: str


class GotifyVersionModel(AttributeDict):
    buildDate: str
    commit: str
    version: str


class GotifyErrorModel(AttributeDict):
    error: str
    errorCode: int
    errorDescription: str

    def __init__(self, response: requests.Response, *args, **kwargs):
        try:
            j = response.json()
        except ValueError:
            j = {
                "error": "unknown",
                "errorCode": response.status_code,
                "errorDescription": "",
            }

        super(GotifyErrorModel, self).__init__(j, *args, **kwargs)
