import os
import json
import subprocess
import webbrowser
import threading
import queue
import requests
from pyttsx3 import init as init_engine
import datetime
import speech_recognition as sr
from bs4 import BeautifulSoup
from tkinter import Toplevel, Label, Scrollbar, Text, VERTICAL, RIGHT, Y, END, Button, messagebox, Listbox, SINGLE
import re
import pyttsx3
from config.gui_setup import *
import datetime
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, SINGLE
import pyttsx3



def class_management(command, output_label):
    root = tk.Tk()
    root.title("Class Management")
    root.geometry("400x500")
    root.withdraw() 

    def load_schedule():
        try:
            with open(CLASS_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_schedule(schedule):
        with open(CLASS_FILE, 'w') as file:
            json.dump(schedule, file, indent=4)

    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def add_data():
        subject = subject_entry.get()
        class_type = type_entry.get()
        day = day_entry.get()
        start_time = start_entry.get()
        end_time = end_entry.get()
        location = location_entry.get()
        lecturer = lecturer_entry.get()

        if not subject or not class_type or not day or not start_time or not end_time or not location or not lecturer:
            messagebox.showerror("Error", "All fields are required")
            return

        schedule = load_schedule()

        for row in schedule:
            if row['subject'].lower() == subject.lower() and row['type'].lower() == class_type.lower():
                messagebox.showerror("Error", "Class already exists")
                return

        new_class = {
            'subject': subject,
            'type': class_type,
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'lecturer': lecturer
        }

        schedule.append(new_class)
        save_schedule(schedule)
        messagebox.showinfo("Success", "Class added successfully")

    def delete_data():
        selected_class_index = class_listbox.curselection()
        if not selected_class_index:
            messagebox.showerror("Error", "No class selected")
            return

        schedule = load_schedule()
        del schedule[selected_class_index[0]]
        save_schedule(schedule)
        load_class_list() 
        messagebox.showinfo("Success", "Class deleted successfully")

    def get_classes_today(schedule):
        today = datetime.datetime.now().strftime("%A").lower()
        return [row for row in schedule if row['day'].lower() == today]

    def get_next_class(schedule):
        now = datetime.datetime.now()
        today = now.strftime("%A").lower()
        next_classes = []

        for row in schedule:
            class_start_time = row['start_time']
            if row['day'].lower() == today and class_start_time > now.strftime("%I:%M %p"):
                next_classes.append((class_start_time, row))

        if next_classes:
            next_classes.sort(key=lambda x: x[0])
            _, next_class = next_classes[0]
            return next_class
        else:
            return None

    def get_classes_on_day(schedule, day):
        return [row for row in schedule if row['day'].lower() == day.lower()]

    def process_input(user_input):
        schedule = load_schedule()
        response = ""

        if "class" in user_input or "session" in user_input:
            if "add" in user_input or "remove" in user_input or "edit" in user_input or "delete" in user_input:
                root.deiconify()
                return

            if "today" in user_input:
                classes_today = get_classes_today(schedule)
                if classes_today:
                    response = "Today's classes are: " + ", ".join([f"{c['subject']} from {c['start_time']} to {c['end_time']}" for c in classes_today])
                else:
                    response = "There are no classes today."
            elif "next" in user_input:
                next_class = get_next_class(schedule)
                if next_class:
                    response = f"Your next class is {next_class['subject']} from {next_class['start_time']} to {next_class['end_time']} in {next_class['location']}."
                else:
                    response = "There are no more classes today."
            else:
                day_match = re.search(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", user_input, re.IGNORECASE)
                if day_match:
                    day = day_match.group(0).lower()
                    classes_on_day = get_classes_on_day(schedule, day)
                    if classes_on_day:
                        response = f"Classes on {day.capitalize()} are: " + ", ".join([f"{c['subject']} from {c['start_time']} to {c['end_time']}" for c in classes_on_day])
                    else:
                        response = f"There are no classes on {day.capitalize()}."
                else:
                    next_class = get_next_class(schedule)
                    if next_class:
                        response = f"Your next class is {next_class['subject']} from {next_class['start_time']} to {next_class['end_time']} in {next_class['location']}."
                    else:
                        response = "There are no more classes today."

        if response:
            print(response)
            speak(response)

    def load_class_list():
        schedule = load_schedule()
        class_listbox.delete(0, tk.END)
        for cls in schedule:
            class_listbox.insert(tk.END, f"{cls['subject']} ({cls['type']}) on {cls['day']} from {cls['start_time']} to {cls['end_time']} at {cls['location']}")


    root = tk.Tk()
    root.title("Class Management")
    root.geometry("400x500")
    root.withdraw()  

    title_label = tk.Label(root, text="Your Sessions", font=("arial", 16, "bold"))
    title_label.place(x=20, y=10)
  
    class_listbox = Listbox(root, selectmode=SINGLE)
    class_listbox.place(x=20, y=50, width=360, height=120)

    scrollbar = Scrollbar(root)
    scrollbar.place(x=380, y=50, height=120)

    class_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=class_listbox.yview)

    delete_button = tk.Button(root, text="Delete", width=10, background="#CC7726", command=delete_data)
    delete_button.place(x=20, y=180)

    subject_label = tk.Label(root, text="Subject", font=("arial", 12, "bold"))
    subject_label.place(x=20, y=220)

    subject_entry = tk.Entry(root)
    subject_entry.place(x=120, y=220)

    type_label = tk.Label(root, text="Type", font=("arial", 12, "bold"))
    type_label.place(x=20, y=250)

    type_entry = tk.Entry(root)
    type_entry.place(x=120, y=250)

    day_label = tk.Label(root, text="Day", font=("arial", 12, "bold"))
    day_label.place(x=20, y=280)

    day_entry = tk.Entry(root)
    day_entry.place(x=120, y=280)

    start_label = tk.Label(root, text="Start Time", font=("arial", 12, "bold"))
    start_label.place(x=20, y=310)

    start_entry = tk.Entry(root)
    start_entry.place(x=120, y=310)

    end_label = tk.Label(root, text="End Time", font=("arial", 12, "bold"))
    end_entry = tk.Entry(root)
    end_label.place(x=20, y=340)

    end_entry = tk.Entry(root)
    end_entry.place(x=120, y=340)

    location_label = tk.Label(root, text="Location", font=("arial", 12, "bold"))
    location_label.place(x=20, y=370)

    location_entry = tk.Entry(root)
    location_entry.place(x=120, y=370)

    lecturer_label = tk.Label(root, text="Lecturer", font=("arial", 12, "bold"))
    lecturer_label.place(x=20, y=400)

    lecturer_entry = tk.Entry(root)
    lecturer_entry.place(x=120, y=400)

    add_button = tk.Button(root, text="Add", width=10, background="#CC7726", command=add_data)
    add_button.place(x=180, y=440)


    load_class_list()

    process_input(command)
