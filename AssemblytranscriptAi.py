pip install streamlit
!pip install requests
Requirement already satisfied: requests in c:\users\tdh it\anaconda3\lib\site-packages (2.32.3)
Requirement already satisfied: charset-normalizer<4,>=2 in c:\users\tdh it\anaconda3\lib\site-packages (from requests) (3.3.2)
Requirement already satisfied: idna<4,>=2.5 in c:\users\tdh it\anaconda3\lib\site-packages (from requests) (3.7)
Requirement already satisfied: urllib3<3,>=1.21.1 in c:\users\tdh it\anaconda3\lib\site-packages (from requests) (2.2.3)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\tdh it\anaconda3\lib\site-packages (from requests) (2025.1.31)
STEP 2: INSTALLING ASSEMBLY AI AND ENDPOINTS
import requests
import time
import streamlit
# Replace with your AssemblyAI API key
API_KEY = 'a49e7c835a2b40d18c8ec7eb9da8f8e1'
HEADERS = {
    'authorization': API_KEY,
    'content-type': 'application/json'
}
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'
STEP 3: Function to Upload Audio File
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
STEP 4: Function to Transcribe Audio
def transcribe_audio(audio_url):
    json = {
        'audio_url': audio_url
    }
    response = requests.post(TRANSCRIPT_ENDPOINT, json=json, headers=HEADERS)
    return response.json()['id']
STEP 5:Function to Poll for Transcription Result
def poll_transcription_result(transcription_id):
    while True:
        response = requests.get(f'{TRANSCRIPT_ENDPOINT}/{transcription_id}', headers=HEADERS)
        result = response.json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            return 'Error in transcription'
        time.sleep(5)
STEP 6:Main Function to Transcribe Audio File
def transcribe_file(file_path_or_url):
    if file_path_or_url.startswith('http'):
        # If it's a URL, use it directly
        audio_url = file_path_or_url
    else:
        # If it's a local file, upload it first
        audio_url = upload_audio_file(file_path_or_url)
    
    transcription_id = transcribe_audio(audio_url)
    transcription_text = poll_transcription_result(transcription_id)
    return transcription_text
STEP 7: TRANSCRIPTION AND SAVING TEXT FILE
file_path_or_url = 'C:\\Users\\TDH IT\\20230607_me_canadian_wildfires.mp3'
#'https://assembly.ai/sports_injuries.mp3'# Use a URL
# file_path_or_url = 'path_to_your_audio_file.mp3'  # Use a local file

transcription = transcribe_file(file_path_or_url)
print(transcription)

# Save transcription to a file
with open('transcription.txt', 'w') as f:
    f.write(transcription)
