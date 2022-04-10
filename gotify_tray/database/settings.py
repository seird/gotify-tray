import pickle
from typing import Any
from .default_settings import DEFAULT_SETTINGS


from PyQt6 import QtCore


class Settings(QtCore.QSettings):
    def value(self, key: str, defaultValue: Any = None, type: Any = None) -> Any:
        if type:
            return super().value(
                key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key), type=type
            )
        else:
            return super().value(
                key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key)
            )

    def export(self, path: str):
        data = {
            key: self.value(key)
            for key in self.allKeys()
            if not (  # skip settings that might not translate well between platforms
                isinstance(self.value(key), QtCore.QByteArray)
                or key == "export/path"
                or key == "message/last"
            )
        }

        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            data = pickle.load(f)

        self.clear()

        for key in data:
            self.setValue(key, data[key])
