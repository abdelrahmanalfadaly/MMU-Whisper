from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("MMU Whisper")
root.geometry("350x400")


def button_a():
    text.insert(END,"Listening...\n")

logo_image= ImageTk.PhotoImage(file="logo.png")
image_level=Label(root,image=logo_image,height=150,width=350)
image_level.place(x=0,y=0)

c_image= ImageTk.PhotoImage(file="c.png")
c_button=Button(root,image=c_image, borderwidth=0)
c_button.place(x=20,y=150)

a_image= ImageTk.PhotoImage(file="a.png")
a_button=Button(root,image=a_image, borderwidth=0, command=button_a)
a_button.place(x=120,y=140)

b_image= ImageTk.PhotoImage(file="b.png")
b_button=Button(root,image=b_image, borderwidth=0)
b_button.place(x=250,y=150)

text=Text(root)
text.place(x=50,y=275,width=250,height=80)
text.config(bg="#B5B5B5")

root.mainloop()