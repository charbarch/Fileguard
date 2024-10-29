import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QInputDialog, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
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

    # Setup UI
    def setup_ui(self):
        layout = QVBoxLayout()

        # Buttons for Encrypt and Decrypt
        button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.encrypt_button.clicked.connect(self.encrypt)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt", self)
        self.decrypt_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.decrypt_button.clicked.connect(self.decrypt)
        button_layout.addWidget(self.decrypt_button)

        layout.addLayout(button_layout)

        # Drag and Drop area
        self.drop_area_label = QLabel("Drag n Drop or Click to Pick", self)
        self.drop_area_label.setStyleSheet("border: 2px dashed #ffffff; color: #ffffff; padding: 20px;")
        self.drop_area_label.setAlignment(Qt.AlignCenter)
        self.drop_area_label.mousePressEvent = self.select_file_or_folder  # Enable clicking to pick folder or file
        self.drop_area_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.drop_area_label)

        # File path label with tooltip and truncation
        self.file_label = QLabel("File: None", self)
        self.file_label.setStyleSheet("color: #00ff00; padding: 5px; font-style: italic;")
        self.file_label.setToolTip("No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        # Remove Path button - placed below the file path label
        self.remove_path_button = QPushButton("Remove Path", self)
        self.remove_path_button.clicked.connect(self.remove_selected_path)
        self.remove_path_button.setStyleSheet("background-color: red; color: white;")
        self.remove_path_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.remove_path_button)

        # Add a spacer to push the copyright label to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Copyright label at the bottom
        self.copyright_label = QLabel("© 2024 CharbArch. All rights reserved.", self)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); padding: 5px; font-size: 12px;")
        layout.addWidget(self.copyright_label)

        # Set layout for the main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Set file path with truncation
    def set_file_path(self, file_path):
        self.file_path = file_path
        if len(file_path) > 40:  # If the file path is too long, truncate it
            displayed_path = f"{file_path[:15]}...{file_path[-15:]}"
        else:
            displayed_path = file_path

        self.file_label.setText(f"File: {displayed_path}")
        self.file_label.setToolTip(file_path)  # Tooltip shows the full path

    # Get password with dark theme dialog
    def get_password(self):
        password_dialog = QInputDialog(self)
        password_dialog.setWindowTitle("Password")
        password_dialog.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e; /* Dark background */
                color: #c8c8c8; /* Light grey text */
            }
            QLabel {
                color: #c8c8c8; /* Light grey label text */
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2e2e2e; /* Slightly lighter grey background for input field */
                color: #ffffff; /* White text inside input fields */
                border: 1px solid #4682B4; /* Blue border for focus */
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #5a9bd3; /* Lighter blue border when focused */
                background-color: #3a3a3a; /* Slightly lighter grey background when focused */
            }
            QPushButton {
                background-color: #3674A3; /* Blue button background */
                color: white;
                border-radius: 5px;
                padding: 7px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2A5273; /* Darker blue when hovering */
            }
            QPushButton:pressed {
                background-color: #1E3A4C; /* Even darker blue when pressed */
            }
            QDialogButtonBox {
                background-color: #1e1e1e; /* Match the dialog background */
            }
            QMessageBox {
                background-color: #1e1e1e; /* Dark background for message box */
                color: #c8c8c8; /* Light grey text */
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
                    background-color: #1e1e1e; /* Match the dark theme */
                    color: #ffffff; /* White text */
                }
                QLabel {
                    color: #ffffff; /* Ensure labels have white text */
                }
                QPushButton {
                    background-color: #2979ff; /* Blue button background */
                    color: white; /* White text */
                    border-radius: 5px;
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
        file_folder_choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        # Set button texts
        file_folder_choice.button(QMessageBox.Yes).setText("File")
        file_folder_choice.button(QMessageBox.No).setText("Folder")
        cancel_button = file_folder_choice.button(QMessageBox.Cancel)
        cancel_button.setText("Cancel")

        # Apply red color to the Cancel button
        cancel_button.setStyleSheet("background-color: red; color: white;")

        choice = file_folder_choice.exec()

        # Handle cancel or dialog closed
        if choice == QMessageBox.Cancel:
            return  # Do nothing if the user cancels or closes the dialog

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