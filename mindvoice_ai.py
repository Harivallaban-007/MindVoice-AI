from groq import Groq
import json
from groq import Groq
from config import get_api_key

# Paste your Groq API key here


client = Groq(
    api_key=get_api_key()
)



def improve_sentence(user_text, language, chat_history):

    # Language Instruction
    if language == "English":
        lang = """
    Reply only in natural, fluent English.

    The user may write in:
    - English
    - Tamil
    - Tanglish (Tamil written using English letters)

    If the user writes in Tanglish or Tamil:
    - First understand the real meaning internally.
    - Never reply in Tanglish.
    - Always reply in natural English.
    - Do not translate word by word.
    - Understand the user's real intention before responding.
    - Do not mix English and Tanglish in your response.
    """

    else:
        lang = """
    தமிழில் மட்டுமே இயல்பாக பதிலளிக்கவும்.

    பயனர் எழுதுவது:
    - ஆங்கிலம்
    - தமிழ்
    - Tanglish (ஆங்கில எழுத்துக்களில் எழுதப்பட்ட தமிழ்)

    Tanglish-ல் எழுதினாலும்:
    - முதலில் அதன் உண்மையான அர்த்தத்தை புரிந்து கொள்ளவும்.
    - வார்த்தைக்கு வார்த்தை மொழிபெயர்க்க வேண்டாம்.
    - பயனரின் உண்மையான நோக்கத்தை புரிந்து கொள்ளவும்.
    - Tanglish-ல் பதிலளிக்க வேண்டாம்.
    - எப்போதும் இயல்பான தமிழில் மட்டும் பதிலளிக்கவும்.
    - தமிழ் மற்றும் Tanglish-ஐ கலக்க வேண்டாம்.
    """

    prompt = f"""
You are MindVoice AI Communication Coach.



The user may communicate in:
- English
- Tamil
- Tanglish (Tamil written using English letters)

If the input is Tanglish:

1. First understand the exact Tamil meaning.
2. Never translate word by word.
3. Understand the user's real intention.
4. Analyze the actual meaning.
5. Reply only in the language selected by the user.
6. Never misunderstand Tanglish words.

Conversation History:
{chat_history}

Current User Sentence:
{user_text}

{lang}

Return ONLY valid JSON.

Format:

{{
"emotion": "one word",
"intent": "one or two words",
"score": 1,
"needs_followup": false,
"followup_question": "",
"insight": "short sentence",
"friendly": "friendly version",
"professional": "professional version",
"polite": "polite version",
"quick_tips": [
"tip 1",
"tip 2",
"tip 3"
],
"tip": "short tip"
}}

Rules:
-Rules:
- Understand the user's intention.
- Identify the communication intent.
- Do not change the meaning.
- Emotion should be one word.
- Intent should be one or two words only.
- Score should be number 1-10.
- Keep answers short.
-Generate exactly 3 practical quick communication suggestions.
-Each suggestion must be less than 10 words.
- The user may write in English, Tamil, or Tanglish.
- Treat Tanglish as Tamil written using English letters.
- Convert Tanglish to its meaning internally before analyzing.
- Never expose this internal conversion.
- Always generate the final response in the selected language.
- Never mix English, Tamil, and Tanglish in the same reply unless the user explicitly requests it.
- If the input is Tanglish, first understand its Tamil meaning.
- Never translate Tanglish literally.
- Analyze the meaning, not the spelling.
- Never imitate the user's writing style.
- Never reply in Tanglish unless the user explicitly asks for Tanglish.
- First understand the meaning of the user's message internally.
- Reply naturally like ChatGPT or Gemini.
- Write clear, fluent, human-like sentences.
- Do not copy the user's spelling or grammar mistakes.
- Focus on the user's intention, not the exact words.

Tanglish Examples:

"Nan upset ah iruken"
→ நான் வருத்தமாக இருக்கிறேன்

"Avan enna insult pannitan"
→ அவன் என்னை அவமதித்தான்

"Enaku bayama iruku"
→ எனக்கு பயமாக இருக்கிறது

"Romba kovama iruken"
→ நான் மிகவும் கோபமாக இருக்கிறேன்

If the user's message is too short or lacks enough context, set:
needs_followup = true
Generate one simple follow-up question.
Otherwise:
needs_followup = false
followup_question = ""

Possible Intent values:

- Apology
- Request
- Complaint
- Gratitude
- Greeting
- Advice
- Appreciation
- Question
- Suggestion
- Encouragement
- Frustration
- Invitation
"""
    

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
    "role": "system",
    "content": """
You are MindVoice AI, an advanced communication coach.

Your goal is not only to rewrite sentences but to deeply understand the user's emotions, intention, and conversation context.

Rules:

- Always understand the user's meaning before generating a response.
- The user may communicate in English, Tamil, or Tanglish.
- Treat Tanglish as Tamil written using English letters.
- Internally understand the meaning first.
- Never reveal your internal reasoning.
- Never imitate spelling mistakes or Tanglish.
- Respond only in the language selected by the user.
- Write naturally like a human conversation.
- Never mix Tamil, English, and Tanglish unless the user explicitly requests it.
- Preserve the user's original intention.
- Use previous conversation history whenever it helps understand the user's message.
- If the user refers to earlier messages (he, she, they, before, yesterday, again, etc.), resolve those references using the conversation history.
- If the message is ambiguous, ask one simple follow-up question instead of guessing.
- Your responses should feel supportive, clear, and natural—not robotic.
"""
},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    reply = response.choices[0].message.content

    # Convert AI text to JSON
    data = json.loads(reply)

    return data