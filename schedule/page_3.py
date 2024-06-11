from tkinter import *
from PIL import ImageTk, Image
import json
import os

def get_schedule_file_path():
    return os.path.join(os.path.dirname(__file__), 'data.json')

def load_schedule():
    try:
        with open(get_schedule_file_path(), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_schedule(schedule):
    with open(get_schedule_file_path(), 'w') as file:
        json.dump(schedule, file, indent=4)

def add_data():
    subject = subject_entry.get()
    class_type = type_entry.get()
    day = day_entry.get()
    start_time = start_entry.get()
    end_time = end_entry.get()
    location = location_entry.get()
    lecturer = lecturer_entry.get()

    if not subject or not class_type or not day or not start_time or not end_time or not location or not lecturer:
        print("Error: All fields are required")
        return

    schedule = load_schedule()

    for row in schedule:
        if row['subject'].lower() == subject.lower() and row['type'].lower() == class_type.lower():
            print("Class already exists")
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
    print("Class added successfully")

def delete_data():
    subject = subject_entry.get()
    class_type = type_entry.get()

    if not subject or not class_type:
        print("Error: Subject and Type fields are required")
        return

    schedule = load_schedule()

    new_schedule = [row for row in schedule if not (row['subject'].lower() == subject.lower() and row['type'].lower() == class_type.lower())]

    if len(new_schedule) == len(schedule):
        print("No matching class found to delete")
    else:
        save_schedule(new_schedule)
        print("Class deleted successfully")

root = Tk()
root.title("MMU Whisper")
root.geometry("350x450")

logo_image = ImageTk.PhotoImage(file="logo.png")
image_label = Label(root, image=logo_image, height=150, width=350)
image_label.place(x=0, y=0)

subject_label = Label(root, text="Subject", font=("arial", 12, "bold"))
subject_label.place(x=20, y=180)

subject_entry = Entry(root)
subject_entry.place(x=120, y=180)

type_label = Label(root, text="Type", font=("arial", 12, "bold"))
type_label.place(x=20, y=210)

type_entry = Entry(root)
type_entry.place(x=120, y=210)

day_label = Label(root, text="Day", font=("arial", 12, "bold"))
day_label.place(x=20, y=240)

day_entry = Entry(root)
day_entry.place(x=120, y=240)

start_label = Label(root, text="Start Time", font=("arial", 12, "bold"))
start_label.place(x=20, y=270)

start_entry = Entry(root)
start_entry.place(x=120, y=270)

end_label = Label(root, text="End Time", font=("arial", 12, "bold"))
end_label.place(x=20, y=300)

end_entry = Entry(root)
end_entry.place(x=120, y=300)

location_label = Label(root, text="Location", font=("arial", 12, "bold"))
location_label.place(x=20, y=330)

location_entry = Entry(root)
location_entry.place(x=120, y=330)

lecturer_label = Label(root, text="Lecturer", font=("arial", 12, "bold"))
lecturer_label.place(x=20, y=360)

lecturer_entry = Entry(root)
lecturer_entry.place(x=120, y=360)

add_button = Button(root, text="Add", width=10, background="#CC7726", command=add_data)
add_button.place(x=180, y=400)

delete_button = Button(root, text="Delete", width=10, background="#CC7726", command=delete_data)
delete_button.place(x=260, y=400)

root.mainloop()
