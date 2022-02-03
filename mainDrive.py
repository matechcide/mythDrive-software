#coding:utf-8

import tkinter
import os
import asyncio
import time
import requests
import myTool
import threading
import json
import drive
import syncDrive
from myRequests import upLoadList
from myRequests import downLoadList
from myRequests import exwr
import customWindow
import option

def main(window, currentWindow):

    transferThread = threading.Thread(target=transfer)
    transferThread.start()

    while 1:
        if currentWindow.cw == "mainDriveWindow":
            currentWindow.clear()
            currentWindow = drive.mainDriveWindow(window)

            while currentWindow.cw == "mainDriveWindow":
                time.sleep(0.1)
                pass

        if currentWindow.cw == "mainSyncDriveWindow":
            tempdir = currentWindow.folderDir
            currentWindow.clear()
            currentWindow = syncDrive.mainSyncDriveWindow(window, tempdir)

            while currentWindow.cw == "mainSyncDriveWindow":
                time.sleep(0.1)
                pass

        if currentWindow.cw == "optionWindow":
            currentWindow.clear()
            currentWindow = option.optionWindow(window)

            while currentWindow.cw == "optionWindow":
                time.sleep(0.1)
                pass

        if currentWindow.cw == "cpWindow":
            currentWindow.clear()
            currentWindow = option.cpWindow(window)

            while currentWindow.cw == "cpWindow":
                time.sleep(0.1)
                pass

def transfer():
    def up():
        while 1:
            for file in upLoadList:
                drive.waitRequestFile('UpLoad', file[0], file[1])
                upLoadList.remove(file)

            time.sleep(0.1)
            pass

    def down():
        while 1:
            for file in downLoadList:
                drive.waitRequestFile('DownLoad', file[0], file[1])
                downLoadList.remove(file)

            time.sleep(0.1)
            pass

    upThread = threading.Thread(target=up)
    upThread.daemon = True
    upThread.start()

    downThread = threading.Thread(target=down)
    downThread.daemon = True
    downThread.start()