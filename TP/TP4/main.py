from typing import List, Callable
import ast
import random

Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[State, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2
PLAYER1 = 1
PLAYER2 = 2

EMPTY_GRID: Grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
GRID_0: Grid = EMPTY_GRID
GRID_1: Grid = ((0, 0, 0), (0, X, O), (0, 0, 0))
# (0, 0, 0),
# (0, X, O),
# (0, 0, 0))

GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
#((O, 0, X),
# (X, X, O),
# (O, X, 0)

GRID_3: Grid = ((O, 0, X), (0, X, O), (O, X, 0))
#((O, 0, X),
# (0, X, O),
# (O, X, 0))

GRID_4: Grid = ((0, 0, 0), (X, X, O), (0, 0, 0))
#((0, 0, 0),
# (X, X, O),
# (0, 0, 0))

GRID_FULL : Grid = ((O, O, X), (X, X, O), (O, X, X))
#((O, O, X),
# (X, X, O),
# (O, X, X))

GRID_PLAYER1 : Grid = ((O, 0, X), (X, X, X), (O, X, 0))

GRID_PLAYER2 : Grid = ((O, 0, X), (X, O, O), (O, X, O))



def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    liste : List = []
    for i in grid:
        tmp : List = []
        for j in i:
            tmp.append(j)
        liste.append(tmp)
    return liste

#print(grid_tuple_to_grid_list(((O, 0, X), (0, X, O), (O, X, 0))))

def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    t: tuple
    l : List = []
    for i in grid:
        l.append((i[0], i[1], i[2]))
    t = (l[0], l[1], l[2])
    return t

#print(grid_list_to_grid_tuple([[2, 0, 1], [0, 1, 2], [2, 1, 0]]))


def legals(grid: State) -> list[Action]:
    actions : List = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                actions.append((i,j))
    return actions

#print(legals(((O, X, X), (O, X, O), (O, X, X))))

def line(grid: State, player: Player) -> bool:
    val_ligne : bool
    for i in range(len(grid)):
        val_ligne = True
        for j in range(len(grid[i])):
            if grid[i][j] == player and val_ligne == True:
                val_ligne = True
            else:
                val_ligne = False
        if val_ligne == True:
            return val_ligne
    return val_ligne

#print(line(((1, 1, 0), (1, 1, 0), (0, 0, 0)), 1))

def column(grid: State, player: Player) -> bool:
    val_col : bool
    for i in range(len(grid)):
        val_col = True
        for j in range(len(grid[i])):
            if grid[j][i] == player and val_col == True:
                val_col = True
            else:
                val_col = False
        if val_col == True:
            return val_col
    return val_col

#print(column(((1, 1, 0), (1, 1, 0), (1, 0, 0)), 1))

def diag(grid: State, player: Player) -> bool:
    val_diag : bool = True
    for i in range(len(grid)):
        if grid[i][i] == player and val_diag == True:
            val_diag = True
        else:
            val_diag = False
    if not(val_diag):
        val_diag = True
        for i in range(len(grid)):
            #print([i, len(grid[i]) - 1 - i])
            if grid[i][len(grid[i]) - 1 - i] == player and val_diag == True:
                val_diag = True
            else:
                val_diag = False
    return val_diag

#print(diag(((1, 1, 0), (1, 1, 0), (1, 0, 1)), 1))

def verify(grid: State, player: Player) -> bool:
    if line(grid, player) or column(grid, player) or diag(grid, player):
        return True
    return False

#print(verify(((1, 1, 1), (1, 0, 0), (0, 0, 1)), PLAYER1))

def final(grid: State) -> bool:
    if verify(grid, PLAYER1) or verify(grid, PLAYER2) or not(legals(grid)):
        return True
    return False

#print(final(GRID_2))

def score(grid: State) -> int:
    if final(grid):
        if verify(grid, PLAYER1):
            return 1
        elif verify(grid, PLAYER2):
            return -1
        return 0
    
#print(score(GRID_PLAYER2))

def pprint(grid: State):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                print("X ", end="")
            elif grid[i][j] == 2:
                print("O ", end="")
            else:
                print("0 ", end="")
        print("")

#pprint(GRID_PLAYER1)

def play(grid: State, player: Player, action: Action) -> State:
    my_grid : list[list[int]] = grid_tuple_to_grid_list(grid)
    my_grid[action[0]][action[1]] = player
    return(grid_list_to_grid_tuple(my_grid))

#play(GRID_1, PLAYER1, (0,1))

#def strategy(grid: State, player: Player) -> Action:


def strategy(grid: State, player: Player) -> Action:
    test : bool = False
    print(f"à vous de jouer, joueur {player}")
    while not(test):
        pprint(grid)
        print("Ligne : ", end="")
        l = int(input())
        print("Colonne :", end="")
        c = int(input())
        if (l,c) in legals(grid):
            return (l,c)
        print("Ce coup n'est pas possible")

#print(strategy(GRID_1, PLAYER1))



def strategy_first_legal(grid: State, player: Player) -> Action:
    coups : list[Action] = legals(grid)
    choix : Action = coups[0]
    print(f"Choix du joueur {player} : {choix}")
    return choix


def strategy_random(grid: State, player: Player) -> Action:
    coups : list[Action] = legals(grid)
    n = random.randint(0, len(coups) - 1)
    choix : Action = coups[n]
    print(f"Choix du joueur {player} : {choix}")
    return choix



def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    if not debug:
        grid : Grid = EMPTY_GRID
        player : int = PLAYER1
        while not(final(grid)):
            print("---------------------------")
            if player == PLAYER1:
                grid = play(grid, player, strategy_X(grid, player))
                player = PLAYER2
            else :
                grid = play(grid, player, strategy_O(grid, player))
                player = PLAYER1
        result : int = score(grid)
        print("---------------------------")
        if result == 0:
            print("Match nul")
        else :
            print(f"Le vainqueur est le joueur {result}")
        pprint(grid)
        return result
    return result

#tictactoe(strategy_random, strategy_random)


def minmax(grid: State, player: Player) -> float:
    best : float
    coups : list[Action]
    if final(grid):
        return score(grid)
    if player == PLAYER1:
        best = float("-inf")
        coups = legals(grid)
        for coup in coups:
            tmp : State = play(grid, player, coup)
            val = minmax(tmp, PLAYER2)
            if max(best, val) == val:
                best = val
        return best
    
    if player == PLAYER2:
        best = float("inf")
        coups = legals(grid)
        for coup in coups:
            tmp : State = play(grid, player, coup)
            val = minmax(tmp, PLAYER1)
            if min(best, val) == val:
                best = val
        return best


#print(minmax(GRID_1, PLAYER1))


def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[float, Action]:
    best : tuple[float, Action]
    coups : list[Action]
    if final(grid):
        return (score(grid), (-1, -1))
    
    if player == PLAYER1:
        best = (float("-inf"), (-1, -1))
        coups = legals(grid)
        for coup in coups:
            tmp : State = play(grid, player, coup)
            val = minmax_action(tmp, PLAYER2, depth - 1)
            if max(best[0], val[0]) == val[0]:
                best = (val[0], coup)
        return best
    
    if player == PLAYER2:
        best = (float("inf"), (-1, -1))
        coups = legals(grid)
        for coup in coups:
            tmp : State = play(grid, player, coup)
            val = minmax_action(tmp, PLAYER1, depth - 1)
            if min(best[0], val[0]) == val[0]:
                best = (val[0], coup)
        return best

# problème : vu que dans tous les cas il va perdre il prend pas le coup qui fait durer la partie le plus longtemps, seulement le premier


GRID_TEST: Grid = ((0, 0, 0), (0, X, O), (0, 0, X))
# (0, 0, 0),
# (0, X, O),
# (0, 0, X))    

print(minmax_action(GRID_TEST, PLAYER2))