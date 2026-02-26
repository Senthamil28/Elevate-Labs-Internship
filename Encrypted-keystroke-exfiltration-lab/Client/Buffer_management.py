import datetime
import time
import threading


class BufferManager:
    def __init__(self, max_size=10, flush_interval=10):
        self.buffer = []
        self.max_size = max_size
        self.flush_interval = flush_interval
        self.last_flush_time = time.time()
        self.sequence_number = 0
        self.lock = threading.Lock()

    def _timestamp(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def add_event(self, key_value):
        event = {
            "event_type": "keystroke",
            "key": key_value,
            "timestamp": self._timestamp()
        }

        with self.lock:
            self.buffer.append(event)

    def should_flush(self):
        with self.lock:
            if len(self.buffer) >= self.max_size:
                return True

        if time.time() - self.last_flush_time >= self.flush_interval:
            return True

        return False

    def flush(self):
        with self.lock:
            if not self.buffer:
                return None

            self.sequence_number += 1

            batch = {
                "protocol_version": "1.0",
                "event_type": "keystroke_batch",
                "sequence_number": self.sequence_number,
                "generated_at": self._timestamp(),
                "data": self.buffer.copy()
            }

            self.buffer.clear()
            self.last_flush_time = time.time()

        return batch
