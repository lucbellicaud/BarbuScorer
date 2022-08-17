from __future__ import annotations
from functools import partial
import tkinter as tk
from typing import Dict, List
from games import Game
from res_imput_UI import ImputResUI

from utils import Declaration, Direction, declaration_dic_transformation


class ImputBidUI(tk.Frame):
    def __init__(self, parent, players_position: Dict[Direction, str], declarer: Direction,game : Game,validate_func : function) -> None:
        tk.Frame.__init__(self, parent)
        self.game=game
        self.players_position=players_position
        self.declarer=declarer
        self.parent=parent
        self.validate_func=validate_func

        self.forbidden_bids = {dir: {dir2 : [Declaration.REDOUBLE] for dir2 in Direction}
                               for dir in Direction}

        self.west = declarer.next()
        self.west_UI = PlayerAuction(
            self, players_position, self.west, self.forbidden_bids[self.west])
        self.west_UI.grid(row=1, column=0)

        self.north = declarer.next().next()
        self.north_UI = PlayerAuction(
            self, players_position, self.north, self.forbidden_bids[self.north])
        self.north_UI.grid(row=0, column=1)

        self.east = declarer.next().next().next()
        self.east_UI = PlayerAuction(
            self, players_position, self.east, self.forbidden_bids[self.east])
        self.east_UI.grid(row=1, column=2)

        self.south = declarer
        for dir in Direction :
            self.forbidden_bids[self.south][dir].append(Declaration.DOUBLE)
        self.south_UI = PlayerAuction(
            self, players_position, self.south, self.forbidden_bids[self.south])
        self.south_UI.grid(row=2, column=1)

        self.valider = tk.Button(self,text="Entrer les résultats",command=self.enter_results)
        self.valider.grid(row=3,column=0,columnspan=3,sticky="nsew")

    def update_forbiden_bids(self,dir1,dir2 : Direction, new_bid=Declaration) :
        if new_bid==Declaration.PASS :
            self.forbidden_bids[dir2][dir1]=[Declaration.REDOUBLE]
        if new_bid==Declaration.DOUBLE :
            self.forbidden_bids[dir2][dir1]=[Declaration.DOUBLE]
        if new_bid==Declaration.REDOUBLE :
            self.forbidden_bids[dir2][dir1]=[Declaration.PASS,Declaration.REDOUBLE]
        
        self.west_UI.forbidden_bids = self.forbidden_bids[self.west]
        self.north_UI.forbidden_bids = self.forbidden_bids[self.north]
        self.east_UI.forbidden_bids = self.forbidden_bids[self.east]
        self.south_UI.forbidden_bids = self.forbidden_bids[self.south]

        self.west_UI.check_validity()
        self.north_UI.check_validity()
        self.east_UI.check_validity()
        self.south_UI.check_validity()

    def enter_results(self) :
        dic : Dict[Direction,Dict[Direction,Declaration]] = {}
        dic[self.west] = self.west_UI.get_all_bids()
        dic[self.north] = self.north_UI.get_all_bids()
        dic[self.east] = self.east_UI.get_all_bids()
        dic[self.south] = self.south_UI.get_all_bids()

        score_imput_window = tk.Toplevel(self)
        self.game.doubles = declaration_dic_transformation(dic)
        score_imput: ImputResUI = ImputResUI(
            score_imput_window, players_position=self.players_position, declarer=self.declarer,game=self.game,validate_func=self.validate_func)
        score_imput.pack()


class PlayerAuction(tk.Frame):
    def __init__(self, parent, players_position: Dict[Direction, str], player: Direction, forbidden_bids: Dict[Direction, List[Declaration]]) -> None:
        tk.Frame.__init__(self, parent,highlightbackground="black",highlightthickness=1)
        self.forbidden_bids = forbidden_bids
        self.parent = parent
        self.player=player
        name = tk.Label(self, text='{:^20}'.format(players_position[player]),font=("Segoe UI", 20))
        name.grid(row=0, column=0,columnspan=4)
        current_player = player.next()
        i = 0
        self.bids: Dict[Direction, tk.StringVar] = {}
        while current_player != player:
            self.bids[current_player] = tk.StringVar(self,value= '{:^20}'.format(Declaration.PASS.print_as_txt()))
            label = tk.Label(self, text = '{:^20}'.format(players_position[current_player]))
            label.grid(row=1, column=i)


            button = tk.Button(self, textvariable=self.bids[current_player], command=partial(
                self.change_bid, self.bids[current_player], current_player))
            button.grid(row=2, column=i)

            current_player = current_player.next()
            i+=1

    def change_bid(self, txtvar: tk.StringVar, current_player : Direction):
        new_dec = Declaration.from_str(txtvar.get().strip()).next()
        while new_dec in self.forbidden_bids[current_player]:
            new_dec = new_dec.next()

        txtvar.set('{:^20}'.format(new_dec.print_as_txt()))
        self.parent.update_forbiden_bids(self.player,current_player,new_dec)

    def check_validity(self) :
        for dir in Direction :
            if dir==self.player :
                continue
            if Declaration.from_str(self.bids[dir].get().strip()) in self.forbidden_bids[dir] :
                self.change_bid(self.bids[dir],dir)

    def get_all_bids(self) :
        dic : Dict[Direction,Declaration] = {}
        for dir in Direction :
            if dir==self.player :
                continue
            dic[dir] = Declaration.from_str(self.bids[dir].get().strip())
        return dic


class DoubleImput():
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
