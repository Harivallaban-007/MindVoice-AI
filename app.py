# =====================================================
# MindVoice - AI Communication Coach
# Part 1 : Imports + Page Setup + Sidebar Navigation
# =====================================================

import streamlit as st
import speech_recognition as sr
import datetime
import pandas as pd
from streamlit_option_menu import option_menu   # NEW: pip install streamlit-option-menu

from mindvoice_ai import improve_sentence
from communication_tips import get_quick_tips

from groq import Groq
from config import get_api_key

client = Groq(
    api_key=get_api_key()
)

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(
    page_title="MindVoice | AI Communication Coach",
    page_icon="🧠🎤",
    layout="wide"          # CHANGED: centered -> wide (sidebar ku space)
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
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "waiting_followup" not in st.session_state:
    st.session_state.waiting_followup = False

if "original_message" not in st.session_state:
    st.session_state.original_message = ""

if "history_log" not in st.session_state:          # NEW: stores every analyzed message for History/Insights
    st.session_state.history_log = []

# =====================================================
# Part 2 : SIDEBAR (Logo + Nav Menu + Quote) - NEW
# =====================================================

with st.sidebar:

    st.image("assets/logo.svg", width=90)

    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-title">MindVoice</span>
        <div class="sidebar-tagline">Speak Better, Regret Less</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Chat", "History", "Insights", "Settings", "About"],
        icons=["chat-dots", "clock-history", "bar-chart-line", "gear", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00C853", "font-size": "16px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0",
                "color": "#dddddd",
                "border-radius": "10px",
                "padding": "10px 14px"
            },
            "nav-link-selected": {
                "background-color": "rgba(0,200,83,0.18)",
                "color": "#00C853",
                "font-weight": "600"
            },
        }
    )

    st.markdown("""
    <div class="sidebar-quote">
        "Think before you speak."<br>
        <span style="color:#00C853; font-weight:600;">Speak better.</span>
        <span style="color:#FF9800; font-weight:600;"> Regret less.</span>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Part 3 : MAIN HEADER (Title + Listening Mode Toggle)
# =====================================================

col_title, col_toggle = st.columns([5, 1])

with col_title:
    st.image("assets/logo.svg", width=110)
    st.markdown("""
    <div class="main-header">
        <h1>MindVoice</h1>
        <p>Your AI Communication Assistant</p>
    </div>
    """, unsafe_allow_html=True)

with col_toggle:
    st.write("")
    st.write("")
    listening_mode = st.toggle("🟠 Listening Mode", value=False)


# =====================================================
# Part 4 : PAGE ROUTING
# =====================================================

if selected == "Chat":

    # -------------------------
    # Language Selection
    # -------------------------
    language = st.selectbox(
        "🌐 Language",
        ["English", "தமிழ்", "Auto Detect"]
    )

    whisper_lang = "ta" if language == "தமிழ்" else "en"

    st.write("Selected Language:", language)

    # -------------------------
    # Clear Chat
    # -------------------------
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # -------------------------
    # Display Chat History
    # -------------------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # -------------------------
    # Floating Mic Button (fixed near bottom bar, ChatGPT-style)
    # -------------------------
    st.markdown('<div class="mic-anchor"></div>', unsafe_allow_html=True)
    voice_clicked = st.button("🎙️", key="mic_button")

    # -------------------------
    # Fixed Bottom Chat Input (ChatGPT / Gemini / Claude style)
    # -------------------------
    user_input = st.chat_input("Type your message...")

    # =====================================================
    # Part 5 : Voice Input (Speech to Text)
    # =====================================================

    if voice_clicked:

        try:
            # Check a mic actually exists before trying to open one
            mic_names = sr.Microphone.list_microphone_names()

            if not mic_names:
                st.error(
                    "🎙️ No microphone found on this device.\n\n"
                    "Check: (1) a mic is physically connected, "
                    "(2) Windows Settings → Privacy → Microphone → "
                    "'Allow apps to access your microphone' is turned ON."
                )
                st.stop()

            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                st.info("🎤 Listening... Speak now!")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            with open("audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            with open("audio.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3",
                    language=whisper_lang
                )

            text = transcription.text
            st.success("✅ Speech Recognized")

            st.session_state.messages.append(
                {"role": "user", "content": text}
            )

            with st.chat_message("user"):
                st.write(text)

            user_input = text

        except OSError:
            st.error(
                "🎙️ No default input device available. Please check that "
                "a microphone is connected and enabled, then try again."
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # =====================================================
    # Part 6 : MindVoice AI Response (unchanged logic)
    # =====================================================

    if user_input:

        if st.session_state.waiting_followup:
            user_input = f"""
        Original Message:
        {st.session_state.original_message}

        Additional Information:
        {user_input}
        """
            st.session_state.waiting_followup = False
            st.session_state.original_message = ""

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.write(user_input)

        tips = get_quick_tips(user_input)

        if tips:
            st.markdown("### 💡 Quick Suggestions")
            for tip in tips:
                st.info(tip)

        with st.spinner("🧠 MindVoice thinking..."):
            chat_history = ""
            for msg in st.session_state.messages:
                chat_history += f"{msg['role']}: {msg['content']}\n"

            response = improve_sentence(
                user_input,
                language,
                chat_history
            )

        if response["needs_followup"]:
            st.session_state.waiting_followup = True
            st.session_state.original_message = user_input

            st.warning("💬 I need a little more information.")
            st.info(response["followup_question"])

            st.stop()

        # NEW: log this analyzed message for History + Insights pages
        st.session_state.history_log.append({
            "date": datetime.datetime.now().strftime("%d %b %Y"),
            "time": datetime.datetime.now().strftime("%I:%M %p"),
            "message": user_input,
            "emotion": response["emotion"],
            "intent": response["intent"],
            "score": int(response["score"])
        })

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
            {"role": "assistant", "content": assistant_reply}
        )

        with st.chat_message("assistant"):

            st.markdown("## 🧠 MindVoice Analysis")

            emotion = response["emotion"].lower()

            emotion_emoji = {
                "anger": "😡",
                "sadness": "😢",
                "happiness": "😊",
                "fear": "😨",
                "neutral": "😐"
            }

            emoji = emotion_emoji.get(emotion, "🧠")

            st.info(f"🧠 Emotion\n\n{emoji} {response['emotion']}")
            st.info(f"🎯 Intent\n\n{response['intent']}")

            score = int(response["score"])
            st.success(f"📊 Communication Score\n\n⭐ {score} / 10")
            st.progress(score / 10)

            if score >= 9:
                st.success("🟢 Excellent Communication")
            elif score >= 7:
                st.info("🟡 Good Communication")
            elif score >= 5:
                st.warning("🟠 Needs Improvement")
            else:
                st.error("🔴 Poor Communication")

            st.markdown("### 💡 Quick Suggestions")
            for quick_tip in response["quick_tips"]:
                st.info(f"✔ {quick_tip}")

            st.write(f"💭 **MindVoice Insight:**\n\n{response['insight']}")

            st.markdown("### 😊 Friendly")
            st.write(response["friendly"])

            st.markdown("### 💼 Professional")
            st.write(response["professional"])

            st.markdown("### 🙏 Polite")
            st.write(response["polite"])

            st.warning(f"💡 MindVoice Tip\n\n{response['tip']}")


elif selected == "History":

    st.markdown("### 📜 Chat History")

    if not st.session_state.history_log:
        st.info("No conversations yet. Chat with MindVoice to build your history!")

    else:
        if st.button("🗑️ Clear History"):
            st.session_state.history_log = []
            st.rerun()

        st.markdown("---")

        # Most recent conversation first
        for entry in reversed(st.session_state.history_log):

            score = entry["score"]

            if score >= 8:
                badge = "🟢"
            elif score >= 5:
                badge = "🟡"
            else:
                badge = "🔴"

            preview = entry["message"].strip().replace("\n", " ")
            if len(preview) > 55:
                preview = preview[:55] + "..."

            with st.expander(f"{badge}  {preview}   —   {entry['date']} · {entry['time']}"):
                st.write(f"**Message:** {entry['message']}")
                st.write(f"**🧠 Emotion:** {entry['emotion']}")
                st.write(f"**🎯 Intent:** {entry['intent']}")
                st.write(f"**📊 Score:** {score} / 10")


elif selected == "Insights":

    st.markdown("### 📊 Communication Insights")

    if not st.session_state.history_log:
        st.info("No data yet. Chat with MindVoice to see your insights!")

    else:
        df = pd.DataFrame(st.session_state.history_log)

        # Summary metric cards
        col1, col2, col3 = st.columns(3)
        col1.metric("💬 Total Messages", len(df))
        col2.metric("⭐ Average Score", round(df["score"].mean(), 1))
        col3.metric("🏆 Best Score", int(df["score"].max()))

        st.markdown("---")

        st.markdown("#### 📈 Score Trend (over your conversations)")
        st.line_chart(df["score"])

        st.markdown("#### 😊 Emotion Breakdown")
        emotion_counts = df["emotion"].value_counts()
        st.bar_chart(emotion_counts)

        st.markdown("#### 🎯 Most Common Intents")
        intent_counts = df["intent"].value_counts()
        st.bar_chart(intent_counts)

elif selected == "Settings":
    st.markdown("### ⚙️ Settings")
    st.info("App settings — coming soon.")

elif selected == "About":
    st.markdown("### ℹ️ About MindVoice")
    st.write(
        "MindVoice is your AI Communication Coach — understand your emotions, "
        "improve your message, and communicate better in English, Tamil, or Tanglish."
    )
