import os
import tkinter
import time
import tkinter.ttk as ttk

images = {}

def loadImages():
    for image in os.listdir('./app/images/'):
        img = os.path.join('./app/images/' + image)
        images[image] = tkinter.PhotoImage(file=img)