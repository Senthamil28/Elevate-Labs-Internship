import socketio
import threading
import sys

from crypto_utils import (
    generate_keys,
    load_public_key,
    encrypt_message,
    decrypt_message,
    get_fingerprint,
    sign_message,
    verify_signature
)

sio = socketio.Client()

# ------------------ GLOBALS ------------------
username = input("Enter Username: ").strip().capitalize()

private_key, public_pem = generate_keys()

print("Your Fingerprint:", get_fingerprint(public_pem))

known_keys = {}
pending_messages = {}
online_users = []

running = True
users_loaded = False

print_lock = threading.Lock()


# ------------------ CONNECTION ------------------
@sio.event
def connect():
    with print_lock:
        print("Connected to server")

    sio.emit("register", {
        "username": username,
        "public_key": public_pem.decode()
    })


@sio.event
def disconnect():
    with print_lock:
        print("\n🔌 Disconnected from server")


# ------------------ USER LIST ------------------
@sio.on("user_list")
def user_list(data):
    global online_users, users_loaded

    online_users = data
    users_loaded = True

    with print_lock:
        print("\n👥 Online Users:", data)

    # auto request keys
    for user in data:
        if user != username and user not in known_keys:
            sio.emit("request_key", {
                "requester": username,
                "target": user
            })


# ------------------ RECEIVE KEY ------------------
@sio.on("receive_key")
def receive_key(data):
    user = data["username"]
    public_pem_bytes = data["public_key"].encode()

    fp = get_fingerprint(public_pem_bytes)

    with print_lock:
        print("\n🔐 Received key from:", user)
        print("Fingerprint:", fp[:25], "...")

    # AUTO TRUST (no blocking input)
    key = load_public_key(public_pem_bytes)
    known_keys[user] = key

    with print_lock:
        print("✅ Key stored for", user)

    # send pending messages
    if user in pending_messages:
        messages = pending_messages.pop(user)

        for msg in messages:
            signature = sign_message(msg, private_key)

            encrypted_data = encrypt_message(msg, known_keys[user])

            sio.emit("send_message", {
                "sender": username,
                "receiver": user,
                "payload": encrypted_data,
                "signature": signature
            })

        with print_lock:
            print(f"📤 Sent {len(messages)} pending message(s) to {user}")


# ------------------ RECEIVE MESSAGE ------------------
@sio.on("receive_message")
def receive_message(data):
    sender = data["sender"]

    try:
        decrypted = decrypt_message(data["payload"], private_key)
    except:
        return

    if sender in known_keys:
        valid = verify_signature(
            decrypted,
            data["signature"],
            known_keys[sender]
        )

        if not valid:
            with print_lock:
                print("\n⚠️ Signature verification failed!")
            return
    else:
        return

    with print_lock:
        print(f"\n💬 {sender}: {decrypted}")


# ------------------ SEND MESSAGE ------------------
def send_message():
    if not online_users:
        return

    receiver = input("\nSend to: ").strip().capitalize()

    if not receiver:
        return

    if receiver == username:
        print("⚠️ Cannot message yourself")
        return

    message = input("Message: ").strip()

    if not message:
        return

    if receiver not in known_keys:
        print(f"🔑 Requesting key for {receiver}...")

        sio.emit("request_key", {
            "requester": username,
            "target": receiver
        })

        if receiver not in pending_messages:
            pending_messages[receiver] = []

        pending_messages[receiver].append(message)

        print(f"📩 Message queued for {receiver}")
        return

    signature = sign_message(message, private_key)

    encrypted_data = encrypt_message(
        message,
        known_keys[receiver]
    )

    sio.emit("send_message", {
        "sender": username,
        "receiver": receiver,
        "payload": encrypted_data,
        "signature": signature
    })

    print("✅ Message sent")


# ------------------ INPUT LOOP ------------------
def input_loop():
    global running

    # wait until user list is received
    while not users_loaded and running:
        pass

    while running:
        try:
            send_message()

        except KeyboardInterrupt:
            running = False
            break

        except Exception as e:
            print("Error:", e)


# ------------------ MAIN ------------------
def main():
    global running

    try:
        sio.connect("http://localhost:5000", transports=["websocket"])

        threading.Thread(target=input_loop, daemon=True).start()

        while running:
            sio.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Exiting chat...")

    finally:
        running = False
        try:
            sio.disconnect()
        except:
            pass
        sys.exit(0)


if __name__ == "__main__":
    main()
