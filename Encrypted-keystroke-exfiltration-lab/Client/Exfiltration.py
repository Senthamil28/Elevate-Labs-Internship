import socket
import struct
import json
import time
import os
from datetime import datetime

from encryption import encrypt_data, decrypt_data

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds

FALLBACK_DIR = "fallback_storage"


# -------------------------------------------------
# Utility: Receive exact number of bytes
# -------------------------------------------------
def receive_exact(sock, length):
    data = b""
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data


# -------------------------------------------------
# Store encrypted payload locally (per batch file)
# -------------------------------------------------
def store_locally(encrypted_payload):
    os.makedirs(FALLBACK_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(FALLBACK_DIR, f"batch_{timestamp}.enc")

    with open(filename, "wb") as f:
        f.write(encrypted_payload)

    print(f"[!] Stored encrypted batch locally: {filename}")


# -------------------------------------------------
# Send single batch to server
# -------------------------------------------------
def send_batch(batch_dict):
    """
    Returns:
        True   -> success
        False  -> failed (stored locally)
        "STOP" -> kill switch received
    """

    # Defensive empty check
    if not batch_dict or not batch_dict.get("data"):
        print("[!] Empty batch. Skipping send.")
        return True

    try:
        payload_bytes = json.dumps(batch_dict).encode()
    except Exception as e:
        print(f"[!] JSON serialization failed: {e}")
        return False

    encrypted_payload = encrypt_data(payload_bytes)
    message = struct.pack(">I", len(encrypted_payload)) + encrypted_payload

    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((SERVER_IP, SERVER_PORT))
                client.sendall(message)

                client.settimeout(5)

                # Receive response length
                raw_length = receive_exact(client, 4)
                if not raw_length:
                    print("[!] No response from server.")
                    return False

                response_length = struct.unpack(">I", raw_length)[0]
                encrypted_response = receive_exact(client, response_length)

                if not encrypted_response:
                    print("[!] Incomplete server response.")
                    return False

                decrypted_response = decrypt_data(encrypted_response)
                response_data = json.loads(decrypted_response.decode())

                if not isinstance(response_data, dict):
                    print("[!] Invalid server response format.")
                    return False

                print("[+] Batch delivered successfully.")
                print("[+] Server response:", response_data)

                command = response_data.get("command")

                if command == "STOP":
                    print("[!] Kill switch received.")
                    return "STOP"

                return True

        except Exception as e:
            attempt += 1
            print(f"[!] Attempt {attempt} failed: {e}")
            time.sleep(RETRY_DELAY)

    # All retries failed
    store_locally(encrypted_payload)
    return False


# -------------------------------------------------
# Retry sending stored encrypted batches
# -------------------------------------------------
def resend_stored_batches():
    if not os.path.exists(FALLBACK_DIR):
        return None

    files = sorted(os.listdir(FALLBACK_DIR))
    if not files:
        return None

    print("[*] Attempting to resend stored batches...")

    for file in files:
        filepath = os.path.join(FALLBACK_DIR, file)

        try:
            with open(filepath, "rb") as f:
                encrypted_payload = f.read()

            message = struct.pack(">I", len(encrypted_payload)) + encrypted_payload

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((SERVER_IP, SERVER_PORT))
                client.sendall(message)

                client.settimeout(5)

                raw_length = receive_exact(client, 4)
                if not raw_length:
                    print("[!] No response during retry.")
                    break

                response_length = struct.unpack(">I", raw_length)[0]
                encrypted_response = receive_exact(client, response_length)

                if not encrypted_response:
                    print("[!] Incomplete retry response.")
                    break

                decrypted_response = decrypt_data(encrypted_response)
                response_data = json.loads(decrypted_response.decode())

                if response_data.get("command") == "STOP":
                    print("[!] STOP received during retry.")
                    return "STOP"

                print(f"[+] Successfully resent stored batch: {file}")
                os.remove(filepath)

        except Exception as e:
            print(f"[!] Retry failed for {file}: {e}")
            break

    return None
