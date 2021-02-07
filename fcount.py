#Good luck understanding my variable names and inspired code
#If you find a bug feel free to tell me on discord: breadguy#5091

#Recommended to turn off battle backgrounds and always show battle hud

import numpy as nm
import pytesseract
import cv2
import tkinter as tk
from tkinter import *
from PIL import ImageGrab
import win32gui, win32api
import time
import csv
import threading
from playsound import playsound

def count_occurrences(word, sentence):
    return sentence.lower().split().count(word)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.bCapture = False
        self.showSettings = False
        self.rCoords = [319, 92, 1396, 196]
        self.pokelist = []
        self.cPokemon = ''
        self.cEncounters = 0
        self.tEncounters = 0
        self.lTime = 0
        self.pokemonSeen = ['none', 0]
        self.noPokemon = True
        self.quitting = False
        self.easter = False
        self.importPokes()
        self.master = master
        self.pack()
        self.create_widgets()

        t2 = threading.Thread(target=self.checkHotkey, name='t2')
        t2.start()

    def importPokes(self):
        with open('plist.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.pokelist.append(row)
        
        for i, x in enumerate(self.pokelist):
            self.tEncounters += int(self.pokelist[i][1])

    def create_widgets(self):
        self.count = tk.Button(self, text='Start Counting (INS)',command=self.tCapture, fg='white', background='green')
        self.count.pack(pady=3)

        self.settings = tk.Button(self, text='Settings',command=self.showingSettings)
        self.settings.pack(pady=3)

        self.eggLabel = Label(self, text='Thank you for your help Revz and Team LEM!')
        if self.easter:
            self.eggLabel.pack(side='bottom')

        self.teLabel = Label(self, text=f'Total Encounters: {self.tEncounters}')
        self.teLabel.pack(side='bottom')

        self.eLabel = Label(self, text=f'{self.cPokemon} Encounters: {self.cEncounters}')
        self.eLabel.pack(side='bottom', pady=3)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.quitProgram)
        self.quit.pack(side="bottom", pady=3)

    def deletePokes(self):
        for i, x in enumerate(self.pokelist):
            self.pokelist[i][1] = 0
            self.tEncounters += int(self.pokelist[i][1])
            print(self.pokelist[i])

    def savePokes(self):
        with open('plist.csv', 'w') as f:
            for line in self.pokelist:
                f.write(f'{line[0]},{line[1]}\n')

    def quitProgram(self):
        self.bCapture = False
        self.quitting = True
        self.savePokes()
        self.master.destroy()

    def showingSettings(self):
        def egg():
            rP = False
            eP = False
            vP = False
            zP = False

            while self.showSettings:
                if win32api.GetAsyncKeyState(0x52):
                    rP = True
                if win32api.GetAsyncKeyState(0x45):
                    eP = True
                if win32api.GetAsyncKeyState(0x56):
                    vP = True
                if win32api.GetAsyncKeyState(0x5A):
                    zP = True
                if rP and eP and vP and zP:
                    self.easter = True


        if not self.showSettings:
            self.showSettings = True
            self.count.destroy()
            self.settings.destroy()
            self.eLabel.destroy()
            self.teLabel.destroy()
            self.eggLabel.destroy()
            self.quit.destroy()
            


            self.cRegion = tk.Button(self, text='Change Region', command=self.changeRegion)
            self.cRegion.pack(side='top')

            self.delPokes = tk.Button(self, text='Clear Encounters', fg='red', command=self.deletePokes)
            self.delPokes.pack(side='bottom', pady=20)

            self.back = tk.Button(self, text="Back", fg="red", command=self.showingSettings)
            self.back.pack(side='bottom')

            self.saveButton = tk.Button(self, text='Save', command=self.savePokes)
            self.saveButton.pack(side='left', padx=7, pady=10)

            self.loadButton = tk.Button(self, text='Load', command=self.importPokes)
            self.loadButton.pack(side='left')

            t3 = threading.Thread(target=egg, name='t3')
            t3.start()

            #self.rOneLabel = Label(self, text=f'[{self.rCoords[0]}, {self.rCoords[1]}]')
            #self.rOneLabel.pack(side='right')

            #self.rTwoLabel = Label(self, text=f'[{self.rCoords[2]}, {self.rCoords[3]}]')
            #self.rTwoLabel.pack(side='right')


        elif self.showingSettings:
            self.showSettings = False
            self.cRegion.destroy()
            self.saveButton.destroy()
            self.loadButton.destroy()
            self.back.destroy()
            #self.rOneLabel.destroy()
            #self.rTwoLabel.destroy()
            self.delPokes.destroy()
            self.create_widgets()

    def changeRegion(self):
        self.bCapture = False
        state_left = win32api.GetAsyncKeyState(0x01)

        for z in range(2):
            loop = True
            time.sleep(.3)
            while loop:
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                a = win32api.GetAsyncKeyState(0x01)

                if a < 0:
                    if z == 0:
                        print(f'Coordinates Set! X:{x} Y:{y}')
                        self.rCoords[z] = x
                        self.rCoords[z+1] = y
                    elif z == 1:
                        print(f'Coordinates Set! X:{x} Y:{y}')
                        self.rCoords[z+1] = x
                        self.rCoords[z+2] = y
                    print(z)
                    loop = False
        #self.rOneLabel.configure(text=f'[{self.rCoords[0]}, {self.rCoords[1]}]')
        #self.rTwoLabel.configure(text=f'[{self.rCoords[2]}, {self.rCoords[3]}]')

    def tCapture(self):
        if self.bCapture:
            self.bCapture = False
            self.count.configure(text='Start Counting (INS)', background='green')
        elif not self.bCapture:
            self.bCapture = True
            self.count.configure(text='Stop Counting (INS)', background='#990000')
            t1 = threading.Thread(target=self.startCapturing, name='t1')
            t1.start()
            

    def startCapturing(self):
        while self.bCapture:
            self.capture()

    def checkHotkey(self):
        while not self.quitting:
            if win32api.GetAsyncKeyState(0x2D):
                self.tCapture()
                time.sleep(.3)

    def achievedShiny(self):
        playsound('shiny.wav')

    def capture(self):
        #start = time.time()
        # Path of tesseract executable
        pytesseract.pytesseract.tesseract_cmd ='Tesseract-OCR\\tesseract.exe'
        while True:
            cap = ImageGrab.grab(bbox =(self.rCoords[0], self.rCoords[1], self.rCoords[2], self.rCoords[3]))

            tesstr = pytesseract.image_to_string(cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),lang ='eng')

            #print(tesstr)

            if self.noPokemon:
                if self.pokemonSeen[0] == 'none':
                    for x in self.pokelist:
                        amt = count_occurrences(x[0].lower(), tesstr)
                        if amt > 0:
                            x[1] = int(x[1]) + amt

                            self.pokemonSeen = x
                            self.cPokemon = x[0]
                            if 'shiny' in tesstr:
                                t3 = threading.Thread(target=self.achievedShiny, name='t3')
                                t3.start()
                                self.cEncounters = 0
                            else:
                                self.cEncounters = x[1]
                            if self.bCapture:
                                self.eLabel.configure(text=f'{self.cPokemon} Encounters: {self.cEncounters}')
                                self.tEncounters += amt
                                self.teLabel.configure(text=f'Total Encounters: {self.tEncounters}')

                            if self.lTime == 0:
                                self.lTime = time.time()
                            elif (self.lTime - time.time()) >= 120:
                                self.savePokes()
                                self.importPokes()
                            self.noPokemon = False
                            break
                        else:
                            self.noPokemon = True
                else:
                    amt = count_occurrences(self.pokemonSeen[0].lower(), tesstr)
                    if amt > 0:
                        self.pokemonSeen[1] = int(self.pokemonSeen[1]) + amt

                        self.cPokemon = self.pokemonSeen[0]
                        self.cEncounters = self.pokemonSeen[1]
                        if self.bCapture:
                            self.eLabel.configure(text=f'{self.cPokemon} Encounters: {self.cEncounters}')

                        if self.lTime == 0:
                            self.lTime = time.time()
                        elif (self.lTime - time.time()) >= 120:
                            self.savePokes()
                            self.importPokes()
                        self.noPokemon = False
                    else:
                        self.noPokemon = True
                        self.pokemonSeen = ['none', 0]
            else:
                amt = count_occurrences(self.pokemonSeen[0].lower(), tesstr)
                if amt == 0:
                    cap = ImageGrab.grab(bbox =(279, 136, 612, 204))

                    tesstr = pytesseract.image_to_string(cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),lang ='eng')
                    amt = count_occurrences(self.pokemonSeen[0].lower(), tesstr)
                    if amt == 0:
                        self.noPokemon = True
                        self.pokemonSeen = ['none', 0]

        
            if not self.bCapture:
                break
            
            #print(f'Captured in {(time.time() - start)} seconds.')
            #start = time.time()

root = tk.Tk()
root.title('County')
photo = PhotoImage(file = 'wutcat.png')
root.iconphoto(False, photo)
root.attributes('-topmost', 'true')
root.geometry('234x160')
root.geometry('+806+367')
root.resizable(False, False)
app = Application(master=root)
print('Happy Hunting!')
app.mainloop()
