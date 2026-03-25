# 🛡️ Log File Analyzer for Intrusion Detection

A Python-based tool that analyzes system and web server logs to detect suspicious activities such as brute-force attacks and abnormal traffic patterns.

---

## 🚀 Features

* 📂 Parses log files (Apache & SSH)
* 🔐 Detects brute-force login attempts
* 🔎 Identifies high traffic / scanning behavior
* 📊 Displays suspicious IP activity
* 📁 Generates analysis report (.txt)
* 🧼 Handles file path issues (copy-paste safe)

---

## 🛠️ Tech Stack

* Python
* Regular Expressions (re)
* collections (defaultdict)

---

## 📂 Project Structure

```
project/
│
├── log_analyzer.py
├── sample.log
└── README.md
```

---

## ⚙️ Installation

No external dependencies required.

---

## ▶️ Usage

```bash
python log_analyzer.py
```

Enter log file path when prompted.

---

## 🔍 Detection Logic

### 🔐 Brute Force Detection

* Identifies repeated failed login attempts from same IP
* Threshold: more than 3 failed attempts

### 🔎 High Traffic Detection

* Detects IPs with unusually high request counts
* Threshold: more than 10 requests

---

## 📊 Example Output

```
🚨 Suspicious Activity Report

🔎 High Traffic IPs:
10.0.0.5 → 11 requests

🔐 Brute Force Attempts:
192.168.1.50 → 5 failed logins
```

---

## 📁 Report Generation

* Results are saved in `report.txt`
* Includes suspicious IPs and detected threats

---

## ⚠️ Limitations

* Basic threshold-based detection
* No real-time monitoring
* CLI-based interface

---

## 🔮 Future Improvements

* Real-time log monitoring
* GUI dashboard
* Database storage (SQLite)
* Email alert system
* Advanced anomaly detection

---

## 👨‍💻 Author

Senthamilselva
MSC Computer Science
Cyber Security Intern

---
