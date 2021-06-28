from tkinter import *
from PIL import Image, ImageSequence, ImageTk
from threading import Thread
from tkinter import ttk
from typing import ClassVar, List
from time import sleep
main_window: ClassVar = Tk()
main_window.title("ANIMATION")
main_window.geometry("250x250")
main_window.iconbitmap("icon.ico")
# main_window.resizable(width=FALSE, height=FALSE)
main_window.configure(background="#fff")
updater_theme = ttk.Style()
updater_theme.theme_use('clam')
updater_theme.configure("TLabel", background='#fff', foreground='#000', border='0')
img_frames: List = []


def load_img():
    global img_frames
    img: ClassVar = Image.open("download_light.gif")
    for frame in ImageSequence.Iterator(img):
        img_frames.append(ImageTk.PhotoImage(frame.copy().convert('RGBA')))
    while True:
        for frame in img_frames:
            image_label.configure(image=frame)
            sleep(0.015)



image_label: ClassVar = ttk.Label(main_window, image=None)
Thread(target=load_img, daemon=True).start()
image_label.place(relx=0.5, rely=0.5, anchor="center")
main_window.mainloop()