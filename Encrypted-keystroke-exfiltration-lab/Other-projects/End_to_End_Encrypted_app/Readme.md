# 🔐 Secure CLI Chat Application

A secure command-line chat application built using Python that implements **End-to-End Encryption (E2EE)**, **Digital Signatures**, and **Secure Key Exchange**.

---

## 🚀 Features

* 🔐 End-to-End Encryption (RSA + AES)
* ✍️ Digital Signature Verification
* 🔑 Public Key Exchange System
* 👥 Online User Management
* 📩 Message Queueing (if key not available)
* 🧵 Multi-threaded CLI interaction
* ⚡ Real-time messaging using Socket.IO

---

## 🛠️ Tech Stack

* Python
* Flask
* Flask-SocketIO
* Socket.IO
* Cryptography (RSA, AES)
* Threading

---

## 📂 Project Structure

```
project/
│
├── server.py
├── client.py
├── crypto_utils.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/Senthamil28/secure-cli-chat.git
cd secure-cli-chat
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Usage

### Start Server

```
python server.py
```

### Start Client

```
python client.py
```

---

## 🔄 How It Works

1. Users connect to the server
2. Public keys are exchanged
3. Messages are encrypted using AES
4. AES keys are securely shared via RSA
5. Messages are digitally signed
6. Receiver decrypts and verifies the signature

---

## 🔐 Security Implementation

* AES for message encryption
* RSA for secure key exchange
* Digital signatures for integrity and authenticity
* Fingerprint generation for key verification

---

## ⚠️ Limitations

* CLI-based interface
* Public keys are auto-trusted (for demo purposes)
* Uses Flask development server (not optimized for production WebSocket handling)
* No persistent message storage

---

## 🔮 Future Improvements

* Man-in-the-middle (MITM) attack detection
* Replay attack prevention
* Logging and auditing system
* Graphical User Interface (GUI)
* Production-ready deployment using eventlet/gevent

---

## 👨‍💻 Author

Senthamilselvan
MSC Computer Science
Cybersecurity Intern

---

