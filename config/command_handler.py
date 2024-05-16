import re
import os
import json
import subprocess
import webbrowser
import threading
import queue
import requests
import pyttsx3
from pyttsx3 import init as init_engine
import datetime
import speech_recognition as sr
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import Toplevel, Label, Scrollbar, Text, VERTICAL, RIGHT, Y, END, Button, messagebox, Listbox, SINGLE
import datetime
import platform
from config.gui_setup import *
from mmu_tools.class_management import *
from mmu_tools.campus_navigation import *
from functions.weather import *

COMMANDS_FILE = 'data/commands.json'
CUSTOM_COMMANDS_FILE = 'data/custom.json'
CLASS_FILE = 'data/class.json'
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
            full_path = os.path.abspath(path_or_url)  
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
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%B %d, %Y")
    if "time" in command:
        display_and_speak(f"The current time is {current_time}", output_label)
    if "date" in command:
        display_and_speak(f"Today's date is {current_date}", output_label)

def get_weather_report(command, output_label):
    weather_report = fetch_weather_report()
    display_and_speak(weather_report, output_label)

def ai_search_engine(command, output_label):
    def clean_command(command, command_type):
        if command_type == "file_or_folder":
            for word in ["file", "folder", "open"]:
                command = command.lower().replace(word, "").strip()
        elif command_type == "website":
            command = command.lower().replace("website", "").strip()
        return command

    def open_path(path):
        if os.path.isdir(path):
            if platform.system() == "Windows":
                subprocess.run(["explorer", path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", path])
        else:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", path])

    def search_and_open(search_term, search_dirs):
        for search_dir in search_dirs:
            print(f"Searching in directory: {search_dir}")
            for root, dirs, files in os.walk(search_dir):
                for name in dirs + files:
                    if search_term.lower() in name.lower():
                        path = os.path.join(root, name)
                        open_path(path)
                        return True
        return False

    def get_base_url(url):
        parts = url.split('/')
        if len(parts) > 2:
            base_url = f"{parts[0]}//{parts[2]}"
            return base_url
        return url

    def search_and_open_website(search_query):
        search_url = f"https://www.google.com/search?q={search_query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'url?q=' in href:
                url = href.split('url?q=')[1].split('&')[0]
                if url.startswith("http") and not 'maps.google.com' in url:
                    main_url = get_base_url(url)
                    webbrowser.open(main_url)
                    print(f"Opened URL: {main_url}")
                    return True
        print("Website not found. Please try again.")
        return False

    user_home_dir = os.path.expanduser("~")
    search_dirs = [os.path.join(user_home_dir, "OneDrive")]

    command_part = command.lower().split("open", 1)[1].strip()
    if any(x in command_part for x in ["folder", "file"]):
        search_term = clean_command(command_part, "file_or_folder")
        found = search_and_open(search_term, search_dirs)
        if found:
            print(f"Opened: {search_term}")
        else:
            print(f"{search_term} not found.")
    elif "website" in command_part:
        search_term = clean_command(command_part, "website")
        found = search_and_open_website(search_term)
        if found:
            print(f"Searching for website: {search_term}")
    else:
        display_and_speak(f"{command} is unrecognized", output_label)

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
        "\n1) Campus Navigation / Say: \"Dicrections from (e.g. FCI) to (e.g. FOE)\"\n"
        "\n2) AI search engine - Whisper can search for whatever you ask for.\nsay: \"open (e.g. Youtube) website\", or \"open (e.g. download) folder\", or \"open (e.g. notes.txt) file\" \n"
        "\n3) Current Time and Date - Displays when \"time\" or \"date\" is detected in your command \n"
        "\n4) Current Weather- Displays when \"weather\"is detected in your command\n"
        "\n5) Pomodoro timer - Say \"open pomodoro\"\n"
        "\n6) Class Management - Insert your sessions schduel by saying \"Add class\",  then you may ask \"What is my next class\" or \"classes on (e.g. Monday)\"\n"
        "\n7) Customized commands - you can add custom commands phrases that opens URL, folders, files, and programs, \nsay: \"Add command\"\n"
        "\n8) MMU latest events - say 'envent'\n"
        "\n\n\nYour Current Customized Commands:\n"
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
    text_widget.tag_add("title", "1.0", "1.24")  
    text_widget.tag_add("title", "1.26", "1.53") 
    
    def open_commands_json():
        open_resource(CUSTOM_COMMANDS_FILE, 'custom commands file', output_label)
    
    open_button = Button(help_window, text="Custom Commands", command=open_commands_json)
    open_button.pack(pady=10)

def campus_navigation(command, output_label):
    from mmu_tools.campus_navigation import extract_directions, create_google_maps_url

    origin, destination = extract_directions(command)
    
    if origin and destination:
        url = create_google_maps_url(origin, destination)
        display_and_speak(f"Navigating from {origin} to {destination}", output_label)
        webbrowser.open(url)
    else:
        display_and_speak("Couldn't detect a valid direction query.", output_label)


def start_speech_recognition(output_label):
    threading.Thread(target=listen_and_handle_commands, args=(output_label,)).start()

def handle_command(command, output_label):
    commands = load_commands()
    command = command.lower() 
    print(f"{command}")
    for cmd, action in commands.items():
        cmd = cmd.lower()  
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
    display_and_speak(f"'{command}' is Unrecognized", output_label)

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
    output_label.after(100, update_gui, output_label) 
