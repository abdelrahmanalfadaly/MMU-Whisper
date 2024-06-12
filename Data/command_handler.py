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
            speak("Opening")
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

def search_on_google_maps_from(command):
    parts = command.split("direction from")[1].strip().split(" to ")
    if len(parts) == 2:
        origin = parts[0].strip()
        destination = parts[1].strip()
        url = f"https://www.google.com/maps/dir/?api=1&origin={origin.replace(' ', '+')}&destination={destination.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Opening directions from {origin} to {destination} on Google Maps")
    else:
        speak("Sorry, I don't understand the direction request.")

def direction_from_fci_to_fom():
    url = "https://www.google.com/maps/dir/Faculty+of+Computing+%26+Informatics/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9295715,101.6411213,18.25z/data=!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to FOM on Google Maps")
def direction_from_fci_to_dtc():
    url = "https://www.google.com/maps/dir/FCI,+Cyberjaya,+Selangor/Dewan+Tun+Canselor,+63000+Cyberjaya,+Selangor/@2.9300315,101.6389089,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to DTC on Google Maps") 
def direction_from_fci_to_lecture_complex():
    url = "https://www.google.com/maps/dir/FCI,+Cyberjaya,+Selangor/Central+Lecture+Complex,+63000+Cyberjaya,+Selangor/@2.9298632,101.6393714,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to Central Lecture Complex on Google Maps")
def direction_from_fci_to_library():
    url = "https://www.google.com/maps/dir/FCI,+Cyberjaya,+Selangor/Siti+Hasmah+Digital+Library+Multimedia+University,+Jalan+Multimedia,+63000+Cyberjaya,+Selangor/@2.927968,101.6384988,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e88b8bd7b5:0xaa996a4c4300b49a!2m2!1d101.6416346!2d2.9275867?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to Library on Google Maps")
def direction_from_fci_to_fcm():
    url = "https://www.google.com/maps/dir/FCI,+Cyberjaya,+Selangor/Faculty+of+Creative+Multimedia+(FCM),+Multimedia+University+-+MMU+Cyberjaya,+43300+Cyberjaya,+Selangor/@2.9279468,101.6394593,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e620ee76a1:0x8d156f59872affd7!2m2!1d101.6431581!2d2.9261747?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to FCM on Google Maps")
def direction_from_fci_to_foe():
    url = "https://www.google.com/maps/dir/FCI,+Cyberjaya,+Selangor/Faculty+of+Engineering,+Multimedia+University+-+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9273244,101.6395266,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643!1m5!1m1!1s0x31cdb6e87ea95201:0x56a1170947b3c79!2m2!1d101.6411458!2d2.9263857?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FCI to FOE on Google Maps")

def direction_from_fom_to_fci():
    url = "https://www.google.com/maps/dir/FOM,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Faculty+of+Computing+%26+Informatics,+Multimedia+University,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9300167,101.6385836,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to FCI on Google Maps")
def direction_from_fom_to_dtc():
    url = "https://www.google.com/maps/dir/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Dewan+Tun+Canselor,+63000+Cyberjaya,+Selangor/@2.9299535,101.6397542,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to DTC on Google Maps")
def direction_from_fom_to_library():
    url = "https://www.google.com/maps/dir/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Siti+Hasmah+Digital+Library+Multimedia+University,+Jalan+Multimedia,+63000+Cyberjaya,+Selangor/@2.9289181,101.6384664,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e88b8bd7b5:0xaa996a4c4300b49a!2m2!1d101.6416346!2d2.9275867?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to Library on Google Maps")
def direction_from_fom_to_lecture_complex():
    url = "https://www.google.com/maps/dir/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Central+Lecture+Complex,+63000+Cyberjaya,+Selangor/@2.9293926,101.6410605,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to Central Lecture Complex on Google Maps")
def direction_from_fom_to_fcm():
    url = "https://www.google.com/maps/dir/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Faculty+of+Creative+Multimedia+(FCM),+Multimedia+University+-+MMU+Cyberjaya,+43300+Cyberjaya,+Selangor/@2.9285867,101.6398544,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e620ee76a1:0x8d156f59872affd7!2m2!1d101.6431581!2d2.9261747?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to FCM on Google Maps")
