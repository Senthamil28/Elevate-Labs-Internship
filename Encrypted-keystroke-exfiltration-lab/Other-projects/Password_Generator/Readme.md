# 🔐 Password Strength Analyzer & Wordlist Generator

A Python-based security tool that analyzes password strength and generates custom wordlists based on user-specific inputs. This tool demonstrates practical concepts used in password cracking and cybersecurity testing.

---

## 🚀 Features

* 🔐 Password strength analysis using zxcvbn
* 📊 Crack time estimation
* 🧠 Feedback on weak passwords
* 🧾 Custom wordlist generation
* 🔄 Leetspeak variations (@, 3, 0, etc.)
* 🔢 Appends common patterns (years, numbers)
* 📁 Export wordlist to .txt file

---

## 🛠️ Tech Stack

* Python
* argparse
* zxcvbn
* itertools

---

## 📂 Project Structure

```
project/
│
├── pass_gen.py
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

### Analyze Password

```bash
python tool.py -p mypassword123
```

### Generate Wordlist

```bash
python tool.py -i john 2002 dog -o wordlist.txt
```

---

## 🔐 How It Works

1. Password is analyzed using zxcvbn
2. Strength score and crack time are calculated
3. User inputs are processed
4. Variations are generated:

   * lowercase / uppercase
   * leetspeak substitutions
   * combinations
   * appended numbers/years
5. Wordlist is exported as a .txt file

---

## ⚠️ Limitations

* CLI-based interface only
* Limited wordlist size
* No real-time attack simulation

---

## 🔮 Future Improvements

* GUI using Tkinter
* Advanced pattern generation
* Integration with password cracking tools
* Machine learning-based strength prediction

---

## 👨‍💻 Author

Senthamilselvan
MSC Computer Science
Cybersecurity Intern

---

