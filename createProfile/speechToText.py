import speech_recognition as sr
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import io
def main(audio_file):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=dirpath + "/credentials.json"
    # r = sr.Recognizer()
    # text = "Sorry Google voice did not understand"
    # with sr.AudioFile(audio_file) as source:
    #     audio = r.record(source)
    # try:
    #     text = r.recognize_google(audio)
    #     print("Google Voice Recognizer thinks you said: \n" + text)
    #     return text
    # except sr.UnknownValueError:
    #     print("Google Voice Recognition could not understand audio")
    #     return ""
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    # Loads the audio into memory
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MULAW,
        sample_rate_hertz=44100,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
