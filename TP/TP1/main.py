"""TP1 IA02"""

from typing import List, Dict, Generator


def decomp(n: int, nb_bits: int) -> List[bool]:
    """Calcule la décomposition binaire de n"""
    tmp: str = bin(n)[2:]
    tmp2: str = tmp[::-1]
    list1: list[bool] = []
    for i in range(nb_bits):
        list1.append(False)
    for i, tmp_2 in enumerate(tmp2):
        if tmp_2 == "1":
            list1[i] = True
    return list1


# print(decomp(3, 4))


def interpretation(voc: List[str], vals: List[bool]) -> Dict[str, bool]:
    """Crée un dictionnaire qui associe à chaque variable la valeur True ou False"""
    dict1: dict = {}
    if len(voc) != len(vals):
        raise Exception("problème de taille des variables")
    for i, voc_i in enumerate(voc):
        dict1[voc_i] = vals[i]
    return dict1


# print(interpretation(['A', 'B', 'C'], [True, True, False]))


def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None]:
    """Génère toutes les interprétations possibles pour le vocabulaire donné"""
    for i in range(2 ** len(voc)):
        yield interpretation(voc, decomp(i, len(voc)))


def valuate(formula: str, interps: Dict[str, bool]) -> bool:
    """Évalue la formule en fonction de l'interprétation qui lui est donnée"""
    return eval(formula, interps)


# print(valuate("A and not(C)", {"A": True, "B": False, "C": False}))


def table(formula: str, interps: Dict[str, bool]) -> None:
    """Affiche la table de vérité"""
    var: List = []
    for i in interps:
        var.append(i)

    print("+", end="")
    for _ in range(len(var)):
        print("---+", end="")
    print("-------+")

    print("|", end="")
    for i in range(3):
        print(f" {var[i]}", end="")
        print(" |", end="")
    print(" eval. |")

    print("+", end="")
    for _ in range(len(var)):
        print("---+", end="")
    print("-------+")

    interp: Generator = gen_interpretations(var)
    for i in range(2 ** len(var)):
        print("|", end="")
        ligne: dict = next(interp)
        for _, var_j in enumerate(var):
            tmp: str = str(ligne[var_j])
            print(f" {tmp[0]} |", end="")
        tmp_eval: str = str(valuate(formula, ligne))
        print(f"   {tmp_eval[0]}   |", end="")
        print("")

    print("+", end="")
    for _ in range(len(var)):
        print("---+", end="")
    print("-------+")


def is_valid(formula: str) -> bool:
    """Vérifie si la fonction est valide"""
    tmp: str = (
        formula.replace("(", "")
        .replace(")", "")
        .replace("and", "")
        .replace("or", "")
        .replace("not", "")
    )
    var: list[str] = tmp.split("  ")

    interp: Generator = gen_interpretations(var)
    for _ in range(2 ** len(var)):
        if valuate(formula, next(interp)) is False:
            return False
    return True


def is_contradictory(formula: str) -> bool:
    """Vérifie si la fonction est contradictoire"""
    tmp: str = (
        formula.replace("(", "")
        .replace(")", "")
        .replace("and", "")
        .replace("or", "")
        .replace("not", "")
    )
    var: list[str] = tmp.split("  ")

    interp: Generator = gen_interpretations(var)
    for _ in range(2 ** len(var)):
        if valuate(formula, next(interp)) is True:
            return False
    return True


def is_contingent(formula: str) -> bool:
    """Vérifie si la formule est contingente"""
    if not is_valid(formula) and not is_contradictory(formula):
        return True
    return False


def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    """Vérifie si la formule f2 est une conséquence logique de la formule f1"""
    interp: Generator = gen_interpretations(voc)
    for _ in range(2 ** len(voc)):
        ligne: Dict[str, bool] = next(interp)
        if valuate(f1, ligne) and not valuate(f2, ligne):
            return False
    return True


# decomp(5, 4)

# g = gen_interpretations(["A", "B", "C"])
# print(next(g))
# print(next(g))

# for i in gen_interpretations(["toto", "tutu"]):
#    print(i)

# table("(A or B) and not(C)", {"A": True, "B": False, "C": False})

# print(is_valid("not(A and not(A))"))
# print(is_contradictory("A and not(A)"))
# print(is_contingent("A and not(A)"))
# print(is_cons("A", "A and B", ['A', 'B'])) # False
# print(is_cons("A and B", "A", ['A', 'B'])) # True
