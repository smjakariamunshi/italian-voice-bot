
import streamlit as st
import openai
import tempfile
import os
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

# OpenAI API key from Hugging Face secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Italian Voice Chatbot 🇮🇹", layout="centered")
st.title("🗣️ Italian Voice Chatbot 🇮🇹")
st.markdown("**কথা বলো ইতালিয়ান ভাষায় 🎤 এবং বট তোমাকে উত্তর দেবে!**")

audio_file = st.file_uploader("🎧 আপনার ভয়েস রেকর্ড (WAV/MP3)", type=["wav", "mp3"])

if audio_file is not None:
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    with sr.AudioFile(tmp_path) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="it-IT")
            st.success(f"তুমি বলছো: `{text}`")
        except:
            st.error("😢 ভয়েস বোঝা যায়নি। আবার চেষ্টা করো।")
            text = None

    if text:
        with st.spinner("🤖 AI ভাবছে..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Italian teacher. Reply in Italian only."},
                    {"role": "user", "content": text}
                ]
            )
            reply = response.choices[0].message.content.strip()
            st.markdown(f"**🤖 বট বলছে:** {reply}")

            tts = gTTS(reply, lang="it")
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            st.audio(audio_bytes, format="audio/mp3")
