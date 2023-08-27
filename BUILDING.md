Get the source and install the requirements:

```shell
$ git clone https://github.com/seird/gotify-tray.git
$ cd gotify-tray
$ pip install -r requirements.txt
$ pip install pyinstaller
```

Currently it's only possible to create installer packages from the pyinstaller output. For any target platform, first create the executable with pyinstaller:

```shell
$ pyinstaller gotify-tray.spec
```


# Windows

## Create an installer with Inno Setup

Create an installer for windows with [inno setup](https://github.com/jrsoftware/issrc) from pyinstaller output:

```shell
$ iscc gotify-tray.iss
```

The installer is created at `inno-output/gotify-tray-installer.exe`.


# Linux

Packages can be created from the pyinstaller output with [fpm](https://fpm.readthedocs.io/). Run the `build_linux.sh` script with the desired package type:

## Create a deb package


```shell
$ ./build_linux.sh deb
```


## Create a pacman package


```shell
$ ./build_linux.sh pacman
```


# MacOS

## Create a macos .app

```shell
$ pip install pyinstaller Pillow
$ pyinstaller gotify-tray.spec
```

# Create and install a pip package

- Create the pip package:
    ```shell
    $ python -m build
    ```

- Install the pip package:
    ```shell
    $ pip install dist/gotify_tray-{{VERSION}}-py3-none-any.whl
    ```

- Launch from the command line:
    ```shell
    $ gotify-tray
    ```
