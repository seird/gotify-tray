build-macos: clean
	pip install -r requirements.txt
	pip install pyinstaller
	pip install Pillow
	pyinstaller gotify-tray.spec

clean:
	rm -rf dist build
