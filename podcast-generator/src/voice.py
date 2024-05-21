from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import os


class Voice:
    def __init__(self):
        el_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.client = ElevenLabs(api_key=el_api_key)
    
    def transform_script(self, script):
        conversation = []
        for dialogue in script.content.split("\n\n"):
            person, text = dialogue.split(':')
            conversation.append((person, text))
        return conversation

    def generate_audio(self, script):
        conversation = self.transform_script(script)
        audios = []
        for i, (person, text) in enumerate(conversation):
            if person == 'Person 1':
               voice = 'Chris'
            else:
                voice = 'Rachel'
            audio = self.client.generate(text=text, voice=voice, model='eleven_monolingual_v1')
            audios.append([i, voice, audio])

        print("Audio files generated successfully!")
        return audios
    
    def save_audio(self, audios):
        os.makedirs("./audio_files", exist_ok=True)
        for i, voice, audio in audios:
            save(audio, f"audio_files/{voice}_{i}.mp3")
        
        print("Audio files saved successfully!")
    

    def play_audio(self, audios):
        for i, voice, audio in audios:
            play(audio)
    

        
