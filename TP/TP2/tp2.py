"""Code de l'exercice 3 du TP2 de IA02"""

from typing import List
import subprocess
import math


def at_least_one(s):
    """au moins une couleur pour chaque sommet"""
    l: List = []
    for i in range(3):
        l.append((s - 1) * 3 + i + 1)
    return l


def at_most_one(s):
    """au maximum une couleur pour chaque sommet"""
    l: List = []
    l.append([-((s - 1) * 3 + 1), -((s - 1) * 3 + 1 + 1)])
    l.append([-((s - 1) * 3 + 1), -((s - 1) * 3 + 1 + 2)])
    l.append([-((s - 1) * 3 + 1 + 1), -((s - 1) * 3 + 1 + 2)])
    return l


def contraintes(t):
    "définit les contraintes entre les sommets"
    l: List = []
    for _, i in enumerate(t):
        # print(-((t[i][0]-1)*3+1))
        l.append([-((i[0] - 1) * 3 + 1), -((i[1] - 1) * 3 + 1)])
        l.append([-((i[0] - 1) * 3 + 2), -((i[1] - 1) * 3 + 2)])
        l.append([-((i[0] - 1) * 3 + 3), -((i[1] - 1) * 3 + 3)])
    # print(len(l))
    return l


def graph(c, n, s, a):
    """définit fichier cnf"""
    cnf: str = ""
    cnf += "c tp2.cnf\nc\n"
    l: List = []
    for i, _ in enumerate(s):
        l.append(at_least_one(i + 1))
        tmp: List = at_most_one(i + 1)
        for i in tmp:
            l.append(i)
    tmp2: List = contraintes(a)
    for _, tmp2_i in enumerate(tmp2):
        l.append(tmp2_i)
    # print(len(l))
    # print(l)

    cnf += f"p cnf {c*n} {len(l)}\n"
    for _, i in enumerate(l):
        for _, j in enumerate(i):
            cnf += f"{j} "
        cnf += "0\n"
    cnf += "\n"

    with open("/home/jpontoire/Documents/UTC/GI02/IA02/TP/TP2/tp2.cnf", "w", encoding="utf8") as file:
        file.write(cnf)

    print(cnf)


def affichage(path: str) -> None:
    """Affichage du résultat"""
    colors: dict = {0: "bleu", 1: "vert", 2: "rouge"}
    process = subprocess.run(
        f"/home/jpontoire/go/bin/gophersat {path}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    returned_values: str = process.stdout
    temp: list = returned_values.split("\n")
    results = temp[2].replace("v", "").split(" ")
    results.remove("")
    results.pop(len(results) - 1)
    # print(results)
    sommets_colors = {}
    for item in results:
        number = int(item)
        if number > 0:
            sommet: int = math.ceil(number / 3)
            color: str = colors[int(number % 3)]
            sommets_colors[sommet] = color
    # print(sommets_colors)
    for cle, valeur in sommets_colors.items():
        print(f"Sommet {cle} : {valeur}")


def main() -> None:
    """fontion main"""
    c: int = 3
    n: int = 10
    sommets: List = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    arretes: List = [
        (1, 2),
        (1, 5),
        (1, 6),
        (2, 3),
        (3, 4),
        (4, 5),
        (2, 7),
        (3, 8),
        (4, 9),
        (5, 10),
        (6, 8),
        (7, 10),
        (6, 9),
        (7, 9),
        (8, 10),
    ]
    graph(c, n, sommets, arretes)
    affichage("/home/jpontoire/Documents/UTC/GI02/IA02/TP/TP2/tp2.cnf")


if __name__ == "__main__":
    main()
