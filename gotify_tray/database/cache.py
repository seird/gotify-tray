import glob
import logging
import os
import uuid

import requests

from PyQt6 import QtCore

from .database import Database

logger = logging.getLogger("gotify-tray")


class Cache(object):
    def __init__(self):
        self.database = Database("cache")
        self.cursor = self.database.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS cache (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            url       TEXT,
            filename  TEXT,
            cached_on TEXT)
        """
        )

        # create a directory to store cached files
        path = QtCore.QStandardPaths.standardLocations(
            QtCore.QStandardPaths.StandardLocation.CacheLocation
        )[0]
        self.cache_dir = os.path.join(path, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def clear(self):
        self.cursor.execute("DELETE FROM cache")
        self.database.commit()

        if not self.cache_dir:
            logger.error("Cache directory is empty.")
            return

        for filename in glob.glob(self.cache_dir + "/*"):
            os.remove(filename)

    def lookup(self, key: str) -> str:
        if q := self.cursor.execute(
            "SELECT filename FROM cache WHERE url=?", (key,)
        ).fetchone():
            # Cache hit
            return q["filename"] if os.path.exists(q["filename"]) else ""
        else:
            # Cache miss
            return ""

    def store(self, key: str, response: requests.Response) -> str:
        # Create a file and store the response contents
        filepath = os.path.join(self.cache_dir, uuid.uuid4().hex)

        with open(filepath, "wb") as f:
            f.write(response.content)

        self.cursor.execute(
            "INSERT INTO cache (url, filename, cached_on) VALUES(?, ?, datetime('now', 'localtime'))",
            (key, filepath),
        )
        self.database.commit()
        return filepath
