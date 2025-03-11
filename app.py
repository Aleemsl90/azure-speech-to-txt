import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import pydub
from PIL import Image

def speech_recognize_from_file(sound):
    """performs speech-to-text transcription with Azure SDK"""
    speech_config = speechsdk.SpeechConfig(subscription="----enter subscription----", region="Germany West Central")
    audio_config = speechsdk.audio.AudioConfig(filename=sound)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="en-US", audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        st.write("Transcribed Speech: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.write("No Speech Recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        st.write ("Speech Recognition cancelled: {}".format(result.cancellation_details.reason))

        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.write("Error details: {}".format(result.cancellation_details.error_details))


st.title("WebApp Azure speech to text")

image = Image.open('./1.png')
st.image(image)
st.write("This app uses Azure speech SDK to transcribe audio to text")

st.subheader("Choose a .wav file to convert to text")
uploaded_file = st.file_uploader("Select a .wav file")

if uploaded_file:
    try:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='wav')
        audio = pydub.AudioSegment.from_wav(uploaded_file)
        audio.export('./saved.wav', format='wav')
        speech_recognize_from_file('./saved.wav')

    except:
        st.error("Please upload a short audio .wav file")
