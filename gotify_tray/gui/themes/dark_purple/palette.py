from PyQt6 import QtGui


def get_palette() -> QtGui.QPalette:
    palette = QtGui.QPalette()
    
    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0x3B3B3D))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0x404042))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, QtGui.QColor(0x424242))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0xCACBCE))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0xC8C8C6))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0xCACBCE))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0xC8C8C6))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0x7D7D82))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0x87888C))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor(0x737373))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0x252627))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0x2D2D2F))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(0x333333))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0x27272A))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0x2A2A2D))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, QtGui.QColor(0x343437))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0x2C2C30))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0x2B2B2F))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(0x36363A))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(0x5522a8))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(0xBFBFBF))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0x28282B))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0x28282B))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, QtGui.QColor(0x2B2A2A))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0xB9B9BE))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0x9E9FA5))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(0x73747E))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0x6D29DC))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0x5522a8))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0x5522a8))

    palette.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0xCCCCCC))
    palette.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0xCECECE))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(0x707070))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Light, QtGui.QColor(0x414145))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Midlight, QtGui.QColor(0x39393C))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Mid, QtGui.QColor(0x2F2F32))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Dark, QtGui.QColor(0x202022))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(0x19191A))

    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.Link, QtGui.QColor(0xAE7AFF))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Link, QtGui.QColor(0xAE7AFF))
    palette.setColor(QtGui.QPalette.ColorGroup.All, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(0x5522a8))
    palette.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.LinkVisited, QtGui.QColor(0x6D29DC))

    return palette
