from flask import Flask, request, jsonify
from googletrans import Translator
from gtts import gTTS
import whisper
import os

app = Flask(__name__)

# Enable CORS to allow requests from the mobile app
from flask_cors import CORS
CORS(app)

# Load Whisper model
model = whisper.load_model("medium")

# Function to transcribe audio
def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, src='en', dest=target_language)
    return translation.text

# Function to convert text to speech
def text_to_speech(text, language_code, output_file):
    tts = gTTS(text=text, lang=language_code)
    tts.save(output_file)
    return output_file

# API endpoint to process audio
@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = "uploaded_audio.wav"
    file.save(file_path)

    # Step 1: Transcribe
    transcribed_text = transcribe_audio(file_path)

    # Step 2: Translate
    target_language = request.form.get("language", "en")
    translated_text = translate_text(transcribed_text, target_language)

    # Step 3: Convert to speech
    output_audio_path = "output_audio.mp3"
    text_to_speech(translated_text, target_language, output_audio_path)

    return jsonify({
        "transcribed_text": transcribed_text,
        "translated_text": translated_text,
        "audio_url": "http://your_server.com/output_audio.mp3"
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
