#coding:utf-8

import tkinter
import json
import myTool
import time
import threading

class choiceWindow:
    def __init__(self, windowTable, table):

        def test():
            self.title = windowTable[0]
            self.size = windowTable[1] + "x" + windowTable[2]
            self.window = tkinter.Tk()
            self.window.resizable(width=False, height=False)

            for widget in table:
                if widget[0] == "label":
                    self.widget.append( tkinter.Label(self.window, text=widget[1], font=("Helvetica", widget[2])) )
                    self.widget[len(self.widget)-1].place(x=widget[3], y=widget[4])
                
                elif widget[0] == "button":
                    self.widget.append( 
                        tkinter.Button(self.window, text=widget[1], command= lambda temp = widget[2]: [
                            self.setResult(temp)
                        ])
                    )
                    self.widget[len(self.widget)-1].place(x=widget[3], y=widget[4])

            self.window.protocol("WM_DELETE_WINDOW", lambda : self.setResult("close"))
            self.window.title(self.title)
            self.window.geometry(self.size)

            self.window.mainloop()

        testThead = threading.Thread(target=test)
        testThead.daemon = True
        testThead.start()

    def setResult(self, ncw):
        self.result = ncw
        self.window.destroy()

    result = ""
    thread = {}
    window = {}
    animation = True
    widget = []
    title = ""
    size = ""