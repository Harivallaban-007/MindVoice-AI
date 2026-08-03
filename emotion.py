from groq import Groq
from groq import Groq
from config import get_api_key

client = Groq(
    api_key=get_api_key()
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