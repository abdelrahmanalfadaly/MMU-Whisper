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

def main():
    # Create the main window
    root = tk.Tk()
    root.title("MMU Whisper")
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
    logo_image = tk.PhotoImage(file="Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    # Add buttons to section 2
    button1_image = tk.PhotoImage(file="Button1.png")
    button1 = tk.Button(section2, image=button1_image, bg="white", borderwidth=0)
    button1.image = button1_image
    button1.grid(row=0, column=0, padx=(40, 5), pady=10)

    button2_image = tk.PhotoImage(file="Button2.png")
    button2 = tk.Button(section2, image=button2_image, bg="white", borderwidth=0)
    button2.image = button2_image
    button2.grid(row=0, column=1, padx=(5, 5), pady=10)

    button3_image = tk.PhotoImage(file="Button3.png")
    button3 = tk.Button(section2, image=button3_image, bg="white", borderwidth=0)
    button3.image = button3_image
    button3.grid(row=0, column=2, padx=(5, 40), pady=10)
    
    # Adjust column weights to center buttons
    section2.columnconfigure(0, weight=1)
    section2.columnconfigure(1, weight=1)
    section2.columnconfigure(2, weight=1)

    # Add a rounded rectangle label with gray background to section 3
    canvas = tk.Canvas(section3, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
