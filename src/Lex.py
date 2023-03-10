from typing import Tuple, List, Dict
from src.NFA import NFA, NFANode
from src.Parser import Parser
from src.DFA import toDFA

# Get longest substring from temporary result, first token to appear in
# configuration has bigger priority.
def getLongestSubstring(configurations: Dict[str, str], substrings: Dict[str, str]) -> tuple[str, str]:
	res: tuple[str, str] = None
	# iterate through configuration
	for (token, _) in configurations.items():
		substring = substrings.get(token)
		if substring is not None: # if temporary result has substring at token
			# if function result is empty, save the found substring
			if res is None: 
				res = (token, substring)
			else:
				# save the longer substring
				if len(substring) > len(res[1]):
					res = (token, substring)
	return res

# get line and column of a char in word for proper error reporting
def getLineColumn(word: str, chrIndex: int) -> tuple[int, int]:
	column = 0
	line = 0
	for i in range(len(word)):
		if word[i] == "\n":
			line += 1
			column = 0
		if i == chrIndex:
			break
		column += 1
	return (line, column)

# performs required operations if current DFA state is final
def processFinalState(currentState, tmpRes, word, wordStart, i):
	if not currentState.isFinal:
		return False
	for NFAState in currentState.NFAGroup:
		if NFAState.isFinal:
			substring = tmpRes.get(NFAState.token)
			newSubstring = word[wordStart:i] # substring from last sink state
			if substring is None:
				tmpRes[NFAState.token] = newSubstring # write new temp result
			else:
				# save longest substring
				if len(newSubstring) > len(substring):
					tmpRes[NFAState.token] = newSubstring
	return True

class Lexer:

	"""
		This constructor initializes the lexer with a configuration
		The configuration is passed as a dictionary TOKEN -> REGEX

		You are encouraged to use the functions from the past stages to parse the regexes
	"""
	def __init__(self, configurations: Dict[str, str]) -> None:
		initialNFANode = NFANode() # initial NFA node for an single NFA
		finalNFAGraph: list[NFANode] = []
		finalNFAGraph.append(initialNFANode)
		for (token, regex) in configurations.items():
			tmpNFA = NFA.fromPrenex(Parser.toPrenex(regex))
			tmpNFA.graph[-1].token = token # save token for last nodes
			# Create transition between the initial node to initial nodes of
			# other NFAs.
			initialNFANode.transitions.append((tmpNFA.graph[0], "eps"))
			finalNFAGraph += tmpNFA.graph # add nodes to a single graph
		self.DFATable = toDFA(finalNFAGraph) # convert the result NFA to DFA
		# save configurations for future use
		self.configurations = configurations

	"""
		The main functionality of the lexer, receives a word and lexes it
		according to the provided configuration.

		The return value is either a List of tuples (TOKEN, LEXEM) if the lexer succedes
		or a string message if the lexer fails
	"""
	def lex(self, word: str) -> List[Tuple[str, str]] | str:
		# used for DFA traversing
		currentIndex = 0
		currentState = self.DFATable["states"][currentIndex]

		# temporary and final results
		tmpRes: Dict[str, str] = {}
		res: list[tuple[str, str]] = []
		
		# index of character in word in the moment of last sink state visit
		wordStart = 0
		i = 0 # main character index
		while True:
			if i >= len(word): # check if end of word reached
				if processFinalState(currentState, tmpRes, word, wordStart, i):
					# finish lexer execution when final state reached on word end
					break 
				else:
					toAppend = getLongestSubstring(self.configurations, tmpRes)
					if toAppend is None:
						line, _ = getLineColumn(word, len(word) - 1)
						return f'No viable alternative at character EOF, line {line}'
					res.append(toAppend) # write one more result, if any
					wordStart += len(toAppend[1])
					i = wordStart # put index back to seek for new substring
					tmpRes = {}
					# reset DFA
					currentIndex = 0
					currentState = self.DFATable["states"][currentIndex]
					if i >= len(word):
						break

			chr = word[i]
			# if character not in DFA then report error
			if chr not in self.DFATable:
				line, column = getLineColumn(word, i)
				return f'No viable alternative at character {column}, line {line}'

			processFinalState(currentState, tmpRes, word, wordStart, i)
			
			# if current state is sink
			if len(currentState.NFAGroup) == 0:
				toAppend = getLongestSubstring(self.configurations, tmpRes)
				if toAppend is None:
					line, column = getLineColumn(word, i)
					return f'No viable alternative at character {column - 1}, line {line}'
				res.append(toAppend)
				wordStart += len(toAppend[1])
				i = wordStart
				tmpRes = {}
				currentIndex = 0
				currentState = self.DFATable["states"][currentIndex]
				continue

			# to next character, state
			currentState = self.DFATable[chr][currentIndex]
			try:
				currentIndex = self.DFATable["states"].index(currentState)
			except ValueError:
				line, column = getLineColumn(word, i)
				return f'No viable alternative at character {column}, line {line}'
			i += 1

		# save last temporary results
		toAppend = getLongestSubstring(self.configurations, tmpRes)
		if toAppend is not None:
			res.append(toAppend)
		if len(res) > 0:
			return res
		# if no final results -- report error
		line, _ = getLineColumn(word, len(word) - 1)
		return f'No viable alternative at character EOF, line {line}'