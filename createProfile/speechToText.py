import speech_recognition as sr
def main(audio_file):
    r = sr.Recognizer()
    text = "Sorry Google voice did not understand"
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print("Google Voice Recognizer thinks you said: \n" + text)
        return text
    except sr.UnknownValueError:
        print("Google Voice Recognition could not understand audio")
        return ""
