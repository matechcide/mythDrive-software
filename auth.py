#coding:utf-8

import tkinter
import os
import asyncio
import time
import requests
import myTool
import threading
from validate_email import validate_email
import json
from myRequests import myRequests
from myRequests import exwr


class loginWindow:
    def  __init__(self, window):

        self.widget[0] = tkinter.Label(window, text="mail", fg='black', font=("Helvetica", 10))
        self.widget[0].place(x=30, y=30)

        self.widget[1] = tkinter.Label(window, text="PassWord", fg='black', font=("Helvetica", 10))
        self.widget[1].place(x=30, y=60)

        self.widget[2] = tkinter.Entry(window, bd=3, width=35)
        self.widget[2].place(x=120, y=30)

        self.widget[3] = tkinter.Entry(window, bd=3, show="*", width=35)
        self.widget[3].place(x=120, y=60)

        self.widget[4] = tkinter.Button(window, text="Connect", command= lambda: [
            self.connectAccount(window, self.widget[2].get(), self.widget[3].get())
        ])
        self.widget[4].place(x=30, y=90)

        self.widget[5] = tkinter.Button(window, text="Create account", command= lambda: [
            self.setCw("createAccountWindow")
        ])
        self.widget[5].place(x=120, y=90)

        window.title(self.title)
        window.geometry(self.size)
    
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
    
    def connectAccount(self, window, mail, pw):
        if mail == "" or pw == "":
            self.labelInfo(window, "A box is empty")
        
        elif len(f"{pw}") < 8:
            self.labelInfo(window, "Password is too shot")
        
        elif len(f"{pw}") > 21:
            self.labelInfo(window, "Password is too tall")
        
        elif validate_email(f"{mail}") == False:
            self.labelInfo(window, "Email is not valide")

        else:
            def casr():
                log = {
                "mail" : f"{mail}",
                "password" : f"{pw}"
                }
                rqt = myRequests("http://mythdrive.ml:1080/ConnectAccount", "post", log)
                exwr["Request"] = rqt.result
                exwr["identifier"] = log
                exwr["destination"] = "waitRequest"


            self.setCw("waitRequest")
            tempThead = threading.Thread(target=casr)
            tempThead.start()
    
    def labelInfo(self, window, info):
        try:
            self.widget[6].destroy()
        except: pass

        self.widget[6] = tkinter.Label(window, text=info, fg='red', font=("Helvetica", 7))
        self.widget[6].place(x=120, y=120)

    cw = "loginWindow"
    widget = {}
    title = "myDrive : Auth"
    size = "365x150"
    

class createAccountWindow:
    def __init__(self, window):

        self.widget[0] = tkinter.Label(window, text="mail", fg='black', font=("Helvetica", 10))
        self.widget[0].place(x=30, y=30)

        self.widget[1] = tkinter.Label(window, text="PassWord", fg='black', font=("Helvetica", 10))
        self.widget[1].place(x=30, y=60)

        self.widget[2] = tkinter.Label(window, text="Confirm    \nPassWord", fg='black', font=("Helvetica", 10))
        self.widget[2].place(x=30, y=90)

        self.widget[3] = tkinter.Entry(window, bd=3, width=35)
        self.widget[3].place(x=120, y=30)

        self.widget[4] = tkinter.Entry(window, bd=3, show="*", width=35)
        self.widget[4].place(x=120, y=60)

        self.widget[5] = tkinter.Entry(window, bd=3, show="*", width=35)
        self.widget[5].place(x=120, y=100)


        self.widget[6] = tkinter.Button(window, text="back", command= lambda: [
            self.setCw("loginWindow")
        ])
        self.widget[6].place(x=30, y=140)

        self.widget[7] = tkinter.Button(window, text="Create account", command= lambda: [
            self.createAccount(window, self.widget[3].get(), self.widget[4].get(), self.widget[5].get())
        ])
        self.widget[7].place(x=120, y=140)

        window.title(self.title)
        window.geometry(self.size)

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
    
    def createAccount(self, window, mail, pw, cpw):
        if mail == "" or pw == "" or cpw == "":
            self.labelInfo(window, "A box is empty")

        elif f"{pw}" != f"{cpw}":
            self.labelInfo(window, "Passwords is not equal")
        
        elif len(f"{pw}") < 8:
            self.labelInfo(window, "Password is too shot")
        
        elif len(f"{pw}") > 21:
            self.labelInfo(window, "Password is too tall")
        
        elif validate_email(f"{mail}") == False:
            self.labelInfo(window, "Email is not valide")

        else:
            def casr():
                log = {
                    "mail" : f"{mail}",
                    "password" : f"{pw}"
                }
                rqt = myRequests("http://mythdrive.ml:1080/CreateAccount", "post", log)
                exwr["destination"] = "waitRequest"
                exwr["identifier"] = log
                exwr["Request"] = rqt.result

            self.setCw("waitRequest")
            tempThead = threading.Thread(target=casr)
            tempThead.start()
    
    def labelInfo(self, window, info):
        try:
            self.widget[8].destroy()
        except: pass

        self.widget[8] = tkinter.Label(window, text=info, fg='red', font=("Helvetica", 7))
        self.widget[8].place(x=120, y=170)

    cw = "createAccountWindow"
    widget = {}
    title = "myDrive : Create Account"
    size = "365x200"

