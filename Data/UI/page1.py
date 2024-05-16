from tkinter import *
from PIL import Image
root = Tk()
root.title("MMU Wishper")
root.geometry("500x750")
root.config(bg="#DEDEDE")


frame = LabelFrame(root, relief="raised")
frame.grid(row=0, column=0,pady=00)

text_label= Label(frame,text="MMU Wishper", font=("DarkOrange",14))
text_label.grid(row=0,column=0)

e_image = PhotoImage(file="e.png")
image_label=Label(frame,image=e_image)
image_label.grid(row=1,column=0)

a_image = PhotoImage(file="a.png")
image_label=Label(frame,image=a_image)
image_label.grid(row=2,column=0)


c_image = PhotoImage(file="c.png")
image_label=Label(frame,image=c_image)
image_label.grid(row=2,column=1)
image_label.place(x=70, y=550)

b_image = PhotoImage(file="b.png")
image_label=Label(frame,image=b_image)
image_label.grid(row=2,column=2)
image_label.place(x=350, y=550)

text=Text(root)
text.grid(row=2,column=0)
text.place(x=70,y=657,width=366,height=80)
text.config(bg="#B5B5B5")

root.mainloop()