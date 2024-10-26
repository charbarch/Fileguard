
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_file(file_path: str, password: bytes) -> None:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(salt + encrypted_data)

def decrypt_file(file_path: str, password: bytes) -> str:
    with open(file_path, 'rb') as file:
        salt = file.read(16)
        encrypted_data = file.read()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception:
        return "Invalid key or corrupt data!"
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)
    return "File decrypted successfully."

def encrypt_folder(folder_path: str, password: bytes) -> None:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, password)

def decrypt_folder(folder_path: str, password: bytes) -> None:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, password)