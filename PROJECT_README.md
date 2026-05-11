# Sunbird AI Pipeline App

## Project Description

This is a Generative AI web application built with Streamlit and powered entirely by Sunbird AI's API ecosystem. It processes text and audio inputs through a sequential NLP pipeline: transcribing spoken audio, summarizing the context, translating the summary into a selected Ugandan local language, and synthesizing that translated text back into playable native speech.

## Architecture Overview

- **Input**: User provides typed text or uploads an audio file (`.wav`, `.mp3`, `.ogg`, `.m4a`, `.aac`).
- **Speech-to-Text (STT)**: Uploaded audio is sent to Sunbird's `/stt` endpoint to retrieve a text transcript.
- **Summarize**: The transcript or raw text is summarized concisely using the Sunflower LLM (`/sunflower_inference`).
- **Translate**: The summary is translated into the user's target Ugandan language (Luganda, Runyankole, Ateso, Lugbara, or Acholi) via Sunflower LLM.
- **Text-to-Speech (TTS)**: The translated string is synthesized into an audio clip using Sunbird's `/tts` endpoint.
- **Output**: The UI displays side-by-side intermediate text results (Transcript, Summary, Translation) and presents a playable audio element for the final generated speech.

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd internship-assessment
   ```
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Create a `.env` file in the root directory (you can reference `.env.example`). Add your Sunbird API token:
   ```env
   SUNBIRD_API_TOKEN=your_token_here
   ```
5. **Run the app locally:**
   ```bash
   python -m streamlit run app.py
   ```

## Environment Variables

- `SUNBIRD_API_TOKEN`: Your API token obtained from the [Sunbird AI API Portal](https://api.sunbird.ai/). Required for authenticating all Sunbird AI API requests.

## Usage Walkthrough

1. **Choose Input**: Select either "Text" or "Audio Upload" using the radio toggle.
2. **Select Language**: Pick the target local language (e.g., Lugbara, Luganda) from the dropdown.
3. **Execute Setup**:
   - _Text_: Paste your text and click **"Run Pipeline (Summarize & Translate)"**.
   - _Audio_: Upload an audio file, click **"Transcribe Audio"**, wait for the text to populate, and then click **"Run Pipeline"**.
4. **View & Listen**: Read the generated Summary and Translated output on the screen, then play the generated Text-to-Speech audio blob.

## Known Limitations

- **Audio constraints:** Imposed a strong < 5-minute audio length constraint to avoid overwhelming the inference nodes and triggering 504 server timeouts.
- **Gateway Timeouts:** Occasional 504 Gateway Timeouts happen with the STT API; re-running the transaction handles this gracefully.

---

## Assessment Compliance & Evidence

### Deployment Proof & Public Link Evidence

- **Public URL**: `[INSERT_YOUR_HUGGING_FACE_SPACE_URL_HERE]`
- **Deployment Status**: Live / Deployed to Hugging Face Spaces.

### Model Ranking Table

| Model Endpoint / Service            | Task                        | Selection Priority & Rationale                                                                            |
| ----------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Sunflower Inference (Qwen base)** | Summarization & Translation | **Rank 1**: Selected for primary pipeline. Strongest multi-lingual alignment for Ugandan native dialects. |
| Sunflower Inference (Gemma base)    | Summarization & Translation | **Rank 2**: Lightweight alternative, but base Qwen was heavily tuned resulting in less hallucination.     |
| Sunbird STT Endpoint                | Audio Transcription         | **Rank 1**: Exclusive required endpoint for Speech-to-Text inference constraint.                          |
| Sunbird TTS Endpoint                | Speech Synthesis            | **Rank 1**: Native voice arrays per speaker ID (e.g., ID 248 for Luganda).                                |
