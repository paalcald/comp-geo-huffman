from collections import Counter #Counter
from functools import total_ordering 
from queue import PriorityQueue
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

def decode(s, ht):
    decodedString = ''
    rootNode = ht
    currentNode = ht
    for c in s:
	while not currentNode.is_leaf():
	    if c == '0':
		currentNode = currentNode.children[0]
	    if c == '1':
		currentNode = currentNode.children[1]
	decodedString.append(currentNode.value.value)
	currentNode = rootNode
    return decodedString
