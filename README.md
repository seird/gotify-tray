# Gotify Tray


A tray notification application for receiving messages from a [Gotify server](https://github.com/gotify/server).


[![logo](https://raw.githubusercontent.com/gotify/logo/master/gotify-logo.png)](https://github.com/gotify/logo)

## Download


[Download the latest release.](https://github.com/seird/gotify-tray/releases/latest)


## Install

Get the source and install the requirements:

```
$ git clone https://github.com/seird/gotify-tray.git
$ cd gotify-tray
$ pip install -r requirements.txt
```

### Run from source

```
$ python entry_point.py
```

### Create a pyinstaller executable

```
$ pip install pyinstaller==4.4
$ pyinstaller gotify-tray.spec
```
An executable is created at `dist/gotify-tray/`.


### Create a deb package

```
$ make build

# or install

$ sudo make install
```

### (Inno setup (Windows))

Create an installer for windows with inno setup:

```
$ iscc gotify-tray.iss
```


## Images

![notification](images/notification.png)

![main_window](images/main_window.png)

![notification_centre](images/notification_centre.png)



## Requirements

- python 3.9
- PyQt6
- requests
- websocket-client
