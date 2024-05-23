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

def setup_text_interface():
    root = tk.Tk()
    root.title("Text")
    root.geometry("400x500")
    root.configure(background="white")
    
    section1 = tk.Frame(root, bg="white", width=400, height=100)
    section1.grid(row=0, column=0, sticky="nsew")

    section2 = tk.Frame(root, bg="white", width=100, height=300)
    section2.grid(row=1, column=0, sticky="nsew")

    section3 = tk.Frame(root, bg="white", width=400, height=100)
    section3.grid(row=2, column=0, sticky="nsew")

    section4 = tk.Frame(root, bg="white", width=400, height=200)
    section4.grid(row=3, column=0, sticky="nsew")
    
    logo_image = tk.PhotoImage(file="Data/UI/Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    input_entry = tk.Entry(section2, bg="#e0e0e0", relief="flat", fg='grey')
    input_entry.pack(padx=40, pady=10, fill="y")

    button_frame = tk.Frame(section3, bg="white")
    button_frame.pack(expand=True, fill="both")
    
    settingbs_image = tk.PhotoImage(file="Data/UI/settingbs.png")
    settingbs = tk.Button(button_frame, image=settingbs_image, bg="white", relief="flat")
    settingbs.image = settingbs_image
    settingbs.pack(side="left", padx=(30, 10), pady=10, expand=True)

    srb_image = tk.PhotoImage(file="Data/UI/srb.png")
    srb = tk.Button(button_frame, image=srb_image, bg="white", relief="flat")
    srb.image = srb_image
    srb.pack(side="left", padx=(10, 10), pady=10, expand=True)

    sttb_image = tk.PhotoImage(file="Data/UI/sttb.png")
    sttb = tk.Button(button_frame, image=sttb_image, bg="white", relief="flat")
    sttb.image = sttb_image
    sttb.pack(side="left", padx=(10, 10), pady=10, expand=True)

    stsrb_image = tk.PhotoImage(file="Data/UI/stsrb.png")
    stsrb = tk.Button(button_frame, image=stsrb_image, bg="white", relief="flat")
    stsrb.image = stsrb_image
    stsrb.pack(side="left", padx=(10, 30), pady=10, expand=True)

    canvas = tk.Canvas(section4, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    output_label = tk.Label(canvas, text="", bg="#e6e6e6", fg="black")
    output_label.place(relx=0.5, rely=0.5, anchor="center")

    return root, input_entry, output_label, (settingbs, srb, sttb, stsrb)

def setup_speech_interface():
    root = tk.Tk()
    root.title("Speech")
    root.geometry("400x500")
    root.configure(background="white")
    
    section1 = tk.Frame(root, bg="white", width=400, height=150)
    section1.grid(row=0, column=0, sticky="nsew")

    section2 = tk.Frame(root, bg="white", width=400, height=150)
    section2.grid(row=1, column=0, sticky="nsew")

    section3 = tk.Frame(root, bg="white", width=400, height=200)
    section3.grid(row=2, column=0, sticky="nsew")
    
    logo_image = tk.PhotoImage(file="Data/UI/Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    button_frame = tk.Frame(section2, bg="white")
    button_frame.pack(expand=True, fill="both")
    
    settingbs_image = tk.PhotoImage(file="Data/UI/settingbs.png")
    settingbs = tk.Button(button_frame, image=settingbs_image, bg="white", relief="flat")
    settingbs.image = settingbs_image
    settingbs.pack(side="left", padx=(30, 10), pady=10, expand=True)

    srb_image = tk.PhotoImage(file="Data/UI/srb.png")
    srb = tk.Button(button_frame, image=srb_image, bg="white", relief="flat")
    srb.image = srb_image
    srb.pack(side="left", padx=(10, 10), pady=10, expand=True)

    sttb_image = tk.PhotoImage(file="Data/UI/sttb.png")
    sttb = tk.Button(button_frame, image=sttb_image, bg="white", relief="flat")
    sttb.image = sttb_image
    sttb.pack(side="left", padx=(10, 10), pady=10, expand=True)

    stsrb_image = tk.PhotoImage(file="Data/UI/stsrb.png")
    stsrb = tk.Button(button_frame, image=stsrb_image, bg="white", relief="flat")
    stsrb.image = stsrb_image
    stsrb.pack(side="left", padx=(10, 30), pady=10, expand=True)

    canvas = tk.Canvas(section3, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    output_label = tk.Label(canvas, text="", bg="#e6e6e6", fg="black")
    output_label.place(relx=0.5, rely=0.5, anchor="center")

    input_entry = None  # No input entry in speech mode

    return root, input_entry, output_label, (settingbs, srb, sttb, stsrb)

def update_output_text(output_label, text):
    if output_label:
        output_label.config(text=text)
