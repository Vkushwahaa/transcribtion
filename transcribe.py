import whisper
import os
import time
import torchaudio
from tqdm import tqdm

MODEL = whisper.load_model("base")

def get_audio_duration(file_path):
    try:
        metadata = torchaudio.info(file_path)
        return metadata.num_frames / metadata.sample_rate
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return

    try:
        print(f"🔍 Processing: {file_path} ...")

        # Get audio duration
        duration = get_audio_duration(file_path)
        if duration is None:
            print("⚠️ Unable to determine duration. Setting arbitrary progress duration.")
            duration = 10  # Default fallback

        # Initialize progress bar
        pbar = tqdm(total=duration, desc="🔊 Transcribing", unit="sec", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}s", leave=False)

        # Perform transcription
        result = MODEL.transcribe(file_path, fp16=False, verbose=False)

        # Update progress dynamically based on timestamps
        for segment in result["segments"]:
            pbar.n = segment["end"]  # Move progress to actual timestamp
            pbar.refresh()
            time.sleep(0.5)  # Small delay for smooth updates

        # Ensure progress reaches 100%
        pbar.n = duration
        pbar.refresh()
        pbar.close()

        # Save transcription
        output_file = file_path.rsplit(".", 1)[0] + ".txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"✅ Transcription saved: {output_file}")

    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")

