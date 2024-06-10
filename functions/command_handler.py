import os
import json
import subprocess
import webbrowser
import threading
import queue
import requests
from pyttsx3 import init as init_engine
from datetime import datetime
import speech_recognition as sr
from bs4 import BeautifulSoup
from tkinter import Toplevel, Label, Scrollbar, Text, VERTICAL, RIGHT, Y, END, Button
from functions.gui_setup import *

COMMANDS_FILE = 'config/commands.json'
CUSTOM_COMMANDS_FILE = 'config/custom.json'
output_queue = queue.Queue()

def Speach_Recognition(output_label):
    r = sr.Recognizer()
    update_output_text(output_label, "Listening...")
    output_label.update_idletasks()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source)
        audioInput = r.listen(source)
        try:
            return r.recognize_google(audioInput).lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.", output_label)
        except sr.RequestError:
            display_and_speak("Speech recognition service error.", output_label)
        return ""

def load_commands():
    commands = {}
    for file in [CUSTOM_COMMANDS_FILE, COMMANDS_FILE]:
        if os.path.exists(file):
            with open(file, 'r') as f:
                commands.update(json.load(f))
    return commands

def display(text, output_label):
    print(f"\n{text}")
    output_queue.put(text)
    update_gui(output_label)

def speak(text):
    def speak_text_inner(text):
        engine = init_engine()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak_text_inner, args=(text,)).start()

def display_and_speak(text, output_label):
    print(f"\n{text}")
    output_queue.put(text)
    threading.Thread(target=speak, args=(text,)).start()
    update_gui(output_label)


def open_resource(path_or_url, command_phrase, output_label, is_url=False):
    try:
        display_and_speak(f"Opening {command_phrase}", output_label)
        if is_url:
            webbrowser.open(path_or_url)
        else:
            full_path = os.path.abspath(path_or_url)  # Get the absolute path
            if os.name == 'nt':
                os.startfile(full_path)
            elif os.uname().sysname == 'Darwin':
                subprocess.call(['open', full_path])
            else:
                subprocess.call(['xdg-open', full_path])
    except Exception as e:
        display_and_speak(f"I can't open the {'URL' if is_url else 'file'}", output_label)
        print(e)

def date_and_time(command, output_label):
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%B %d, %Y")
    if "time" in command:
        display_and_speak(f"The current time is {current_time}", output_label)
    if "date" in command:
        display_and_speak(f"Today's date is {current_date}", output_label)

def get_weather_report(command, output_label):
    def get_ipv6_address():
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data.get('ip')

    def get_location(ip):
        response = requests.get(f"https://ipinfo.io/{ip}")
        data = response.json()
        return data['city']

    ipv6 = get_ipv6_address()
    if ipv6:
        location = get_location(ipv6)
        if location:
            url = f"http://wttr.in/{location}?format=j1"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'current_condition' in data:
                current_condition = data['current_condition'][0]
                temp_c = current_condition['temp_C']
                description = current_condition['weatherDesc'][0]['value']
                weather_report = f"The current weather in {location} is {temp_c}°C, {description}."
                display_and_speak(weather_report, output_label)
            else:
                display_and_speak("Could not retrieve weather data.", output_label)
        else:
            display_and_speak("Could not determine location.", output_label)
    else:
        display_and_speak("Could not retrieve IP address.", output_label)

