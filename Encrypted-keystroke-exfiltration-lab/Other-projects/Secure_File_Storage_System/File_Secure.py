import os
import json
import hashlib
from cryptography.fernet import Fernet

# ------------------ KEY ------------------
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()
#------------------ FIle Path --------------
def clean_path(path):

    path = path.strip()

    path = path.replace("\u202a", "").replace("\u202b", "")

    path = path.strip().strip('"').strip("'")

    path = path.replace("\\\\", "\\")

    return path

# ------------------ HASH ------------------
def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

# ------------------ ENCRYPT ------------------
def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    enc_file = filepath + ".enc"
    with open(enc_file, "wb") as file:
        file.write(encrypted)

    # metadata
    metadata = {
        "original_file": filepath,
        "hash": get_file_hash(filepath)
    }

    with open(enc_file + ".meta", "w") as f:
        json.dump(metadata, f)

    print("File encrypted:", enc_file)

# ------------------ DECRYPT ------------------
def decrypt_file(enc_file):
    key = load_key()
    fernet = Fernet(key)

    with open(enc_file, "rb") as file:
        encrypted = file.read()

    decrypted = fernet.decrypt(encrypted)

    output_file = "decrypted_" + os.path.basename(enc_file.replace(".enc", ""))

    with open(output_file, "wb") as file:
        file.write(decrypted)

    # verify hash
    meta_file = enc_file + ".meta"
    if os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            metadata = json.load(f)

        new_hash = get_file_hash(output_file)

        if new_hash == metadata["hash"]:
            print("Integrity Verified")
        else:
            print("File may be tampered!")

    print("File decrypted:", output_file)

# ------------------ CLI ------------------
def main():
    print("\n Secure File Storage System")
    print("1. Encrypt File")
    print("2. Decrypt File")

    choice = input("Choose option: ").strip()

    if choice == "1":
        filepath = input("Enter file path: ")
        filepath = clean_path(filepath)
        if os.path.exists(filepath):
            encrypt_file(filepath)
        else:
            print("File not found")

    elif choice == "2":
        filepath = input("Enter .enc file path: ")
        filepath = clean_path(filepath)
        if os.path.exists(filepath):
            decrypt_file(filepath)
        else:
            print("File not found")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
