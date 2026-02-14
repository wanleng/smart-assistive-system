import json
import datetime
import time
import threading

class DataLogger:
    def __init__(self, filepath="detections.jsonl"):
        self.filepath = filepath
        self.lock = threading.Lock()

    def log(self, event_data: dict):
        """
        Thread-safe appending of event data to JSONL file.
        """
        # Ensure timestamp exists
        if "timestamp" not in event_data:
            # Use local time with timezone information
            event_data["timestamp"] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

        with self.lock:
            with open(self.filepath, "a", encoding="utf-8") as f:
                json_line = json.dumps(event_data)
                f.write(json_line + "\n")
