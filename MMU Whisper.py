import os
import json
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

COMMANDS_FILE = 'Data/commands.json'

def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_commands(commands):
    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

commands = load_commands()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    with sr.Microphone() as source:
        clear_console()
        print("\nListening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            clear_console()
            print(f"\nCommand received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
        return ""

def text_command():
    clear_console()
    return input("Enter your command: ").lower()

def open_file(filepath):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(filepath)
        elif os.uname().sysname == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        else:  # Linux
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        print(f"Error opening file: {e}")
        speak(f"Error opening file")

def open_url(url):
    try:
        webbrowser.open(url)
        print(f"Opening {url}")
        speak(f"Opening")
    except Exception as e:
        print(f"Error opening URL: {e}")
        speak(f"Error opening URL")

def handle_command(command):
    for keyword, action in commands.items():
        if keyword in command:
            if action["type"] == "speak":
                response = action["response"]
                print(f"\n{response}")
                speak(response)
            elif action["type"] == "open":
                filepath = action["path"]
                open_file(filepath)
            elif action["type"] == "browse":
                url = action["url"]
                open_url(url)
            return False
    if "add command" in command:
        add_new_command()
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

    save_commands(commands)
    print(f"Command '{command}' added successfully.")
    speak(f"Command '{command}' added successfully.")

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
    try:
        main()
    except KeyboardInterrupt:
        clear_console()
        print("\nProgram terminated by user.")
        speak("Program terminated by user.")
