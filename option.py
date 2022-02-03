#coding:utf-8

import tkinter
import tkinter.filedialog
import os
import json
import time
import threading
import sys
import myTool
from images import images
from myRequests import myRequests
from myRequests import exwr
from myRequests import upLoadList
from myRequests import downLoadList
import customWindow
import math

class optionWindow:
    def __init__(self, window):
        self.window = window

        self.window.title(self.title)
        self.window.geometry(self.size)

        self.widget[0] = tkinter.Button(self.window, text="disconnection", command= lambda : [
            self.disconnection()
        ])
        self.widget[0].place(x=10, y=10)

        self.widget[1] = tkinter.Button(self.window, text="change password", command= lambda : [
            self.setCw("cpWindow")
        ])
        self.widget[1].place(x=10, y=50)

        self.widget[2] = tkinter.Button(self.window, text="back", command= lambda : [
            self.setCw("mainDriveWindow")
        ])
        self.widget[2].place(x=10, y=90)

    def disconnection(self):
        os.remove('identifier.json')
        os._exit(1)

    def setCw(self, ncw):
        self.cw = ncw
    
    def clear(self):
        t = 0
        while 1:
            try:
                self.widget[t]
            except: break
            else:
                self.widget[t].destroy()
            t = t + 1
    
    def refresh(self):
        if self.cw == "optionWindow":
            self.clear()
            self.__init__(self.window)

    cw = "optionWindow"
    title = "myDrive : Option"
    size = "200x200"
    window = {}
    widget = {}

class cpWindow:
    def __init__(self, window):
        self.window = window

        self.window.title(self.title)
        self.window.geometry(self.size)

        self.widget[0] = tkinter.Label(self.window, text="new PassWord", fg='black', font=("Helvetica", 10))
        self.widget[0].place(x=20, y=30)

        self.widget[1] = tkinter.Label(self.window, text="Confirm    \nnew PassWord", fg='black', font=("Helvetica", 10))
        self.widget[1].place(x=20, y=60)

        self.widget[2] = tkinter.Entry(self.window, bd=3, show="*", width=35)
        self.widget[2].place(x=120, y=30)

        self.widget[3] = tkinter.Entry(self.window, bd=3, show="*", width=35)
        self.widget[3].place(x=120, y=60)


        self.widget[4] = tkinter.Button(self.window, text="back", command= lambda: [
            self.setCw("optionWindow")
        ])
        self.widget[4].place(x=30, y=100)

        self.widget[5] = tkinter.Button(self.window, text="change password", command= lambda: [
            self.cp(self.widget[2].get(), self.widget[3].get())
        ])
        self.widget[5].place(x=120, y=100)

        self.widget[6] = tkinter.Label(window, text="", fg='red', font=("Helvetica", 7))
        self.widget[6].place(x=120, y=85)

    def cp(self, pw, cpw):
        if pw == "" or cpw == "":
            self.labelInfo("A box is empty", "red")

        elif f"{pw}" != f"{cpw}":
            self.labelInfo("Passwords is not equal", "red")
        
        elif len(f"{pw}") < 8:
            self.labelInfo("Password is too shot", "red")
        
        elif len(f"{pw}") > 21:
            self.labelInfo("Password is too tall", "red")

        else:
            log = {
                "action": "changePassword",
                "newPassword" : f"{pw}"
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)

            if rqt.result["status"] == "error":
                self.labelInfo(rqt.result["info"], "red")

            else:
                self.refresh()
                self.labelInfo(rqt.result["info"], "green")
                fileJson = json.loads(open("identifier.json").read().replace("'", '"'))
                fileJson["password"] = pw
                file = open("identifier.json", "w")
                file.write(json.dumps(fileJson))
                file.close()
                pass

    def labelInfo(self, info, color):
        try:
            self.widget[6].destroy()
        except: pass

        self.widget[6] = tkinter.Label(self.window, text=info, fg=color, font=("Helvetica", 7))
        self.widget[6].place(x=120, y=85)

    def setCw(self, ncw):
        self.cw = ncw
    
    def clear(self):
        t = 0
        while 1:
            try:
                self.widget[t]
            except: break
            else:
                self.widget[t].destroy()
            t = t + 1
    
    def refresh(self):
        if self.cw == "cpWindow":
            self.clear()
            self.__init__(self.window)

    cw = "cpWindow"
    title = "myDrive : Option"
    size = "365x135"
    window = {}
    widget = {}