from command_handler import load_commands, handle_command, add_new_command
from speech_recognition import listen_for_commands
from gui_setup import setup_text_interface, setup_speech_interface

def main():
    mode = "speech"  # Change this to switch between text and speech mode
    commands = load_commands()

    if mode == "text":
        setup_text_interface()
    elif mode == "speech":
        setup_speech_interface()

    while True:
        if mode == "speech":
            command = input("\nEnter your command: ").lower()
        elif mode == "speech":
            command = listen_for_commands()
        
        if command == "exit":
            print("Exiting. Goodbye!")
            break
        
        if mode == "text" or (mode == "speech" and command):
            if handle_command(command, commands):
                add_new_command(commands)

if __name__ == "__main__":
    main()