def direction_from_fom_to_foe():
    url = "https://www.google.com/maps/dir/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+Cyberjaya,+Selangor/Faculty+of+Engineering,+Multimedia+University+-+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9282745,101.6384664,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632!1m5!1m1!1s0x31cdb6e87ea95201:0x56a1170947b3c79!2m2!1d101.6411458!2d2.9263857?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from FOM to FOE on Google Maps") 

def direction_from_dtc_to_fci():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Faculty+of+Computing+%26+Informatics,+Multimedia+University,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9300315,101.6389089,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to FCI on Google Maps")
def direction_from_dtc_to_fom():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9300564,101.6392917,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to FOM on Google Maps")
def direction_from_dtc_to_library():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Siti+Hasmah+Digital+Library+Multimedia+University,+Jalan+Multimedia,+63000+Cyberjaya,+Selangor/@2.9284174,101.6393519,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e88b8bd7b5:0xaa996a4c4300b49a!2m2!1d101.6416346!2d2.9275867?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to Library on Google Maps")
def direction_from_dtc_to_lecture_complex():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Central+Lecture+Complex,+63000+Cyberjaya,+Selangor/@2.9284611,101.6399466,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to Central Lecture Complex on Google Maps")
def direction_from_dtc_to_fcm():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Faculty+of+Creative+Multimedia+(FCM),+Multimedia+University+-+MMU+Cyberjaya,+43300+Cyberjaya,+Selangor/@2.9276552,101.6414169,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e620ee76a1:0x8d156f59872affd7!2m2!1d101.6431581!2d2.9261747?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to FCM on Google Maps")
def direction_from_dtc_to_foe():
    url = "https://www.google.com/maps/dir/Dewan+Tun+Canselor/Faculty+of+Engineering,+Multimedia+University+-+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9279895,101.6393519,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363!1m5!1m1!1s0x31cdb6e87ea95201:0x56a1170947b3c79!2m2!1d101.6411458!2d2.9263857?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from DTC to FOE on Google Maps") 

