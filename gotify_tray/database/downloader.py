import logging

import requests

from .cache import Cache
from .settings import Settings


logger = logging.getLogger("gotify-tray")
settings = Settings("gotify-tray")


class Downloader(object):
    def __init__(self):
        self.cache = Cache()
        self.session = requests.Session()

    def get(self, url: str) -> requests.Response:
        """
        Get the response of an http get request.
        Bypasses the cache.
        """
        return self.session.get(url)

    def get_filename(self, url: str) -> str:
        """
        Get the content of an http get request, as a filename.
        """
        if filename := self.cache.lookup(url):
            return filename

        try:
            response = self.get(url)
        except Exception as e:
            logger.error(f"get_filename: downloading {url} failed.: {e}")
            return ""

        return self.cache.store(url, response) if response.ok else ""
