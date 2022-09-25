import os
import platform
import re
import subprocess

from pathlib import Path


def verify_server(force_new: bool = False, enable_import: bool = True) -> bool:
    from gotify_tray.gui import ServerInfoDialog
    from gotify_tray.database import Settings

    settings = Settings("gotify-tray")

    url = settings.value("Server/url", type=str)
    token = settings.value("Server/client_token", type=str)

    if not url or not token or force_new:
        dialog = ServerInfoDialog(url, token, enable_import)
        if dialog.exec():
            settings.setValue("Server/url", dialog.line_url.text())
            settings.setValue("Server/client_token", dialog.line_token.text())
            return True
        else:
            return False
    else:
        return True


def convert_links(text):
    _link = re.compile(
        r'(?:(https://|http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)',
        re.I,
    )

    def replace(match):
        groups = match.groups()
        protocol = groups[0] or ""  # may be None
        www_lead = groups[1] or ""  # may be None
        return '<a href="http://{1}{2}" rel="nofollow">{0}{1}{2}</a>{3}{4}'.format(
            protocol, www_lead, *groups[2:]
        )

    return _link.sub(replace, text)


def get_abs_path(s) -> str:
    h = Path(__file__).parent.parent
    p = Path(s)
    return os.path.join(h, p).replace("\\", "/")


def open_file(filename: str):
    if platform.system() == "Linux":
        subprocess.call(["xdg-open", filename])
    elif platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filename])


def get_icon(name: str) -> str:
    if platform.system() == "Darwin":
        name += "-macos"

    return get_abs_path(f"gotify_tray/gui/images/{name}.png")