def direction_from_lecture_complex_to_fci():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Faculty+of+Computing+%26+Informatics,+Multimedia+University,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9298632,101.6393714,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e9ab2c6603:0xdedb9094d553b194!2m2!1d101.6405899!2d2.9290643?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to FCI on Google Maps")
def direction_from_lecture_complex_to_fom():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Faculty+of+Management+(FOM)+@+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9293926,101.6407425,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e9a19f8cdb:0xc983ff350ca6a201!2m2!1d101.6412675!2d2.9299632?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to FOM on Google Maps")
def direction_from_lecture_complex_to_dtc():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Dewan+Tun+Canselor,+63000+Cyberjaya,+Selangor/@2.9284611,101.641234,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e91af90d0b:0x397f973de1f102c0!2m2!1d101.6423872!2d2.9291363?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to DTC on Google Maps")
def direction_from_lecture_complex_to_library():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Siti+Hasmah+Digital+Library+Multimedia+University,+Jalan+Multimedia,+63000+Cyberjaya,+Selangor/@2.9284174,101.6393519,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e88b8bd7b5:0xaa996a4c4300b49a!2m2!1d101.6416346!2d2.9275867?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to Library on Google Maps")
def direction_from_lecture_complex_to_fcm():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Faculty+of+Creative+Multimedia+(FCM),+Multimedia+University+-+MMU+Cyberjaya,+43300+Cyberjaya,+Selangor/@2.9270144,101.6401813,17z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e620ee76a1:0x8d156f59872affd7!2m2!1d101.6431581!2d2.9261747?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to FCM on Google Maps")
def direction_from_lecture_complex_to_foe():
    url = "https://www.google.com/maps/dir/Central+Lecture+Complex,+Cyberjaya,+Selangor/Faculty+of+Engineering,+Multimedia+University+-+MMU+Cyberjaya,+Persiaran+Multimedia,+63100+Cyberjaya,+Selangor/@2.9267289,101.6409283,18z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x31cdb6e8ee9603fb:0x5e22e91aeb8f5c0d!2m2!1d101.6424968!2d2.9278174!1m5!1m1!1s0x31cdb6e87ea95201:0x56a1170947b3c79!2m2!1d101.6411458!2d2.9263857?hl=en&entry=ttu"
    webbrowser.open(url)
    speak("Opening directions from Central Lecture Complex to FOE on Google Maps") 

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
                elif action["function"] == "search_on_google_maps_from":
                    search_on_google_maps_from(command)
                    update_output_text(output_label, f"Searching for directions on Google Maps.")
                elif action["function"] == "direction_from_fci_to_fom":
                    direction_from_fci_to_fom()
                    update_output_text(output_label, f"Opening direction from FCI to FOM on Google Maps.")
                elif action["function"] == "direction_from_fci_to_dtc":
                    direction_from_fci_to_dtc()
                    update_output_text(output_label, f"Opening direction from FCI to DTC on Google Maps.")
                elif action["function"] == "direction_from_fci_to_lecture_complex":
                    direction_from_fci_to_lecture_complex()
                    update_output_text(output_label, f"Opening direction from FCI to Central Lecture Complex on Google Maps.")
                elif action["function"] == "direction_from_fci_to_library":
                    direction_from_fci_to_library()
                    update_output_text(output_label, f"Opening direction from FCI to Library on Google Maps.")
                elif action["function"] == "direction_from_fci_to_fcm":
                    direction_from_fci_to_fcm()
                    update_output_text(output_label, f"Opening direction from FCI to FCM on Google Maps.")
                elif action["function"] == "direction_from_fci_to_foe":
                    direction_from_fci_to_fcm()
                    update_output_text(output_label, f"Opening direction from FCI to FOE on Google Maps.")
                elif action["function"] == "direction_from_fom_to_fci":
                    direction_from_fom_to_fci()
                    update_output_text(output_label, f"Opening direction from FOM to FCI on Google Maps.")
                elif action["function"] == "direction_from_fom_to_dtc":
                    direction_from_fom_to_dtc()
                    update_output_text(output_label, f"Opening direction from FOM to DTC on Google Maps.")
                elif action["function"] == "direction_from_fom_to_lecture_complex":
                    direction_from_fom_to_lecture_complex()
                    update_output_text(output_label, f"Opening direction from FOM to Central Lecture Complex on Google Maps.")
                elif action["function"] == "direction_from_fom_to_library":
                    direction_from_fom_to_library()
                    update_output_text(output_label, f"Opening direction from FOM to Library on Google Maps.")
                elif action["function"] == "direction_from_fom_to_fcm":
                    direction_from_fom_to_fcm()
                    update_output_text(output_label, f"Opening direction from FOM to FCM on Google Maps.")
                elif action["function"] == "direction_from_fom_to_foe":
                    direction_from_fom_to_fcm()
                    update_output_text(output_label, f"Opening direction from FOM to FOE on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_fci":
                    direction_from_dtc_to_fci()
                    update_output_text(output_label, f"Opening direction from DTC to FCI on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_fom":
                    direction_from_dtc_to_fom()
                    update_output_text(output_label, f"Opening direction from DTC to FOM on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_lecture_complex":
                    direction_from_dtc_to_lecture_complex()
                    update_output_text(output_label, f"Opening direction from DTC to Central Lecture Complex on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_library":
                    direction_from_dtc_to_library()
                    update_output_text(output_label, f"Opening direction from DTC to Library on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_fcm":
                    direction_from_dtc_to_fcm()
                    update_output_text(output_label, f"Opening direction from DTC to FCM on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_foe":
                    direction_from_dtc_to_foe()
                    update_output_text(output_label, f"Opening direction from DTC to FOE on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_fci":
                    direction_from_lecture_complex_to_fci()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to FCI on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_fom":
                    direction_from_lecture_complex_to_fom()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to FOM on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_dtc":
                    direction_from_lecture_complex_to_dtc()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to Central Lecture Complex on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_library":
                    direction_from_lecture_complex_to_library()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to Library on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_fcm":
                    direction_from_lecture_complex_to_fcm()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to FCM on Google Maps.")
                elif action["function"] == "direction_from_lecture_complex_to_foe":
                    direction_from_lecture_complex_to_foe()
                    update_output_text(output_label, f"Opening direction from Central Lecture Complex to FOE on Google Maps.")
                elif action["function"] == "direction_from_dtc_to_fci":
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

commands = load_commands()
