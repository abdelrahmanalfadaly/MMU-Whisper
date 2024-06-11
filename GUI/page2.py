from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("MMU Whisper")
root.geometry("350x400")


def button_a():
    text_2.insert(END,"Listening...\n")

logo_image= ImageTk.PhotoImage(file="logo.png")
image_level=Label(root,image=logo_image,height=150,width=350)
image_level.place(x=0,y=0)

text_1=Text(root)
text_1.place(x=50,y=170,width=250,height=35)
text_1.config(bg="#B5B5B5")

c_image= ImageTk.PhotoImage(file="c.png")
c_button=Button(root,image=c_image, height=65, width=65, borderwidth=0)
c_button.place(x=90,y=220)

a_image= ImageTk.PhotoImage(file="a.png")
a_button=Button(root,image=a_image, height=65, width=65, borderwidth=0, command=button_a)
a_button.place(x=190,y=220)

text_2=Text(root)
text_2.place(x=50,y=305,width=250,height=80)
text_2.config(bg="#B5B5B5")

root.mainloop()