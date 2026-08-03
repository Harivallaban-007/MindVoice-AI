import speech_recognition as sr
from mindvoice_ai import improve_sentence

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak now...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("\nYou said:", text)

    print("\n🤖 MindVoice is thinking...\n")
    reply = improve_sentence(text)

    print("🤖 MindVoice:")
    print(reply)

except Exception as e:
    print("Error:", e)