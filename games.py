from typing import Dict
from utils import Direction,Declaration,declaration_dic_transformation
from abc import abstractclassmethod,abstractmethod,ABC

class Game(ABC) :
    total : int
    abbreviation : str
    
    def __init__(self) -> None:
        self.result_wo_declaration : Dict[Direction,int]={}
        self.doubles : Dict[Direction,Dict[Direction,Declaration]]={}
        self.final_result : Dict[Direction,int]={}

    def result_imput(self,result_wo_declaration : Dict[Direction,int],doubles : Dict[Direction,Declaration]) :
        self.result_wo_declaration=result_wo_declaration
        self.doubles=doubles
    
    @abstractmethod
    def score(self) -> Dict[Direction,int] :
        return

    def calculate_declarations(self) -> Dict[Direction,int]:
        double_scores : Dict[Direction,int] = {dir:0 for dir in Direction}
        print(self.result_wo_declaration)
        for player1,values in self.doubles.items() :
            for player2,declaration in values.items() :
                double_scores[player1] += (self.result_wo_declaration[player1] - self.result_wo_declaration[player2]) * declaration.barbu_multiplactor()
                double_scores[player2] += (self.result_wo_declaration[player2] - self.result_wo_declaration[player1]) * declaration.barbu_multiplactor() 
        self.final_result = {}
        for direction in Direction :
            self.final_result[direction] = double_scores[direction] + self.result_wo_declaration[direction]

        return self.final_result

class Barbu(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=-20
        self.abbreviation="R♥"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=-20
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores 

class Queens(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=-28
        self.abbreviation="Q"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=-7
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores 

class NL2(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=-30
        self.abbreviation="NL2"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=-10
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores

class Misere(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=-26
        self.abbreviation="Mis"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=-2
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores

class NoHearts(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=-30
        self.abbreviation="♥"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=-2
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores

class Dominoes(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=65
        self.abbreviation="Dom"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            match self.result_wo_declaration[direction] :
                case 1 :
                    self.result_wo_declaration[direction]=45
                case 2 :
                    self.result_wo_declaration[direction]=20
                case 3 :
                    self.result_wo_declaration[direction]=5
                case 4 :
                    self.result_wo_declaration[direction]=-5
                case _ :
                    self.result_wo_declaration[direction]=-5
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores

class Trumps(Game) :
    def __init__(self) -> None:
        super().__init__()
        self.total=65
        self.abbreviation="Trp"

    def score(self) :
        for direction in self.result_wo_declaration.keys() :
            self.result_wo_declaration[direction]*=5
        scores = self.calculate_declarations()
        if sum(scores.values())!= self.total :
            raise Exception("Les calculs ne sont pas bons Kévin")
        return scores

if __name__ == '__main__':
    game = Queens()
    res = {Direction.SOUTH:1,Direction.WEST:1,Direction.NORTH:2,Direction.EAST:0}
    double_dic = {
        
        Direction.SOUTH : {
            Direction.NORTH : Declaration.REDOUBLE,
            Direction.EAST : Declaration.DOUBLE,
            Direction.WEST : Declaration.DOUBLE
        },
        Direction.WEST : {
            Direction.SOUTH : Declaration.PASS,
            Direction.EAST : Declaration.PASS,
            Direction.NORTH : Declaration.PASS
        },
        Direction.NORTH : {
            Direction.SOUTH : Declaration.DOUBLE,
            Direction.EAST : Declaration.DOUBLE,
            Direction.WEST : Declaration.DOUBLE
        },
        Direction.EAST : {
            Direction.SOUTH : Declaration.PASS,
            Direction.NORTH : Declaration.PASS,
            Direction.WEST : Declaration.PASS
        },
        
    }
    game.result_imput(res,declaration_dic_transformation(double_dic))
    print(game.score())