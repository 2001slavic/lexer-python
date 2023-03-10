from ast import List
import copy
import itertools
from typing import Callable, Generic, TypeVar

S = TypeVar("S")
T = TypeVar("T")

# ast node class
class ASTNode:
    def __init__(self, data, children = None):
        if children is None:
            children = []
        self.data = data
        self.children: list[ASTNode] = children

# My split() function so characters such as '@' and '\n' can be splitted
# properly.
def mySplit(string: str) -> 'List[str]':
	res = []
	# iterate through each character
	i = 0
	tmp = ""
	while i < len(string):
		
		if (string[i] == "'"): # if apostrophe encountered
			# Updated apostrophe processing, similar as in preprocess function
			# from Parser.py
			if string[i + 1] == "'":
				res.append(string[i + 1])
				i += 2
			else:
				for j in range(i + 1, len(string)):
					if string[j] == "'":
						res.append(tmp)
						tmp = ""
						i = j
						break
					tmp += string[j]
		elif (string[i] == " "): # if space, reset temp result
			if (len(tmp) > 0):
				res.append(tmp)
				tmp = ""
		else:
			tmp = tmp + string[i]
		i += 1

	if (len(tmp) > 0):
		res.append(tmp)

	return res

# convert list of strings to AST
def toAST(wordList: 'list[str]') -> 'tuple[ASTNode, str]':
    node = ASTNode(wordList[0])
    if (node.data == "UNION") or (node.data == "CONCAT"):
		# recursive call consuming a string
        child1, wordList = toAST(wordList[1:])
        child2, wordList = toAST(wordList[1:])
		# append to results after the required recursive calls
        node.children.append(child1)
        node.children.append(child2)
    elif (node.data == "STAR"):
        child, wordList = toAST(wordList[1:])
        node.children.append(child)
	# convert MAYBE to UNION and eps equivalent
    elif (node.data == "MAYBE"):
        node.data = "UNION"
        child1, wordList = toAST(wordList[1:])
        node.children.append(child1)
        node.children.append(ASTNode("eps"))
	# convert PLUS to CONCAT and STAR equivalent
    elif (node.data == "PLUS"):
        node.data = "CONCAT"
        child1, wordList = toAST(wordList[1:])
        node.children.append(child1)
        node.children.append(ASTNode("STAR", [child1]))
	# if atom is reached, just return is made

    return node, wordList

# NFA node class
class NFANode:
	newid = itertools.count()
	def __init__(self, token: str = None):
		# id + 1 on each constructor call
		self.id = next(NFANode.newid)
		self.transitions: list[tuple[NFANode, str]] = []
		self.isFinal = False
		self.token = token

# convert AST to NFA graph
def toNFA(tree: ASTNode) -> list[NFANode]:
	res = []
	expression = tree.data # save operation or atom name
	if (expression == "UNION"):
		startNode = NFANode() # create new start node
		res.append(startNode) # append it to result graph

		# get AST tree children
		child1 = tree.children[0]
		child2 = tree.children[1]

		# to NFA conversion on first branch of UNION
		branch1 = toNFA(child1)
		endNode = NFANode() # create end node of UNION
		# Add eps transition from start node of UNION to first node of first
		# UNION branch.
		startNode.transitions.append((branch1[0], "eps"))
		# eps transition from last node of branch1 to end node of UNION
		branch1[-1].transitions.append((endNode, "eps"))

		branch2 = toNFA(child2) # toNFA on second branch of UNION
		# eps transition from UNION start to branch2 start
		startNode.transitions.append((branch2[0], "eps"))
		# eps from last of branch2 to last of UNION
		branch2[-1].transitions.append((endNode, "eps"))

		res += branch1 + branch2 # combine results
		res.append(endNode) # add UNION end node to graph

	elif (expression == "CONCAT"):
		child1 = tree.children[0]
		child2 = tree.children[1]

		# to NFA both children
		# op = operand (in this case)
		op1 = toNFA(child1)
		op2 = toNFA(child2)

		res = op1 + op2 # combine results and save in res graph

		endNode1 = op1[-1]
		node2 = op2[0]

		# connect end node of op1 and start node of op2 with an eps transition
		endNode1.transitions.append((node2, "eps"))

	elif (expression == "STAR"):
		startNode = NFANode()
		res.append(startNode)

		child = tree.children[0]
		# process the inner NFA of STAR
		nfa = toNFA(child)
		endNode = NFANode()

		# add required eps transitions for STAR as per Thompson's construction
		startNode.transitions.append((endNode, "eps"))
		startNode.transitions.append((nfa[0], "eps"))
		nfa[-1].transitions.append((nfa[0], "eps"))
		nfa[-1].transitions.append((endNode, "eps"))

		# append results to final graph
		res += nfa
		res.append(endNode)
	
	# if atom
	else:
		# create start, end nodes
		startNode = NFANode()
		endNode = NFANode()
		res.append(startNode)

		# set transition between
		startNode.transitions.append((endNode, expression))

		res.append(endNode)
	
	return res

# recursvie accept helper function for NFA
def NFAAccept(graph: list[NFANode], currentNode: NFANode, input: str) -> bool:
	res = False
	# if no more word and node is final
	# NEW for stage 3 -- improved final node (state) check
	if len(input) <= 0 and currentNode.isFinal:
		return True

	for transition in currentNode.transitions:
		if (len(input) > 0) and (transition[1] == input[0]):
			res = NFAAccept(graph, transition[0], input[1:])
		elif transition[1] == "eps":
			# do not consume word if eps transition
			res = NFAAccept(graph, transition[0], input)
		if res == True:
			return True

	return False



class NFA(Generic[S]):
	def __init__(self, graph):
		# NFANode.newid = itertools.count() # reset id count for each new NFA
		self.graph: list[NFANode] = graph

	def map(self, f: Callable[[S], T]) -> 'NFA[T]':
		graph2 = copy.deepcopy(self.graph)
		for node in graph2:
			# apply function for each id in copy of NFA graph
			node.id = f(node.id)
		return NFA(graph2)

	def next(self, from_state: S, on_chr: str) -> 'set[S]':
		state: NFANode = None
		res = set()
		# locate the state with given id
		for node in self.graph:
			if node.id == from_state:
				state = node
				break

		if state is None:
			return res

		# Iterate through all transitions and add to set these which are on
		# required character.
		for transition in state.transitions:
			if transition[1] == on_chr:
				res.add(transition[0].id)

		return res

	def getStates(self) -> 'set[S]':
		res = set()
		# iterate through adjacency list and add ids to result set
		for node in self.graph:
			res.add(node.id)
		return res

	def accepts(self, str: str) -> bool:
		# call helper function
		return NFAAccept(self.graph, self.graph[0], str)

	def isFinal(self, state: S) -> bool:
		# NEW for stage 3 -- final state check based on new member variable
		for node in self.graph:
			if (node.id == state) and node.isFinal:
				return True
		return False

	@staticmethod
	def fromPrenex(str: str) -> 'NFA[int]':
		
		# call helper functions
		graph = toNFA(toAST(mySplit(str))[0])
		graph[-1].isFinal = True # NEW for stage 3, mark the last state as final
		return NFA(graph)

