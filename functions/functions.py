import subprocess
import sys
import os
import datetime
import json
import speech_recognition as sr
import pyttsx3
import pyaudio
import subprocess
import sys
import os

r = sr.Recognizer()
engine = pyttsx3.init()

def install_and_update_packages(packages):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    with sr.Microphone() as source:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nI am your voice assistant, Please ask me something.")
        print("\nListening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print(f"\nCommand received: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I don't understand.")
            return ""

def clock_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time

def clock_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    return current_date

def clock_date_custom():
    now = datetime.datetime.now()
    custom_date = now.strftime("%d/%m/%Y")  
    return custom_date

def get_schedule_file_path():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'data.json')
    print(f"Looking for schedule file at: {file_path}")
    return file_path

def fetch_schedule():
    try:
        file_path = get_schedule_file_path()
        with open(file_path, 'r') as file:
            schedule = json.load(file)
            return schedule
    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file_path} does not exist.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: Could not parse JSON file {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Exception: An error occurred while reading the file {file_path}: {e}")
        return []

def save_schedule(schedule):
    with open(get_schedule_file_path(), 'w') as file:
        json.dump(schedule, file, indent=4)

def find_class_info(schedule, subject):
    info = []
    for row in schedule:
        if row['subject'].lower() == subject.lower():
            info.append(f"{subject.capitalize()} is on {row['day']}, from {row['start_time']} to {row['end_time']} in {row['location']}. The lecturer is {row['lecturer']}.")
    return info

def get_next_class(schedule):
    now = datetime.datetime.now()
    current_time = now.time()
    next_classes = []
    for row in schedule:
        class_start_time = datetime.datetime.strptime(row['start_time'], "%H:%M:%S").time()
        if row['day'].lower() == now.strftime("%A").lower() and class_start_time > current_time:
            next_classes.append((class_start_time, row))
    if next_classes:
        next_classes.sort(key=lambda x: x[0])
        start_time, next_class = next_classes[0]
        return next_class
    else:
        return None

def get_class_details(schedule, subject, class_type):
    details = []
    for row in schedule:
        if row['subject'].lower() == subject.lower() and row['type'].lower() == class_type.lower():
            details.append(f"{row['subject'].capitalize()} {row['type']} is on {row['day']}, from {row['start_time']} to {row['end_time']} in {row['location']}. The lecturer is {row['lecturer']}.")
    return details

def count_classes(schedule, day):
    classes_on_day = [row for row in schedule if row['day'].lower() == day.lower()]
    return len(classes_on_day)

def classes_today(schedule, day):
    today_classes = [row for row in schedule if row['day'].lower() == day.lower()]
    details = []
    for row in today_classes:
        details.append(f"{row['subject'].capitalize()} {row['type']} from {row['start_time']} to {row['end_time']} in {row['location']}.")
    return details
