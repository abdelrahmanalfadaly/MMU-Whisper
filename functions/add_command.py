import json
import os

COMMANDS_FILE = 'commands.json'

def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_commands(commands):
    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

def add_new_command():
    commands = load_commands()

    print("Adding a new command.")
    command = input("Enter the command phrase: ").strip().lower()
    command_type = input("Enter the command type (speak/url/path): ").strip().lower()
    response = input(f"Enter the {command_type}: ").strip()
    exact_match = input("Should this be an exact match? (yes/no): ").strip().lower() == 'yes'

    if command in commands:
        print("Command already exists. Overwriting the existing command.")

    commands[command] = {
        "type": command_type,
        "response": response,
        "exact_match": exact_match
    }

    save_commands(commands)
    print(f"Command '{command}' added successfully.")

if __name__ == "__main__":
    add_new_command()
