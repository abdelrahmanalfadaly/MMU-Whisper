import tkinter as tk

def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    canvas.create_polygon(points, **kwargs, smooth=True)

def on_focus_in(event):
    event.widget.config(fg='black')

def on_focus_out(event):
    if event.widget.get() == '':
        event.widget.config(fg='grey')

def setup_text_interface():
    root = tk.Tk()
    root.title("Text")
    root.geometry("400x500")
    root.configure(background="white")
    
    # Divide into 4 sections
    section1 = tk.Frame(root, bg="white", width=400, height=100)
    section1.grid(row=0, column=0, sticky="nsew")

    section2 = tk.Frame(root, bg="white", width=100, height=300)
    section2.grid(row=1, column=0, sticky="nsew")

    section3 = tk.Frame(root, bg="white", width=400, height=100)
    section3.grid(row=2, column=0, sticky="nsew")

    section4 = tk.Frame(root, bg="white", width=400, height=200)
    section4.grid(row=3, column=0, sticky="nsew")
    
    # logo at section 1
    logo_image = tk.PhotoImage(file="Data/UI/Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    # rounded input at section 2
    input_entry = tk.Entry(section2, bg="#e0e0e0", relief="flat", fg='grey')
    input_entry.bind('<FocusIn>', on_focus_in)
    input_entry.bind('<FocusOut>', on_focus_out)
    input_entry.pack(padx=40, pady=10, fill="y")

    # buttons at section 3
    button_frame = tk.Frame(section3, bg="white")
    button_frame.pack(expand=True, fill="both")
    
    settingbs_image = tk.PhotoImage(file="Data/UI/settingbs.png")
    settingbs = tk.Button(button_frame, image=settingbs_image, bg="white", relief="flat")
    settingbs.image = settingbs_image
    settingbs.pack(side="left", padx=(30, 10), pady=10, expand=True)

    stsrb_image = tk.PhotoImage(file="Data/UI/stsrb.png")
    stsrb = tk.Button(button_frame, image=stsrb_image, bg="white", relief="flat")
    stsrb.image = stsrb_image
    stsrb.pack(side="left", padx=(10, 30), pady=10, expand=True)

    # rounded rectangle label at section 4
    canvas = tk.Canvas(section4, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    input_entry.focus()
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    output_label = tk.Label(canvas, text="", bg="#e6e6e6", fg="black")
    output_label.place(relx=0.5, rely=0.5, anchor="center")

    return root, input_entry, output_label, (settingbs, stsrb)

def setup_speech_interface():
    root = tk.Tk()
    root.title("Speech")
    root.geometry("400x500")
    root.configure(background="white")
    
    # Divide the window into 3 sections horizontally
    section1 = tk.Frame(root, bg="white", width=400, height=150)
    section1.grid(row=0, column=0, sticky="nsew")

    section2 = tk.Frame(root, bg="white", width=400, height=150)
    section2.grid(row=1, column=0, sticky="nsew")

    section3 = tk.Frame(root, bg="white", width=400, height=200)
    section3.grid(row=2, column=0, sticky="nsew")
    
    # Add a logo to section 1
    logo_image = tk.PhotoImage(file="Data/UI/Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    # Add buttons to section 2
    settingbs_image = tk.PhotoImage(file="Data/UI/settingbs.png")
    settingbs = tk.Button(section2, image=settingbs_image, bg="white", borderwidth=0)
    settingbs.image = settingbs_image
    settingbs.grid(row=0, column=0, padx=(40, 5), pady=10)

    srb_image = tk.PhotoImage(file="Data/UI/srb.png")
    srb = tk.Button(section2, image=srb_image, bg="white", borderwidth=0)
    srb.image = srb_image
    srb.grid(row=0, column=1, padx=(5, 5), pady=10)

    sttb_image = tk.PhotoImage(file="Data/UI/sttb.png")
    sttb = tk.Button(section2, image=sttb_image, bg="white", borderwidth=0)
    sttb.image = sttb_image
    sttb.grid(row=0, column=2, padx=(5, 40), pady=10)
    
    # Adjust column weights to center buttons
    section2.columnconfigure(0, weight=1)
    section2.columnconfigure(1, weight=1)
    section2.columnconfigure(2, weight=1)

    # Add a rounded rectangle label with gray background to section 3
    canvas = tk.Canvas(section3, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    output_label = tk.Label(canvas, text="", bg="#e6e6e6", fg="black")
    output_label.place(relx=0.5, rely=0.5, anchor="center")

    return root, None, output_label, (settingbs, srb, sttb)

def update_output_text(output_label, text):
    if output_label:
        output_label.config(text=text)
