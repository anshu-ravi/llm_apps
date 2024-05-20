import os 
from dotenv import load_dotenv
import speech_recognition as sr
from elevenlabs import play
from elevenlabs.client import ElevenLabs

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
elevenlabs_key = os.getenv("ELEVEN_LABS_API_KEY")

# This class is responsible for handling the audio input and output
# It uses the SpeechRecognition library to convert audio to text
# It uses the ElevenLabs library to convert text to audio
# The convert_audio_to_text method uses the OpenAI API to convert audio to text using the whisper API
class AudioInterface:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.client = ElevenLabs(api_key=elevenlabs_key)

    def convert_audio_to_text(self, audio) -> str:
        try: 
            text = self.recognizer.recognize_whisper_api(audio, api_key=openai_key)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand what you said"
        except sr.RequestError:
            return "Sorry, there was an error with the API request"
        

    def record_audio(self) -> sr.AudioData:
        with self.microphone as source:
            print("Please say something!")
            audio = self.recognizer.listen(source)
        
        return audio

    def listen(self) -> str:
        audio = self.record_audio()
        print("Got it! Now to recognize it...")
        text = self.convert_audio_to_text(audio)
        if text:
            return text
    
    def speak(self, text) -> None:
        audio = self.client.generate(text=text, voice='Chris', model='eleven_monolingual_v1')
        play(audio)
