import os
import speech_recognition as sr
import pyttsx3

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    with sr.Microphone() as source:
        clear_console()
        print("\nListening...")
        speak("I am Listening.")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            clear_console()
            print(f"\nCommand received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            speak("Sorry, there was an issue with the speech recognition service.")
        return ""

def text_command():
    clear_console()
    return input("Enter your command: ").lower()

def handle_command(command):
    if "hello" in command:
        response = "Hello There, I am MMU Whisper, your Smart Campus Voice Companion. You have successfully tested the prototype, can't wait to show you the final results."
        print(f"\n{response}")
        speak(response)
    elif "exit" in command:
        print("\nExiting...")
        speak("Exiting. Goodbye!")
        return True
    elif "text command" in command:
        return "text"
    elif "sr" in command:
        return "speech"
    else:
        print(f"\nUnrecognized command: {command}")
        speak("Unrecognized command. Please try again.")
    return False

def main():
    mode = "text"
    while True:
        if mode == "speech":
            command = listen_for_commands()
        else:
            command = text_command()

        result = handle_command(command)
        if result == "text":
            mode = "text"
        elif result == "speech":
            mode = "speech"
        elif result:
            break

if __name__ == "__main__":
    clear_console()
    r = sr.Recognizer()
    engine = pyttsx3.init()
    try:
        main()
    except KeyboardInterrupt:
        clear_console()
        print("\nProgram terminated by user.")
        speak("Program terminated by user.")
