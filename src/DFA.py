from collections import defaultdict
import copy
import itertools
from typing import Callable, Generic, TypeVar
from src.NFA import NFA, NFANode

S = TypeVar("S")
T = TypeVar("T")

# dfa state (node) class
class DFAState:
	newid = itertools.count()
	def __init__(self, NFAGroup: list[NFANode]):
		self.id = next(DFAState.newid)
		self.NFAGroup = NFAGroup
		self.isInitial = False
		self.isFinal = False

# get all characters which are found in transitions in NFA graph
def getAlphabet(NFAgraph: list[NFANode]) -> set[str]:
	res = set()
	for node in NFAgraph:
		for transition in node.transitions:
			# except "eps"
			if transition[1] != "eps":
				res.add(transition[1])
	
	return res

# Get nodes which can be accessed from initial given node by going to given
# character transitions.
def getCharTransitions(node: NFANode, char: str) -> list[NFANode]:
	res = []
	for transition in node.transitions:
		if transition[1] == char:
			res.append(transition[0])

	return res

# get nodes which can be accessed through eps transitions, recursively
def getEpsTransitions(initialNode: NFANode, res: list[NFANode] = []) -> list[NFANode]:
	res.append(initialNode)
	for transition in initialNode.transitions:
		if transition[1] == "eps" and (transition[0] not in res):
			getEpsTransitions(transition[0], res)

	return res

# main function to build DFA transition table
def toDFA(NFAGraph: list[NFANode]) -> defaultdict[str, list[DFAState]]:
	transitionTable = defaultdict(list[DFAState])

	# get eps transitions from initial node of NFA as initial step
	initialState = DFAState(getEpsTransitions(NFAGraph[0], []))
	initialState.isInitial = True # set the resulting DFA state as initial
	# check if initial state is also final
	for node in initialState.NFAGroup:
		if node.isFinal:
			initialState.isFinal = True
	# append newly created initial state to final table
	transitionTable["states"].append(initialState)

	alphabet = getAlphabet(NFAGraph)

	
	for state in transitionTable["states"]:
		for char in alphabet:
			tmp = []
			for node in state.NFAGroup:
				if node.isFinal:
					state.isFinal = True
				tmp += getCharTransitions(node, char)
		
			tmpEps = []
			for value in tmp:
				tmpEps = getEpsTransitions(value, tmpEps)
			# result NFA group in tmpEps
			newState = None
			addToEps = True
			# check if NFA group to add already has an associated DFA state
			for checkState in transitionTable["states"]:
				if checkState.NFAGroup == tmpEps:
					newState = checkState
					addToEps = False
					break
			if newState is None:
				newState = DFAState(tmpEps)

			transitionTable[char].append(newState)
			if addToEps:
				transitionTable["states"].append(newState)
		

	return transitionTable

class DFA(Generic[S]):
	def __init__(self, table):
		DFAState.newid = itertools.count()
		self.table = table

	def map(self, f: Callable[[S], T]) -> 'DFA[T]':
		table2 = copy.deepcopy(self.table)
		for state in table2["states"]:
			state.id = f(state.id)
		return DFA(table2)

	def next(self, from_state: S, on_chr: str) -> S:
		i = 0
		while i < len(self.table["states"]):
			state = self.table["states"][i]
			if state.id == from_state:
				return self.table[on_chr][i].id
			i += 1

		return None

	def getStates(self) -> 'set[S]':
		res = set()
		for state in self.table["states"]:
			res.add(state.id)
		return res

	def accepts(self, str: str) -> bool:
		# start with initial state (which is always first in table)
		currentIndex = 0
		currentState = self.table["states"][currentIndex]
		# iterate through all characters of the input
		for chr in str:
			# if character not in DFA then reject
			if chr not in self.table:
				return False
			currentState = self.table[chr][currentIndex]
			try:
				currentIndex = self.table["states"].index(currentState)
			except ValueError:
				return False
		# if input is over and current state is final then accept
		if currentState.isFinal:
			return True
		return False

	def isFinal(self, state: S) -> bool:
		for state in self.table["states"]:
			if state.id == state:
				if state.isFinal:
					return True
				return False
				
		return False

	@staticmethod
	def fromPrenex(str: str) -> 'DFA[int]':

		# NEW for stage 3 -- using NFA's fromPrenex to build the DFA
		GenericNFA = NFA.fromPrenex(str)
		NFAGraph = GenericNFA.graph
		table = toDFA(NFAGraph)
		return DFA(table)

