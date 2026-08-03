from groq import Groq
from groq import Groq
from config import get_api_key

client = Groq(
    api_key=get_api_key()
)
with open("audio.wav", "rb") as file:

    transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3"
    )

print(transcription.text)