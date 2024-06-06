import tkinter as tk
import threading
import pygame
import os

# Initialize pygame mixer for playing sounds
pygame.mixer.init()

# Constants for the timer
STUDY_TIME = 0.1  # in minutes
SHORT_BREAK_TIME = 0.2  # in minutes
CYCLE = 4

STUDY_SEC = int(STUDY_TIME * 60)
SHORT_BREAK_SEC = int(SHORT_BREAK_TIME * 60)

STUDY_SOUND_FILE = "Data\\Study Tools\\break.mp3"
SHORT_BREAK_SOUND_FILE = "Data\\Study Tools\\study.mp3"

# Function to play local sound file
def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        
        self.timer_label = tk.Label(root, text="Timer", font=("Arial", 24))
        self.timer_label.pack(pady=20)
        
        self.time_label = tk.Label(root, text=f"{STUDY_SEC // 60}:{STUDY_SEC % 60:02d}", font=("Arial", 24))
        self.time_label.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=10)
        
        self.reps = 0
        self.timer_running = False
        self.paused = False
        self.time_left = STUDY_SEC
        self.is_study = True

    def reset_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer)
        self.time_label.config(text=f"{STUDY_SEC // 60}:{STUDY_SEC % 60:02d}")
        self.timer_label.config(text="Timer")
        self.reps = 0
        self.timer_running = False
        self.paused = False
        self.time_left = STUDY_SEC
        self.is_study = True

    def pause_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer)
            self.timer_running = False
            self.paused = True

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            if self.paused:
                self.paused = False
                self.count_down(self.time_left)
            else:
                self.is_study = True
                self.time_left = STUDY_SEC
                self.timer_label.config(text="Studying")
                self.count_down(self.time_left)

    def start_break(self):
        self.is_study = False
        self.time_left = SHORT_BREAK_SEC
        self.timer_label.config(text="Short Break")
        self.count_down(self.time_left)

    def count_down(self, count):
        minutes = count // 60
        seconds = count % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
        if count > 0:
            self.timer = self.root.after(1000, self.count_down, count - 1)
            self.time_left = count - 1
        else:
            threading.Thread(target=play_sound, args=(STUDY_SOUND_FILE if self.is_study else SHORT_BREAK_SOUND_FILE,)).start()
            if self.is_study:
                self.is_study = False
                self.start_break()  # Automatically start break session
            else:
                self.reps += 1
                if self.reps % CYCLE == 0:
                    self.timer_label.config(text="Cycle Completed")
                    self.timer_running = False
                else:
                    self.is_study = True
                    self.start_timer()  # Automatically start study session

def run():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    run()
