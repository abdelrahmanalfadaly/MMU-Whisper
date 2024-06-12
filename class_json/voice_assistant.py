from functions import *
import os

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
            subprocess.Popen([sys.executable, 'GUI.py'])

        elif "delete class" in command:
            response = "Opening the class management window."
            print(response)
            speak(response)
            subprocess.Popen([sys.executable, 'GUI.py'])

        elif "update class" in command:
            response = "Opening the class management window."
            print(response)
            speak(response)
            subprocess.Popen([sys.executable, 'GUI.py'])

        else:
            response = "Sorry, I don't understand."
            print(response)
            speak(response)

if __name__ == "__main__":
    main()
