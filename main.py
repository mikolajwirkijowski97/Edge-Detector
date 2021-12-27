from matplotlib import pyplot as plt
from PIL import ImageTk as PImage
import numpy as np
from Canny import canny_edge_detection
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
from mathTools import arr_to_img


def test():
    current_image = np.asarray(Image.open("test.jpg"))
    canny_edge_detection(current_image, 0.5, 0.8, 0.1)
    print("did it")




def get_current_value():
    return '{: .2f}'.format(current_value.get())


tk_image = None
current_image = None


def refresh_image():
    if not current_image:
        load_image()
    canvas.delete("all")
    val = float(get_current_value())
    print("USED VAL", val)
    img = canny_edge_detection(np.asarray(current_image), 0.5, val / 1500, 0.1)
    img = arr_to_img(img)
    global tk_image
    tk_image = PImage.PhotoImage(img)
    canvas.create_image(10, 10, anchor='nw', image=tk_image)


def load_image():
    filename = askopenfilename()
    global current_image
    current_image = Image.open(filename)
    refresh_image()


window = Tk()

window.title("Moja drużyna to fanatyk informatyki")
window.geometry("1920x1080")
window.configure(bg='grey')

btn_refresh = Button(window, text="Refresh", fg='black', command=refresh_image)
btn_load = Button(window, text="Load", fg='black', command=load_image)

# slider current value
current_value = DoubleVar()

slider = Scale(window, from_=0, to=255, orient='horizontal', variable=current_value)

btn_load.place(x=200, y=600)
btn_refresh.place(x=100, y=600)
slider.place(x=100, y=500)
canvas = Canvas(window, width=900, height=900, bg='black')
canvas.pack()
window.mainloop()
