build: clean
	pip install -r requirements.txt
	pip install pyinstaller
	pyinstaller gotify-tray.spec
	cp -r debian build/debian
	mkdir build/debian/usr/lib
	cp -r dist/gotify-tray build/debian/usr/lib/gotify-tray
	dpkg -b build/debian dist/gotify-tray_amd64.deb

build-macos: clean
	pip install -r requirements.txt
	pip install pyinstaller
	pip install Pillow
	pyinstaller gotify-tray.spec

install: build
	sudo dpkg -i dist/gotify-tray_amd64.deb

uninstall:
	sudo dpkg -r gotify-tray

clean:
	rm -rf dist build
