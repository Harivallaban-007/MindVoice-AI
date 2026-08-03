from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def communication_score(text):

    prompt = f"""
You are an AI communication evaluator.

Score the user's sentence from 1 to 10.

Rules:
- 10 = Very polite
- 8 = Good
- 5 = Neutral
- 3 = Slightly rude
- 1 = Very rude

Return ONLY:

Score: <number>

Sentence:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content