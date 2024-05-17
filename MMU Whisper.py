import os
import json
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3

COMMANDS_FILE = 'Data/commands.json'

r = sr.Recognizer()
engine = pyttsx3.init()

def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

commands = load_commands()

def speak(text):
    print(f"\n{text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
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

def text_command():
    return input("\nEnter your command: ").lower()

def open_file(filepath):
    try:
        if os.name == 'nt':
            os.startfile(filepath)
            speak("Opening ")
        elif os.uname().sysname == 'Darwin':
            subprocess.call(('open', filepath))
        else:
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        speak("I cant open the  file")

def open_url(url):
    try:
        webbrowser.open(url)
        speak("Opening URL")
    except Exception as e:
        speak("Error opening URL")
        print(f"{e}")


def handle_command(command):
    for keyword, action in commands.items():
        if keyword in command:
            if action["type"] == "speak":
                speak(action["response"])
            elif action["type"] == "open":
                open_file(action["path"])
            elif action["type"] == "browse":
                open_url(action["url"])
            return False
    if "add command" in command:
        add_new_command()
    elif "exit" in command:
        speak("Exiting. Goodbye!")
        return True
    elif "text command" in command:
        return "text"
    elif "sr" in command:
        return "speech"
    else:
        print(f"Unrecognized command: {command}")
    return False

def add_new_command():
    command = input("Enter the new command: ").lower()
    action_type = input("Enter the action type (speak/open/browse): ").lower()
    
    if action_type == "speak":
        response = input("Enter the response text: ")
        commands[command] = {"type": "speak", "response": response}
    elif action_type == "open":
        path = input("Enter the file/folder path: ")
        commands[command] = {"type": "open", "path": path}
    elif action_type == "browse":
        url = input("Enter the URL: ")
        commands[command] = {"type": "browse", "url": url}
    else:
        print("Invalid action type.")
        return

    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)
    speak(f"Command '{command}' added successfully.")

def main():
    mode = "text"
    while True:
        command = listen_for_commands() if mode == "speech" else text_command()
        result = handle_command(command)
        if result == "text":
            mode = "text"
        elif result == "speech":
            mode = "speech"
        elif result:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Program terminated by user.")
