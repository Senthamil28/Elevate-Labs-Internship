import datetime
import os
from colorama import Fore, init

init(autoreset=True)

LOG_FILE = "log/firewall.log"

def log_allow(ip, port):
    print(Fore.GREEN + f"[ALLOW] {ip} -> Port {port}")
    write_log(f"ALLOW {ip} -> {port}")

def log_block(ip):
    print(Fore.RED + f"[BLOCK] {ip}")
    write_log(f"BLOCK {ip}")

def log_alert(msg):
    print(Fore.YELLOW + f"[ALERT] {msg}")
    write_log(f"ALERT {msg}")

def log_info(msg):
    print(Fore.CYAN + f"[INFO] {msg}")
    write_log(f"INFO {msg}")

def write_log(msg):

    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} {msg}\n")
