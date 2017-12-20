# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 22:55:49 2017

@author: Swifty
"""

import tkinter as tk
import numpy as np
import random

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.counter = 0
        self.stoppingFlag = True
        self.flag = True
        self.buttonIsPressed = False
        self.colours = ["#82CAFF","#3BB9FF", "#38ACEC", "#56A5EC", "#1589FF", "#306EFF",
                        "#157DEC", "#2B65EC", "#0041C2", "#0020C2", "#0000A0", "#000080", 
                        "#151B54", 'black']
        self.canvas = tk.Canvas(self, width=500, height=550, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        
        self.rows = 50
        self.columns = 50
        self.cellwidth = 10
        self.cellheight = 10
        self.x = 0
        self.y = 0
        self.rect = {}
        
        #creating the grid
        for column in range(50):
            for row in range(50):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="dead")
    
    #next generation play button            
    def play(self):
        self.flag = True
        self.buttonIsPressed = True
        self.stoppingFlag = True
        self.canvas.itemconfig("dead",fill = "white")
        self.redrawAfterPlay(50)
    
    #algorithm
    def next_generation(self, a):
        a_new = np.lib.pad(a, ((1, 1), (1, 1)), 'wrap')
        for i in range(1, a.shape[0]+1):
            for j in range(1, a.shape[1]+1):
                population = np.sum(a_new[i-1:i+2, j-1:j+2])
                if (population == 3):
                   a[i-1, j-1] = 1
                elif(population == 4):
                    if(a_new[i, j] == 1):
                        a[i-1, j-1] = 1
                else:
                    a[i-1, j-1] = 0
        return a
    
    #The stop button function. Stops the redraw pattern
    def stop(self):
        self.buttonIsPressed = False
        self.stoppingFlag = False
        self.flag = True
        
    #clears the grid 
    def clear(self):
        self.stoppingFlag = True
        for cell in self.rect.keys():
            self.canvas.itemconfig(self.rect[cell[1], cell[0]], tag="dead")
        self.canvas.itemconfig("dead",fill = "white")   

    #coordinates of the mouse
    def motion(self, event):
        if(event.y  < 500 and self.flag):
            self.x, self.y = event.x, event.y
            self.x = int(self.x/10)
            self.y = int(self.y/10)  
            self.redraw(0)
        
      
    #as each widget has its own coordinates, we need to check
    #when we're in the widget so that the coordinates of the 
    #mouse are correct, otherwise - many, many bugs
    def enterWidget(self, event):
        self.flag = False
        self.y = 500

    #same as the enterWidget
    def leftWidget(self, event):
        self.flag = True
        
    #when clicking on the grid
    def redraw(self, delay):
        if(self.buttonIsPressed == False): #ensures that we're not clicking on the grid
            item_id = self.rect[self.y,self.x]  #when a pattern is already running
            if (self.canvas.gettags(item_id)[0] == "dead"):
                self.canvas.itemconfig(item_id, tag="alive") 
            else:
                self.canvas.itemconfig(item_id, tag="dead")
            self.canvas.itemconfig("dead", fill="white")
            self.canvas.itemconfig("alive", fill="black")
        #self.after(delay, lambda: self.redraw(delay))
      
    #sequence of next generations
    def redrawAfterPlay(self,delay):
        if (self.stoppingFlag):
            #self.counter += 1
            a = np.zeros((50, 50))
            for cell in self.rect.keys():
                if (self.canvas.gettags(self.rect[cell[1], cell[0]])[0] == "alive"):
                    a[cell[1], cell[0]] = 1
                    
            a = self.next_generation(a)
        
            for i in range(a.shape[0]):
                for j in range(a.shape[1]):
                    if(a[i, j] == 1.0):
                        self.canvas.itemconfig(self.rect[i, j], tag="alive")
                    else:
                        self.canvas.itemconfig(self.rect[i, j], tag="dead")
            #self.canvas.itemconfig("alive", fill=random.choice(self.colours))
            #self.canvas.itemconfig("alive", fill=self.colours[self.counter%14])
            self.canvas.itemconfig("alive", fill = "black")
            self.canvas.itemconfig("dead", fill = "white")
            self.after(delay, lambda: self.redrawAfterPlay(delay))
            
        
    def createWidgets(self):
        self.START = tk.Button(self)
        self.START["text"] = "Next Generation"
        self.START["fg"] = 'black'
        self.START["command"] = self.play
        self.START["width"] = 14
        self.START.bind('<Enter>', self.enterWidget)
        self.START.bind('<Leave>', self.leftWidget)     
        
        self.START.pack({"side":"left"})
        
        self.STOP = tk.Button(self)
        self.STOP["text"] = "Stop"
        self.STOP["fg"] = 'black'
        self.STOP["width"] = 10
        self.STOP.bind('<Enter>', self.enterWidget)
        self.STOP.bind('<Leave>', self.leftWidget) 
        self.STOP["command"] = self.stop
        
        self.STOP.pack({"side":"right"})
        
        self.CLEAR= tk.Button(self)
        self.CLEAR["text"] = "New Canvas"
        self.CLEAR["fg"] = 'black'
        self.CLEAR["command"] = self.clear
        self.CLEAR["width"] = 14
        self.CLEAR.bind('<Enter>', self.enterWidget)
        self.CLEAR.bind('<Leave>', self.leftWidget)     
        
        self.CLEAR.pack({"side":"bottom"})
        
        
        self.pattern1 = tk.Button(self)
        self.pattern1["text"] = "Butterfly"
        self.pattern1["fg"] = 'black'
        self.pattern1["width"] = 10
        self.pattern1.bind('<Enter>', self.enterWidget)
        self.pattern1.bind('<Leave>', self.leftWidget) 
        self.pattern1["command"] = self.butterfly
        
        self.pattern1.pack({"side":"bottom"})
        
        
        self.pattern2 = tk.Button(self)
        self.pattern2["text"] = "Spaceship"
        self.pattern2["fg"] = 'black'
        self.pattern2["width"] = 10
        self.pattern2.bind('<Enter>', self.enterWidget)
        self.pattern2.bind('<Leave>', self.leftWidget) 
        self.pattern2["command"] = self.spaseship
        
        self.pattern2.pack({"side":"bottom"})
            
            
    def spaseship(self):
        a = np.zeros((50, 50))
        a[14, 16] = 1
        a[15:17, 14] = 1
        a[17, 15:17] = 1
        a[15:17, 17] = 1
        
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if(a[i, j] == 1.0):
                    self.canvas.itemconfig(self.rect[i, j], tag="alive")
                else:
                    self.canvas.itemconfig(self.rect[i, j], tag="dead")
        self.redrawAfterPlay(50)


    def butterfly(self):
        a = np.zeros((50, 50))
        
        a[10, 10:12]=1
        a[12:15, 12] = 1
        a[10:12, 13]= 1
        a[16, 11] = 1
        a[16, 9] = 1
        
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if(a[i, j] == 1.0):
                    self.canvas.itemconfig(self.rect[i, j], tag="alive")
                else:
                    self.canvas.itemconfig(self.rect[i, j], tag="dead")
        self.redrawAfterPlay(50)        
            
        
        
        


if __name__ == "__main__":
    app = App()
    app.bind('<Button-1>', app.motion)
    app.createWidgets()
    app.mainloop()

    
    