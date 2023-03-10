import unittest
from src.Parser import Parser
from src.DFA import DFA

class RegexParseTests(unittest.TestCase):
    def test_single_char(self):
        s = "a"
        # self.assertEqual(Parser.toPrenex(s), "a")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertFalse(DFA.fromPrenex(s).accepts(""))
        self.assertFalse(DFA.fromPrenex(s).accepts("aa"))
        self.assertFalse(DFA.fromPrenex(s).accepts("b"))
        print("single char (1p)")

    def test_single_concat(self):
        s = "aa"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT a a")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("aa"))
        self.assertFalse(DFA.fromPrenex(s).accepts("a"))
        self.assertFalse(DFA.fromPrenex(s).accepts("aaa"))
        self.assertFalse(DFA.fromPrenex(s).accepts("b"))
        print("single concat (1p)")

    def test_single_union(self):
        s = "a|b"
        #self.assertEqual(Parser.toPrenex(s), "UNION a b")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertFalse(DFA.fromPrenex(s).accepts("aa"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ab"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ba"))
        print("single union (1p)")

    def test_single_star(self):
        s = "a*"
        #self.assertEqual(Parser.toPrenex(s), "STAR a")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aa"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aaaaaaaaa"))
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        print("single star (1p)")
    
    def test_union_concat_1(self):
        s =  "ab|c"
        #self.assertEqual(Parser.toPrenex(s), "UNION CONCAT a b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("c"))
        self.assertTrue(DFA.fromPrenex(s).accepts("ab"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ac"))
        self.assertFalse(DFA.fromPrenex(s).accepts("abc"))
        print("union concat 1 (2p)")
    
    def test_union_concat_2(self):
        s = "a|bc"
        # self.assertEqual(Parser.toPrenex(s), "UNION a CONCAT b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bc"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ac"))
        print("union concat 2 (2p)")
    
    def test_multiple_union(self):
        s = "a|b|c|d"
        #self.assertEqual(Parser.toPrenex(s), "UNION UNION UNION a b c d")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertTrue(DFA.fromPrenex(s).accepts("c"))
        self.assertTrue(DFA.fromPrenex(s).accepts("d"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ab"))
        print("multiple union (3p)")

    def test_union_concat_with_par_1(self):
        s = "(a|b)c"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT UNION a b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("ac"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bc"))
        self.assertFalse(DFA.fromPrenex(s).accepts("c"))
        self.assertFalse(DFA.fromPrenex(s).accepts("a"))
        self.assertFalse(DFA.fromPrenex(s).accepts("abc"))
        print("union concat with par 1 (3p)")
    
    def test_union_concat_with_par_2(self):
        s = "a(b|c)"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT a UNION b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("ab"))
        self.assertTrue(DFA.fromPrenex(s).accepts("ac"))
        self.assertFalse(DFA.fromPrenex(s).accepts("c"))
        self.assertFalse(DFA.fromPrenex(s).accepts("a"))
        self.assertFalse(DFA.fromPrenex(s).accepts("abc"))
        print("union concat with par 2 (3p)")
    
    def test_union_star(self):
        s = "a|b*"
        #self.assertEqual(Parser.toPrenex(s), "UNION a STAR b")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bbbbbbbbbb"))
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertFalse(DFA.fromPrenex(s).accepts("ab"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ba"))
        print("union star (2p)")

    def test_concat_star(self):
        s = "ab*cd*"
        #self.assertEqual(Parser.toPrenex(s), "CONCAT a CONCAT STAR b CONCAT c STAR d")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("ac"))
        self.assertTrue(DFA.fromPrenex(s).accepts("acd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abc"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abcd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abbbbbbbbcdddd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abbbbbbbbc"))
        self.assertTrue(DFA.fromPrenex(s).accepts("acddd"))
        print("concat star (3p)")

    def test_complex_union_concat(self):
        s = "a|(b|(c|de))"
        #self.assertEqual(Parser.toPrenex(s), "UNION a UNION b UNION c CONCAT d e")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertTrue(DFA.fromPrenex(s).accepts("c"))
        self.assertTrue(DFA.fromPrenex(s).accepts("de"))
        self.assertFalse(DFA.fromPrenex(s).accepts("ab"))
        self.assertFalse(DFA.fromPrenex(s).accepts("abc"))
        self.assertFalse(DFA.fromPrenex(s).accepts("abde"))
        print("complex union concat (6p)")

    def test_all_basic_1(self):
        s = "a(b|c)*"
        #self.assertEqual(Parser.toPrenex(s), "CONCAT a STAR UNION b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abbbbbb"))
        self.assertTrue(DFA.fromPrenex(s).accepts("accccccccc"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abccbbbbcbcbcbcb"))
        self.assertTrue(DFA.fromPrenex(s).accepts("acccbbcbcbbbc"))
        print("all basic 1 (6p)")

    def test_all_basic_2(self):
        s = "(a|b)(c|d)*"
        #self.assertEqual(Parser.toPrenex(s), "CONCAT UNION a b STAR UNION c d")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertTrue(DFA.fromPrenex(s).accepts("acdcdcdddc"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bddddcddcddd"))
        print("all basic 2 (6p)")

    def test_all_basic_3(self):
        s = "a*|b|c"
        #self.assertEqual(Parser.toPrenex(s), "UNION UNION STAR a b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        self.assertTrue(DFA.fromPrenex(s).accepts("c"))
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aaaaaa"))
        print("all basic 3 (6p)")

    def test_all_basic_4(self):
        s = "a*|bc|d"
        # self.assertEqual(Parser.toPrenex(s), "UNION UNION STAR a CONCAT b c d")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertTrue(DFA.fromPrenex(s).accepts("bc"))
        self.assertTrue(DFA.fromPrenex(s).accepts("d"))
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aaaaaaaaaaaa"))
        print("all basic 4 (6p)")

    def test_all_basic_5(self):
        s = "a*(b|c)d"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT STAR a CONCAT UNION b c d")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("bd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("cd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aaaaaacd"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aaaaaaaaaaaabd"))
        print("all basic 5 (6p)")
    
    def test_all_basic_6(self):
        s = "(ab(b|c)*)*"
        # self.assertEqual(Parser.toPrenex(s), "STAR CONCAT CONCAT a b STAR UNION b c")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertTrue(DFA.fromPrenex(s).accepts("ab"))
        self.assertTrue(DFA.fromPrenex(s).accepts("ababab"))
        self.assertTrue(DFA.fromPrenex(s).accepts("abbababcabcababb"))
        print("all basic 6 (6p)")
    
    def test_all_basic_7(self):
        s = "a(a|A)*((bcd*|ecf*)|aA)*"
        # self.assertEqual(Parser.toPrenex(s),"CONCAT CONCAT a STAR UNION a A STAR UNION CONCAT b CONCAT c UNION STAR d CONCAT d CONCAT c STAR b CONCAT a A")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aAaAaaAAAAAAa"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aAaAaAbcddddbcecffffaAaA"))
        print("all basic 7 (6p)")

    # Total 70%
    def test_eps(self):
        s = "eps"
        # self.assertEqual(Parser.toPrenex(s), "eps")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertFalse(DFA.fromPrenex(s).accepts(" "))
        print("eps (1p)")

    def test_escaped_chars_1(self):
        s = "\' \'\'a\'"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT @ a")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(" a"))
        self.assertFalse(DFA.fromPrenex(s).accepts("@a"))
        print("escaped chars 1 (1p)")
    
    def test_escaped_chars_2(self):
        s = "\'\n\'a\'\t\'b"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT \n CONCAT a CONCAT \t b")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("\na\tb"))
        print("escaped chars 2 (1p)")

    def test_0_to_9(self):
        s = "[0-9]"
        # self.assertEqual(Parser.toPrenex(s), "UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("0"))
        self.assertTrue(DFA.fromPrenex(s).accepts("7"))
        self.assertTrue(DFA.fromPrenex(s).accepts("2"))
        print("0 to 9 (2p)")

    def test_a_to_z(self):
        s = "[a-z]"
        # self.assertEqual(Parser.toPrenex(s), "UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION a b c d e f g h i j k l m n o p r s t u v w x y z")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("a"))
        self.assertTrue(DFA.fromPrenex(s).accepts("l"))
        self.assertTrue(DFA.fromPrenex(s).accepts("z"))
        print("a to z (2p)")
    
    def test_A_to_Z(self):
        s = "[A-Z]"
        # self.assertEqual(Parser.toPrenex(s), "UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION A B C D E F G H I J K L M N O P R S T U V W X Y Z")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("K"))
        self.assertTrue(DFA.fromPrenex(s).accepts("T"))
        self.assertTrue(DFA.fromPrenex(s).accepts("U"))
        print("A to Z (2p)")

    def test_plus(self):
        s = "0+"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT 0 STAR 0")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("0"))
        self.assertTrue(DFA.fromPrenex(s).accepts("0000000"))
        self.assertFalse(DFA.fromPrenex(s).accepts(""))
        print("plus (1p)")

    def test_question_mark(self):
        s = "0?"
        # self.assertEqual(Parser.toPrenex(s), "UNION 0 eps")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(""))
        self.assertTrue(DFA.fromPrenex(s).accepts("0"))
        self.assertFalse(DFA.fromPrenex(s).accepts("00"))
        print("question mark (1p)")

    def test_q_and_p(self):
        s = "0?1+"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT UNION 0 eps CONCAT 1 STAR 1")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("11111"))
        self.assertTrue(DFA.fromPrenex(s).accepts("011111111"))
        self.assertFalse(DFA.fromPrenex(s).accepts("0"))
        self.assertFalse(DFA.fromPrenex(s).accepts("001111"))
        self.assertFalse(DFA.fromPrenex(s).accepts(""))
        print("q and p (1p)")

    def test_0_to_9_star(self):
        s = "[0-9]*|b"
        # self.assertEqual(Parser.toPrenex(s), "UNION STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9 b")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("012377777"))
        self.assertTrue(DFA.fromPrenex(s).accepts("98555561312"))
        self.assertTrue(DFA.fromPrenex(s).accepts("b"))
        print("0 to 9 star (3p)")

    def test_squared_ops(self):
        s = "a([a-z]*|[A-Z]*)z"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT a CONCAT UNION STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION a b c d e f g h i j k l m n o p r s t u v w x y z STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION A B C D E F G H I J K L M N O P R S T U V W X Y Z z")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("az"))
        self.assertTrue(DFA.fromPrenex(s).accepts("acetareetemaz"))
        self.assertTrue(DFA.fromPrenex(s).accepts("aFASTz"))
        print("squared ops (3p)")

    def test_complex(self):
        s = "[0-9]+(\'-\'[0-9]+)*"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT CONCAT UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9 STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9 STAR CONCAT - CONCAT UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9 STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("0"))
        self.assertTrue(DFA.fromPrenex(s).accepts("1231212"))
        self.assertTrue(DFA.fromPrenex(s).accepts("777-333"))
        self.assertTrue(DFA.fromPrenex(s).accepts("7-3-5-6-7-8"))
        self.assertTrue(DFA.fromPrenex(s).accepts("11-23-94-312-413231"))
        print("complex (6p)")

    def test_all(self):
        s = "([0-9]*|b+)c?d(da)(\' \'|[A-Z]|\'a\')?"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT CONCAT CONCAT UNION STAR UNION UNION UNION UNION UNION UNION UNION UNION UNION 0 1 2 3 4 5 6 7 8 9 CONCAT b STAR b UNION c eps d CONCAT CONCAT d a UNION UNION @ UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION UNION A B C D E F G H I J K L M N O P R S T U V W X Y Z a eps")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts("bdda "))
        self.assertTrue(DFA.fromPrenex(s).accepts("28121274849cdda"))
        self.assertTrue(DFA.fromPrenex(s).accepts("dda"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bbbbbbcddaa"))
        self.assertTrue(DFA.fromPrenex(s).accepts("bddaT"))
        self.assertTrue(DFA.fromPrenex(s).accepts("07cdda "))
        self.assertFalse(DFA.fromPrenex(s).accepts("07bcdda "))
        print("all (6p)")
