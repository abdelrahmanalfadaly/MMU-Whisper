import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

COMMANDS_FILE = 'data/custom.json'

def load_commands():
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_commands(commands):
    with open(COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

def add_new_command(command, command_type, response, exact_match):
    commands = load_commands()

    if command in commands:
        overwrite = messagebox.askyesno("Overwrite Command", "Command already exists. Do you want to overwrite it?")
        if not overwrite:
            return

    commands[command] = {
        "type": command_type,
        "response": response,
        "exact_match": exact_match
    }

    save_commands(commands)
    update_command_list()
    messagebox.showinfo("Success", f"Command '{command}' added successfully.")

def on_submit():
    command = command_entry.get().strip().lower()
    command_type_display = command_type_var.get().strip().lower()
    response = response_entry.get().strip()
    exact_match = exact_match_var.get()

    command_type_map = {
        "speak": "speak",
        "open website": "url",
        "open folder/file": "path"
    }
    command_type = command_type_map.get(command_type_display)

    if not command or not command_type or not response:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    add_new_command(command, command_type, response, exact_match)

def update_response_label(event):
    command_type_display = command_type_var.get().strip().lower()
    response_text_map = {
        "speak": "Enter response:",
        "open website": "Enter URL:",
        "open folder/file": "Enter path:"
    }
    response_label.config(text=response_text_map.get(command_type_display, "Enter the response:"))

def update_command_list():
    commands = load_commands()
    command_listbox.delete(0, tk.END)
    for command in commands:
        command_listbox.insert(tk.END, command)

def delete_selected_command():
    try:
        selected_command = command_listbox.get(command_listbox.curselection())
    except tk.TclError:
        messagebox.showwarning("Selection Error", "No command selected.")
        return

    commands = load_commands()
    if selected_command in commands:
        del commands[selected_command]
        save_commands(commands)
        update_command_list()
        messagebox.showinfo("Success", f"Command '{selected_command}' deleted successfully.")
    else:
        messagebox.showwarning("Deletion Error", f"Command '{selected_command}' not found.")

root = tk.Tk()
root.title("Add New Command")
root.geometry("500x500")

tk.Label(root, text="Phrase:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
command_entry = tk.Entry(root, width=30)
command_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Command Type:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
command_type_var = tk.StringVar()
command_type_combobox = ttk.Combobox(root, textvariable=command_type_var, width=27, state="readonly")
command_type_combobox['values'] = ("Speak", "Open Website", "Open Folder/File")
command_type_combobox.grid(row=1, column=1, padx=10, pady=10)
command_type_combobox.bind("<<ComboboxSelected>>", update_response_label)

response_label = tk.Label(root, text="Enter response:")
response_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
response_entry = tk.Entry(root, width=30)
response_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Exact Match:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
exact_match_var = tk.BooleanVar()
exact_match_checkbutton = tk.Checkbutton(root, text="Yes", variable=exact_match_var)
exact_match_checkbutton.grid(row=3, column=1, padx=10, pady=10, sticky="w")

submit_button = tk.Button(root, text="Add Command", command=on_submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

tk.Label(root, text="Commands List:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
command_listbox = tk.Listbox(root, width=50)
command_listbox.grid(row=5, column=1, padx=10, pady=10)

delete_button = tk.Button(root, text="Delete Selected Command", command=delete_selected_command)
delete_button.grid(row=6, column=0, columnspan=2, pady=10)

update_command_list()

root.mainloop()
