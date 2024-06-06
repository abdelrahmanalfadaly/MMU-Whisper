from Data.command_handler import *
from Data.speech_recognition import *
from Data.gui_setup import *

mode = "speech"

def main():
    global mode
    commands = load_commands()
    
    if mode == "text":
        root, input_entry, output_label, buttons = setup_text_interface()
        settingbs_button, stsrb_button = buttons
        srb_button = None
        sttb_button = None
    elif mode == "speech":
        root, input_entry, output_label, buttons = setup_speech_interface()
        settingbs_button, srb_button, sttb_button = buttons
        stsrb_button = None

    settingbs_button.config(command=lambda: open_file('.'))
    if srb_button:
        srb_button.config(command=start_speech_recognition)
    if sttb_button:
        sttb_button.config(command=lambda: switch_mode("text", root))
    if stsrb_button:
        stsrb_button.config(command=lambda: switch_mode("speech", root))

    def on_enter(event):
        command = input_entry.get().lower()
        handle_user_command(command, commands, output_label)

    if input_entry:
        input_entry.bind('<Return>', on_enter)
    
    root.mainloop()

if __name__ == "__main__":
    main()
