import unittest

from wick.parse.lexer import Lexer, LexError, new_lexer


class TestLexer(unittest.TestCase):
    def test_basic(self):
        program = 'aba'
        a_matches = 0

        def increment_a(a):
            nonlocal a_matches
            a_matches += 1

            return a

        lexer = Lexer(program)
        lexer.add_rule('a', lambda m: increment_a(m))
        lexer.add_rule('b', lambda m: m)

        self.assertEqual(a_matches, 0, 'There should be no "a" matches')
        result = lexer.lex()
        self.assertEqual(result, 'a', 'The match should be "a"')
        self.assertEqual(a_matches, 1, 'There should be one "a" matches')
        result = lexer.lex()
        self.assertEqual(result, 'b', 'The match should be "b"')
        self.assertEqual(a_matches, 1, 'There should be one "a" matches')
        result = lexer.lex()
        self.assertEqual(result, 'a', 'The match should be "a"')
        self.assertEqual(a_matches, 2, 'There should be two "a" matches')
        result = lexer.lex()
        self.assertIsNone(result, 'Lex should yield None when finished')
        result = lexer.lex()
        self.assertIsNone(result, 'Lex should yield None when finished')

    def test_raises_on_add_after_lex(self):
        program = 'abbaa'

        lexer = Lexer(program)
        lexer.add_rule('a', lambda m: m)
        lexer.lex()

        with self.assertRaises(LexError):
            lexer.add_rule('b', lambda m: m)

    def test_raises_on_lex_with_no_rules(self):
        program = 'aabb'

        lexer = Lexer(program)

        with self.assertRaises(LexError):
            lexer.lex()

    def test_single_line_comment(self):
        program = '// Single line comment.'
        lexer = new_lexer(program)
        token = lexer.lex()

        self.assertIsNotNone(token, 'Token should not be None')
        self.assertEqual(token.type, 'comment', 'The type should be comment')
        self.assertEqual(token.value, '// Single line comment.', 'Value should be "// Single line comment."')

    def test_multi_line_comment(self):
        program = """/*
 * Multi-line comment
 */"""
        lexer = new_lexer(program)
        token = lexer.lex()

        self.assertIsNotNone(token, 'Token should not be None')
        self.assertEqual(token.type, 'comment', 'The type should be comment')
        self.assertEqual(token.value, program, 'Value should be equal')

    def test_numbers(self):
        program = '0 12345'
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.type, 'number', 'Type should be "number"')
        self.assertEqual(token.value, '0', 'Value should be 0')
        token = lexer.lex()
        self.assertEqual(token.type, 'number', 'Type should be "number"')
        self.assertEqual(token.value, '12345', 'Value should be 12345')

    def test_type(self):
        program = 'char unsigned char bool short unsigned short int unsigned int long unsigned long float long long unsigned long long double'
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'char', 'Value should be "char"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'unsigned char', 'Value should be "unsigned char"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'bool', 'Value should be "bool"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'short', 'Value should be "short"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'unsigned short', 'Value should be "unsigned short"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'int', 'Value should be "int"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'unsigned int', 'Value should be "unsigned int"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'long', 'Value should be "long"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'unsigned long', 'Value should be "unsigned long"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'float', 'Value should be "float"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'long long', 'Value should be "long long"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'unsigned long long', 'Value should be "unsigned long long"')

        token = lexer.lex()
        self.assertEqual(token.type, 'type', 'Type should be type')
        self.assertEqual(token.value, 'double', 'Value should be "double"')

        token = lexer.lex()
        self.assertIsNone(token, 'Value should be None')

    def test_verify_whitespace_skip(self):
        program = """ 1
2
"""
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.value, '1', 'Value should be "1"')
        token = lexer.lex()
        self.assertEqual(token.value, '2', 'Value should be "2"')

    def test_names(self):
        program = 'int flag'
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.value, 'int', 'Value should be "int"')
        token = lexer.lex()
        self.assertEqual(token.type, 'name', 'Type should be "name"')
        self.assertEqual(token.value, 'flag', 'Value should be "flag"')

    def test_operators(self):
        program = '{ } [ ] ; ,'
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, '{', 'Value should be "{"')
        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, '}', 'Value should be "}"')
        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, '[', 'Value should be "["')
        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, ']', 'Value should be "]"')
        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, ';', 'Value should be ";"')
        token = lexer.lex()
        self.assertEqual(token.type, 'operator', 'Type should be "operator"')
        self.assertEqual(token.value, ',', 'Value should be ","')
        token = lexer.lex()
        self.assertIsNone(token, 'Value should be None')

    def test_struct(self):
        program = """
struct foo {
    int x;
};
"""
        lexer = new_lexer(program)

        token = lexer.lex()
        self.assertEqual(token.value, 'struct', 'Value should be "struct"')
        token = lexer.lex()
        self.assertEqual(token.value, 'foo', 'Value should be "foo"')
        token = lexer.lex()
        self.assertEqual(token.value, '{', 'Value should be "{"')
        token = lexer.lex()
        self.assertEqual(token.value, 'int', 'Value should be "int"')
        token = lexer.lex()
        self.assertEqual(token.value, 'x', 'Value should be "x"')
        token = lexer.lex()
        self.assertEqual(token.value, ';', 'Value should be ";"')
        token = lexer.lex()
        self.assertEqual(token.value, '}', 'Value should be "}"')
        token = lexer.lex()
        self.assertEqual(token.value, ';', 'Value should be ";"')
        token = lexer.lex()
        self.assertIsNone(token, 'Value should be None')


if __name__ == '__main__':
    unittest.main()
