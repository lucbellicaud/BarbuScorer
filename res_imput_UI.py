from __future__ import annotations
from functools import partial
import tkinter as tk
from typing import Dict, List
from games import Game
from tkinter import messagebox

from utils import Declaration, Direction

class ImputResUI(tk.Frame) :
    def __init__(self, parent, players_position: Dict[Direction, str], declarer: Direction,game : Game,validate_func : function) -> None:
        tk.Frame.__init__(self, parent)
        self.game=game
        self.declarer=declarer
        self.parent=parent
        self.validate_func=validate_func

        self.west = declarer.next()
        self.west_UI = ScoreImputUI(
            self, players_position, self.west)
        self.west_UI.grid(row=1, column=0)

        self.north = declarer.next().next()
        self.north_UI = ScoreImputUI(
            self, players_position, self.north)
        self.north_UI.grid(row=0, column=1)

        self.east = declarer.next().next().next()
        self.east_UI = ScoreImputUI(
            self, players_position, self.east)
        self.east_UI.grid(row=1, column=2)

        self.south = declarer
        self.south_UI = ScoreImputUI(
            self, players_position, self.south)
        self.south_UI.grid(row=2, column=1)

        self.valider = tk.Button(self,text="Valider",command=self.validate)
        self.valider.grid(row=3,column=0,columnspan=3,sticky="nsew")

    def validate(self) :
        dic : Dict[Direction,int] = {}
        dic[self.west] = self.west_UI.get()
        dic[self.north] = self.north_UI.get()
        dic[self.east] = self.east_UI.get()
        dic[self.south] = self.south_UI.get()

        self.game.result_wo_declaration = dic
        # try :
        score = self.game.score()
        self.validate_func(score,self.game)
        self.destroy()
        self.parent.destroy()
        # except :
        #     messagebox.showerror("Erreur","Résultats non valides (fait un effort ptn)")

class ScoreImputUI(tk.Frame) :
    def __init__(self, parent, players_position: Dict[Direction, str], player: Direction) -> None:
        tk.Frame.__init__(self, parent)
        self.direction = player
        self.nom = tk.Label(self,text=players_position[player]+" : ")
        self.nom.grid(row=0,column=0)

        self.var = tk.IntVar(self,value=0)
        self.entry = tk.Entry(self,textvariable=self.var)
        self.entry.grid(row=0,column=1)

    def get(self) ->str :
        return self.var.get()