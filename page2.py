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
    root.title("Page 2")
    root.geometry("400x500")
    root.configure(background="white")
    
    # Divide the window into 4 sections vertically
    section1 = tk.Frame(root, bg="white", width=400, height=100)
    section1.grid(row=0, column=0, sticky="nsew")

    section2 = tk.Frame(root, bg="white", width=100, height=300)
    section2.grid(row=1, column=0, sticky="nsew")

    section3 = tk.Frame(root, bg="white", width=400, height=100)
    section3.grid(row=2, column=0, sticky="nsew")

    section4 = tk.Frame(root, bg="white", width=400, height=200)
    section4.grid(row=3, column=0, sticky="nsew")
    
    # Add a logo to section 1
    logo_image = tk.PhotoImage(file="Logo.png")  
    logo_label = tk.Label(section1, image=logo_image, bg="white")
    logo_label.image = logo_image  
    logo_label.pack(pady=10)

    # Add standard size rounded text input to section 2
    input_entry = tk.Entry(section2, bg="#e0e0e0", relief="flat", fg='grey')
    input_entry.bind('<FocusIn>')
    input_entry.bind('<FocusOut>')
    input_entry.pack(padx=40, pady=1, fill="y")

    # Add buttons to section 3
    button_frame = tk.Frame(section3, bg="white")
    button_frame.pack(expand=True, fill="both")
    
    button1_image = tk.PhotoImage(file="button1.png")
    button1 = tk.Button(button_frame, image=button1_image, bg="white", relief="flat")
    button1.image = button1_image
    button1.pack(side="left", padx=(30, 10), pady=10, expand=True)

    button2_image = tk.PhotoImage(file="button2.5.png")
    button2 = tk.Button(button_frame, image=button2_image, bg="white", relief="flat")
    button2.image = button2_image
    button2.pack(side="left", padx=(10, 30), pady=10, expand=True)


    # Add a rounded rectangle label with gray background to section 4
    canvas = tk.Canvas(section4, bg="white", width=400, height=200, highlightthickness=0)
    canvas.pack(expand=True, fill="both")
    input_entry.focus()
    draw_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#e6e6e6", outline="", width=0)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
