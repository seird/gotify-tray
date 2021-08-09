echo "Creating executable"


try {C:/Python39/Scripts/pyinstaller gotify-tray.spec}
catch {pyinstaller gotify-tray.spec}

try {Remove-Item "dist/gotify-tray/opengl32sw.dll"} catch {}

echo "Creating installer"
iscc gotify-tray.iss
