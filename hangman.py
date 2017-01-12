#!/usr/bin/env python3
# -*- coding: utf-8  -*-


import tkinter as tk
from tkinter import ttk
from tkinter import font

import random

import requests as rq
import json as jn


LARGE_FONT = ("Verdana", 15)

class Hangman(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('700x700+500+500')
        self.wm_iconbitmap(tk.PhotoImage("icon.bmp"))
        tk.Tk.wm_title(self, "HANGMAN")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #self.frames = {}

        frame = StartPage(container, self)

        self.frames = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):

        self.frames.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.TITLE_FONT = font.Font(family='Bank Gothic', size=34, weight='bold')

        self.points = 0

        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        label = tk.Label(self, text="H A N G M A N", font=self.TITLE_FONT)
        label.grid(row=0, column=0, columnspan=2, sticky='new')

        ttk.Style().configure('TButton',foreground='#22aa00', background='blue', padding=10, font=LARGE_FONT)
        button1 = ttk.Button(self, style='TButton', text="Play", command=self.startGame)
        button1.grid(row=5, column=0, columnspan=2, sticky='ew')

        button2 = ttk.Button(self, style='TButton', text="Beenden", command=quit)
        button2.grid(row=5, column=2, sticky='ew')

        self.hangman = tk.Canvas(self)
        self.hangman.grid(row=1, column=0, sticky='n')

        for enfant in parent.winfo_children(): enfant.grid_configure(padx=10, pady=10)
        self.hangman.grid_configure(pady=50)

    def startGame(self):

        self.hangman.delete('all')
        self.sortie = tk.StringVar()
        self.count = 0

        RIDDLE_FONT = font.Font(family='Times New Roman', size=20)

        les_mots = open('franzwords.txt', 'r')
        what = les_mots.readlines()
        les_mots.close()
        self.Le_mot = random.choice(what)

        combien = len(self.Le_mot) - 1
        self.motlist = list(self.Le_mot.lower()[:-1])

        vide = "-" * combien
        self.sortieList = list(vide)
        self.sortie.set(self.sortieList)
        frame_i = tk.Frame(self, width=20, height=2, borderwidth=2, bg='black')
        frame_i.grid(row=2, column=0, pady=20, sticky='n')
        indicateur = tk.Label(frame_i, width=20, wraplength=0, anchor='n', compound=tk.TOP,
                              borderwidth=1, pady=10, padx=10, justify=tk.LEFT,
                              bg='#cccccc', font=RIDDLE_FONT, textvariable=self.sortie)
        indicateur.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        frame_i.grid_propagate(0) # probably not necessary

        self.aider()

        frame_i.focus_set()

        frame_i.bind("<Key>", self.touche)


    def aider(self):
        for d in self.winfo_children():
            if d.winfo_class() == 'Message':
                d.destroy()
        parameters = {'from': "fra", 'dest': "eng", 'format': "json", 'phrase': self.Le_mot[:-1]}
        response = rq.get('https://glosbe.com/gapi/translate', params=parameters)
        data = response.json()

        try:
            data = data['tuc'][0]['meanings']
            en = [x for x in range(len(data)) if data[x]['language'] == 'en' and x <= 3]
            if en == []:
                en = [x for x in range(len(data)) if data[x]['language'] == 'fr' and x <= 1]
            translations = "\n".join([data[e]['text'] for e in en])
        except:
            try:
                data = data['tuc'][0]['phrase']
                translations = data['text']
            except (IndexError, KeyError):
                translations = "Je suis désolé, il n'y a pas d'une traduction, merde.\n"
        translationVar = tk.StringVar()
        aider = tk.Message(self, width=400, bg='white', textvariable=translationVar)
        aider.grid(row=3, column=0)

        translationVar.set(translations)



    def touche(self, avoir):
        touche = eval(repr(avoir.char))
        if touche.isalpha() and touche in self.motlist:
            while touche in self.motlist:
                index = self.motlist.index(touche)
                self.motlist[index] = '*'
                self.sortieList[index] = self.Le_mot[index]
                self.sortie.set(self.sortieList)
            if "-" not in self.sortieList:
                self.hangman.delete('all')
                self.hangman.create_text(150, 100, text="V I C T O R Y", font=self.TITLE_FONT, fill='#2255ff')
        else:
            self.drawMan()


    def drawMan(self):
        bois = '#a54433'
        pericliter = [
                      "self.hangman.create_polygon(120, 200, 180, 200, 160, 180, 140, 180, width=2, fill=bois)",
                      "self.hangman.create_line(150, 180, 150, 5, width=3, fill=bois)",
                      "self.hangman.create_line(100, 5, 150, 5, width=3, fill=bois)",
                      "self.hangman.create_line(100, 5, 100, 70, width=2, fill='#bbb')",
                      "self.hangman.create_oval(90, 70, 110, 90)",   # le tête
                      "self.hangman.create_arc(95, 88, 105, 85, start=0, extent=180, style='arc')", # le bouche
                      "self.hangman.create_line(95, 83, 99, 82)",        # les yeux
                      "self.hangman.create_line(101, 82, 105, 83)",
                      "self.hangman.create_line(100, 90, 100, 125)",     # le corps
                      "self.hangman.create_line(100, 125, 110, 145)",    # la jambe droite
                      "self.hangman.create_line(100, 125, 90, 145)",     # la jambe gauche
                      "self.hangman.create_line(100, 95, 105, 120)",     # le bras droit
                      "self.hangman.create_line(100, 95, 95, 120)",      # le bras gauche
                      ]
        eval(pericliter[self.count])
        self.count += 1
        if self.count == 13:
            self.hangman.create_text(100, 100, text="GAME OVER", font=LARGE_FONT)
            self.focus_set()
            self.sortie.set(list(self.Le_mot[:-1]))



app = Hangman()
app.lift()
app.mainloop()
