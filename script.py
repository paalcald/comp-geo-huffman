from collections import Counter #Counter
from functools import total_ordering 
from queue import PriorityQueue
from itertools import chain
import csv 
from math import log2

@total_ordering
class HT:
    def __init__(self, *args):
        if len(args) == 1:
            value = args[0]
            self.depth = 0
            self.value = value
            self.children = []
        else:
            lnode = args[0]
            rnode = args[1]
            self.depth = max(lnode.depth, rnode.depth) + 1
            self.value = lnode.value + rnode.value
            self.children = [lnode, rnode]

    def __add__(self, other):
        return HT(self,other)

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self.value

    def get_value(self):
        return self.value

    def is_leaf(self):
        return (self.depth == 0)

    def __eq__(self, other):
        return (self.value == other.value)

    def __lt__(self, other):
        return (self.value < other.value)

    def __str__(self):
        return str(self.value)

@total_ordering
class HTnode:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency

    def __eq__(self, other):
        return self.frequency == other.frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __add__(self, other):
        new_tree = "[" + self.value + ", " + other.value + "]"
        new_frequency = self.frequency + other.frequency
        return HTnode(new_tree, new_frequency)

    def __str__(self):
        str_repr = "[" + self.value + \
            "->" + str(self.frequency) + "]"
        return str_repr

def FTtoPQ(ftab):
    pq = PriorityQueue()
    for char, frequency in ftab.items():
        pq.put(HT(HTnode(char, frequency)))
    return pq

def PQtoHT(q):
    while q.qsize() >= 2:
        elem1 = q.get()
        elem2 = q.get()
        q.put(HT(elem1, elem2))
    return q.get()

def getCodes(ht):
    d = {}
    getCodesRec(ht, d)
    return d

def getCodesRec(ht, codes, prefix = ""):
    if ht.depth == 0:
        codes[ht.value.value] = prefix
    else:
        getCodesRec(ht.children[0], codes, prefix + "0")
        getCodesRec(ht.children[1], codes, prefix + "1")

def satisfiesShannonFirstTheorem(H, L, output=True):
    if H - 1 <= L and L <= H + 1:
        if output:
            print(f"{H - 1} <= {L} <= {H + 1}")
            print("Se cumple el primer teorema de Shannon")
        return True
    else:
        return False

def encode(string, code):
    encoded = ''
    for char in string:
        encoded += code[char]
    return encoded

def decode(s, ht):
    decodedString = ''
    rootNode = ht
    n = ht
    for c in s:
        n = n.children[0] if c == '0' else n.children[1]
        if n.is_leaf():
            decodedString += n.value.value
            n = rootNode
    return decodedString

def primerApartado(H_es, L_es, D_es, H_en, L_en, D_en):
    with open("codes.csv", 'w', encoding = "utf8") as codes:
        codes.write("Char, Code_{Esp}, Code_{Eng}\n")
        for char in chain(D_es, D_en):
            codes.write(f"{repr(char)}, {D_es.get(char, '-')}, {D_en.get(char, '-')}\n")

    print(f"La longitud media L_esp es {L_es}")
    print(f"La entropia H_esp es {H_es}")
    assert satisfiesShannonFirstTheorem(H_es, L_es)

    print(f"La longitud media L_eng es {L_en}")
    print(f"La entropia H_eng es {H_en}")
    assert satisfiesShannonFirstTheorem(H_en, L_en)

def segundoApartado(D_es, D_en): 
    X_en = ''
    X_es = ''
    palabra = 'medieval'
    for letter in palabra:
        X_en += D_en[letter]
        X_es += D_es[letter]

    percent_es = int(len(palabra*8)/len(X_es)*100)
    print(f"\'{palabra}\' compreso con S_Esp es \'{X_es}\'")
    print(f"sin comprimir es {percent_es}% mas largo")

    percent_en = int(len(palabra*8)/len(X_en)*100)
    print(f"\'{palabra}\' compreso con S_Eng es \'{X_en}\'")
    print(f"sin comprimir es {percent_en}% mas largo")

def tercerApartado(HT_en):
    encoded = "10111101101110110111011111"
    decoded = decode(encoded, HT_en)
    sol = f"{encoded} es {decoded}"\
        f"Los arboles de Huffman NO son únicos"\
        f"y este apartado está mal planteado."
    print(sol)

filename_es = 'GCOM2022_pract2_auxiliar_esp.txt'
with open(filename_es, 'r', encoding = "utf8") as ifile:
    es = ifile.read()

tab_es = Counter(es)
HT_es = PQtoHT(FTtoPQ(tab_es))
D_es = getCodes(HT_es)
Les_i = [len(code) * tab_es[letter]
         for letter, code in D_es.items()]
L_es = sum(Les_i) / len(es)
Hes_i = [freq / len(es) * log2(freq / len(es))
         for freq in tab_es.values()]
H_es = -1 * sum(Hes_i)

filename_en = 'GCOM2022_pract2_auxiliar_eng.txt'
with open(filename_en, 'r', encoding = "utf8") as ifile:
    en = ifile.read()

tab_en = Counter(en)
HT_en = PQtoHT(FTtoPQ(tab_en))
D_en = getCodes(HT_en)
Len_i = [len(code) * tab_en[letter]
         for letter, code in D_en.items()]
L_en = sum(Len_i) / len(en)
Hen_i = [freq / len(en) * log2(freq / len(en))
         for freq in tab_en.values()]
H_en = -1 * sum(Hen_i)

primerApartado(H_es, L_es, D_es, H_en, L_en, D_en)
segundoApartado(D_es, D_en)
tercerApartado(HT_en)
