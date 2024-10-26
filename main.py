import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import FileGuardApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('images/icon.ico'))

    window = FileGuardApp()
    window.show()
    sys.exit(app.exec_())