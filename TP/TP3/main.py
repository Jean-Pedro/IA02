"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.0
"""

from typing import List, Tuple
import subprocess
from itertools import combinations

# alias de types
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]


example_mort: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [1, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]

empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#### fonctions fournies


def write_dimacs_file(dimacs: str, filename: str):
    "écrit le fichier .cnf"
    with open(filename, "w", newline="", encoding="utf8") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    "exécute gophersat sur le fichier saisi en paramètre"
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    """passage d'une case à une valeur"""
    ligne: int = i * 81
    colonne: int = j * 9
    return ligne + colonne + val + 1


# print(cell_to_variable(0, 1, 0))


def variable_to_cell(var: PropositionnalVariable) -> Tuple[int, int, int]:
    "passage d'une valeur à une case"
    tmp: int = var - 1
    val: int = tmp % 9
    j: int = (tmp // 9) % 9
    i: int = tmp // 81
    return (i, j, val)


# print(variable_to_cell(729))


def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    "transforme un modèle en un grid"
    g: Grid = [[] for _ in range(nb_vals)]
    for i in model:
        if i > 0:
            tmp: Tuple[int, int, int] = variable_to_cell(i)
            g[tmp[0]].append(tmp[2] + 1)
            # print(tmp[2])
    return g


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    "génère les clauses at least one"
    l: list = []
    for i in variables:
        l.append(i)
    return l


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    "génère les clauses unique"
    l: list = []
    l.append(at_least_one(variables))
    tmp: List[PropositionnalVariable] = []
    for i in variables:
        tmp.append(-i)
    a = combinations(tmp, 2)
    for i in a:
        tmp2: list = []
        for j in i:
            tmp2.append(j)
        l.append(tmp2)
    return l


def create_cell_constraints() -> ClauseBase:
    "crée les clauses d'une cellule"
    clauses: ClauseBase = []
    for i in range(0, 729, 9):  # un pas de 9 pour avoir bien 9 varaibles par cellule
        clauses += unique([1+i, 2+i, 3+i, 4+i, 5+i, 6+i, 7+i, 8+i, 9+i])
    return clauses


def create_line_constraints() -> ClauseBase:
    "crée les clauses d'une ligne"
    clauses: ClauseBase = []
    liste: List = []
    for i in range(9):
        for j in range(9):
            liste = []
            for a in range(9):  # 9 valeurs par cellule
                liste.append(cell_to_variable(i, a, j))
            clauses.append(at_least_one(liste))
    return clauses


def create_column_constraints() -> ClauseBase:
    "crée les clauses d'une colonne"
    clauses: ClauseBase = []
    liste: List = []
    for i in range(9):
        for j in range(9):
            liste = []
            for k in range(9):  # 9 valeurs par cellule
                liste.append(cell_to_variable(k, i, j))
            clauses.append(at_least_one(liste))
    return clauses


# il y a moyen d'optimiser la complexité en faisant les lignes et les colonnes en même temps


def create_box_constraints() -> ClauseBase:
    "crée les clauses d'une box"
    clauses: ClauseBase = []
    liste: List = []
    for i in range(3):
        for j in range(3):
            for k in range(9):
                liste = []
                for l in range(3):
                    for m in range(3):
                        liste.append((3*j + m)*9 + (3*i + l)*81 + k + 1)
                        # *9 correspond aux lignes (+ 9 par variable), *81 les colonnes, k nb de box
                clauses.append(at_least_one(liste))
    return clauses


def create_value_constraints(grid: Grid) -> ClauseBase:
    "crée les clauses des valeurs présentes de base dans le sudoku"
    clauses: ClauseBase = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                clauses.append([cell_to_variable(i, j, grid[i][j] - 1)])
    return clauses


def generate_problem(grid: Grid) -> ClauseBase:
    "génère le problème à partir de toutes les clauses constituant la grille"
    clauses: ClauseBase = []
    clauses += create_cell_constraints()
    clauses += create_line_constraints()
    clauses += create_column_constraints()
    clauses += create_box_constraints()
    clauses += create_value_constraints(grid)
    return clauses


def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    "transforme la base de clauses en format dimacs"
    txt: str = "c DESCRIPTION: solveur SAT Sudoku \n"
    txt += f"p cnf {nb_vars} {len(clauses)} \n"
    for i in clauses:
        for x in i:
            txt += f"{x} "
        txt += "0\n"
    return txt


def afficher_sudoku(grille: Grid):
    "affiche la grille de sudoku"
    print("-------------------------")
    for i, ligne in enumerate(grille):
        if (i % 3 == 0) and (i != 0):
            print("-------------------------")
        print("|", end=" ")
        for j, val in enumerate(ligne):
            if (j % 3 == 0) and (j != 0):
                print("|", end=" ")
            print(val, end=" ")
        print("|")
    print("-------------------------")


#### fonction principale


def main():
    "fonction principale"
    # print(model_to_grid(model))
    # print(unique([1, 3, 5]))
    # print(create_cell_constraints())
    problem: ClauseBase = generate_problem(example)
    write_dimacs_file(clauses_to_dimacs(problem, 729), "sudoku.cnf")
    booleen: bool
    clauses: Model
    booleen, clauses = exec_gophersat("sudoku.cnf")
    grid_sol: Grid = model_to_grid(clauses)
    print(booleen)
    if booleen:
        afficher_sudoku(grid_sol)


if __name__ == "__main__":
    main()
