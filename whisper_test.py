from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

with open("audio.wav", "rb") as file:

    transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3"
    )

print(transcription.text)