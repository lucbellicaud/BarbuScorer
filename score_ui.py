from __future__ import annotations
import tkinter as tk
from typing import Dict

from games import NL2, Barbu, Dominoes, Game, Misere, NoHearts, Queens, Trumps
from bid_imput_UI import ImputBidUI

from utils import Direction
from functools import partial


class ScoreSheet(tk.Frame):
    def __init__(self, parent, names) -> None:
        tk.Frame.__init__(self, parent)
        self.players_position = {
            dir: name for dir, name in zip(Direction, names)}
        self.players: Dict[Direction, Player] = {dir: Player(
            self, dir, self.players_position) for dir in Direction}

        for i, val in enumerate(self.players.values()):
            val.grid(row=i%2, column=i//2)
            val.propagate(0)

        self.total = ScoreSheetTotal(self,self.players_position)
        self.total.grid(row=2,column=0,columnspan=1)

    def calculate_total(self) :
        dic_total : Dict[Direction,int] = {dir:0 for dir in Direction}
        for dir,player in self.players.items() :
            temp = player.sum_scores()
            dic_total = {k: temp.get(k, 0) + dic_total.get(k, 0) for k in set(temp)}
        self.total.total.set_scores(dic_total)


        

class ScoreSheetTotal(tk.Frame) :
    def __init__(self, parent, players_position) -> None:
        tk.Frame.__init__(self, parent,width=1000)
        self.players_position = players_position
        self.total_label = tk.Label(self, text='{:^20s}'.format("Total"))
        self.total_label.grid(row=0,column=0,rowspan=2)
        for i, name in enumerate(self.players_position):
            self.name = tk.Label(
                self, text='{:^20s}'.format(self.players_position[name]))
            self.name.grid(row=0, column=i+1,sticky="nsew")
        self.total = ScoreLine(self)
        self.total.grid(row=1, column=1,columnspan=4,sticky="nsew")



class Player(tk.Frame):
    def __init__(self, parent, dir: Direction, players_position) -> None:
        tk.Frame.__init__(
            self, parent, highlightbackground="black", highlightthickness=1)
        self.players_position = players_position
        self.dir = dir
        self.parent=parent

        self.name = tk.Label(self, text='{:^20}'.format(
            players_position[dir]), font=("Segoe UI", 20))
        self.name.grid(row=0, column=0, columnspan=5,sticky="nsew")

        for i, name in enumerate(players_position):
            self.name = tk.Label(
                self, text='{:^20s}'.format(players_position[name]))
            self.name.grid(row=1, column=i+1,sticky="nsew")

        self.games: Dict[Game, ScoreLine] = {}
        self.games[Barbu()] = ScoreLine(self)
        self.games[NL2()] = ScoreLine(self)
        self.games[Misere()] = ScoreLine(self)
        self.games[NoHearts()] = ScoreLine(self)
        self.games[Queens()] = ScoreLine(self)
        self.games[Trumps()] = ScoreLine(self)
        self.games[Dominoes()] = ScoreLine(self)

        for i, (game, scoreline) in enumerate(self.games.items()):
            label = tk.Button(self, text='{:^20s}'.format(
                game.abbreviation), command=partial(self.enter_score, game))
            label.grid(row=i+2, column=0,sticky="nsew")
            scoreline.grid(row=i+2, column=1, columnspan=4,sticky="nsew")

        self.total_label = tk.Label(self, text='{:^20s}'.format("Total"))
        self.total_label.grid(row=9,column=0)
        self.total = ScoreLine(self)
        self.total.grid(row=9, column=1,columnspan=4,sticky="nsew")

    def sum_scores(self) -> Dict[Direction,int] :
        dic = {dir:0 for dir in Direction}
        for line in self.games.values() :
            for dir,score_cell in line.cells.items() :
                dic[dir]+=score_cell.get()
        self.total.set_scores(dic)
        return dic


    def enter_score(self, game: Game):
        pass
        score_imput_window = tk.Toplevel(self)
        score_imput: ImputBidUI = ImputBidUI(
            score_imput_window, players_position=self.players_position, declarer=self.dir,game=game,validate_func=self.set_score)
        score_imput.pack()

    def set_score(self, scores : Dict[Direction,int], game : Game) :
        self.games[game].set_scores(scores)
        self.sum_scores()
        self.parent.calculate_total()
    
    def calculate_sum(self) :
        pass


class ScoreLine(tk.Frame):
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.cells: Dict[Direction, ScoreCell] = {}

        for i, dir in enumerate(Direction):
            self.cells[dir] = ScoreCell(self)
            self.cells[dir].grid(row=0, column=i,sticky="nsew")
    
    def set_scores(self, scores : Dict[Direction,int]) :
        for dir,val in scores.items() :
            self.cells[dir].val.set('{:^25d}'.format(val))

class ScoreCell(tk.Frame):
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.val = tk.IntVar(self, value='')
        self.label = tk.Label(self, textvariable=self.val)
        self.label.grid(row=0, column=0,sticky="nsew")

    def get(self) :
        try :
            return self.val.get()
        except :
            return 0


root = tk.Tk()
root.title(string="BarbuScorer")
UI = ScoreSheet(root, ["Luc", "Pierre", "Raphi", "Margaux"])
UI.grid(row=0, column=0)
UI.propagate(0)
root.mainloop()
