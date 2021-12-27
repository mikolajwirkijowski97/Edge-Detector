from matplotlib import pyplot as plt
from PIL import ImageTk as PImage
import numpy as np
from Canny import canny_edge_detection
from tkinter import *
from PIL import Image
from mathTools import arr_to_img


def get_current_value():
    return '{: .2f}'.format(current_value.get())


tk_image = None


def refresh_image():
    canvas.delete("all")
    val = float(get_current_value())
    print("USED VAL", val)
    img = canny_edge_detection(np.asarray(current_image), 0.5, val / 2550, 0.1)
    img = arr_to_img(img)
    global tk_image
    tk_image = PImage.PhotoImage(img)
    canvas.create_image(200, 200, anchor='nw', image=tk_image)


window = Tk()
current_image = Image.open("test.jpg")

window.title("Moja drużyna to fanatyk informatyki")
window.geometry("1920x1080")
btn = Button(window, text="Refresh", fg='blue', command=refresh_image)

# slider current value
current_value = DoubleVar()

slider = Scale(window, from_=0, to=255, orient='horizontal', variable=current_value)

btn.place(x=100, y=600)
slider.place(x=100, y=500)
canvas = Canvas(window, width=900, height=900, bg='black')
canvas.pack()
window.mainloop()
