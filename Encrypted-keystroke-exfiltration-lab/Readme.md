# Encrypted Keystroke Collection & Controlled Exfiltration Simulation (Isolated Lab)

## ⚠️ Disclaimer

This project was developed strictly for **educational purposes** within an isolated virtual lab environment.

It demonstrates encrypted TCP communication, secure data handling, buffer management, retry logic, and controlled command execution for red-team simulation learning.

This project is **NOT intended for malicious use**.  
No persistence mechanisms or real-world deployment features are implemented.

---

## 📌 Project Overview

This project simulates encrypted keystroke collection and controlled data exfiltration between:

- **Windows 10 Client (Virtual Machine)**
- **Kali Linux Server (Virtual Machine)**

Communication occurs over a **host-only isolated network**, ensuring no internet exposure.

The implementation focuses on secure transmission, reliability, and controlled shutdown mechanisms.

---

## 🏗 Architecture Flow

```
Keyboard Input
     ↓
Thread-Safe Buffer
     ↓ (Flush: Max Size / Time Interval)
Encrypt Data (Fernet - AES based)
     ↓
Length-Prefixed TCP Transmission
     ↓
Server Decrypt & Validate
     ↓
Command Response (OK / STOP)
```

---

## 🔐 Core Features

- AES-based symmetric encryption using **Fernet (cryptography library)**
- Length-prefixed encrypted JSON payloads
- Thread-safe keystroke capture
- Intelligent buffer management:
  - Flush on maximum batch size
  - Flush on time interval
  - Skip empty payloads
- Retry mechanism with encrypted local fallback storage
- Remote kill switch (`STOP` command)
- Clean shutdown handling
- Structured and modular design

---

## 🔁 Retry & Resilience Logic

If the server is unreachable:

- Encrypted batches are stored locally
- Client retries transmission
- Stored batches are resent when connection is restored
- No empty payloads are transmitted

This simulates controlled and resilient data exfiltration behavior within a safe lab environment.

---

## 🧪 Lab Environment

- Windows 10 VM (Client)
- Kali Linux VM (Server)
- Host-only network configuration
- No internet connectivity
- No persistence mechanism implemented
- Isolated academic testing setup

---

## 🛡 Defensive & Detection Considerations

From a defensive (blue-team) perspective, the following artifacts may be observable:

- Outbound TCP connection to a fixed port
- Encrypted traffic patterns
- Consistent packet length prefix behavior
- Python process activity
- Local encrypted batch storage files

This project was built to understand both **offensive simulation techniques** and **defensive detection opportunities**.

---

## 🚀 How to Run (Isolated Lab Only)

### 1️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Start the Server (Kali VM)

```
python server.py
```

### 3️⃣ Run the Client (Windows VM)

```
python client.py
```

### 4️⃣ Stop the Client

Send the `STOP` command from the server when prompted to trigger a clean shutdown.

---

## 📦 Requirements

- Python 3.x
- cryptography
- pynput

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Senthamil Selvan  
MSc Computer Science  
Cyber Security Intern

---

## 📚 Educational Purpose Statement

This repository exists solely to demonstrate secure coding practices, encrypted communication design, and controlled red-team simulation concepts in an academic lab environment.

It must not be used outside an isolated and authorized testing setup.
