import subprocess
import sys
import os
import datetime
import time
import json
import speech_recognition as sr
import pyttsx3
import pyaudio

def install_and_update_packages(packages):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ['SpeechRecognition', 'pyttsx3', 'pyaudio']

try:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nI am now updating and installing libraries, to Speak and receive your voice commands.")
    import speech_recognition as sr
    import pyttsx3
    import pyaudio
except ImportError as e:
    print("\nInstalling...")
    time.sleep(2)
    install_and_update_packages(required_packages)
    import speech_recognition as sr
    import pyttsx3
    import pyaudio
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nPackages installed successfully.")
    input("\nPress Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')

r = sr.Recognizer()
engine = pyttsx3.init()

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
    return os.path.join(os.path.dirname(__file__), 'data.json')

def fetch_schedule():
    try:
        with open(get_schedule_file_path(), 'r') as file:
            schedule = json.load(file)
            return schedule
    except FileNotFoundError:
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

def main():
    schedule = fetch_schedule()
    if not schedule:
        speak("I couldn't fetch your schedule. Please check your data file.")
        return
    
    while True:
        command = listen_for_commands()
        if "hello" in command or "hi" in command:
            response = "Hello There, I am MMU Whisper, your Smart Campus Voice Companion."
            print(response)
            speak(response)

        elif "exit" in command or "close" in command or "bye" in command:
            response = "Goodbye!"
            print(response)
            speak(response)
            break

        elif "current time" in command or "time now" in command:
            current_time = clock_time()
            response = "The current time is " + current_time
            print(response)
            speak(response)

        elif "custom date" in command:
            custom_date = clock_date_custom()
            response = "Today's date in custom format is " + custom_date
            print(response)
            speak(response)

        elif "date today" in command or "today's date" in command:
            current_date = clock_date()
            response = "Today is " + current_date
            print(response)
            speak(response)

        elif "how many classes do i have today" in command or "today classes" in command:
            today = clock_date().split(',')[0] 
            classes_today_count = count_classes(schedule, today)
            response = f"You have {classes_today_count} classes today."
            print(response)
            speak(response)

        elif "what classes do i have today" in command:
            today = clock_date().split(',')[0]
            today_class_details = classes_today(schedule, today)
            response = "Here are your classes for today:\n" + "\n".join(today_class_details)
            print(response)
            speak(response)

        elif "details about" in command:
            words = command.split()
            try:
                subject_index = words.index("about") + 1
                subject = words[subject_index]
                class_type_index = words.index(subject) + 1
                class_type = words[class_type_index]
                details = get_class_details(schedule, subject, class_type)
                if details:
                    response = "\n".join(details)
                else:
                    response = f"No details found for {subject} {class_type}."
            except (ValueError, IndexError):
                response = "Sorry, I couldn't find the subject or type in your command."
            print(response)
            speak(response)
        
        elif "next class for today" in command or "what is my next class" in command:
            next_class = get_next_class(schedule)
            if next_class:
                response = f"Your next class is {next_class['subject']} at {datetime.datetime.strptime(next_class['start_time'], '%H:%M:%S').strftime('%I:%M %p')}."
            else:
                response = "You don't have any more classes today."
            print(response)
            speak(response)

        elif "where is my next class" in command or "location for next class" in command:
            next_class = get_next_class(schedule)
            if next_class:
                response = f"Your next class is in {next_class['location']}."
            else:
                response = "You don't have any more classes today."
            print(response)
            speak(response)

        elif "when is my next class" in command or "time for next class" in command:
            next_class = get_next_class(schedule)
            if next_class:
                response = f"Your next class is at {datetime.datetime.strptime(next_class['start_time'], '%H:%M:%S').strftime('%I:%M %p')} on {next_class['day']}."
            else:
                response = "You don't have any more classes today."
            print(response)
            speak(response)

        elif "add class" in command:
            response = "Opening the class management window."
            print(response)
            speak(response)
            subprocess.Popen([sys.executable, 'page_3.py'])

        elif "delete class" in command:
            response = "Opening the class management window."
            print(response)
            speak(response)
            subprocess.Popen([sys.executable, 'page_3.py'])

        else:
            response = "Sorry, I don't understand."
            print(response)
            speak(response)

if __name__ == "__main__":
    main()
