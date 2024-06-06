import subprocess
import sys
import os
import datetime
from tkinter import *
from PIL import ImageTk
import speech_recognition as sr
import pyttsx3
import pyaudio
import weather
import wikipedia
import webbrowser


def install_and_update_packages(packages):
    """Updates pip and installs the given list of packages."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
      

required_packages = ['SpeechRecognition', 'pyttsx3', 'pyaudio', 'pillow']


import speech_recognition as sr
import pyttsx3
import pyaudio

root = Tk()
root.title("MMU Assistance")
root.geometry("460x750")
root.config(bg="OrangeRed")

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def clock_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time

def clock_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    return current_date

def wiki_person(text):
    list_wiki = text.split()
    for i in range(len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]

def wiki_item(text):
    list_wiki = text.split()
    for i in range(len(list_wiki)):
        if i + 2 <= len(list_wiki) - 1 and list_wiki[i].lower() == "what" and list_wiki[i + 1].lower() == "is":
            return " ".join(list_wiki[i + 2:])
    return "" 
        


def listen_for_commands():
    with sr.Microphone() as source:
        root.update()
        text.insert(END, "\nListening...\n")
        text.see(END)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            text.insert(END, f"\nCommand received: {command}\n")
            text.see(END)
            return command
        except sr.UnknownValueError:
            text.insert(END, "Sorry, I did not understand that.\n")
            text.see(END)
        return ""

def handle_speech_command():
    command = listen_for_commands()
    if "hello" in command:
        response = "\nHello There, I am MMU Whisper, your Smart Campus Voice Companion. You have successfully Tested the prototype, can't wait to show you the final results"
        text.insert(END, response + "\n")
        text.see(END)
        speak(response)

    elif "what is the time" in command:
        current_time = clock_time()
        print("\nThe current time is "+ current_time)
        speak("The current time is " + current_time)
        
    elif "what is the date" in command:
        current_date = clock_date()
        print("\nToday's date is " + current_date)
        speak("Today's date is "+ current_date)

    elif "exit" in command:
        text.insert(END, "\nExiting...\n")
        text.see(END)
        root.quit()

    elif "what is the weather" in command:
        location = "Cyberjaya"  
        current_weather = weather.get_weather(location)
        print("\nToday's weather is " + current_weather)
        speak( current_weather)


    elif "wikipedia" in command:
        if "who is" in command:
            person = wiki_person(command)
            if person:
                wiki_summary = wikipedia.summary(person, sentences=2)
                response = f"\n{wiki_summary}\n"
                text.insert(END, response)
                speak(wiki_summary)
            else:
                text.insert(END, "Sorry, I couldn't find that person.\n")
                speak("Sorry, I couldn't find that person.")
        elif "what is" in command:
            item = wiki_item(command)
            if item:
                wiki_summary = wikipedia.summary(item, sentences=2)
                response = f"\n{wiki_summary}\n"
                text.insert(END, response)
                speak(wiki_summary)
            else:
                text.insert(END, "Sorry, I couldn't find this item.\n")
                speak("Sorry, I couldn't find this item.")

    
                
                
    elif "search on youtube" in command:
        ind = command.split().index("youtube")
        search = command.split()[ind + 1:]
        webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(search))
        speak("Opening " + " ".join(search) + " on YouTube")



    elif "search on google" in command:
        ind = command.split().index("google")
        search = command.split()[ind + 1:]
        webbrowser.open("http://www.google.com/search?q=" + "+".join(search))
        speak("Opening " + " ".join(search) + " on Google")


    elif "direction from fci to fom" in command:
        url = "https://www.google.com/maps/dir/Faculty+of+Computing+%26+Informatics/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9295715,101.6411213,18.25z/data=!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632?hl=en&entry=ttu"
        print("Opening URL:", url)  # Debugging statement3
        webbrowser.open(url)
        speak("Opening direction from FCI to FOM on Google Maps")


frame = LabelFrame(root, relief="raised")
frame.grid(row=0, column=0, pady=0)

text_label = Label(frame, text="MMU Assistance", font=("DarkOrange", 14))
text_label.grid(row=0, column=0)

ai_image = PhotoImage(file="ai.png")
image_label = Label(frame, image=ai_image)
image_label.grid(row=1, column=0)

text = Text(root)
text.grid(row=2, column=0)
text.place(x=0, y=660, width=460, height=90)
text.config(bg="#9cc2ff")

button_1 = Button(root, text="Speak", bg="DeepSkyBlue", command=handle_speech_command)
button_1.place(x=120, y=560, width=215, height=60)

root.mainloop()
