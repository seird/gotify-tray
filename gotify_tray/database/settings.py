from typing import Any
from .default_settings import DEFAULT_SETTINGS


from PyQt6 import QtCore


class Settings(QtCore.QSettings):
    def value(self, key: str, defaultValue: Any = None, type: Any = None) -> Any:
        if type:
            return super().value(key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key), type=type)
        else:
            return super().value(key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key))
