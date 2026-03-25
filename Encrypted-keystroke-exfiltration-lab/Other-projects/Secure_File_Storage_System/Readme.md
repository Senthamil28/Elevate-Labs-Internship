# 🔐 Secure File Storage System (AES)

A Python-based tool for securely encrypting and decrypting files using AES encryption. This application ensures both confidentiality and integrity of stored files.

---

## 🚀 Features

* 🔐 AES-based file encryption (Fernet)
* 🔓 Secure file decryption
* 📁 Encrypted file storage with `.enc` extension
* 🧾 Metadata storage (original filename, hash)
* 🔍 Integrity verification using SHA-256
* 🧼 Robust file path handling (copy-paste & drag-drop support)
* 💻 Command-line interface (CLI)

---

## 🛠️ Tech Stack

* Python
* cryptography (Fernet)
* hashlib
* json
* os

---

## 📂 Project Structure

```
project/
│
├── secure_storage.py
├── secret.key
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run the Program

```bash 
python secure_storage.py
```

### Options

1. Encrypt File
2. Decrypt File

---

## 🔐 How It Works

1. A secret key is generated and stored locally
2. File is encrypted using AES (Fernet)
3. Encrypted file is saved with `.enc` extension
4. Metadata file stores original filename and hash
5. During decryption:

   * File is decrypted
   * Hash is recalculated
   * Integrity is verified

---

## 🔐 Security Implementation

* AES encryption using Fernet
* SHA-256 hashing for integrity
* Metadata-based verification
* Secure key storage

---

## ⚠️ Limitations

* CLI-based interface only
* Key is stored locally (not password protected)
* No multi-user support

---

## 🔮 Future Improvements

* Password-based key derivation
* GUI interface (PyQt/Tkinter)
* Cloud storage integration
* Key management system

---

## 👨‍💻 Author

Senthamilselvan
MSC Computer Science
Cyber Security Intern

---