class waitRequest:
    def __init__(self, window):

        window.title(self.title)
        window.geometry(self.size)
        size = self.size.split("x")
        self.widget[0] = tkinter.Canvas(window, width=size[0], height=size[1])
        self.widget[0].pack()
        self.widget[0].create_rectangle(0, 0, size[0], size[1], fill="#f0f0f0", outline="#f0f0f0", width=0)
        self.widget[0].create_rectangle(30, 100, 345, 125, fill="#ABABE7", outline="#FFFFFF", width=0)
        react1 = self.widget[0].create_rectangle(-50, 100, 30, 125, fill="#11E62B", outline="#FFFFFF", width=0)
        self.widget[0].create_rectangle(0, 100, 30, 125, fill="#f0f0f0", outline="#f0f0f0", width=0)
        self.widget[0].create_rectangle(345, 100, 415, 125, fill="#f0f0f0", outline="#f0f0f0", width=0)

        self.widget[1] = tkinter.Label(window, text="Waiting a requests :", fg='#000000', font=("Helvetica", 10))
        self.widget[1].place(x=30, y=72)

        def wwr():
            t = 0
            while self.animation == True:
                try:
                    if t >= 400:
                        self.widget[0].move(react1, -t, 0)
                        t = 0
                    t += 2
                    self.widget[0].move(react1, 2, 0)
                    time.sleep(0.01)
                    self.widget[0].update()
                    pass
                except: break

        waitThead = threading.Thread(target=wwr)
        waitThead.start()

    def receive(self, window, title, info, identifier={}):
        if title == "successful" and info == "Successful identification.":
            time.sleep(0.1)
            file = open("identifier.json", "w")
            file.write(json.dumps(identifier))
            file.close()
            self.setCw("mainDriveWindow")
        else:
            self.widget[0] = tkinter.Label(window, text=info, fg='black', font=("Helvetica", 10))
            self.widget[0].place(x=30, y=80)
            self.widget[1] = tkinter.Label(window, text=title, fg='black', font=("Helvetica", 15))
            self.widget[1].place(x=30, y=50)
            self.widget[2] = tkinter.Button(window, text="back", command= lambda: [
                self.setCw("loginWindow")
            ])
            self.widget[2].place(x=15, y=160)

    def setCw(self, ncw):
        self.cw = ncw
    
    def clear(self):
        t = 0
        while 1:
            try: self.widget[t]
            except: break
            else:
                try: self.widget[t].destroy()
                except: del self.widget[t]
            t = t + 1

    animation = True
    cw = "waitRequest"
    widget = {}
    title = "myDrive : Wait Response"
    size = "365x200"