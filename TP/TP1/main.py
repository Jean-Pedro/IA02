from typing import List, Dict, Generator

def decomp(n: int, nb_bits: int) -> List[bool] :
    tmp : str = bin(n)[2:]
    tmp2 : str = tmp[::-1]
    list1 : list[bool] = []
    for i in range(nb_bits):
        list1.append(False)
    for i in range(len(tmp2)):
        if(tmp2[i] == '1'):
            list1[i] = True

    return list1


def interpretation(voc: List[str], vals: List[bool]) -> Dict[str, bool] :
    dict1 : dict = {}
    if len(voc) != len(vals):
        raise Exception("problème de taille des variables")
    for i in range(len(voc)):
        dict1[voc[i]] = vals[i]
    return dict1

def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None] :
    for i in range(2**len(voc)):
        list1 : List[bool] = decomp(i, len(voc))
        dict1 : Dict[str, bool] = {}
        for j in range(len(voc)):
            dict1[voc[j]] = list1[j]
        yield dict1


def valuate(formula: str, interpretation: Dict[str, bool]) -> bool:
    tmp : str = formula
    tmp2 : str = formula.replace("(", "").replace(")", "").replace("and", "").replace("or", "").replace("not", "")
    tmp3 : list[str] = tmp2.split("  ")
    for i in tmp3:
        tmp_interp : str = str(interpretation[i])
        tmp = tmp.replace(i, tmp_interp, 1)
    return eval(tmp)
        
#print(valuate("(A or B) and not(C)", {"A": True, "B": False, "C": False}))


def table(formula: str, interpretation: Dict[str, bool]) -> None:
    var : List = []
    for i in interpretation:
        var.append(i)
    
    print("+", end='')
    for i in range(len(var)):
        print("---+", end='')
    print('-------+')

    print("|", end='')
    for i in range(3):
        print(f' {var[i]}', end='')
        print(" |", end='')
    print(" eval. |")

    print("+", end='')
    for i in range(len(var)):
        print("---+", end='')
    print('-------+')

    interp : Generator = gen_interpretations(var)
    for i in range(2**len(var)):
        print("|", end='')
        ligne : dict = next(interp)
        for j in range(len(var)):
            tmp : str = str(ligne[var[j]])
            print(f' {tmp[0]} |', end='')
        tmp_eval : str = str(valuate(formula, ligne))
        print(f'   {tmp_eval[0]}   |', end='')
        print('')

    print("+", end='')
    for i in range(len(var)):
        print("---+", end='')
    print('-------+')


def is_valid(formula : str) -> bool:
    tmp : str = formula.replace("(", "").replace(")", "").replace("and", "").replace("or", "").replace("not", "")
    var : list[str] = tmp.split("  ")

    interp : Generator = gen_interpretations(var)
    for i in range(2**len(var)):
        if valuate(formula, next(interp)) == False :
            return False
    return True

def is_contradictory(formula : str) -> bool:
    tmp : str = formula.replace("(", "").replace(")", "").replace("and", "").replace("or", "").replace("not", "")
    var : list[str] = tmp.split("  ")

    interp : Generator = gen_interpretations(var)
    for i in range(2**len(var)):
        if valuate(formula, next(interp)) == True :
            return False
    return True

def is_contingent(formula : str) -> bool:
    if not(is_valid(formula)) and not(is_contradictory(formula)):
        return True
    return False


def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    interp : Generator = gen_interpretations(voc)
    for i in range(2**len(voc)):
        ligne : Dict[str, bool] = next(interp)
        if valuate(f1, ligne) and not valuate(f2, ligne):
            return False
    return True



#decomp(5, 4)
#print(interpretation(['A', 'B', 'C'], [True, True, False]))
#g = gen_interpretations(["A", "B", "C"])
#print(next(g))
#print(next(g))

#for i in gen_interpretations(["toto", "tutu"]):
#    print(i)
    
#table("(A or B) and not(C)", {"A": True, "B": False, "C": False})

#print(is_valid("not(A and not(A))"))
#print(is_contradictory("A and not(A)"))
#print(is_contingent("A and not(A)"))
#print(is_cons("A", "A and B", ['A', 'B'])) # False
#print(is_cons("A and B", "A", ['A', 'B'])) # True
