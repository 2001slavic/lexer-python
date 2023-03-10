import unittest
import json, os
from src.DFA import DFA
from src.Lex import Lexer

class RegexParseTests(unittest.TestCase):
    def test_simple_lexer_concat(self):
        s = {"A": "a", "BC": "bc", "DEF": "def"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("a") == [("A", "a")])
        self.assertTrue(lexer.lex("aa") == [("A", "a"), ("A", "a")])
        self.assertTrue(lexer.lex("abca") == [("A", "a"), ("BC", "bc"), ("A", "a")])
        self.assertTrue(lexer.lex("abcdefdefbca") == [("A", "a"), ("BC", "bc"), ("DEF", "def"), ("DEF", "def"), ("BC", "bc"), ("A", "a")])
        print("lexer simple concat (2p)")

    def test_simple_lexer_union(self):
        s = {"AorB": "a|b", "DorE": "d|e"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("a") == [("AorB", "a")])
        self.assertTrue(lexer.lex("abba") == [("AorB", "a"), ("AorB", "b"), ("AorB", "b"), ("AorB", "a")])
        self.assertTrue(lexer.lex("abde") == [("AorB", "a"), ("AorB", "b"), ("DorE", "d"), ("DorE", "e")])
        self.assertTrue(lexer.lex("adbeb") == [("AorB", "a"), ("DorE", "d"), ("AorB", "b"), ("DorE", "e"), ("AorB", "b")])
        print("lexer simple union (2p)")

    def test_simple_lexer_priority(self):
        s = {"smallA": "a", "bigA": "aaaa"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("a") == [("smallA", "a")])
        self.assertTrue(lexer.lex("aa") == [("smallA", "a"), ("smallA", "a")])
        self.assertTrue(lexer.lex("aaaa") == [("bigA", "aaaa")])
        self.assertTrue(lexer.lex("aaaaaa") == [("bigA", "aaaa"), ("smallA", "a"), ("smallA", "a")])
        self.assertTrue(lexer.lex("aaaaaaaa") == [("bigA", "aaaa"), ("bigA", "aaaa")])
        self.assertTrue(lexer.lex("aaaaaaaaaaaa") == [("bigA", "aaaa"), ("bigA", "aaaa"), ("bigA", "aaaa")])
        print("lexer simple priority(5p)")

    def test_lexer_space_and_zeros_char(self):
        s = {"SPACE": "' '", "ZEROS": "0+"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("0000 0") == [("ZEROS", "0000"), ("SPACE", " "), ("ZEROS", "0")])
        self.assertTrue(lexer.lex(" 0000") == [("SPACE", " "), ("ZEROS", "0000")])
        self.assertTrue(lexer.lex("00000000000000000000000000000000000000") == [("ZEROS", "00000000000000000000000000000000000000")])
        self.assertTrue(lexer.lex("0 00 000 0000 000 000 00 0 ") == [("ZEROS", "0"), ("SPACE", " "), ("ZEROS", "00"), ("SPACE", " "), ("ZEROS", "000"), ("SPACE", " "), ("ZEROS", "0000"), ("SPACE", " "), ("ZEROS", "000"), ("SPACE", " "), ("ZEROS", "000"), ("SPACE", " "), ("ZEROS", "00"), ("SPACE", " "), ("ZEROS", "0"), ("SPACE", " ")])
        print("lexer split, space and zeros (5p)")

    def test_lexer_ones_and_twos_char(self):
        s = {"TWO": "2", "PATTERN": "11*(00)*101(0|1)(0|1)*"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("1001010") == [("PATTERN", "1001010")])
        self.assertTrue(lexer.lex("1101010101") == [("PATTERN", "1101010101")])
        self.assertTrue(lexer.lex("2110000101112") == [("TWO", "2"), ("PATTERN", "11000010111"), ("TWO", "2")])
        self.assertTrue(lexer.lex("111100001010211011") == [("PATTERN", "111100001010"), ("TWO", "2"), ("PATTERN", "11011")])
        self.assertTrue(lexer.lex("2211100000010111011000110110010022") == [("TWO", "2"), ("TWO", "2"), ("PATTERN", "111000000101110110001101100100"), ("TWO", "2"), ("TWO", "2")])
        self.assertTrue(lexer.lex("2100101121101112110101012100001011211011110111101") == [('TWO', '2'), ('PATTERN', '1001011'), ('TWO', '2'), ('PATTERN', '110111'), ('TWO', '2'), ('PATTERN', '11010101'), ('TWO', '2'), ('PATTERN', '100001011'), ('TWO', '2'), ('PATTERN', '11011110111101')])
        print("lexer split, ones and twos (8p)")

    def test_lexer_plus_and_star_char(self):
        s = {"C": "c", "ABS": "(ab)+", "BS": "b+"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("ab") == [('ABS', 'ab')])
        self.assertTrue(lexer.lex("bbbbb") == [('BS', 'bbbbb')])
        self.assertTrue(lexer.lex("abababcb") == [('ABS', 'ababab'), ('C', 'c'), ('BS', 'b')])
        self.assertTrue(lexer.lex("bbab") == [('BS', 'bb'), ('ABS', 'ab')])
        self.assertTrue(lexer.lex("bbbcbbabbc") == [('BS', 'bbb'), ('C', 'c'), ('BS', 'bb'), ('ABS', 'ab'), ('BS', 'b'), ('C', 'c')])
        self.assertTrue(lexer.lex("cbbbbcbbabcabbbabb") == [('C', 'c'), ('BS', 'bbbb'), ('C', 'c'), ('BS', 'bb'), ('ABS', 'ab'), ('C', 'c'), ('ABS', 'ab'), ('BS', 'bb'), ('ABS', 'ab'), ('BS', 'b')])
        self.assertTrue(lexer.lex("ababbbbabcabbababcb") == [('ABS', 'abab'), ('BS', 'bbb'), ('ABS', 'ab'), ('C', 'c'), ('ABS', 'ab'), ('BS', 'b'), ('ABS', 'abab'), ('C', 'c'), ('BS', 'b')])
        self.assertTrue(lexer.lex("cbbbabcabbabcbbcababab") == [('C', 'c'), ('BS', 'bbb'), ('ABS', 'ab'), ('C', 'c'), ('ABS', 'ab'), ('BS', 'b'), ('ABS', 'ab'), ('C', 'c'), ('BS', 'bb'), ('C', 'c'), ('ABS', 'ababab')])

        print("lexer split, plus and star (8p)")

    def test_lexer_whitespaces_char(self):
        s = {"SPACE": "' '", "NEWLINE": "'\n'", "PATTERN1": "1' '0", "PATTERN2": "(10)+", "PATTERN3": "' '001' '", "PATTERN4": "(101' ')+", "PATTERN5": "1*01"}
        
        lexer = Lexer(s)

        self.assertTrue(lexer.lex("1 0") == [('PATTERN1', '1 0')])
        self.assertTrue(lexer.lex("101010") == [('PATTERN2', '101010')])
        self.assertTrue(lexer.lex("101010 1 0 1 0") == [('PATTERN2', '101010'), ('SPACE', ' '), ('PATTERN1', '1 0'), ('SPACE', ' '), ('PATTERN1', '1 0')])
        self.assertTrue(lexer.lex("1 0 001 1 010 ") == [('PATTERN1', '1 0'), ('PATTERN3', ' 001 '), ('PATTERN1', '1 0'), ('PATTERN2', '10'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("1 0 \n  001 1 0") == [('PATTERN1', '1 0'), ('SPACE', ' '), ('NEWLINE', '\n'), ('SPACE', ' '), ('PATTERN3', ' 001 '), ('PATTERN1', '1 0')])
        self.assertTrue(lexer.lex("101 101 1 01010  ") == [('PATTERN4', '101 101 '), ('PATTERN1', '1 0'), ('PATTERN2', '1010'), ('SPACE', ' '), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("101 1010\n  001   001  101010 ") == [('PATTERN4', '101 '), ('PATTERN2', '1010'), ('NEWLINE', '\n'), ('SPACE', ' '), ('PATTERN3', ' 001 '), ('SPACE', ' '), ('PATTERN3', ' 001 '), ('SPACE', ' '), ('PATTERN2', '101010'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("11101\n1 0  001 101 ") == [('PATTERN5', '11101'), ('NEWLINE', '\n'), ('PATTERN1', '1 0'), ('SPACE', ' '), ('PATTERN3', ' 001 '), ('PATTERN4', '101 ')])
        self.assertTrue(lexer.lex("1010\n1 01111101\n 1010 101 101    001 ") == [('PATTERN2', '1010'), ('NEWLINE', '\n'), ('PATTERN1', '1 0'), ('PATTERN5', '1111101'), ('NEWLINE', '\n'), ('SPACE', ' '), ('PATTERN2', '1010'), ('SPACE', ' '), ('PATTERN4', '101 101 '), ('SPACE', ' '), ('SPACE', ' '), ('PATTERN3', ' 001 ')])

        print("lexer split, whitespaces (10p)")

    def test_lexer_abcd_diverse_char(self):
        s = {"SPACE": "' '", "DS": "d+", "ABS": "(ab)+", "ABCORC": "(abc)|c", "APLUSCD": "(a+)cd", "ABD": "abd"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex(" acdaacdabd") == [('SPACE', ' '), ('APLUSCD', 'acd'), ('APLUSCD', 'aacd'), ('ABD', 'abd')])
        self.assertTrue(lexer.lex("abdabc abd ababab ") == [('ABD', 'abd'), ('ABCORC', 'abc'), ('SPACE', ' '), ('ABD', 'abd'), ('SPACE', ' '), ('ABS', 'ababab'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("abababababab ababab c aaacd abd ") == [('ABS', 'abababababab'), ('SPACE', ' '), ('ABS', 'ababab'), ('SPACE', ' '), ('ABCORC', 'c'), ('SPACE', ' '), ('APLUSCD', 'aaacd'), ('SPACE', ' '), ('ABD', 'abd'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("abd c abababab") == [('ABD', 'abd'), ('SPACE', ' '), ('ABCORC', 'c'), ('SPACE', ' '), ('ABS', 'abababab')])
        self.assertTrue(lexer.lex("abababcababdd") == [('ABS', 'ababab'), ('ABCORC', 'c'), ('ABS', 'abab'), ('DS', 'dd')])
        self.assertTrue(lexer.lex("ddddd acd abccdddddd ") == [('DS', 'ddddd'), ('SPACE', ' '), ('APLUSCD', 'acd'), ('SPACE', ' '), ('ABCORC', 'abc'), ('ABCORC', 'c'), ('DS', 'dddddd'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex(" d abab ddabcabcc") == [('SPACE', ' '), ('DS', 'd'), ('SPACE', ' '), ('ABS', 'abab'), ('SPACE', ' '), ('DS', 'dd'), ('ABCORC', 'abc'), ('ABCORC', 'abc'), ('ABCORC', 'c')])
        self.assertTrue(lexer.lex("acdabd aacdc dddd abababc") == [('APLUSCD', 'acd'), ('ABD', 'abd'), ('SPACE', ' '), ('APLUSCD', 'aacd'), ('ABCORC', 'c'), ('SPACE', ' '), ('DS', 'dddd'), ('SPACE', ' '), ('ABS', 'ababab'), ('ABCORC', 'c')])
        self.assertTrue(lexer.lex("caaacdabcaacdcddababd ab abd") == [('ABCORC', 'c'), ('APLUSCD', 'aaacd'), ('ABCORC', 'abc'), ('APLUSCD', 'aacd'), ('ABCORC', 'c'), ('DS', 'dd'), ('ABS', 'abab'), ('DS', 'd'), ('SPACE', ' '), ('ABS', 'ab'), ('SPACE', ' '), ('ABD', 'abd')])
        self.assertTrue(lexer.lex("aacd aacd c abcacddddaacd abccab c") == [('APLUSCD', 'aacd'), ('SPACE', ' '), ('APLUSCD', 'aacd'), ('SPACE', ' '), ('ABCORC', 'c'), ('SPACE', ' '), ('ABCORC', 'abc'), ('APLUSCD', 'acd'), ('DS', 'ddd'), ('APLUSCD', 'aacd'), ('SPACE', ' '), ('ABCORC', 'abc'), ('ABCORC', 'c'), ('ABS', 'ab'), ('SPACE', ' '), ('ABCORC', 'c')])
        
        print("lexer split, abcd diverse (10p)")

    def test_lexer_everything_complex_char(self):
        s = {"SPACE": "' '", "NEWLINE": "'\n'", "PATTERN1": "((b+|e)(a*|b+))+((e+fd)*|(c+a*)*)", "PATTERN2": "(((db)|d+)*(da)*(dc)*)|((dc)+|(a+|b+))+", "PATTERN3": "((e|(db))+|(e+e(e|f*)))+", "PATTERN4": "(((f*a+)|(a*d+))|((a*|e)daf+))+", "PATTERN5": "(((c|d)|f*)*|((f|a)+|(b|c)+))+"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("babbbaadcabaaabbabdcbdcbdcbbbefdefdefdeeefdeefdeefddabbfcdadbacdcfcdcbcfddba\n") == [('PATTERN2', 'babbbaadcabaaabbabdcbdcbdcbbb'), ('PATTERN1', 'e'), ('PATTERN5', 'fd'), ('PATTERN1', 'e'), ('PATTERN5', 'fd'), ('PATTERN1', 'e'), ('PATTERN5', 'fd'), ('PATTERN1', 'eeefdeefdeefd'), ('PATTERN5', 'dabbfcdadbacdcfcdcbcfddba'), ('NEWLINE', '\n')])
        self.assertTrue(lexer.lex("edaffffaaedaffedaffaedaff acccdbdbdbadfdbcfddccfdcf\ndbdbdbddbdcdcdcdcdcdcdcdc\nedafdaedafedafedafdaaedaf ddedafedafedafaafaedafedaf") == [('PATTERN4', 'edaffffaaedaffedaffaedaff'), ('SPACE', ' '), ('PATTERN5', 'acccdbdbdbadfdbcfddccfdcf'), ('NEWLINE', '\n'), ('PATTERN2', 'dbdbdbddbdcdcdcdcdcdcdcdc'), ('NEWLINE', '\n'), ('PATTERN4', 'edafdaedafedafedafdaaedaf'), ('SPACE', ' '), ('PATTERN4', 'ddedafedafedafaafaedafedaf')])
        self.assertTrue(lexer.lex("eabaacaccaccaaccccccccaac bdcbdcbdcaadcdcbbdcabadcdc eecacaaaccaaacccacacaacca\n") == [('PATTERN1', 'eabaacaccaccaaccccccccaac'), ('SPACE', ' '), ('PATTERN2', 'bdcbdcbdcaadcdcbbdcabadcdc'), ('SPACE', ' '), ('PATTERN1', 'eecacaaaccaaacccacacaacca'), ('NEWLINE', '\n')])
        self.assertTrue(lexer.lex("faacadaabccbccbfcdfdffcda ") == [('PATTERN5', 'faacadaabccbccbfcdfdffcda'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("adcaabdcdcdcdcaababbaadca") == [('PATTERN2', 'adcaabdcdcdcdcaababbaadca')])
        self.assertTrue(lexer.lex("eefeefeeffdbedbedbedbdbee eefdefdeeeeeefdeefdefdeefd ") == [('PATTERN3', 'eefeefeeffdbedbedbedbdbee'), ('SPACE', ' '), ('PATTERN1', 'eefdefdeeeeeefdeefdefdeefd'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("afffccdbaaffddfabaacdcdcb\ncbfafafabdaabdfddfcbccdba\naffadaaaffffafffaadedafda ffaedafaaddaedafdedaffaaa ") == [('PATTERN5', 'afffccdbaaffddfabaacdcdcb'), ('NEWLINE', '\n'), ('PATTERN5', 'cbfafafabdaabdfddfcbccdba'), ('NEWLINE', '\n'), ('PATTERN4', 'affadaaaffffafffaadedafda'), ('SPACE', ' '), ('PATTERN4', 'ffaedafaaddaedafdedaffaaa'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("\needbeeeeeedbeefeeefffdbdb\ndbafcacdcfffdfbdcfbfccdad \nebbbacacacaccaaaacccaaaca") == [('NEWLINE', '\n'), ('PATTERN3', 'eedbeeeeeedbeefeeefffdbdb'), ('NEWLINE', '\n'), ('PATTERN5', 'dbafcacdcfffdfbdcfbfccdad'), ('SPACE', ' '), ('NEWLINE', '\n'), ('PATTERN1', 'ebbbacacacaccaaaacccaaaca')])
        self.assertTrue(lexer.lex("dabadffdccaabcbfbfadacfadbaabaadcabdcadcabbdcbbabdc ") == [('PATTERN5', 'dabadffdccaabcbfbfadacfadbaabaadcabdcadcabbdcbbabdc'), ('SPACE', ' ')])
        self.assertTrue(lexer.lex("edbeedbdbdbeeeffdbeefdbdb aaabaadcadcdcbdcababababdc\nebbeaeeecacacaccacaccaaaa\nbcaaccaaccaaaacaccccaacac\n") == [('PATTERN3', 'edbeedbdbdbeeeffdbeefdbdb'), ('SPACE', ' '), ('PATTERN2', 'aaabaadcadcdcbdcababababdc'), ('NEWLINE', '\n'), ('PATTERN1', 'ebbeaeeecacacaccacaccaaaa'), ('NEWLINE', '\n'), ('PATTERN1', 'bcaaccaaccaaaacaccccaacac'), ('NEWLINE', '\n')])

        
        print("lexer split, exerything complex (15p)")

    def test_lexer_simple_error_parsing_char(self):
        s = {"NEWLINE": "'\n'", "ABC": "a(b+)c"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("a zzzz") == "No viable alternative at character 1, line 0")
        self.assertTrue(lexer.lex("z zzzz") == "No viable alternative at character 0, line 0")
        self.assertTrue(lexer.lex("ab zzzz") == "No viable alternative at character 2, line 0")
        self.assertTrue(lexer.lex("abb zzzz") == "No viable alternative at character 3, line 0")
        self.assertTrue(lexer.lex("abbb zzzz") == "No viable alternative at character 4, line 0")
        self.assertTrue(lexer.lex("a") == "No viable alternative at character EOF, line 0")
        self.assertTrue(lexer.lex("ab") == "No viable alternative at character EOF, line 0")
        self.assertTrue(lexer.lex("abb") == "No viable alternative at character EOF, line 0")
        self.assertTrue(lexer.lex("abbb") == "No viable alternative at character EOF, line 0")
        self.assertTrue(lexer.lex("abbbc\nabc\n\n\nabbbbbc\nabbbbb") == "No viable alternative at character EOF, line 5")
        
        print("lexer split, simple parsing error (5p)")

    def test_lexer_complex_error_parsing_char(self):
        s = {"SPACE": "' '", "ABC": "a(b+)c", "AS": "(a)+", "BCS": "(bc)+", "DORC": "(d|c)+"}

        lexer = Lexer(s)

        self.assertTrue(lexer.lex("abcbcbcaabaad dccbca") == "No viable alternative at character 10, line 0")
        self.assertTrue(lexer.lex("d abdbc ccddabbbc") == "No viable alternative at character 4, line 0")
        self.assertTrue(lexer.lex("e abbbcbcaadc c") == "No viable alternative at character 0, line 0")
        self.assertTrue(lexer.lex("dccbcbcaaaa abbcf") == "No viable alternative at character 16, line 0")
        self.assertTrue(lexer.lex("abbcaaabc dcccabcb") == "No viable alternative at character EOF, line 0")
        self.assertTrue(lexer.lex("babbcbcbc abbbcaabc") == "No viable alternative at character 1, line 0")

        print("lexer split, complex paring error (10p)")

    def test_program(self):
        with open("src/configuration.json") as f:
            s = json.load(f)

        lexer = Lexer(s)
        data = []
        results = []

        for file in sorted(os.listdir("test/prog_tests")):
            with open(os.path.join("test/prog_tests", file), 'r') as f:
                data.append(f.read())

        for d in data:
            results.append(lexer.lex(d))

        results = [[token[0] for token in result] for result in results]

        self.assertTrue(results[0] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'END'])
        self.assertTrue(results[1] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'END'])
        self.assertTrue(results[2] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'IF', 'OPEN_PARANTHESIS', 'VARIABLE', 'EQUAL', 'NUMBER', 'CLOSE_PARANTHESIS', 'THEN', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'PLUS', 'NUMBER', 'ELSE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'FI', 'END'])
        self.assertTrue(results[3] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'IF', 'OPEN_PARANTHESIS', 'VARIABLE', 'PLUS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'THEN', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MINUS', 'VARIABLE', 'ELSE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'FI', 'END'])
        self.assertTrue(results[4] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'WHILE', 'OPEN_PARANTHESIS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'DO', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MINUS', 'NUMBER', 'OD', 'END'])
        self.assertTrue(results[5] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'WHILE', 'OPEN_PARANTHESIS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'DO', 'BEGIN', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MULTIPLY', 'VARIABLE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MINUS', 'NUMBER', 'END', 'OD', 'END'])
        self.assertTrue(results[6] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'WHILE', 'OPEN_PARANTHESIS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'DO', 'BEGIN', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MULTIPLY', 'VARIABLE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'MINUS', 'NUMBER', 'IF', 'OPEN_PARANTHESIS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'THEN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'ELSE', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'PLUS', 'NUMBER', 'FI', 'END', 'OD', 'END'])
        self.assertTrue(results[7] == ['BEGIN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'VARIABLE', 'ASSIGN', 'NUMBER', 'IF', 'OPEN_PARANTHESIS', 'VARIABLE', 'MINUS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'THEN', 'VARIABLE', 'ASSIGN', 'NUMBER', 'ELSE', 'BEGIN', 'WHILE', 'OPEN_PARANTHESIS', 'VARIABLE', 'MINUS', 'VARIABLE', 'GREATER', 'NUMBER', 'CLOSE_PARANTHESIS', 'DO', 'VARIABLE', 'ASSIGN', 'VARIABLE', 'PLUS', 'NUMBER', 'OD', 'VARIABLE', 'ASSIGN', 'MINUS', 'NUMBER', 'END', 'FI', 'END'])

        print("lexer for a real language (20p)")
