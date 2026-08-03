from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def detect_emotion(text):

    prompt = f"""
You are an emotion detector.

Read the user's sentence.

Return ONLY:

Emotion: <emotion>
Intensity: <1-10>

User:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content