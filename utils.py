import base64
from hashlib import sha256

def generate_key_from_password(password):
    """Generate a 32-byte key based on the SHA-256 hash of the password and base64 encode it."""
    # Hash the password to get a 32-byte key
    hash_digest = sha256(password.encode()).digest()
    # Base64 encode the key to be used by Fernet
    key = base64.urlsafe_b64encode(hash_digest)
    return key

def generate_file_hash(file_path):
    '''Generate a hash of a file for integrity checking.'''
    hasher = sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def save_file_hash(file_path, file_hash):
    '''Save the hash of a file (for integrity verification).'''
    with open(file_path + '.hash', 'w') as f:
        f.write(file_hash)

def verify_file_integrity(file_path, expected_hash):
    '''Verify that the file's hash matches the expected hash.'''
    file_hash = generate_file_hash(file_path)
    return file_hash == expected_hash