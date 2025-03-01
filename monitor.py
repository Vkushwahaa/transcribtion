from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
from transcribe import transcribe_audio
from file_scanner import SUPPORTED_FORMATS  

stop_flag = False  # Global flag to stop monitoring

class MediaFileHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        if event.is_directory:
            return
        if any(event.src_path.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
            print(f"New file detected: {event.src_path}")
            transcribe_audio(event.src_path)

def monitor_directory(directory):
    global stop_flag
    event_handler = MediaFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    try:
        while not stop_flag:  # Check the flag to stop
            time.sleep(2)
    finally:
        observer.stop()
        observer.join()
        print("Monitoring stopped.")

def user_input_listener():
    global stop_flag
    input("Press ENTER to stop monitoring...\n")  # Waits for Enter key
    stop_flag = True
    print("Stopping monitoring... Please wait.")

def start_monitoring(directory):
    global stop_flag
    stop_flag = False
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_directory, args=(directory,))
    monitor_thread.start()

    # Start user input listener in a separate thread
    input_thread = threading.Thread(target=user_input_listener)
    input_thread.start()

    # Wait for both threads to finish
    monitor_thread.join()
    input_thread.join()
    print("Monitor has exited successfully.")
