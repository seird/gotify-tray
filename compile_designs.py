import glob
import os


ui_files = glob.glob("gotify_tray/gui/designs/*.ui")
for ui_file in ui_files:
    fname, _ = os.path.splitext(ui_file)
    os.system(f"pyuic6 -x {ui_file} -o {fname}.py")
