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

class mainSyncDriveWindow:
    def __init__(self, window, dir):
        self.window = window
        self.folderDir = dir
        self.nameSyncFolder = "/" + dir.split('/')[1]

        self.widget[0] = tkinter.ttk.Treeview(self.window, columns=("Size"), height=19)
        self.widget[0].place(x=30, y=30)
        self.widget[0].bind('<Double-1>', self.selectItem) #<<TreeviewSelect>>
        self.widget[0].heading("#0", text="Name")
        self.widget[0].column("#0", minwidth=300, width=300)
        self.widget[0].heading("Size", text="Size")
        self.widget[0].column("Size", minwidth=100, width=100)

        if dir == self.nameSyncFolder + "/" and self.syncPath == "":
            temp = str(open('identifier.json').read().replace("\'", "\""))
            temp = json.loads(temp)
            try:
                if os.path.exists(temp[self.nameSyncFolder]):
                    self.linkPath(temp[self.nameSyncFolder])
            except: pass
        
        if self.syncPath == "":
            self.widget[1] = tkinter.Button(self.window, text="link Path", command= lambda : [
                self.linkPath()
            ])
        else:
            self.widget[1] = tkinter.Button(self.window, text="change Path", command= lambda : [
                self.linkPath()
            ])
        self.widget[1].place(x=30, y=465)

        self.widget[2] = tkinter.Label(self.window, text="", font=("Helvetica", 7))
        self.widget[2].place(x=210, y=440)

        self.widget[3] = tkinter.Label(self.window, text="Folder " + self.folderDir.replace("|typeFolder|", " "), font=("Helvetica", 10))
        self.widget[3].place(x=30, y=5)

        self.widget[4] = tkinter.Button(self.window, text="back", command= lambda : [
            self.back()
        ])
        self.widget[4].place(x=450, y=30)

        self.widget[5] = tkinter.Label(self.window, text="", font=("Helvetica", 8))
        self.widget[5].place(x=30, y=440)

        self.widget[6] = tkinter.Button(self.window, text="refresh", command= lambda : [
            self.refresh()
        ])
        self.widget[6].place(x=500, y=30)

        self.widget[7] = tkinter.Label(self.window, text=self.syncPath, font=("Helvetica", 8))
        self.widget[7].place(x=110, y=470)

        self.window.title(self.title)
        self.window.geometry(self.size)

        loadListThead = threading.Thread(target=self.loadDir)
        loadListThead.start()

    def loadDir(self):
        log = {
            "dir": f"{self.folderDir}"
        }
        rqt = myRequests("http://mythdrive.ml:1080/DriveList", "post", log)
        self.sizeDrive = int(rqt.result['size'])
        size = f"{round(int(rqt.result['size'])/1024/1024/1024, 2)}" + "/10Go"
        self.widget[5] = tkinter.Label(self.window, text=size, font=("Helvetica", 8))
        self.widget[5].place(x=30, y=440)

        self.listFile = {}
        self.listFolder = {}
        self.listSyncFolder = {}

        if(rqt.result["status"] == "successful"):
            t = 1
            for folder in rqt.result["dir"]:
                self.widget[0].insert("", t, text="  " + folder, image=imagesDisplay('folder', folder))
                self.listFolder[str(hex(t))] = folder
                t += 1

            for file in rqt.result["file"]:
                file = file.split("!")
                size = int(file[1])
                if size < 1024:
                    size = f"{size}" + "o"
                elif size < 1024*1024:
                    size = f"{round(size/1024, 2)}" + "Ko"
                elif size < 1024*1024*1024:
                    size = f"{round(size/1024/1024, 2)}" + "Mo"
                elif size < 1024*1024*1024*1024:
                    size = f"{round(size/1024/1024/1024, 2)}" + "Go"
                self.widget[0].insert("", t, text="  " + file[0], values=(size), image=imagesDisplay('file', file[0]))
                self.listFile[str(hex(t))] = file
                t += 1

        else:
            self.labelInfo(rqt.result["info"], "red")

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
        if self.cw == "mainSyncDriveWindow":
            self.clear()
            self.__init__(self.window, self.folderDir)

    def labelInfo(self, info, color):
        try:
            self.widget[2].destroy()
        except: pass

        self.widget[2] = tkinter.Label(self.window, text=info, fg=color, font=("Helvetica", 7))
        self.widget[2].place(x=210, y=440)

    def back(self):
        folderDir = self.folderDir.split('/')
        folderDir[len(folderDir)-2] = ""
        self.folderDir = ""
        for folder in folderDir:
            if folder != "":
                self.folderDir += f"/{folder}"
        
        self.folderDir += "/"
        if self.folderDir == "/":
            self.syncPath = ""
            self.cw = "mainDriveWindow"
        else:
            self.refresh()
    
    def addFolder(self, folder):
            log = {
                "action": "createFolder",
                "name": folder[2],
                "dir": self.nameSyncFolder + folder[1],
                "syncInfo": self.nameSyncFolder
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
            if(rqt.result["status"] == "successful"):
                pass
            else:
                self.labelInfo(rqt.result["info"], "red")

    def selectItem(self, event):
        try: 
            self.widget[0].selection()[0]
        except: 
            return

        hexDesign = str(hex(int("0X" + self.widget[0].selection()[0].replace('I', ''), 16)))
        type = ""

        try: 
            self.listFile[hexDesign]
            type = "file"
        except:
            try: 
                self.listFolder[hexDesign]
                type = "folder"
            except:
                try: 
                    self.listSyncFolder[hexDesign]
                    type = "syncFolder"
                except: return
        
        if type == "folder":
            self.folderDir = self.folderDir + self.listFolder[hexDesign] + "/"
            self.refresh()
    
    def deleteFolder(self, file):
                
        log = {
            "action": "delete",
            "dir": self.nameSyncFolder + file[1] + file[2]
        }
        rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
        if(rqt.result["status"] == "successful"):
            pass
        else:
            self.labelInfo(rqt.result["info"], "red")

    def selectFile(self, file):
        dir = self.nameSyncFolder + file[1]
        if self.sizeDrive + os.path.getsize(self.syncPath + file[1] + file[2]) > 10*1024*1024*1024:
            self.labelInfo("File too big.", "red")
            return
        
        log = {
            "dir": f"{dir}",
            "lm": math.floor(os.stat(self.syncPath + file[1] + file[2]).st_mtime)
        }

        files = {
            "file": open(self.syncPath + file[1] + file[2], "rb")
        }

        upLoadList.append([files,log])       

    def linkPath(self, file=""):
        if file == "":
            file = tkinter.filedialog.askdirectory(initialdir = os.path.dirname(os.path.realpath(__file__)) + "/../../../..", title='Please select a directory')
            if file == "":
                return

        wt = ["Sync Choice", "250", "170"]
        t = [
            ["label", "Choose the type of synchronization.", 10, 20, 40],
            ["label", file, 8, 20, 70],
            ["button", "DowLoad & Sync", "d&s", 10, 100],
            ["button", "UpLoad & Sync", "u&s", 150, 100],
            ["button", "cancel", "close", 10, 135]
        ]
        choice = customWindow.choiceWindow(wt, t)
        
        while choice.result == "":
            time.sleep(0.1)

        if choice.result == "close":
            return

        elif choice.result == "u&s":
            log = {
            "action": "listSync",
            "dir": self.nameSyncFolder
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)

            self.syncPath = file

            self.oldList = {
                self.syncPath.split('/')[len(self.syncPath.split('/'))-1]: rqt.result["info"][self.nameSyncFolder[1:]]
            }

            temp = str(open('identifier.json').read().replace("\'", "\""))
            temp = json.loads(temp)
            temp[self.nameSyncFolder] = file

            tempFile = open("identifier.json", "w")
            tempFile.write(json.dumps(temp))
            tempFile.close()

            try:
                if self.syncThread.is_alive():
                    return
            except:
                self.syncThread = threading.Thread(target=self.syncFolder)
                self.syncThread.daemon = True
                self.syncThread.start()

        elif choice.result == "d&s":
            log = {
            "action": "listSync",
            "dir": self.nameSyncFolder
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
            self.syncPath = file

            self.oldList = {
                self.syncPath.split('/')[len(self.syncPath.split('/'))-1]: rqt.result["info"][self.nameSyncFolder[1:]]
            }

            temp = str(open('identifier.json').read().replace("\'", "\""))
            temp = json.loads(temp)
            temp[self.nameSyncFolder] = file

            tempFile = open("identifier.json", "w")
            tempFile.write(json.dumps(temp))
            tempFile.close()
            
            listFile = self.loopFile(self.syncPath)
            folderName = self.syncPath.split('/')[len(self.syncPath.split('/'))-1]

            def rm(folderName, object1, object2):
                
                for folder in object1[folderName]["**folder**"]:
                    if folder in object2[folderName]["**folder**"]:
                        rm(folder, object1[folderName][folder], object2[folderName][folder])
                        continue
                    else:
                        os.rmdir(self.syncPath + "/" + object2[folderName]["**path**"] + folder)

                for file in object1[folderName]["**file**"]:
                    if file in object2[folderName]["**file**"]:
                        continue
                    else:
                        os.remove(self.syncPath + object1[folderName]["**path**"] + file[0])
                
                return

            rm(folderName, listFile, self.oldList)
            
            def ad(folderName, object1, object2):
                
                for folder in object1[folderName]["**folder**"]:
                    if folder in object2[folderName]["**folder**"]:
                        ad(folder, object1[folderName][folder], object2[folderName][folder])
                        continue
                    else:
                        os.mkdir(self.syncPath + "/" + object1[folderName]["**path**"] + folder)
                        object2[folderName][folder] = {
                            folder: {
                            "**file**": [],
                            "**folder**" : [],
                            "**path**": ""
                            }
                        }
                        ad(folder, object1[folderName][folder], object2[folderName][folder])

                for file in object1[folderName]["**file**"]:
                    if file in object2[folderName]["**file**"]:
                        continue
                    else:
                        log = {
                            "dir": self.folderDir + object1[folderName]["**path**"] + file[0]
                        }
                        downLoadList.append([self.syncPath + object1[folderName]["**path**"] + file[0],log])
                
                return

            ad(folderName, self.oldList, listFile)

            def wait():
                while 1:
                    time.sleep(2)
                    try:
                        downLoadList[0]
                    except:
                        try:
                            upLoadList[0]
                        except: break

                try:
                    if self.syncThread.is_alive():
                        return
                except:
                    self.syncThread = threading.Thread(target=self.syncFolder)
                    self.syncThread.daemon = True
                    self.syncThread.start()

            waitThread = threading.Thread(target=wait)
            waitThread.start()

    def syncFolder(self):
        while self.syncPath != "":
            add = []
            addfolder = []
            remove = []
            listFile = self.loopFile(self.syncPath)
            folderName = self.syncPath.split('/')[len(self.syncPath.split('/'))-1]

            def rm(folderName, object1, object2):
                for file in object2[folderName]["**file**"]:
                    if file in object1[folderName]["**file**"]:
                        continue
                    else:
                        remove.append(['file', object1[folderName]["**path**"], file[0]])
                
                for folder in object2[folderName]["**folder**"]:
                    if folder in object1[folderName]["**folder**"]:
                        rm(folder, object1[folderName][folder], object2[folderName][folder])
                        continue
                    else:
                        remove.append(['folder', object1[folderName]["**path**"], folder])
                
                return
                
            def ad(folderName, object1, object2):
                for file in object1[folderName]["**file**"]:
                    if file in object2[folderName]["**file**"]:
                        continue
                    else:
                        add.append(['file', object1[folderName]["**path**"], file[0]])
                
                for folder in object1[folderName]["**folder**"]:
                    if folder in object2[folderName]["**folder**"]:
                        ad(folder, object1[folderName][folder], object2[folderName][folder])
                        continue
                    else:
                        addfolder.append(['folder', object1[folderName]["**path**"], folder])
                        object2[folderName][folder] = {
                            folder: {
                            "**file**": [],
                            "**folder**" : [],
                            "**path**": ""
                            }
                        }
                        ad(folder, object1[folderName][folder], object2[folderName][folder])
                
                return

            rm(folderName, listFile, self.oldList)

            for send in remove:
                self.deleteFolder(send)

            ad(folderName, listFile, self.oldList)

            for send in addfolder:
                self.addFolder(send)

            for send in add:
                self.selectFile(send)

            self.oldList = listFile

            time.sleep(5)

    def loopFile(self, pathFolder):
        allFile = {}
        folderName = pathFolder.split('/')[len(pathFolder.split('/'))-1]
        allFile[folderName] = {
            "**file**": [],
            "**folder**" : [],
            "**path**": pathFolder.replace(self.syncPath, '') + "/" 
        }
        for path in os.listdir(pathFolder):
            if os.path.isfile(pathFolder + "/" + path):
                if path != "syncInfo":
                    allFile[folderName]["**file**"].append([path, math.floor(os.stat(pathFolder + "/" + path).st_mtime)])
            else:
                allFile[folderName]["**folder**"].append(path)
                allFile[folderName][path] = self.loopFile(pathFolder + "/" + path)
        return allFile

    choice = ""
    nameSyncFolder = ""
    syncPath = ""
    oldList = {}
    sendStatus = False
    sizeDrive = 0
    cw = "mainSyncDriveWindow"
    folderDir = "/"
    title = "myDrive : Sync Drive"
    size = "800x500"
    window = {}
    widget = {}
    listFile = {}
    listFolder = {}
    listSyncFolder = {}
    syncThread = {}

def imagesDisplay(type, name):
    if type == "file":
        name = name.split('.')
        n = len(name)-1
        name[n] = name[n].lower()
        if name[n] in ['png','jpg']:
            return images['fileImage.png']

        elif name[n] in ['zip','gz','rar','iso']:
            return images['fileZip.png']

        elif name[n] in ['mp4','avi','mkv']:
            return images['fileVideo.png']

        elif name[n] in ['sldprt','sldasm','slddrw','slddrt']:
            return images['file3D.png']

        elif name[n] in ['mp3']:
            return images['fileAudio.png']
        
        else:
            return images['file.png']

    if type == "folder":
        if '|typeFolder|' in name:
            name = name.split('|typeFolder|')
            n = len(name)-1
            if name[n] == "Sync":
                return images['syncFolder.png']
            elif name[n] == "Project":
                return images['projectFolder.png']
        
        else:
            return images['folder.png']