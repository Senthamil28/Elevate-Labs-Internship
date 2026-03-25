from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

users = {}
public_keys = {}
sid_to_user = {}


@socketio.on("register")
def register(data):

    username = data["username"]
    public_key = data["public_key"]

    users[username] = request.sid
    public_keys[username] = public_key
    sid_to_user[request.sid] = username

    print(username, "connected")

    emit("user_list", list(public_keys.keys()), broadcast=True)


@socketio.on("request_key")
def send_key(data):

    target = data["target"]
    requester = data["requester"]

    if target in public_keys and requester in users:
        emit(
            "receive_key",
            {
                "username": target,
                "public_key": public_keys[target]
            },
            room=users[requester]
        )


@socketio.on("send_message")
def relay_message(data):

    receiver = data["receiver"]

    if receiver in users:
        emit("receive_message", data, room=users[receiver])


@socketio.on("disconnect")
def handle_disconnect():

    username = sid_to_user.pop(request.sid, None)

    if username:
        print(username, "disconnected")

        users.pop(username, None)
        public_keys.pop(username, None)

        emit("user_list", list(public_keys.keys()), broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
