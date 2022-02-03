import os
import json
import tkinter
import threading
import requests

class myRequests:
    def __init__(self, url, option, obj="none"):
        if option == "get":
            try:
                r = requests.get(url, headers=self.headers)
            except:
                self.result = {
                    "status" : "error",
                    "info" : "connection to server not possible."
                }
            else:
                self.result = json.loads(r.text)

        elif option == "post":
            try:
                r = requests.post(url, headers=self.headers, json=obj)
            except:
                self.result = {
                    "status" : "error",
                    "info" : "connection to server not possible."
                }
            else:
                self.result = json.loads(r.text)

    result = {}
    headers = {
        "user-agent": "clientMythDrive",
        "token": "get"
    }

rqt = myRequests("http://mythdrive.ml:1080/token", "get")
token = rqt.result["token"]

os.system("main.py " + token)

window = tkinter.Tk()