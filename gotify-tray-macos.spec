# -*- mode: python -*-

block_cipher = None

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
          icon='logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gotify-tray')
app = BUNDLE(coll,
             name='Gotify-Tray.app',
             icon='logo.ico',
             bundle_identifier=None)
