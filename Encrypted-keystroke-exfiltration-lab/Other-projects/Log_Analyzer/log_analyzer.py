import re
from collections import defaultdict
from datetime import datetime

# ------------------ PATTERNS ------------------
# Apache log pattern
apache_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d{3})')

# SSH failed login
ssh_failed_pattern = re.compile(r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)')

#------------------ FIle Path --------------
def clean_path(path):

    path = path.strip()

    path = path.replace("\u202a", "").replace("\u202b", "")

    path = path.strip().strip('"').strip("'")

    path = path.replace("\\\\", "\\")

    return path

# ------------------ ANALYSIS ------------------
def analyze_log(file_path):
    ip_requests = defaultdict(int)
    failed_logins = defaultdict(int)

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            
            # Apache parsing
            apache_match = apache_pattern.search(line)
            if apache_match:
                ip = apache_match.group(1)
                ip_requests[ip] += 1

            # SSH failed login detection
            ssh_match = ssh_failed_pattern.search(line)
            if ssh_match:
                ip = ssh_match.group(1)
                failed_logins[ip] += 1

    return ip_requests, failed_logins


# ------------------ DETECTION ------------------
def detect_anomalies(ip_requests, failed_logins):
    print("\n Suspicious Activity Report\n")

    # High traffic detection
    print(" High Traffic IPs (Possible Scanning):")
    for ip, count in ip_requests.items():
        if count > 10:
            print(f"{ip} → {count} requests")

    # Brute force detection
    print("\n Brute Force Attempts:")
    for ip, count in failed_logins.items():
        if count > 3:
            print(f"{ip} → {count} failed logins")


# ------------------ SAVE REPORT ------------------
def save_report(ip_requests, failed_logins):
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("Log Analysis Report\n\n")

        f.write("High Traffic IPs:\n")
        for ip, count in ip_requests.items():
            if count > 10:
                f.write(f"{ip} → {count} requests\n")

        f.write("\nBrute Force Attempts:\n")
        for ip, count in failed_logins.items():
            if count > 3:
                f.write(f"{ip} → {count} failed logins\n")

    print("\nReport saved as report.txt")


# ------------------ MAIN ------------------
def main():
    print("️ Log File Analyzer")

    file_path = input("Enter log file path: ")
    file_path = clean_path(file_path)

    try:
        ip_requests, failed_logins = analyze_log(file_path)
        detect_anomalies(ip_requests, failed_logins)
        save_report(ip_requests, failed_logins)

    except FileNotFoundError:
        print(" File not found")


if __name__ == "__main__":
    main()
