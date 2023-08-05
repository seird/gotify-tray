import logging

import requests

from PyQt6 import QtCore


logger = logging.getLogger("gotify-tray")


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
    next: str | None = None
    since: int
    size: int


class GotifyMessageModel(AttributeDict):
    appid: int
    date: QtCore.QDateTime
    extras: dict | None = None
    id: int
    message: str
    priority: int | None = None
    title: str | None = None

    def __init__(self, d: dict, *args, **kwargs):
        d.update(
            {"date": QtCore.QDateTime.fromString(d["date"], format=QtCore.Qt.DateFormat.ISODate).toLocalTime()}
        )
        super(GotifyMessageModel, self).__init__(d, *args, **kwargs)


class GotifyPagedMessagesModel(AttributeDict):
    messages: list[GotifyMessageModel]
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
