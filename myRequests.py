#coding:utf-8

import requests
import json
import sys
import threading
import time

exwr = {
    "destination": "",
    "Request": {}
}

upLoadList = []
downLoadList = []

class myRequests:
    def __init__(self, url, option, obj={}, files={}):
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

        elif option == "postFile":
            try:
                r = requests.post(url, headers=self.headers, files=files, data=obj)
            except:
                self.result = {
                    "status" : "error",
                    "info" : "connection to server not possible."
                }
            else:
                self.result = json.loads(r.text)
        
        elif option == "getFile":
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
        "token": sys.argv[1]
    }
