echo "Creating executable"


try {C:/Python39/Scripts/pyinstaller gotify-tray.spec}
catch {pyinstaller gotify-tray.spec}

echo "Creating installer"
iscc gotify-tray.iss
