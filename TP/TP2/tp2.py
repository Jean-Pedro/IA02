"""Code de l'exercice 3 du TP2 de IA02"""
from typing import List


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
    for i in range(len(t)):
        # print(-((t[i][0]-1)*3+1))
        l.append([-((t[i][0] - 1) * 3 + 1), -((t[i][1] - 1) * 3 + 1)])
        l.append([-((t[i][0] - 1) * 3 + 2), -((t[i][1] - 1) * 3 + 2)])
        l.append([-((t[i][0] - 1) * 3 + 3), -((t[i][1] - 1) * 3 + 3)])
    # print(len(l))
    return l


def graph(c, n, s, a):
    """définit fichier cnf"""
    cnf = ""
    cnf += "c tp2.cnf\nc\n"
    l: List = []
    for i in range(len(s)):
        l.append(at_least_one(i + 1))
        tmp: List = at_most_one(i + 1)
        for i in range(len(tmp)):
            l.append(tmp[i])
    tmp2: List = contraintes(a)
    for i in range(len(tmp2)):
        l.append(tmp2[i])
    # print(len(l))
    # print(l)

    cnf += f"p cnf {c*n} {len(l)}\n"
    for i in range(len(l)):
        for j in range(len(l[i])):
            cnf += f"{l[i][j]} "
        cnf += "0\n"
    cnf += "\n"

    with open("tp2.cnf", "w", encoding="utf8") as file:
        file.write(cnf)

    print(cnf)


def main() -> None:
    """fontion main"""
    c = 3
    n = 10
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


if __name__ == "__main__":
    main()