def ai_search_engine(command, output_label):
    user_home_dir = os.path.expanduser("~")
    search_dir = os.path.join(user_home_dir, "OneDrive")

    def open_path(filepath):
        open_resource(filepath, filepath, output_label)

    def search_and_open(search_term, search_dir):
        for root, dirs, files in os.walk(search_dir):
            for name in dirs + files:
                if search_term.lower() in name.lower():
                    path = os.path.join(root, name)
                    open_path(path)
                    return True
        return False

    def process_folder_file_program_command(command_part, search_dir):
        search_term = command_part.replace("folder", "").replace("file", "").replace("program", "").strip()
        if search_term:
            found = search_and_open(search_term, search_dir)
            if found:
                display_and_speak(f"Opened {command_part.split()[0]}: {search_term}", output_label)
            else:
                display_and_speak(f"{search_term} not found: ", output_label)

    def process_website_command(command_part):
        website_url = command_part.replace("website", "").strip().replace(" ", "") + ".com"
        open_resource("http://" + website_url, website_url, output_label, is_url=True)

    command_part = command.lower().split("open", 1)[1].strip()
    if any(x in command_part for x in ["folder", "file", "program"]):
        process_folder_file_program_command(command_part, search_dir)
    elif "website" in command_part:
        process_website_command(command_part)
    else:
        display_and_speak(f"{command} is Unrecognized", output_label)

def show_help(command, output_label):
    def load_custom_commands():
        if os.path.exists(CUSTOM_COMMANDS_FILE):
            with open(CUSTOM_COMMANDS_FILE, 'r') as file:
                return json.load(file)
        return {}

    commands = load_custom_commands()
    help_text = (
        "Welcome to MMU Whisper\n"
        "\nDefault Commands List:\n"
        "\n1) Add command - allows you to add custom commands phrases that opens URL, folders, files, and program\n"
        "\n2) Open - say open \"(e.g. Youtube)\" website, or say open \"(e.g. download)\" folder, or say open \"(e.g. notes.txt)\" file, that will search for whatever you ask for.\n"
        "\n3) Time - tells the current time\n"
        "\n4) Date - tells the current date\n"
        "\n5) Weather - tells the current location's weather"
        "\n6) pomodoro - Opens Pomodoro timer"
        "\n\n\nYour Custom Commands:\n"
    )
    for cmd in commands.keys():
        help_text += f"\n- {cmd.capitalize()}"

    help_window = Toplevel()
    help_window.title("Help")
    
    text_widget = Text(help_window, wrap="word", padx=10, pady=10)
    text_widget.insert("1.0", help_text)
    text_widget.configure(state="disabled")
    text_widget.pack(expand=True, fill="both")
    
    scrollbar = Scrollbar(help_window, orient=VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_widget.tag_configure("title", font=("Helvetica", 16, "bold"))
    text_widget.tag_add("title", "1.0", "1.24")  # Apply title style to "Welcome to MMU Whisper"
    text_widget.tag_add("title", "1.26", "1.53")  # Apply title style to "Available Custom Commands"
    
    def open_commands_json():
        open_resource('custom.json', 'custom commands file', output_label)
    
    open_button = Button(help_window, text="Custom Commands", command=open_commands_json)
    open_button.pack(pady=10)
    
def start_speech_recognition(output_label):
    threading.Thread(target=listen_and_handle_commands, args=(output_label,)).start()

def handle_command(command, output_label):
    commands = load_commands()
    command = command.lower()  # Convert the input command to lowercase
    print(f"{command}")
    for cmd, action in commands.items():
        cmd = cmd.lower()  # Ensure the command keys are also in lowercase
        if (action.get("exact_match") and cmd == command) or (not action.get("exact_match") and cmd in command):
            if action["type"] == "speak":
                display_and_speak(action["response"], output_label)
            elif action["type"] == "url":
                open_resource(action["response"], cmd, output_label, is_url=True)
            elif action["type"] == "path":
                open_resource(action["response"], cmd, output_label)
            elif action["type"] == "custom":
                globals()[action["response"]](command, output_label)
            return
    display_and_speak(f"{command} is Unrecognized", output_label)

def listen_and_handle_commands(output_label):
    command = Speach_Recognition(output_label)
    handle_command(command, output_label)

def update_gui(output_label):
    try:
        text = output_queue.get_nowait()
        output_label.config(text=text)
        output_label.update_idletasks()
    except queue.Empty:
        pass
    output_label.after(100, update_gui, output_label)  # Continue to check for updates
