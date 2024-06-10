from functions.command_handler import *
from functions.gui_setup import *

def main(mode, output_label=None):
    print(f"Starting main with mode: {mode}")
    commands = load_commands()
    app_running = True
    
    def on_closing():
        nonlocal app_running
        app_running = False
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

    def on_closing():
        print("Closing application")
        root.destroy()

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

def on_enter(event, output_label):
    command = event.widget.get()
    handle_command(command, output_label)
    event.widget.delete(0, 'end')  # Clear the input field

def switch_mode(new_mode, root, current_mode, output_label):
    print(f"Switching mode from {current_mode} to {new_mode}")
    root.destroy()
    main(new_mode, output_label)

if __name__ == "__main__":
    mode = "speech"
    app_running = True
    output_label = None
    while app_running:
        mode, app_running, output_label = main(mode, output_label)
