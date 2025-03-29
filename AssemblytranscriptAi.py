import streamlit as st
import requests
import time
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

# Initialize session state
if 'transcription_text' not in st.session_state:
    st.session_state.transcription_text = ""
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False

# Replace with your AssemblyAI API key
API_KEY = 'a49e7c835a2b40d18c8ec7eb9da8f8e1'
HEADERS = {
    'authorization': API_KEY,
    'content-type': 'application/json'
}
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'

# --- Core Functions ---
def upload_audio_file(file_path):
    def read_file(file_path, chunk_size=5242880):
        with open(file_path, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(
        UPLOAD_ENDPOINT,
        headers=HEADERS,
        data=read_file(file_path)
    )
    return response.json()['upload_url']

def transcribe_audio(audio_url):
    json = {
        'audio_url': audio_url
    }
    response = requests.post(TRANSCRIPT_ENDPOINT, json=json, headers=HEADERS)
    return response.json()['id']

def poll_transcription_result(transcription_id):
    while True:
        response = requests.get(f'{TRANSCRIPT_ENDPOINT}/{transcription_id}', headers=HEADERS)
        result = response.json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            return 'Error in transcription'
        time.sleep(5)

def transcribe_file(file_path_or_url):
    if file_path_or_url.startswith('http'):
        audio_url = file_path_or_url
    else:
        audio_url = upload_audio_file(file_path_or_url)
    
    transcription_id = transcribe_audio(audio_url)
    transcription_text = poll_transcription_result(transcription_id)
    return transcription_text

# --- Streamlit UI ---
st.title("🎙️ Audio Transcription Service")
st.markdown("Upload an audio file or provide a URL to transcribe it using AssemblyAI")

# Input options
input_method = st.radio("Select input method:", ("Upload File", "Audio URL"))

audio_source = None
if input_method == "Upload File":
    audio_source = st.file_uploader("Upload audio file", type=['mp3', 'wav', 'm4a'])
else:
    audio_source = st.text_input("Enter audio URL:", placeholder="https://example.com/audio.mp3")

# Transcription button
if st.button("Transcribe Audio") and audio_source:
    st.session_state.is_processing = True
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Temporary file handling for uploads
        if input_method == "Upload File":
            # Save uploaded file temporarily
            temp_file = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_source.read())
            
            status_text.text("Uploading audio file...")
            progress_bar.progress(20)
            
            # Transcribe
            status_text.text("Transcribing audio...")
            st.session_state.transcription_text = transcribe_file(temp_file)
            
            # Clean up temp file
            os.remove(temp_file)
        else:
            status_text.text("Processing audio URL...")
            progress_bar.progress(20)
            st.session_state.transcription_text = transcribe_file(audio_source)
        
        progress_bar.progress(100)
        status_text.text("Transcription complete!")
        st.success("Transcription completed successfully!")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        st.session_state.is_processing = False

# Display results
if st.session_state.transcription_text:
    st.subheader("Transcription Results")
    st.text_area("Transcription", st.session_state.transcription_text, height=300)
    
    # Download button
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="Download Transcription",
        data=st.session_state.transcription_text,
        file_name=f"transcription_{timestamp}.txt",
        mime="text/plain"
    )

# Status indicator
if st.session_state.is_processing:
    st.warning("Processing... This may take several minutes for long audio files.")
