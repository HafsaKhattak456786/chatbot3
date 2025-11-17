from gtts import gTTS
import speech_recognition as sr
import os
import io
import base64

def speak_text(text):
    """Convert text to speech and return base64 encoded audio."""
    tts = gTTS(text, lang='en')
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

def recognize_speech():
    """Recognize speech from microphone input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Could not recognize speech"
