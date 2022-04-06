import os
from pathlib import Path

from ..__version__ import __title__


DEFAULT_SETTINGS = {
    "message/check_missed/notify": True,
    "logging/level": "Disabled",
    "export/path": os.path.join(
        Path.home(), f"{__title__.replace(' ', '-').lower()}-settings.bytes"
    ),
    "shortcuts/quit": "Ctrl+Q",
    "tray/notifications/priority": 5,
    "tray/notifications/duration_ms": 5000,
    "tray/notifications/icon/show": True,
    "watchdog/interval/s": 60,
    "MessageWidget/image/size": 33,
    "MessageWidget/font/title": "Noto Sans,12,-1,5,75,0,0,0,0,0,Bold",
    "MessageWidget/font/date": "Noto Sans,11,-1,5,50,1,0,0,0,0,Italic",
    "MessageWidget/font/message": "Noto Sans,11,-1,5,50,0,0,0,0,0,Regular",
    "ApplicationItem/font": "Noto Sans,10,-1,5,50,0,0,0,0,0,Regular",
    "MainWindow/font/application": "Noto Sans,13,-1,5,75,0,0,0,0,0,Bold",
    "MainWindow/label/size": 25,
    "MainWindow/button/size": 33,
    "MainWindow/application/icon/size": 40,
}
