# =====================================================
# MindVoice - AI Communication Coach
# Part 1 : Imports + Page Setup + CSS + Chat History
# =====================================================

# -------------------------
# Import required libraries
# -------------------------
import streamlit as st
import speech_recognition as sr
import os
from dotenv import load_dotenv
from groq import Groq

# MindVoice AI function
from mindvoice_ai import improve_sentence
from communication_tips import get_quick_tips

# -------------------------
# Groq Client
# -------------------------
# Paste your API key here
load_dotenv()
print(os.getenv("GROQ_API_KEY"))
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(
    page_title="MindVoice",
    page_icon="🧠",
    layout="centered"
)

# -------------------------
# Load Custom CSS
# -------------------------
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -------------------------
# Chat History
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Follow-up State
if "waiting_followup" not in st.session_state:
    st.session_state.waiting_followup = False

if "original_message" not in st.session_state:
    st.session_state.original_message = ""

# -------------------------
# App Title
# -------------------------
st.title("🧠 MindVoice")

st.markdown("""
### Speak Better, Regret Less

##### 🤖 Your AI Communication Coach
---
""")

# -------------------------
# Language Selection
# -------------------------
language = st.selectbox(
    "🌐 Language",
    ["English", "தமிழ்","Auto Detect"]
)

# Whisper language code
if language == "தமிழ்":
    whisper_lang = "ta"
else:
    whisper_lang = "en"

st.write("Selected Language:", language)

st.markdown("---")

# -------------------------
# Display Chat History
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# -------------------------
# Clear Chat Button
# -------------------------
if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    if "text_input" in st.session_state:
        st.session_state.text_input = ""

    st.rerun()

st.markdown("---")

# =====================================================
# Part 2 : Text Input + Microphone UI
# =====================================================

# -------------------------
# Input Area
# -------------------------
col_input, col_mic = st.columns([6, 1])

# Text Input
with col_input:
   user_input = st.text_input(
    "Message",
    placeholder="💬Share What's on Your Mind...",
    key="text_input",
    label_visibility="collapsed"
)
# Microphone Button
with col_mic:
    
    st.write("")  # Small spacing

    voice_clicked = st.button(
        "🎙️",

        use_container_width=True
    )

st.markdown("---")

# =====================================================
# Part 3 : Voice Input (Speech to Text)
# =====================================================

if voice_clicked:

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.info("🎤 Listening... Speak now!")

        # Reduce background noise
        recognizer.adjust_for_ambient_noise(source)

        # Record voice
        audio = recognizer.listen(source)

    try:

        # Save recorded audio
        with open("audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Convert Speech → Text using Groq Whisper
        with open("audio.wav", "rb") as file:

            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3",
                language=whisper_lang
            )

        # Recognized text
        text = transcription.text

        st.success("✅ Speech Recognized")

        # Save user message in chat history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": text
            }
        )

        # Show user message
        with st.chat_message("user"):
            st.write(text)

    except Exception as e:
        st.error(e)
# =====================================================
# Part 4 : MindVoice AI Response
# =====================================================

# -------------------------
# Text Input Processing
# -------------------------

if user_input:
    # Combine follow-up answer with original message
    if st.session_state.waiting_followup:

        user_input = f"""
    Original Message:
    {st.session_state.original_message}

    Additional Information:
    {user_input}
    """

        st.session_state.waiting_followup = False
        st.session_state.original_message = ""

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

     # Quick Suggestions
    tips = get_quick_tips(user_input)

    if tips:

        st.markdown("### 💡 Quick Suggestions")

        for tip in tips:
            st.info(tip)


    # AI Processing
    with st.spinner("🧠 MindVoice thinking..."):

        chat_history = ""

        for msg in st.session_state.messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"

        response = improve_sentence(
            user_input,
            language,
            chat_history
        )
            
    # Check if AI needs more information
    if response["needs_followup"]:

        st.session_state.waiting_followup = True
        st.session_state.original_message = user_input

        st.warning("💬 I need a little more information.")
        st.info(response["followup_question"])

        st.stop()
    # =====================================================
    # Part 6 : Smart AI Cards
    # =====================================================
    
    # Save AI response
    assistant_reply = f"""
    🧠 Emotion: {response['emotion']}

    🎯 Intent: {response['intent']}

    😊 Friendly:
    {response['friendly']}

    💼 Professional:
    {response['professional']}

    🙏 Polite:
    {response['polite']}
    """

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )


    # Display AI response

    with st.chat_message("assistant"):

        st.markdown("## 🧠 MindVoice Analysis")


        # Emotion Card
        # =====================================================
        # Part 7 : Premium UI Upgrade
        # =====================================================

        # Emotion Emoji

        emotion = response["emotion"].lower()

        emotion_emoji = {
            "anger": "😡",
            "sadness": "😢",
            "happiness": "😊",
            "fear": "😨",
            "neutral": "😐"
        }

        emoji = emotion_emoji.get(
            emotion,
            "🧠"
        )


        # Emotion Card

        st.info(
            f"🧠 Emotion\n\n{emoji} {response['emotion']}"
        )
        # Intent Card
        st.info(
            f"🎯 Intent\n\n{response['intent']}"
        )


        # Score Card
        score = int(response["score"])


        st.success(
            f"📊 Communication Score\n\n⭐ {score} / 10"
        )


        st.progress(score / 10)
        # Score Feedback

        if score >= 9:
            st.success("🟢 Excellent Communication")

        elif score >= 7:
            st.info("🟡 Good Communication")

        elif score >= 5:
            st.warning("🟠 Needs Improvement")

        else:
            st.error("🔴 Poor Communication")

        # Quick Suggestions
        st.markdown("### 💡 Quick Suggestions")

        for quick_tip in response["quick_tips"]:
            st.info(f"✔ {quick_tip}")

        # Insight
        st.write(
            f"💭 **MindVoice Insight:**\n\n{response['insight']}"
        )


        # Friendly
        st.markdown("### 😊 Friendly")
        st.write(response["friendly"])


        # Professional
        st.markdown("### 💼 Professional")
        st.write(response["professional"])


        # Polite
        st.markdown("### 🙏 Polite")
        st.write(response["polite"])


        # Tip
        st.warning(
            f"💡 MindVoice Tip\n\n{response['tip']}"
        )