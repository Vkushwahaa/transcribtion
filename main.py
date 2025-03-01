import sys
import os
import psutil  # For checking if script is already running
from file_scanner import find_media_files
from monitor import monitor_directory
from tracking import load_processed_files, transcribe_with_tracking

def is_already_running():
    """Checks if another instance of this script is running."""
    current_pid = os.getpid()
    script_name = os.path.basename(__file__)

    for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = proc.info.get("cmdline")
        if proc.info["pid"] != current_pid and cmdline and script_name in " ".join(cmdline):
            return True
    return False

def main(directory):
    if is_already_running():
        print("⚠️ Another instance of the script is already running. Exiting...")
        sys.exit(1)

    processed_files = load_processed_files()
    for file in find_media_files(directory):
        transcribe_with_tracking(file, processed_files)

    print("Monitoring directory for new files...")
    
    # Handle Ctrl+C more gracefully
    try:
        monitor_directory(directory)
    except KeyboardInterrupt:
        print("Monitoring stopped. Exiting...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <directory>")
        sys.exit(1)

    main(sys.argv[1])
