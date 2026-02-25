import os
from cryptography.fernet import Fernet

Key_File = "Secret.key"

def generate_key():
    # Generates a new fernet key and saves it to a file.
    key = Fernet.generate_key()
    with open(Key_File, "wb") as key_file:
        key_file.write(key)
    print("[+] Encryption key generated and saved.")


def load_key():
    # Loads the Fernet key from file.
    if not os.path.exists(Key_File):
        raise FileNotFoundError("Encryption key not found. Generate it first.")

    with open(Key_File, "rb") as key_file:
        return key_file.read()


def encrypt_data(data: bytes) -> bytes:
    # Encrypts raw bytes using Fernet.
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    return encrypted


def decrypt_data(token: bytes) -> bytes:
    # Decrypts Fernet encrypted bytes.
    key = load_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(token)
    return decrypted
