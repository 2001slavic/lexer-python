from __future__ import annotations
from builtins import print
from src.Regex import Character, Operator

# checks if CONCAT is implied between given two characters and/or operators
def insertConcat(prev, current):
    # operators which need just one operand
    singleOperand = ["STAR", "PLUS", "MAYBE"]
    # if both are characters
    # ex. "ab"
    if type(prev) == type(current) == Character:
        return True
    # if first is ")" and next is character or "("
    # ex. "(a|b)(c|d)" or "(a|b)c"
    if prev == Operator(")") and \
        (type(current) is Character or current == Operator("(")):
        return True
    # if first is character and next is "("
    # ex. "a(b|c)"
    if type(prev) is Character and current == Operator("("):
        return True
    # if first is operator which takes one operand and next is character or "("
    # ex. "a*b" or "a+(b|c)"
    if (type(prev) is Operator and prev.op in singleOperand) and \
        (type(current) is Character or current == Operator("(")):
        return True
    return False
    
def combineSubex(operators: list, operands: list):
    singleOperand = ["STAR", "PLUS", "MAYBE"]

    operator = operators.pop() # pop operator from stack
    # In prefix notation, operator should be first in the string of
    # sub-expression.
    tmp = operator.op + " "

    operand1 = operands.pop() # pop operand from top of the stack
    # If whitespace, enclose in apostrophes so mySplit function from NFA will
    # work properly.
    # if operand1 == " ":
    #     operand1 = "'" + operand1 + "'"

    # if operator requires two operands, extract the second
    if operator.op not in singleOperand:
        operand2 = operands.pop()
        # if operand2 == " ":
        #     operand2 = "'" + operand2 + "'"
        tmp += operand2 + " "
    
    # first extracted operand should be written second, because of the stack
    tmp += operand1 

    operands.append(tmp) # append the result string in operand stack

class Parser:
    # This function should:
    # -> Classify input as either character(or string) or operator
    # -> Convert special inputs like [0-9] to their correct form
    # -> Convert escaped characters
    # You can use Character and Operator defined in Regex.py
    
    # :param str regex: Input regex
    # :return list: List of Operator() or Character()
    @staticmethod
    def preprocess(regex: str) -> list[Character | Operator]:
        # used to convert operators to their literals
        prenexName = {"|" : "UNION",
        "*" : "STAR",
        "+" : "PLUS",
        "?" : "MAYBE",
        "(" : "(",
        ")" : ")"}

        res = []
        i = 0
        while i < len(regex):
            tmp = []
            char = regex[i]
            # expand square brackets syntactic sugars
            if char == "[":
                fromChar = regex[i + 1]
                toChar = regex[i + 3]
                tmp.append(Operator("("))
                i += 4 # skip the 'cursor' to after the syntactic sugar
                for j in range(ord(fromChar), ord(toChar) + 1):
                    tmp.append(Character(chr(j)))
                    tmp.append(Operator(prenexName["|"]))
                tmp = tmp[:-1]
                tmp.append(Operator(")"))
                res += tmp
            # if character is between apostrophes ex. 'c'
            elif char == "'":
                # if two consecutive apostrophes
                if regex[i + 1] == "'":
                    # interpret as single apostrophe ex. '''
                    res.append(Character(regex[i + 1]))
                    i += 2
                else:
                    # take the whole string between apostrophes as a character
                    # ex. 'eps' is a single character eps
                    for j in range(i + 1, len(regex)):
                        if regex[j] == "'":
                            res += tmp
                            i = j # skip the string between apostrophes
                            break
                        tmp.append(Character(regex[j]))
            else:
                # check if operator or not
                if char in "|*+?()":
                    res.append(Operator(prenexName[char]))
                else:
                    # check if char is eps
                    if regex[i:i+3] == "eps":
                        char = "eps"
                        i += 2
                    res.append(Character(char))
            i += 1
        
        return res


    # This function should construct a prenex expression out of a normal one.
    @staticmethod
    def toPrenex(s: str) -> str:
        # define precedence (priority) of operators
        priority = {"UNION" : 1,
        "CONCAT" : 2,
        "STAR" : 3,
        "PLUS" : 3,
        "MAYBE" : 3,
        "(" : 0,
        ")" : 0}

        operators = []
        operands = []

        regex = Parser.preprocess(s)

        prev = None
        i = 0
        while i < len(regex):
            current = regex[i]
            # check and add a CONCAT operator wherever needed, 'on the fly'
            if insertConcat(prev, current):
                # set prev to None to prevent continous insertion of CONCATs
                prev = None
                current = Operator("CONCAT")
                i -= 1 # stay at the same position of input regex
            if type(current) is Character:
                tmp = current.chr
                # NEW for stage 3 -- enclose whitespace here
                # If whitespace, enclose in apostrophes so mySplit function
                # from NFA will work properly.
                if tmp == " ":
                    tmp = "'" + tmp + "'"
                operands.append(tmp)
            else:
                if current == Operator("("):
                    operators.append(current)
                elif current == Operator(")"):
                    # Combine all sub-expressions from nearest "(" on stack to
                    # current ")".
                    while len(operators) > 0 and operators[-1] != Operator("("):
                        combineSubex(operators, operands)
                    operators.pop() # pop the remaining "(" from stack
                else:
                    # Priority condition is set because operators with higher
                    # priority should combine first, hence, they should 'take'
                    # their operator(s) first.
                    while len(operators) > 0 and \
                        priority[current.op] < priority[operators[-1].op]:
                        combineSubex(operators, operands)
                    operators.append(current) # append current operator
                        
            # leave prev as None if current operator was set to CONCAT
            if current != Operator("CONCAT"):
                prev = current
            i += 1

        # Combine the remaining operator - operand expressions into final
        # result. Usually, these are *+? at the end of the regex, outside
        # parantheses.
        while len(operators) > 0:
            combineSubex(operators, operands)
        
        # final result is on top of the 'stack'
        return operands[-1]
