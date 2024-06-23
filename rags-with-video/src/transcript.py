import os
import re
import tempfile
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import whisper


def get_video_id(url: str) -> str:
    match = re.search(r"v=(.*?)&", url)
    if match:
        video_id = match.group(1)
    else:
        # Fallback to extracting video ID without '&' in case URL ends with the video ID
        video_id = re.search(r'v=([^&]*)', url).group(1)
    return video_id

def generate_transcript_with_whisper_api(url: str) -> str:
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first()
    whisper_model = whisper.load_model("base")

    with tempfile.TemporaryDirectory() as tmpdir:
        file = audio.download(output_path=tmpdir, filename="audio")
        text = whisper_model.transcribe(file, fp16=False)["text"].strip()
    
    return text

def get_default_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = [line["text"] for line in transcript]
    text = " ".join(text)
    return text

def get_transcript(url: str) -> str:
    video_id = get_video_id(url)
    file_name = f"./transcript_{video_id}.txt"
    
    # We can check if the file exists and if it does, we can just read the file and return the text.
    if not os.path.exists(file_name):
        try: 
            text = get_default_transcript(video_id) 
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video. Using OpenAI Whisper API to generate transcript.")
            text = generate_transcript_with_whisper_api(url)
        except Exception as e:
            raise Exception(f"Error getting transcript: {e}")
    
        # write to file 
        with open(file_name, "w") as f:
            f.write(text)
        print(f"Transcript saved to {file_name}")


    else:
        print(f"Transcript already exists for video {video_id}. Using existing transcript.")
    
    return file_name
