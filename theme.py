from PyQt5.QtGui import QPalette, QColor

def apply_theme(window):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Windows-like background
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))    # Black text
    palette.setColor(QPalette.Button, QColor(200, 200, 200))  # Button color
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))    # Button text color
    window.setPalette(palette)