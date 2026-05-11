import os
import requests

class SunbirdClient:
    def __init__(self):
        self.api_token = os.environ.get("SUNBIRD_API_TOKEN")
        if not self.api_token:
            raise ValueError("SUNBIRD_API_TOKEN is not set in the environment variables.")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.sunbird.ai/tasks"

    def transcribe_audio(self, audio_bytes, filename="audio.wav", content_type="audio/wav"):
        """Transcribe audio using Speech-to-Text API"""
        url = f"{self.base_url}/stt"
        # STT uses multipart/form-data, so we omit Content-Type from headers
        headers_multipart = {"Authorization": f"Bearer {self.api_token}"}
        
        files = {
            'audio': (filename, audio_bytes, content_type)
        }
        response = requests.post(url, headers=headers_multipart, files=files, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        print(f"DEBUG STT Response: {data}")
        
        # Checking all possible keys the Sunbird API might use for the transcription text
        text = data.get("text", "")
        if not text and "audio_transcription" in data:
            text = data["audio_transcription"]
        elif not text and "output" in data:
            if isinstance(data["output"], dict):
                text = data["output"].get("text", "")
            elif isinstance(data["output"], str):
                text = data["output"]
        
        return text

    def summarize_text(self, text):
        """Summarize text using Sunflower Inference"""
        url = f"{self.base_url}/sunflower_inference"
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Summarize the text provided by the user concisely."},
                {"role": "user", "content": text}
            ]
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        return data.get("content", data.get("output", {}).get("content", ""))

    def translate_text(self, text, target_language):
        """Translate text to the target Ugandan language"""
        url = f"{self.base_url}/sunflower_inference"
        payload = {
            "messages": [
                {"role": "system", "content": f"You are a helpful assistant. Translate the text provided by the user into {target_language}."},
                {"role": "user", "content": text}
            ]
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        return data.get("content", data.get("output", {}).get("content", ""))

    def generate_audio(self, text, speaker_id):
        """Generate speech audio from text using Text-to-Speech API"""
        url = f"{self.base_url}/tts"
        payload = {
            "text": text,
            "speaker_id": speaker_id
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        return data.get("output", {}).get("audio_url", "")
