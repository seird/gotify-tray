
<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=seird&project=gotify-tray&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

# Gotify Tray


A tray notification application for receiving messages from a [Gotify server](https://github.com/gotify/server).


## Getting started


- [Download the latest release.](https://github.com/seird/gotify-tray/releases/latest)

- or, install via pip:
    ```shell
    $ pip install gotify-tray
    ```

- or, run from source:
    ```shell
    $ pip install -r requirements.txt
    $ python -m gotify_tray
    ```


## Features

- Receive gotify messages in the native notification area.
- Reconnect after wake from sleep or losing network connection.
- Disable notification banners for low priority messages.
- Manually delete received messages.
- Go through a history of all previously received messages.
- Receive missed messages after losing network connection.


## Images


### Main window

Default                                         |  Dark                                                      
:-------------------------------------------------:|:---------------------------------------------------------:
![main window default](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/main_default.png)            |  ![main window dark](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/main_dark.png)


### Notification banners

Windows 10                                         |  KDE                                                      |  MacOS 12
:-------------------------------------------------:|:---------------------------------------------------------:|:---------------------------------------------------------:
![notification](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/notification.png)            |  ![kde_notification](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/kde_notification.png)      |  ![macos_notification](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/macos_notification.png)
![notification](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/notification_centre.png)     |  ![kde_notification](https://raw.githubusercontent.com/seird/gotify-tray/develop/images/kde_notification_centre.png) |  


## Build instructions

See [BUILDING](BUILDING.md).


## Requirements

- python >=3.10
