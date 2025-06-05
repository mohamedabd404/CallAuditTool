import whisper
from pydub import AudioSegment
import tempfile
import os

# Load Whisper once
model = whisper.load_model("base")  # Use "tiny" for speed or "medium" for accuracy

# List of rebuttal phrases
REBUTTAL_KEYWORDS = [
    "but", "actually", "let me explain", "here’s why", "the thing is",
    "i understand", "however", "may I ask", "can I explain", "wait", "one sec",
    "hold on", "listen", "before you go"
]

def extract_agent_audio(file_path):
    """Extract only the agent's (left channel) audio from a stereo MP3."""
    audio = AudioSegment.from_mp3(file_path)
    left_channel = audio.split_to_mono()[0]
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        left_channel.export(tmp.name, format="mp3")
        return tmp.name

def contains_rebuttal(transcribed_text):
    """Check if transcript contains any known rebuttal phrases."""
    text = transcribed_text.lower()
    return any(keyword in text for keyword in REBUTTAL_KEYWORDS)

def detect_rebuttal(file_path):
    """Transcribe agent's audio and return 'No Rebuttal' if none detected."""
    agent_audio_file = extract_agent_audio(file_path)
    result = model.transcribe(agent_audio_file)
    transcript = result["text"]
    os.remove(agent_audio_file)

    if not contains_rebuttal(transcript):
        return "No Rebuttal"
    return None
