import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
import requests

from backend.sunbird_client import SunbirdClient

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Sunbird Translation AI", page_icon="🐦")

# Map of languages to their TTS speaker IDs
LANGUAGES = {
    "Luganda": 248,
    "Runyankole": 243,
    "Ateso": 242,
    "Lugbara": 245,
    "Acholi": 241
}

st.title("Sunbird GenAI Application 🐦")
st.write("Transcribe, Summarize, Translate, and Listen using Sunbird AI!")

# Initialize the client
try:
    client = SunbirdClient()
except Exception as e:
    st.error("Please add your Sunbird API Token to the `.env` file.")
    st.stop()

# Input Configuration
input_mode = st.radio("Choose Input Mode:", ["Text", "Audio Upload"])

source_text = ""
target_language = st.selectbox("Select Target Language for Translation:", list(LANGUAGES.keys()))

if input_mode == "Text":
    source_text = st.text_area("Enter the text you want to process:")
else:
    audio_file = st.file_uploader("Upload Audio (Max 5 minutes)", type=["mp3", "wav", "m4a", "ogg", "aac"])
    if audio_file:
        # Check size or just rely on 5 minute limit constraint 
        # (A 5 minute MP3 is around 5-10MB, which is well below the 100MB direct upload limit)
        st.audio(audio_file)
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing..."):
                try:
                    audio_file.seek(0)
                    audio_bytes = audio_file.read()
                    st.session_state["transcription"] = client.transcribe_audio(
                        audio_bytes, 
                        filename=audio_file.name, 
                        content_type=audio_file.type
                    )
                except Exception as e:
                    st.error(f"Error during transcription: {e}")
        
    if "transcription" in st.session_state:
        st.text_area("Transcription:", st.session_state["transcription"], disabled=True)
        source_text = st.session_state["transcription"]

if source_text:
    if st.button("Run Pipeline (Summarize & Translate)"):
        with st.spinner("Summarizing..."):
            try:
                summary = client.summarize_text(source_text)
                st.session_state["summary"] = summary
            except Exception as e:
                st.error(f"Error during summarization: {e}")
                st.stop()

        with st.spinner(f"Translating to {target_language}..."):
            try:
                translation = client.translate_text(summary, target_language)
                st.session_state["translation"] = translation
            except Exception as e:
                st.error(f"Error during translation: {e}")
                st.stop()

        with st.spinner("Generating Speech..."):
            try:
                speaker_id = LANGUAGES[target_language]
                audio_url = client.generate_audio(translation, speaker_id)
                st.session_state["audio_url"] = audio_url
            except Exception as e:
                st.error(f"Error during Text-to-Speech: {e}")
                
    # Display the results outside the button click so they survive reruns
    if "summary" in st.session_state:
        st.success("Summary Generated!")
        st.write("**Summary:**")
        st.info(st.session_state["summary"])
        
    if "translation" in st.session_state:
        st.success("Translation complete!")
        st.write(f"**Translated to {target_language}:**")
        st.info(st.session_state["translation"])
        
    if "audio_url" in st.session_state:
        st.success("Audio generated!")
        st.audio(st.session_state["audio_url"])

