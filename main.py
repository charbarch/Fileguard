import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import FileGuardApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application icon
    app.setWindowIcon(QIcon('FileGuard.ico'))

    # Global dark theme stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #2979ff;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #1e63d9;
        }
        QLabel {
            color: white;
        }
        QMessageBox {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLineEdit {
            background-color: #1c1c1c;
            color: #ffffff;
            border: 1px solid #2979ff;
        }
        QDialog {
            background-color: #1e1e1e;
            color: #c8c8c8;
        }
        QLineEdit {
            background-color: #2e2e2e;
            color: #ffffff;
            border: 1px solid #4682B4;
            border-radius: 5px;
            padding: 5px;
        }
        QLineEdit:focus {
            border: 1px solid #5a9bd3;
            background-color: #3a3a3a;
        }
        QDialogButtonBox {
            background-color: #1e1e1e;
        }
        QPushButton {
            background-color: #3674A3;
            color: white;
            border-radius: 5px;
            padding: 7px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2A5273;
        }
        QPushButton:pressed {
            background-color: #1E3A4C;
        }
    """)

    # Create and show the main window
    window = FileGuardApp()
    window.show()

    # Execute the application
    sys.exit(app.exec_())