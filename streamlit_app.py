import streamlit as st
from TTS.api import TTS

# Load Italian voice
tts = TTS(model_name="tts_models/it/mai_female/glow-tts", progress_bar=True, gpu=False)

st.title("Italian Voice Bot")
text = st.text_area("Write something in Italian:")

if st.button("Speak"):
    tts.tts_to_file(text=text, file_path="output.wav")
    audio_file = open("output.wav", "rb")
    st.audio(audio_file.read(), format="audio/wav")