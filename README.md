
# FileGuard

**FileGuard** is an encryption and file protection tool designed for Windows. This project allows users to manage file permissions and secure sensitive files using encryption techniques. It features a graphical user interface (GUI) for ease of use and allows users to manage themes and utilities for a more customized experience.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [License](#license)

## Features

- **Encryption**: Encrypt and decrypt files to protect sensitive information.
- **Hash Generation**: Generate secure hashes to verify the integrity of files.
- **GUI Interface**: A user-friendly graphical interface for ease of use.
- **Theming**: Customize the appearance using themes.
- **Utilities**: Helpful tools to manage file encryption and permissions.

## Installation

To install and run the project, follow the steps below:

1. Clone the repository to your local machine using:
    ```bash
    git clone https://github.com/charbarch/FileGuard.git
    ```
2. Navigate to the project directory:
    ```bash
    cd FileGuard
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the main script:
    ```bash
    python main.py
    ```

## Usage

Once installed, FileGuard provides an easy-to-use interface for encryption, decryption, and managing files.

1. Launch the application by running `main.py`.
2. Use the GUI to select files for encryption or decryption.
3. Customize the appearance with the available themes in the settings.
4. Use utilities to manage file permissions or generate secure hashes.

## Files

- `credits.py`: Manages credits and acknowledgments within the application.
- `encryption.py`: Contains the core logic for encrypting and decrypting files.
- `gui.py`: Handles the graphical user interface for the application.
- `main.py`: The entry point for the application. Initializes the GUI and starts the program.
- `theme.py`: Manages different visual themes for the application.
- `utils.py`: Provides utility functions for managing encryption and other operations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
