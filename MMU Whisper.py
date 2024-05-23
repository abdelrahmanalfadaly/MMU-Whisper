from Data.command_handler import load_commands, handle_command, add_new_command, open_file, update_output_text
from Data.speech_recognition import listen_for_commands
from Data.gui_setup import setup_text_interface, setup_speech_interface

mode = "speech"  # Change this to switch between text and speech mode

def main():
    global mode
    commands = load_commands()
    
    if mode == "text":
        root, input_entry, output_label, buttons = setup_text_interface()
    elif mode == "speech":
        root, input_entry, output_label, buttons = setup_speech_interface()

    settingbs_button, srb_button, sttb_button, stsrb_button = buttons

    settingbs_button.config(command=lambda: open_file('.'))
    srb_button.config(command=start_speech_recognition)
    sttb_button.config(command=lambda: switch_mode("text", root))
    stsrb_button.config(command=lambda: switch_mode("speech", root))

    def on_enter(event):
        command = input_entry.get().lower()
        handle_user_command(command, commands, output_label)

    if input_entry:
        input_entry.bind('<Return>', on_enter)
    
    root.mainloop()

def handle_user_command(command, commands, output_label):
    if command == "exit":
        print("Exiting. Goodbye!")
        exit()

    if handle_command(command, commands, output_label):
        add_new_command(commands)
    update_output_text(output_label, f"Processed command: {command}")

def start_speech_recognition():
    command = listen_for_commands()
    if command:
        handle_user_command(command, load_commands(), None)

def switch_mode(new_mode, root):
    global mode
    mode = new_mode
    root.destroy()
    main()

if __name__ == "__main__":
    main()
