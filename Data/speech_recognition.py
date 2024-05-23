import speech_recognition as sr

def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Speech recognition service error.")
        return ""
