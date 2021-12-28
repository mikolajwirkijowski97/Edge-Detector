from PIL import ImageTk as PImage
import numpy as np
from Canny import canny_edge_detection
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image
from mathTools import arr_to_img


# gets the current value of threshold slider
def get_current_value():
    return '{: .2f}'.format(current_value.get())


# images to be displayed in main canvas
tk_image = None
current_image = None
img = None

# applies edge detection with the set threshold value. Called on button call
def refresh_image():
    if not current_image:
        load_image()
    canvas.delete("all")
    val = float(get_current_value())
    print("USED VAL", val)
    global img
    img = canny_edge_detection(np.asarray(current_image), 0.5, val / 1500, 0.1)
    img = arr_to_img(img)
    global tk_image
    tk_image = PImage.PhotoImage(img)
    canvas.create_image(10, 10, anchor='nw', image=tk_image)


# loads image using the open file dialog window
def load_image():
    filename = askopenfilename()
    global current_image
    current_image = Image.open(filename)
    refresh_image()

# saves image to the place of user's choosing
def save_image():
    filename = asksaveasfilename(defaultextension = '.jpg')
    try:
        with open(filename, 'w') as _:
            img.save(filename)
    except FileNotFoundError:
        print("Cancelled save or error in filename")


# CREATE/CONFIGURE WINDOW
window = Tk()

window.title("Moja drużyna to fanatyk informatyki")
window.geometry("1920x1080")
window.configure(bg='grey')

# CREATE UI ELEMENTS
btn_refresh = Button(window, text="Refresh", fg='black', command=refresh_image)
btn_load = Button(window, text="Load", fg='black', command=load_image)
btn_save = Button(window, text="Save", fg="black", command=save_image)

# slider current value
current_value = DoubleVar()
slider = Scale(window, from_=0, to=255, orient='horizontal', variable=current_value)
slider.set(90)

canvas = Canvas(window, width=900, height=900, bg='black')

# PLACE UI ELEMENTS
btn_load.place(x=150, y=600)
btn_refresh.place(x=50, y=600)
btn_save.place(x=250, y=600)
slider.place(x=100, y=500)

# PACK THE CANVAS AND START THE WINDOW LOOP
canvas.pack()
window.mainloop()
