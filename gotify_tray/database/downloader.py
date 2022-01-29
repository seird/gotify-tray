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
        self.session.proxies.update(
            {
                "https": settings.value("proxies/https", type=str),
                "http": settings.value("proxies/http", type=str),
            }
        )

    def get(self, url: str) -> requests.Response:
        """
        Get the response of an http get request.
        Bypasses the cache.
        """
        return self.session.get(url)

    def get_bytes(self, url: str, cached: bool = True, add_time: bool = True) -> bytes:
        """
        Get the content of an http get request, as bytes.
        Optionally use the cache.
        """
        if cached:
            # Retrieve from cache
            filename = self.cache.lookup(url)
            if filename:
                with open(filename, "rb") as f:
                    return f.read()

        try:
            response = self.get(url)
        except Exception as e:
            logger.error(f"get_bytes: downloading {url} failed.: {e}")
            return b""

        if not response.ok:
            return b""

        if cached:
            # Store in cache
            self.cache.store(url, response, add_time=add_time)

        return response.content

    def get_filename(
        self, url: str, retrieve_from_cache: bool = True, add_time: bool = True
    ) -> str:
        """
        Get the content of an http get request, as a filename.
        """
        if retrieve_from_cache:
            filename = self.cache.lookup(url)
            if filename:
                return filename

        try:
            response = self.get(url)
        except Exception as e:
            logger.error(f"get_filename: downloading {url} failed.: {e}")
            return ""

        if not response.ok:
            return ""

        return self.cache.store(url, response, add_time=add_time)
