#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "Call the script with the desired fpm output type [deb, pacman, ...]"
	exit
fi

rm -rf build/linux

pyinstaller gotify-tray.spec

mkdir -p build/linux/opt
mkdir -p build/linux/usr/share/applications
mkdir -p build/linux/usr/share/icons

cp -r dist/gotify-tray build/linux/opt/gotify-tray
cp gotify_tray/gui/images/logo.ico build/linux/usr/share/icons/gotify-tray.ico
cp gotifytray.desktop build/linux/usr/share/applications

find build/linux/opt/gotify-tray -type f -exec chmod 644 -- {} +
find build/linux/opt/gotify-tray -type d -exec chmod 755 -- {} +
find build/linux/usr/share -type f -exec chmod 644 -- {} +
chmod +x build/linux/opt/gotify-tray/gotify-tray

fpm --verbose \
    -C build/linux \
    -s dir \
    -t $1 \
    -p dist/ \
    -n gotify-tray \
    --url https://github.com/seird/gotify-tray \
    -m k.dries@protonmail.com \
    --description "Gotify Tray. A tray notification application for receiving messages from a Gotify server." \
    --category internet \
    --version "$(cat version.txt)" \
    --license GPLv3
