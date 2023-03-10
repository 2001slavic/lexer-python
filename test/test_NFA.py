import unittest
from src.NFA import NFA


class NFATests(unittest.TestCase):
	def test_nfa_from_eps(self):
		self.assertTrue(NFA.fromPrenex("eps").accepts(""))

	def test_nfa_plus(self):
		self.assertTrue(NFA.fromPrenex("CONCAT PLUS a PLUS b").accepts("aaaaaaaaaaaaaaaaab"))
		self.assertFalse(NFA.fromPrenex("CONCAT PLUS a PLUS b").accepts("b"))

	def test_nfa_maybe(self):
		self.assertTrue(NFA.fromPrenex("CONCAT MAYBE a MAYBE b").accepts(""))	
		self.assertTrue(NFA.fromPrenex("CONCAT MAYBE a MAYBE b").accepts("a"))	
		self.assertTrue(NFA.fromPrenex("CONCAT MAYBE a MAYBE b").accepts("ab"))	
		self.assertTrue(NFA.fromPrenex("CONCAT MAYBE a MAYBE b").accepts("b"))
		self.assertFalse(NFA.fromPrenex("CONCAT MAYBE a MAYBE b").accepts("aaaa"))		

	def test_nfa_from_space(self):
		self.assertTrue(NFA.fromPrenex("' '").accepts(" "))
		self.assertFalse(NFA.fromPrenex("' '").accepts(""))


	def test_nfa_from_void(self):
		self.assertFalse(NFA.fromPrenex("void").accepts(""))


	def test_nfa_from_char(self):
		self.assertTrue(NFA.fromPrenex("a").accepts("a"))
		self.assertFalse(NFA.fromPrenex("a").accepts("b"))


	def test_nfa_from_complex_expression1(self):
		expr = "CONCAT a b"
		self.assertTrue(NFA.fromPrenex(expr).accepts("ab"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("aba"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("ba"))


	def test_nfa_from_complex_expression2(self):
		expr = "UNION a b"
		self.assertTrue(NFA.fromPrenex(expr).accepts("a"))
		self.assertTrue(NFA.fromPrenex(expr).accepts("b"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("ab"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("ba"))


	def test_nfa_from_star1(self):
		expr = "STAR a"
		self.assertTrue(NFA.fromPrenex(expr).accepts(""))
		self.assertTrue(NFA.fromPrenex(expr).accepts("a"))
		self.assertTrue(NFA.fromPrenex(expr).accepts("aaaaaaaaaaa"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("aaaaabaaaaa"))


	def test_nfa_from_complex_expression3(self):
		expr = "STAR UNION a b"
		self.assertTrue(NFA.fromPrenex(expr).accepts("aaababaaabaaaaa"))
		self.assertTrue(NFA.fromPrenex(expr).accepts("aaaaaaaaaa"))
		self.assertTrue(NFA.fromPrenex(expr).accepts("bbbbbbbbbbb"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("baaabbbabaacabbbaaabbb"))


	def test_nfa_from_complex_expression4(self):
		expr = "STAR CONCAT a b"
		self.assertTrue(NFA.fromPrenex(expr).accepts("ababababab"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("abababababa"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("abababaabab"))


	def test_nfa_from_complex_expression5(self):
		expr = "STAR CONCAT a b"
		self.assertTrue(NFA.fromPrenex(expr).accepts("ababababab"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("abababababa"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("abababaabab"))


	def test_nfa_from_complex_expression6(self):
		expr = "CONCAT UNION b STAR a STAR c"
		self.assertTrue(NFA.fromPrenex(expr).accepts("aaaaaaaaaccccc"))
		self.assertTrue(NFA.fromPrenex(expr).accepts("bccccccccc"))
		self.assertFalse(NFA.fromPrenex(expr).accepts("bbbbccccccccc"))


	def test_nfa_from_complex_expression7(self):
		expr = "CONCAT a STAR a"
		self.assertTrue(NFA.fromPrenex(expr).accepts("aaa"))
		self.assertFalse(NFA.fromPrenex(expr).accepts(""))

	def test_nfa_map1(self):
		# this is a class used just for this test
		# its get_mapping method recieves a 'state' and returns a unique id for it. if it reiceves the same state multiple time it returns the same id
		class test_it():
			def __init__(self, counter = 0) -> None:
				self.counter = counter
				self.mapping = {}

			def get_mapping(self, x):
				if x not in self.mapping:
					self.mapping[x] = self.counter
					self.counter += 1

				return self.mapping[x]

		it = test_it(5) # a new test_it which gives id's starting with '5'

		# a list of regexes, their alphabets and mapping functions to test the 'map' method on
		regexes = [
			("CONCAT UNION b STAR a STAR c", "abc", lambda x : x + 2 ),
			("CONCAT a STAR a", "a", str ),
			("CONCAT a UNION b STAR CONCAT c d", "abcd", it.get_mapping )
		]

		for regex, alphabet, f in regexes:
			nfa = NFA.fromPrenex(regex)

			mapped_nfa = nfa.map(f)

			states = nfa.getStates()
			newStates = mapped_nfa.getStates()

			# check if the new set of states is the result of mapping f on the old set
			self.assertSetEqual(set(map(f, states)), newStates)

			for s in states:
				# check if the same applies to the set of final states
				self.assertEqual(nfa.isFinal(s), mapped_nfa.isFinal(f(s)))

			# check if f(old_delta(old_state,c)) = new_delta(new_state, c) for each state-character
			# pair (epsilon-tranistions are not checked)
			for c in alphabet:
				for s in states:
					originalNext = nfa.next(s, c)
					mappedNext = mapped_nfa.next(f(s), c)

					self.assertSetEqual(set(map(f, originalNext)), mappedNext)


