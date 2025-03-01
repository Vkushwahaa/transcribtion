import json
import os
from transcribe import transcribe_audio


LOG_FILE = "processed_files.json"

def load_processed_files():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError):
            print("Warning: Corrupted log file. Resetting processed files.")
            return set()
    return set()

def save_processed_files(processed_files):
    temp_file = LOG_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(list(processed_files), f)
        os.replace(temp_file, LOG_FILE) 
    except IOError:
        print("Error: Failed to save processed files.")


def transcribe_with_tracking(file_path, processed_files):
    if file_path not in processed_files:
        transcribe_audio(file_path)
        processed_files.add(file_path)
        save_processed_files(processed_files)
