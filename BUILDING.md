## Get the source and install the requirements:

```shell
$ git clone https://github.com/seird/gotify-tray.git
$ cd gotify-tray
$ pip install -r requirements.txt
```


### Run from source

```shell
$ python -m gotify_tray
```

### Create a pyinstaller executable

```shell
$ pip install pyinstaller
$ pyinstaller gotify-tray.spec
```
An executable is created at `dist/gotify-tray/`.

### Create a macos .app

```shell
$ pip install pyinstaller Pillow
$ pyinstaller gotify-tray.spec
```

### Inno setup (Windows)

Create an installer for windows with inno setup from pyinstaller output:

```shell
$ iscc gotify-tray.iss
```

### Create and install a pip package

- Create the pip package:
    ```shell
    $ python -m build
    ```

- Install the pip package:
    ```shell
    $ pip install dist/gotify_tray-0.1.14-py3-none-any.whl
    ```

- Launch:
    ```shell
    $ gotify-tray
    ```

### Create a deb package

```shell
$ make build

# or install

$ sudo make install
```