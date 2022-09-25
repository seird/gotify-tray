# -*- mode: python -*-

import platform

block_cipher = None

logo = "gotify_tray/gui/images/logo.ico" if platform.system() != "Darwin" else "gotify_tray/gui/images/logo-macos.ico"

a = Analysis(['gotify_tray/__main__.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('gotify_tray/gui/images', 'gotify_tray/gui/images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gotify-tray',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          version='version.py',
          icon=logo)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gotify-tray')

if platform.system() == "Darwin":
    app = BUNDLE(coll,
                name='Gotify Tray.app',
                icon=logo,
                bundle_identifier=None)
