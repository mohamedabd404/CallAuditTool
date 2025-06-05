from pydub import AudioSegment
import os

# Set silence threshold (dBFS below which we consider it silence)
SILENCE_THRESHOLD = -45  # dBFS
MIN_DEAD_CALL_DURATION = 15  # seconds

def load_audio(file_path):
    """Load stereo MP3 and split into agent (left) and customer (right)."""
    audio = AudioSegment.from_mp3(file_path)
    if audio.channels < 2:
        raise ValueError("Audio must be stereo (2 channels)")
    agent_audio = audio.split_to_mono()[0]  # Left channel
    customer_audio = audio.split_to_mono()[1]  # Right channel
    return agent_audio, customer_audio, len(audio) / 1000  # duration in seconds

def is_silent(audio_segment, silence_threshold=SILENCE_THRESHOLD):
    """Check if audio segment is mostly silent."""
    return audio_segment.dBFS < silence_threshold

def detect_issues(file_path):
    """
    Analyze a stereo MP3 and return a list of issues:
    - Releasing (agent completely silent)
    - Dead Call (customer completely silent for more than 15 sec)
    """
    issues = []
    try:
        agent_audio, customer_audio, duration = load_audio(file_path)

        agent_silent = is_silent(agent_audio)
        customer_silent = is_silent(customer_audio)

        if agent_silent and duration > 2:
            issues.append("Releasing")

        if customer_silent and duration >= MIN_DEAD_CALL_DURATION:
            issues.append(f"Dead Call – {int(duration)} sec")

    except Exception as e:
        issues.append(f"Error processing file: {str(e)}")

    return issues
