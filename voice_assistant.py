from functions.command_handler import *
from functions.gui_setup import *
from functions.functions import *
import subprocess
import sys
import datetime

def handle_command(command, output_label):
    schedule = fetch_schedule()
    if "hello" in command or "hi" in command:
        response = "Hello There, I am MMU Whisper, your Smart Campus Voice Companion."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "exit" in command or "close" in command or "bye" in command:
        response = "Goodbye!"
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)
        return False

    elif "current time" in command or "time now" in command:
        current_time = clock_time()
        response = "The current time is " + current_time
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "custom date" in command:
        custom_date = clock_date_custom()
        response = "Today's date in custom format is " + custom_date
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "date today" in command or "today's date" in command:
        current_date = clock_date()
        response = "Today is " + current_date
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "how many classes do i have today" in command or "today classes" in command:
        today = clock_date().split(',')[0]
        classes_today_count = count_classes(schedule, today)
        response = f"You have {classes_today_count} classes today."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "what classes do i have today" in command:
        today = clock_date().split(',')[0]
        today_class_details = classes_today(schedule, today)
        response = "Here are your classes for today:\n" + "\n".join(today_class_details)
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

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
        if output_label:
            output_label.config(text=response)

    elif "next class for today" in command or "what is my next class" in command:
        next_class = get_next_class(schedule)
        if next_class:
            response = f"Your next class is {next_class['subject']} at {datetime.datetime.strptime(next_class['start_time'], '%H:%M:%S').strftime('%I:%M %p')}."
        else:
            response = "You don't have any more classes today."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "where is my next class" in command or "location for next class" in command:
        next_class = get_next_class(schedule)
        if next_class:
            response = f"Your next class is in {next_class['location']}."
        else:
            response = "You don't have any more classes today."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "when is my next class" in command or "time for next class" in command:
        next_class = get_next_class(schedule)
        if next_class:
            response = f"Your next class is at {datetime.datetime.strptime(next_class['start_time'], '%H:%M:%S').strftime('%I:%M %p')} on {next_class['day']}."
        else:
            response = "You don't have any more classes today."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    elif "add class" in command:
        response = "Opening the class management window."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)
        try:
            print("Attempting to open page_3.py for adding a class.")
            subprocess.Popen([sys.executable, 'functions/page_3.py'])
        except Exception as e:
            print(f"Failed to open page_3.py: {e}")

    elif "delete class" in command:
        response = "Opening the class management window."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)
        try:
            print("Attempting to open page_3.py for deleting a class.")
            subprocess.Popen([sys.executable, 'functions/page_3.py'])
        except Exception as e:
            print(f"Failed to open page_3.py: {e}")

    elif "update class" in command:
        response = "Opening the class management window."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)
        try:
            print("Attempting to open page_3.py for updating a class.")
            subprocess.Popen([sys.executable, 'functions/page_3.py'])
        except Exception as e:
            print(f"Failed to open page_3.py: {e}")

    else:
        response = "Sorry, I don't understand."
        print(response)
        speak(response)
        if output_label:
            output_label.config(text=response)

    return True

def on_enter(event, output_label):
    command = event.widget.get()
    continue_running = handle_command(command, output_label)
    event.widget.delete(0, 'end')  # Clear the input field
    if not continue_running:
        event.widget.master.quit()

def switch_mode(new_mode, root, current_mode, output_label):
    print(f"Switching mode from {current_mode} to {new_mode}")
    root.destroy()
    main(new_mode, output_label)

def start_speech_recognition(output_label):
    print("Starting speech recognition")
    while True:
        command = listen_for_commands()
        if not handle_command(command, output_label):
            break

def main(mode="speech", output_label=None):
    print(f"Starting main with mode: {mode}")
    commands = load_commands()
    app_running = True

    def on_closing():
        print("Closing application")
        root.destroy()

    if mode == "text":
        print("Setting up text interface")
        root, input_entry, output_label, buttons = setup_text_interface()
        settingbs_button, stsrb_button = buttons
        srb_button = None
        sttb_button = None
    elif mode == "speech":
        print("Setting up speech interface")
        root, input_entry, output_label, buttons = setup_speech_interface()
        settingbs_button, srb_button, sttb_button = buttons
        stsrb_button = None

    root.protocol("WM_DELETE_WINDOW", on_closing)

    settingbs_button.config(command=lambda: [show_help('', output_label)])
    if srb_button:
        srb_button.config(command=lambda: start_speech_recognition(output_label))
    if sttb_button:
        sttb_button.config(command=lambda: switch_mode("text", root, mode, output_label))
    if stsrb_button:
        stsrb_button.config(command=lambda: switch_mode("speech", root, mode, output_label))

    if input_entry:
        input_entry.bind('<Return>', lambda event: on_enter(event, output_label))
    
    root.mainloop()

if __name__ == "__main__":
    mode = "speech"
    app_running = True
    output_label = None
    while app_running:
        mode, app_running, output_label = main(mode, output_label)
