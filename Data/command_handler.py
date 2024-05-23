import os
import json
import subprocess
import webbrowser
from pyttsx3 import init as init_engine
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
            speak("Opening folder")
        elif os.uname().sysname == 'Darwin':
            subprocess.call(('open', filepath))
        else:
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        speak("I can't open the file")
        print(e)

def open_url(url):
    try:
        webbrowser.open(url)
        speak("Opening URL")
    except Exception as e:
        speak("Error opening URL")
        print(e)

def get_weather(location="Cyberjaya"):
    query = location.replace(" ", "+")
    url = f'https://www.google.com/search?q=weather+{query}&u=c'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            temp = soup.find('span', id='wob_tm').text
            desc = soup.find('span', id='wob_dc').text
            weather_info = f"{temp}°C {desc}"
            speak(weather_info)
            return weather_info
        else:
            error_msg = "Error: Unable to fetch weather information"
            speak(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        speak(error_msg)
        return error_msg

def get_current_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(current_time)
    return current_time

def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    speak(current_date)
    return current_date

def handle_command(command, commands, output_label=None):
    for keyword, action in commands.items():
        if keyword in command:
            if action["type"] == "speak":
                speak(action["response"])
                update_output_text(output_label, action["response"])
            elif action["type"] == "open":
                open_file(action["path"])
                update_output_text(output_label, f"Opening file: {action['path']}")
            elif action["type"] == "browse":
                open_url(action["url"])
                update_output_text(output_label, f"Opening URL: {action['url']}")
            elif action["type"] == "custom":
                if action["function"] == "get_weather":
                    weather_info = get_weather()
                    update_output_text(output_label, weather_info)
                elif action["function"] == "get_current_time":
                    current_time = get_current_time()
                    update_output_text(output_label, current_time)
                elif action["function"] == "get_current_date":
                    current_date = get_current_date()
                    update_output_text(output_label, current_date)
            return False
    return True

def add_new_command(commands):
    command = input("Enter the new command: ").lower()
    action_type = input("Enter the action type (speak/open/browse/custom): ").lower()
    
    if action_type == "speak":
        response = input("Enter the response text: ")
        commands[command] = {"type": "speak", "response": response}
    elif action_type == "open":
        path = input("Enter the file/folder path: ")
        commands[command] = {"type": "open", "path": path}
    elif action_type == "browse":
        url = input("Enter the URL: ")
        commands[command] = {"type": "browse", "url": url}
    elif action_type == "custom":
        function = input("Enter the function name: ")
        commands[command] = {"type": "custom", "function": function}
    else:
        print("Invalid action type.")
        return

    save_commands(commands)
    speak(f"Command '{command}' added successfully.")
    update_output_text(None, f"Command '{command}' added successfully.")

def update_output_text(output_label, text):
    if output_label:
        output_label.config(text=text)
