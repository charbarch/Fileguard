import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from encryption import encrypt_file, decrypt_file, encrypt_folder, decrypt_folder

class FileGuardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileGuard")
        self.setGeometry(300, 300, 600, 400)
        self.setAcceptDrops(True)  # Enable drag and drop functionality
        self.setStyleSheet("""
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
        """)

        self.file_path = None
        self.setup_ui()

    # Setting up the main UI components
    def setup_ui(self):
        layout = QVBoxLayout()

        # Encrypt and Decrypt buttons
        button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.clicked.connect(self.encrypt)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt", self)
        self.decrypt_button.clicked.connect(self.decrypt)
        button_layout.addWidget(self.decrypt_button)

        layout.addLayout(button_layout)

        # Drag and drop area label
        self.drop_area_label = QLabel("Drag n Drop or Click to Pick", self)
        self.drop_area_label.setStyleSheet("border: 2px dashed #ffffff; color: #ffffff; padding: 20px;")
        self.drop_area_label.setAlignment(Qt.AlignCenter)
        self.drop_area_label.mousePressEvent = self.select_file_or_folder  # Enable clicking to pick folder or file
        layout.addWidget(self.drop_area_label)

        # Remove Path button
        self.remove_path_button = QPushButton("Remove Path", self)
        self.remove_path_button.clicked.connect(self.remove_selected_path)
        self.remove_path_button.setStyleSheet("background-color: red; color: white;")
        layout.addWidget(self.remove_path_button)

        # File path label
        self.file_label = QLabel("File: None", self)
        layout.addWidget(self.file_label)

        # Set layout for the main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Get password with validation and dark mode styling
    def get_password(self):
        # Create the password input dialog with dark background and white text
        password_dialog = QInputDialog(self)
        password_dialog.setWindowTitle("Password")

        # Apply the desired dark mode style consistent with the main window
        password_dialog.setStyleSheet("""
    QDialog {
        background-color: #000000;  /* Black background for the dialog */
        color: #ffffff;  /* White text */
    }
    QLabel {
        color: #ffffff;  /* Ensure labels have white text */
    }
    QLineEdit {
        background-color: #2b2b2b;  /* Darker background for input field */
        color: #ffffff;  /* White text inside input fields */
        border: 1px solid #2979ff;  /* Blue border for focus */
        placeholder-text-color: #cccccc;  /* Light grey for placeholder text */
    }
    QPushButton {
        background-color: #2979ff;  /* Blue button background */
        color: white;  /* White text on buttons */
        border-radius: 5px;  /* Rounded button edges */
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #1e63d9;  /* Darker blue when hovering */
    }
    QDialogButtonBox {
        background-color: #000000;  /* Black background for button box */
    }
    QMessageBox {
        background-color: #000000;  /* Black background for message box */
        color: #ffffff;  /* White text */
    }
""")

        # Prompt for password input
        password, ok = password_dialog.getText(self, 'Password', 'Enter your password (min 8 characters):', QLineEdit.Password)

        # Enforce minimum password length
        if ok and len(password) < 8:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Error")
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setText("Password must be at least 8 characters!")
            error_msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2979ff;
                color: white;
            }
            """)
            error_msg.exec()
            return None

        return password.encode() if ok else None

    # Enable drag-and-drop functionality
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # Handle dropped files or folders
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            self.file_path = urls[0].toLocalFile()
            self.file_label.setText(f"File: {self.file_path}")

    # Click to pick a file or folder with dark mode styling
    def select_file_or_folder(self, event):
        file_folder_choice = QMessageBox(self)
        file_folder_choice.setWindowTitle("Pick")
        file_folder_choice.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2979ff;
                color: white;
            }
        """)
        file_folder_choice.setText("Do you want to select a file or a folder?")
        file_folder_choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        file_folder_choice.button(QMessageBox.Yes).setText("File")
        file_folder_choice.button(QMessageBox.No).setText("Folder")
        choice = file_folder_choice.exec()

        if choice == QMessageBox.Yes:  # Yes means select a file
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file to encrypt/decrypt")
        else:  # No means select a folder
            file_path = QFileDialog.getExistingDirectory(self, "Select folder to encrypt/decrypt")

        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"File: {self.file_path}")

    # Handle file/folder encryption
    def encrypt(self):
        if not self.file_path:
            self.file_path, _ = QFileDialog.getOpenFileName(self, "Select file or folder to encrypt")
        self.file_label.setText(f"File: {self.file_path}")

        if not self.file_path:
            QMessageBox.warning(self, "Error", "No file or folder selected!")
            return

        password = self.get_password()
        if not password:
            return

        try:
            if os.path.isfile(self.file_path):
                encrypt_file(self.file_path, password)
            elif os.path.isdir(self.file_path):
                encrypt_folder(self.file_path, password)

            QMessageBox.information(self, "Success", "Encryption successful!")
        except Exception as e:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Error")
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(f"Encryption failed: {str(e)}")
            error_msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2979ff;
                color: white;
            }
            """)
            error_msg.exec()

    # Handle file/folder decryption
    def decrypt(self):
        if not self.file_path:
            self.file_path, _ = QFileDialog.getOpenFileName(self, "Select file or folder to decrypt")
        self.file_label.setText(f"File: {self.file_path}")

        if not self.file_path:
            QMessageBox.warning(self, "Error", "No file or folder selected!")
            return

        password = self.get_password()
        if not password:
            return

        try:
            if os.path.isfile(self.file_path):
                decrypt_file(self.file_path, password)
            elif os.path.isdir(self.file_path):
                decrypt_folder(self.file_path, password)

            QMessageBox.information(self, "Success", "Decryption successful!")
        except Exception as e:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Error")
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(f"Decryption failed: {str(e)}")
            error_msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2979ff;
                color: white;
            }
            """)
            error_msg.exec()

    # Remove the selected path
    def remove_selected_path(self):
        self.file_path = None
        self.file_label.setText("File: None")
