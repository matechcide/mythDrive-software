#coding:utf-8

import auth
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
import math
import requests
import time
import customWindow

class mainDriveWindow:
    def __init__(self, window):
        self.window = window

        self.widget[0] = tkinter.ttk.Treeview(self.window, columns=("Size"), height=19)
        self.widget[0].place(x=30, y=30)
        self.widget[0].bind('<Double-1>', self.selectItem) #<<TreeviewSelect>>
        self.widget[0].heading("#0", text="Name")
        self.widget[0].column("#0", minwidth=300, width=300)
        self.widget[0].heading("Size", text="Size")
        self.widget[0].column("Size", minwidth=100, width=100)

        self.widget[1] = tkinter.Button(self.window, text="add SyncFolder", command= lambda : [
            self.addSyncFolder(self.widget[3].get())
        ])
        if self.folderDir == "/":
            self.widget[1].place(x=30, y=465)

        self.widget[2] = tkinter.Button(self.window, text="add Folder", command= lambda : [
            self.addFolder(self.widget[3].get())
        ])
        self.widget[2].place(x=130, y=465)

        self.widget[3] = tkinter.Entry(self.window, bd=3, width=35)
        self.widget[3].place(x=210, y=465)

        self.widget[4] = tkinter.Label(self.window, text="", font=("Helvetica", 7))
        self.widget[4].place(x=210, y=440)

        self.widget[5] = tkinter.Label(self.window, text="Folder " + self.folderDir.replace("|typeFolder|", " "), font=("Helvetica", 10))
        self.widget[5].place(x=30, y=5)

        self.widget[6] = tkinter.Button(self.window, text="back", command= lambda : [
            self.back()
        ])
        self.widget[6].place(x=450, y=30)

        self.widget[7] = tkinter.Button(self.window, text="delete", command= lambda : [
            self.deleteFolder()
        ])
        self.widget[7].place(x=450, y=70)

        self.widget[8] = tkinter.Button(self.window, text="send file", command= lambda : [
            self.selectFile()
        ])
        self.widget[8].place(x=450, y=110)

        self.widget[9] = tkinter.Label(self.window, text="", font=("Helvetica", 8))
        self.widget[9].place(x=30, y=440)

        self.widget[10] = tkinter.Button(self.window, text="refresh", command= lambda : [
            self.refresh()
        ])
        self.widget[10].place(x=520, y=30)

        self.widget[11] = tkinter.Button(self.window, text="option", command= lambda : [
            self.setCw("optionWindow")
        ])
        self.widget[11].place(x=520, y=70)

        self.widget[12] = tkinter.Button(self.window, text="rename", command= lambda : [
            self.rename(self.widget[3].get())
        ])
        self.widget[12].place(x=440, y=465)

        self.widget[13] = tkinter.Button(self.window, text="deplace", command= lambda : [
            self.deplace()
        ])
        self.widget[13].place(x=450, y=150)

        self.widget[14] = tkinter.Label(self.window, text=self.fileMove[0] + self.fileMove[1], font=("Helvetica", 10))
        self.widget[14].place(x=515, y=152)

        self.window.title(self.title)
        self.window.geometry(self.size)

        loadListThead = threading.Thread(target=self.loadDir)
        loadListThead.start()
    
    def loadDir(self):
        log = {
            "dir": f"{self.folderDir}"
        }
        rqt = myRequests("http://mythdrive.ml:1080/DriveList", "post", log)
    
        self.listFile = {}
        self.listFolder = {}
        self.listSyncFolder = {}

        if(rqt.result["status"] == "successful"):
            self.sizeDrive = int(rqt.result['size'])
            size = f"{round(int(rqt.result['size'])/1024/1024/1024, 2)}" + "/10Go"
            self.widget[9] = tkinter.Label(self.window, text=size, font=("Helvetica", 8))
            self.widget[9].place(x=30, y=440)

            t = 1
            for folder in rqt.result["dir"]:
                self.widget[0].insert("", t, text="  " + folder, image=imagesDisplay('folder', folder))
                self.listFolder[str(hex(t))] = folder
                t += 1
            
            for folder in rqt.result["syncDir"]:
                self.widget[0].insert("", t, text="  " + folder.replace('|typeFolder|Sync', ''), image=imagesDisplay('folder', folder))
                self.listSyncFolder[str(hex(t))] = folder
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
        if self.cw == "mainDriveWindow":
            self.clear()
            self.__init__(self.window)

    def labelInfo(self, info, color):
        try:
            self.widget[4].destroy()
        except: pass

        self.widget[4] = tkinter.Label(self.window, text=info, fg=color, font=("Helvetica", 7))
        self.widget[4].place(x=210, y=440)

    def back(self):
        folderDir = self.folderDir.split('/')
        folderDir[len(folderDir)-2] = ""
        self.folderDir = ""
        for folder in folderDir:
            if folder != "":
                self.folderDir += f"/{folder}"
        
        self.folderDir += "/"
        self.refresh()

    def deplace(self):
        
        if self.fileMove[0] == "":
            try: 
                self.widget[0].selection()[0]
            except: 
                self.labelInfo("Select a item please.", "red")
                return

            try: 
                self.widget[0].selection()[1]
            except: pass
            else:
                self.labelInfo("Select only one item.", "red")
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

            if type == "syncFolder": return

            if type == "file":
                self.fileMove[0] = self.folderDir
                self.fileMove[1] = self.listFile[hexDesign][0]
                
            elif type == "folder":
                self.fileMove[0] = self.folderDir
                self.fileMove[1] = self.listFolder[hexDesign][0] + "/"
        
            self.refresh()

        else:
            log = {
                "action": "rename",
                "old": self.fileMove[0] + self.fileMove[1],
                "new": self.folderDir + self.fileMove[1]
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
            self.fileMove = ["",""]
            if(rqt.result["status"] == "successful"):
                self.refresh()
            else:
                self.labelInfo(rqt.result["info"], "red")

    def rename(self, name):
        try: 
            self.widget[0].selection()[0]
        except: 
            self.labelInfo("Select a item please.", "red")
            return

        try: 
            self.widget[0].selection()[1]
        except: pass
        else:
            self.labelInfo("Select only one item.", "red")
            return
        
        if name == "" or len(f"{name}") >= 30 or "|" in name or ".." in name or "/" in name:
            self.labelInfo("Name is invalid.", "red")

        else:
            hexDesign = str(hex(int("0X" + self.widget[0].selection()[0].replace('I', ''), 16)))
            if int(hexDesign, 16) <= len(self.listFolder):
                log = {
                    "action": "rename",
                    "old": self.folderDir + self.listFolder[hexDesign] + "/",
                    "new": self.folderDir + name + "/"
                }
                rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
                if(rqt.result["status"] == "successful"):
                    self.refresh()
                else:
                    self.labelInfo(rqt.result["info"], "red")
                
            elif int(hexDesign, 16) <= len(self.listSyncFolder) + len(self.listFolder):
                log = {
                    "action": "rename",
                    "old": self.folderDir + self.listSyncFolder[hexDesign] + "/",
                    "new": self.folderDir + name + "|typeFolder|Sync/"
                }
                rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
                if(rqt.result["status"] == "successful"):
                    self.refresh()
                else:
                    self.labelInfo(rqt.result["info"], "red")

            else:
                ext = "." + self.listFile[hexDesign][0].split(".")[len(self.listFile[hexDesign][0].split("."))-1]
                name = name + ext
                log = {
                    "action": "rename",
                    "old": self.folderDir + self.listFile[hexDesign][0],
                    "new": self.folderDir + name 
                }
                rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
                if(rqt.result["status"] == "successful"):
                    self.refresh()
                else:
                    self.labelInfo(rqt.result["info"], "red")

    def addFolder(self, name):
        if name == "" or len(f"{name}") >= 30 or "|" in name or ".." in name or "/" in name:
            self.labelInfo("Name is invalid.", "red")
        else:
            log = {
                "action": "createFolder",
                "name": f"{name}",
                "dir": f"{self.folderDir}"
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
            if(rqt.result["status"] == "successful"):
                self.refresh()
            else:
                self.labelInfo(rqt.result["info"], "red")
    
    def addSyncFolder(self, name):
        if name == "" or len(f"{name}") >= 30 or "|" in name or ".." in name or "/" in name:
            self.labelInfo("Name is invalid.", "red")
            
        else:
            log = {
                "action": "createFolder",
                "name": f"{name}|typeFolder|Sync",
                "dir": f"{self.folderDir}"
            }
            rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
            if(rqt.result["status"] == "successful"):
                self.refresh()
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

        elif type == "syncFolder":
            self.folderDir = self.folderDir + self.listSyncFolder[hexDesign] + "/"
            self.cw = "mainSyncDriveWindow"

        elif type == "file":
            if self.sendStatus == True: 
                return

            for select in self.widget[0].selection():

                hexDesign = str(hex(int("0X" + select.replace('I', ''), 16)))
                try: self.listFile[hexDesign]
                except: continue

                log = {
                    "dir": self.folderDir + self.listFile[hexDesign][0]
                }

                downLoadList.append([os.getcwd() + "\\download\\" + self.listFile[hexDesign][0],log])
                
            self.sendStatus = False
    
    def deleteFolder(self):
        for select in self.widget[0].selection():
            if self.widget[0].item(select, "text")[1:][1:] != self.folderDir and self.widget[0].item(select, "text")[1:][1:] != "":
                hexDesign = str(hex(int("0X" + select.replace('I', ''), 16)))
                file = ""
                try: 
                    file = self.listFile[hexDesign][0]
                except:
                    try: 
                        file = self.listFolder[hexDesign]
                    except:
                        try: 
                            file = self.listSyncFolder[hexDesign]
                        except: return
                
                log = {
                    "action": "delete",
                    "dir": f"{self.folderDir}" + file
                }
                rqt = myRequests("http://mythdrive.ml:1080/DriveAction", "post", log)
                if(rqt.result["status"] == "successful"):
                    pass
                else:
                    self.labelInfo(rqt.result["info"], "red")
                
        self.refresh()

    def selectFile(self):
        try:
            file = tkinter.filedialog.askopenfiles(initialdir = os.path.dirname(os.path.realpath(__file__)) + "/../../../..", title='Please select a file')
        except: return

        if self.sendStatus == True:
            return
        self.sendStatus = True
        dir = self.folderDir
        for tempFile in file:
            if self.sizeDrive + os.path.getsize(tempFile.name) > 10*1024*1024*1024:
                self.labelInfo("File too big.", "red")
                return

            log = {
                "dir": f"{dir}",
                "lm": math.floor(os.stat(tempFile.name).st_mtime)
            }
            files = {
                "file": open(tempFile.name, "rb")
            }
            upLoadList.append([files,log])
        
        self.sendStatus = False

    fileMove = ["",""]
    sendStatus = False
    sizeDrive = 0
    cw = "mainDriveWindow"
    folderDir = "/"
    title = "myDrive : Drive"
    size = "800x500"
    window = {}
    widget = {}
    listFile = {}
    listFolder = {}
    listSyncFolder = {}


class waitRequestFile:
    def __init__(self, title, files, log):
        if title == "UpLoad":
            self.thread = threading.Thread(target= lambda : self.waitUpLoad(log, files))

        elif title == "DownLoad":
            self.thread = threading.Thread(target= lambda : self.waitDownLoad(log, files))

        self.thread.daemon = True
        self.thread.start()

        self.title = title

        self.window = tkinter.Toplevel()
        self.window.resizable(width=False, height=False)
        self.window.iconphoto(False, tkinter.PhotoImage(file='./app/images/ico.png'))

        size = self.size.split("x")
        self.widget[0] = tkinter.Canvas(self.window, width=size[0], height=size[1])
        self.widget[0].pack()
        self.widget[0].create_rectangle(0, 0, size[0], size[1], fill="#f0f0f0", outline="#f0f0f0", width=0)
        self.widget[0].create_rectangle(30, 100, 345, 125, fill="#ABABE7", outline="#FFFFFF", width=0)
        self.widget[0].create_rectangle(0, 100, 30, 125, fill="#f0f0f0", outline="#f0f0f0", width=0)
        self.widget[0].create_rectangle(345, 100, 415, 125, fill="#f0f0f0", outline="#f0f0f0", width=0)

        if title == "UpLoad":
            self.widget[1] = tkinter.Label(self.window, text=files["file"].name, fg='#000000', font=("Helvetica", 10))

        elif title == "DownLoad":
            self.widget[1] = tkinter.Label(self.window, text=log["dir"], fg='#000000', font=("Helvetica", 10))

        self.widget[1].place(x=30, y=72)

        self.widget[2] = tkinter.Label(self.window, text= "0/" + str(round(self.totalSize/1024/1024, 2)) + "Mo", fg='#000000', font=("Helvetica", 8))
        self.widget[2].place(x=30, y=130)

        self.window.protocol("WM_DELETE_WINDOW", self.breakWait)

        t = 0
        while self.animation == True:
            try:
                self.widget[0].create_rectangle(30, 100, t+30, 125, fill="#11E62B", outline="#FFFFFF", width=0)
                time.sleep(0.5)
                self.widget[2].destroy()
                self.widget[2] = tkinter.Label(self.window, text=str(round(self.progress/1024/1024, 2)) + "/" + str(round(self.totalSize/1024/1024, 2)) + "Mo", fg='#000000', font=("Helvetica", 8))
                self.widget[2].place(x=30, y=130)
                if round(315*self.progress/self.totalSize) <= 315:
                    t = round(315*self.progress/self.totalSize)
                else:
                    t = 315
            except: pass
        try:
            self.window.destroy()
        except: pass
    
    def clear(self):
        t = 0
        while 1:
            try: self.widget[t]
            except: break
            else:
                try: self.widget[t].destroy()
                except: del self.widget[t]
            t = t + 1

    def breakWait(self):
        self.animation = False

    def waitUpLoad(self, log, files):
        self.totalSize = os.stat(files["file"].name).st_size

        log["status"] = "start"
        log["name"] = files["file"].name.split("/")[len(files["file"].name.split("/"))-1]
        rqt = json.loads(requests.put("http://mythdrive.ml:1080/DriveUpLoad", headers=self.headers, json=log).text)
        if rqt['status'] == "error":
            self.window.destroy()
            self.winError(rqt['info'])
            self.breakWait
            return

        def status():
            while self.animation == True:
                time.sleep(0.5)
                requests.put("http://mythdrive.ml:1080/DriveUpLoad", headers=self.headers, json={'status': 'run'})

        threadstatus = threading.Thread(target=status)
        threadstatus.daemon = True
        threadstatus.start()

        log["status"] = "launch"
        while True:
            time.sleep(0.5)
            data = files["file"].read(327680)
            if not data or self.animation == False:
                break
            self.progress += 327680
            rqt = json.loads(requests.put("http://mythdrive.ml:1080/DriveUpLoad", headers=self.headers, files={'file': data}, data=log).text)
            if rqt['status'] == "error":
                self.window.destroy()
                self.winError(rqt['info'])
                self.breakWait
                return
        
        log["status"] = "stop"
        rqt = json.loads(requests.put("http://mythdrive.ml:1080/DriveUpLoad", headers=self.headers, json=log).text)
        if rqt['status'] == "error":
            self.window.destroy()
            self.winError(rqt['info'])
            self.breakWait
            return

        files["file"].close()
        self.animation = False

    def waitDownLoad(self, log, files):
        rqt = json.loads(requests.post("http://mythdrive.ml:1080/DriveDownLoad", headers=self.headers, json=log).text)
        if rqt['status'] == "successful":
            self.totalSize = rqt['file']
            r = requests.get("http://mythdrive.ml:1080/getDrive", headers=self.headers, stream=True)
            for chunk in r.iter_content(chunk_size=20480):
                if self.animation == False:
                    break
                time.sleep(0.001)
                self.app += chunk
                self.progress = sys.getsizeof(self.app)

            if self.animation == True:
                file = open(files, "wb")
                file.write(bytearray(self.app))
                file.close()
                date = int(rqt["lm"])
                os.utime(files, (date, date))
                self.animation = False

    def winError(self, error):
        wt = ["Sync Choice", "250", "170"]
        t = [
            ["label", "Error", 10, 20, 40],
            ["label", error, 8, 20, 70],
        ]
        choice = customWindow.choiceWindow(wt, t)
        
        while choice.result == "":
            time.sleep(0.1)

    app = b""
    progress = 0
    totalSize = 1
    thread = {}
    window = {}
    animation = True
    widget = {}
    title = ""
    size = "365x200"
    headers = {
        "user-agent": "clientMythDrive",
        "token": sys.argv[1]
    }

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