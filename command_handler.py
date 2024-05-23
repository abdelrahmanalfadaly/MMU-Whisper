import os
import json
import subprocess
import webbrowser
from pyttsx3 import init as init_engine

COMMANDS_FILE = 'Data/commands.json'

def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_commands(commands):
    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

def speak(text):
    print(f"\n{text}")
    engine = init_engine()
    engine.say(text)
    engine.runAndWait()

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

def handle_command(command, commands):
    for keyword, action in commands.items():
        if keyword in command:
            if action["type"] == "speak":
                speak(action["response"])
            elif action["type"] == "open":
                open_file(action["path"])
            elif action["type"] == "browse":
                open_url(action["url"])
            return False
    return True

def add_new_command(commands):
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
    speak(f"Command '{command}' added successfully.")
