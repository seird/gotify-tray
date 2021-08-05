def verify_server(force_new: bool = False) -> bool:
    from gotify_tray.gui import ServerInfoDialog
    from gotify_tray.database import Settings

    settings = Settings("gotify-tray")

    url = settings.value("Server/url", type=str)
    token = settings.value("Server/client_token", type=str)

    if not url or not token or force_new:
        dialog = ServerInfoDialog(url, token)
        if dialog.exec():
            settings.setValue("Server/url", dialog.line_url.text())
            settings.setValue("Server/client_token", dialog.line_token.text())
            return True
        else:
            return False
    else:
        return True
