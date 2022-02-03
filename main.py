#coding:utf-8

import auth
import tkinter
import os
import json
import time
import threading
import sys
import mainDrive
from myRequests import myRequests
from myRequests import exwr
from images import loadImages

window = tkinter.Tk()

loadImages()

class emptyWin:
    def  __init__(self, window):
        self.cw = window

    def clear(self):
        print('Init')

    cw = ""
    widget = ""

def main():

    currentWindow = emptyWin("loginWindow")

    if os.path.exists(os.path.dirname( os.path.realpath(__file__)) + "/identifier.json" ):
        def casr():
            time.sleep(0.5)
            log = json.load(open("identifier.json"))
            rqt = myRequests("http://mythdrive.ml:1080/ConnectAccount", "post", log)
            exwr["Request"] = rqt.result
            exwr["identifier"] = log
            exwr["destination"] = "waitRequest"

        currentWindow = emptyWin("waitRequest")
        coThead = threading.Thread(target=casr)
        coThead.start()

    if not os.path.exists(os.path.dirname( os.path.realpath(__file__)) + "\\download"):
        os.makedirs(os.path.dirname( os.path.realpath(__file__)) + "\\download")

    pass

    while 1:
        if currentWindow.cw == "loginWindow":
            currentWindow.clear()
            currentWindow = auth.loginWindow(window)

            while currentWindow.cw == "loginWindow":
                time.sleep(0.1)
                pass

        if currentWindow.cw == "createAccountWindow":
            currentWindow.clear()
            currentWindow = auth.createAccountWindow(window)

            while currentWindow.cw == "createAccountWindow":
                time.sleep(0.1)
                pass

        if currentWindow.cw == "waitRequest":
            currentWindow.clear()
            currentWindow = auth.waitRequest(window)

            while currentWindow.cw == "waitRequest":
                if(exwr["destination"] == "waitRequest"):
                    currentWindow.clear()
                    currentWindow.animation == False
                    currentWindow.receive(window, exwr["Request"]["status"], exwr["Request"]["info"], exwr["identifier"])
                    exwr["destination"] = ""
                    exwr["Request"] = ""
                    pass
                time.sleep(0.1)
                pass

        if currentWindow.cw == "mainDriveWindow":
            break
    
    mainDrive.main(window, currentWindow)
        

window.protocol("WM_DELETE_WINDOW", lambda : os._exit(1))
window.resizable(width=False, height=False)
mainThead = threading.Thread(target=main)
mainThead.start()

window.iconphoto(False, tkinter.PhotoImage(file='./app/images/ico.png'))
window.mainloop()
os._exit(1)
