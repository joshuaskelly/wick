import unittest

from wick.parser.common import Range
from wick.parser.parser import parse


class TestParser(unittest.TestCase):
    def assertPositionsEqual(self, first, second, msg=None):
        """Fail if the two positions are not equal"""
        self.assertEqual(first.line, second.line, 'Lines should be "equal"')
        self.assertEqual(first.character, second.character, 'Characters should be "equal"')

    def assertRangesEqual(self, first, second, msg=None):
        """Fail if the two ranges are not equal"""
        self.assertPositionsEqual(first.start, second.start, 'Starts should be "equal"')
        self.assertPositionsEqual(first.end, second.end, 'Ends should be "equal"')

    def assertSymbolsEqual(self, first, second, msg=None):
        self.assertEqual(first.type, second.type, 'Types should be "equal"')
        self.assertEqual(first.value, second.value, 'Values should be "equal"')
        self.assertRangesEqual(first.range, second.range, 'Ranges should be "equal"')

    def get_symbol(self, scope, symbol_value):
        matches = [s for s in scope.definitions.values() if s.value == symbol_value]

        return matches[0] if matches else None

    def test_empty_struct(self):
        source_text = 'struct empty;'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'empty')

        self.assertEqual(symbol.value, 'empty', 'Value should be "empty"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNone(symbol.inner_scope, 'Inner scope should be "None"')
        self.assertRangesEqual(symbol.range, Range((0, 7), (0, 12)))

    def test_single_char_member(self):
        source_text = 'struct single { char x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 21), (0, 22)))

    def test_single_signed_char_member(self):
        source_text = 'struct single { signed char x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'signed char', 'Type should be "signed char"')
        self.assertRangesEqual(symbol.range, Range((0, 28), (0, 29)))

    def test_single_unsigned_char_member(self):
        source_text = 'struct single { unsigned char x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'unsigned char', 'Type should be "unsigned "char')
        self.assertRangesEqual(symbol.range, Range((0, 30), (0, 31)))

    def test_single_bool_member(self):
        source_text = 'struct single { bool x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'bool', 'Type should be "bool"')
        self.assertRangesEqual(symbol.range, Range((0, 21), (0, 22)))

    def test_single_short_member(self):
        source_text = 'struct single { short x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'short', 'Type should be "short"')
        self.assertRangesEqual(symbol.range, Range((0, 22), (0, 23)))

    def test_single_unsigned_short_member(self):
        source_text = 'struct single { unsigned short x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'unsigned short', 'Type should be "unsigned "short')
        self.assertRangesEqual(symbol.range, Range((0, 31), (0, 32)))

    def test_single_int_member(self):
        source_text = 'struct single { int x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'int', 'Type should be "int"')
        self.assertRangesEqual(symbol.range, Range((0, 20), (0, 21)))

    def test_single_unsigned_int_member(self):
        source_text = 'struct single { unsigned int x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'unsigned int', 'Type should be "unsigned "int')
        self.assertRangesEqual(symbol.range, Range((0, 29), (0, 30)))

    def test_single_long_long_member(self):
        source_text = 'struct single { long long x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'long long', 'Type should be "long "long')
        self.assertRangesEqual(symbol.range, Range((0, 26), (0, 27)))

    def test_single_unsigned_long_long_member(self):
        source_text = 'struct single { unsigned long long x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'unsigned long long', 'Type should be "unsigned "long long')
        self.assertRangesEqual(symbol.range, Range((0, 35), (0, 36)))

    def test_single_long_member(self):
        source_text = 'struct single { long x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'long', 'Type should be "long"')
        self.assertRangesEqual(symbol.range, Range((0, 21), (0, 22)))

    def test_single_unsigned_long_member(self):
        source_text = 'struct single { unsigned long x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'unsigned long', 'Type should be "unsigned "long')
        self.assertRangesEqual(symbol.range, Range((0, 30), (0, 31)))

    def test_single_float_member(self):
        source_text = 'struct single { float x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'float', 'Type should be "float"')
        self.assertRangesEqual(symbol.range, Range((0, 22), (0, 23)))

    def test_single_double_member(self):
        source_text = 'struct single { double x; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        symbol = self.get_symbol(parse_tree.scope, 'single')
        self.assertEqual(symbol.value, 'single', 'Value should be "single"')
        self.assertEqual(symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'double', 'Type should be "double"')
        self.assertRangesEqual(symbol.range, Range((0, 23), (0, 24)))

    def test_multiple_char_members(self):
        source_text = 'struct multi { char x; char y; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'multi')
        self.assertEqual(struct_symbol.value, 'multi', 'Value should be "multi"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(struct_symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 20), (0, 21)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'y')
        self.assertEqual(symbol.value, 'y', 'Value should be "y"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 28), (0, 29)))

    def test_multiple_comma_separated_char_members(self):
        source_text = 'struct multi { char x, y; };'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'multi')
        self.assertEqual(struct_symbol.value, 'multi', 'Value should be "multi"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(struct_symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 20), (0, 21)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'y')
        self.assertEqual(symbol.value, 'y', 'Value should be "y"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 23), (0, 24)))

    def test_typedef_struct(self):
        source_text = 'typedef struct td { char x; char y; }alias;'
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'td')
        self.assertEqual(struct_symbol.value, 'td', 'Value should be "td"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')

        symbol = self.get_symbol(struct_symbol.inner_scope, 'x')
        self.assertEqual(symbol.value, 'x', 'Value should be "x"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 25), (0, 26)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'y')
        self.assertEqual(symbol.value, 'y', 'Value should be "y"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((0, 33), (0, 34)))

        alias = struct_symbol.alias
        self.assertEqual(alias.value, 'alias', 'Alias value should be "alias"')
        self.assertEqual(alias.type.value, 'struct', 'Type should be "struct"')

    def test_multiple_structs(self):
        source_text = """
struct A {
    int a;
};

struct B {
    long b;
};
"""
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'A')
        self.assertEqual(struct_symbol.value, 'A', 'Value should be "A"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')
        self.assertRangesEqual(struct_symbol.range, Range((1, 7), (1, 8)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'a')
        self.assertEqual(symbol.value, 'a', 'Value should be "a"')
        self.assertEqual(symbol.type.value, 'int', 'Type should be "int"')
        self.assertRangesEqual(symbol.range, Range((2, 8), (2, 9)))

        struct_symbol = self.get_symbol(parse_tree.scope, 'B')
        self.assertEqual(struct_symbol.value, 'B', 'Value should be "B"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')
        self.assertRangesEqual(struct_symbol.range, Range((5, 7), (5, 8)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'b')
        self.assertEqual(symbol.value, 'b', 'Value should be "b"')
        self.assertEqual(symbol.type.value, 'long', 'Type should be "long"')
        self.assertRangesEqual(symbol.range, Range((6, 9), (6, 10)))

    def test_comments(self):
        source_text = """
/* Description of A */
struct A {
    // Description of a
    int a;
    
    // This is a description
    // of b. It is two lines
    char b;
};
"""

        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'A')
        self.assertEqual(struct_symbol.value, 'A', 'Value should be "A"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')
        self.assertRangesEqual(struct_symbol.range, Range((2, 7), (2, 8)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'a')
        self.assertEqual(symbol.value, 'a', 'Value should be "a"')
        self.assertEqual(symbol.type.value, 'int', 'Type should be "int"')
        self.assertRangesEqual(symbol.range, Range((4, 8), (4, 9)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'b')
        self.assertEqual(symbol.value, 'b', 'Value should be "b"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((8, 9), (8, 10)))

        comment = parse_tree.comments[0]
        self.assertEqual(comment.value, '/* Description of A */', 'Comment text should not change')
        self.assertRangesEqual(comment.range, Range((1, 0), (1, 22)))

        comment = parse_tree.comments[1]
        self.assertEqual(comment.value, '// Description of a', 'Comment text should not change')
        self.assertRangesEqual(comment.range, Range((3, 4), (3, 23)))

        comment = parse_tree.comments[2]
        self.assertEqual(comment.value, '// This is a description\n    // of b. It is two lines')
        self.assertRangesEqual(comment.range, Range((6, 4), (7, 28)))

    def test_c_strings(self):
        source_text = """
struct A {
    char name[32];
};"""
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'A')
        self.assertEqual(struct_symbol.value, 'A', 'Value should be "A"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')
        self.assertRangesEqual(struct_symbol.range, Range((1, 7), (1, 8)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'name')
        self.assertEqual(symbol.value, 'name', 'Value should be "name"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((2, 9), (2, 13)))
        self.assertIsNotNone(symbol.dimension, 'Dimension should not be None')
        self.assertEqual(symbol.dimension.value, '32', 'Dimension should be "32"')

    def test_typedef_alias_only(self):
        source_text = """
typedef struct {
    char name[32];
}A;"""
        parse_tree = parse(source_text)

        self.assertFalse(parse_tree.errors, 'Errors during parsing')

        struct_symbol = self.get_symbol(parse_tree.scope, 'A')
        self.assertEqual(struct_symbol.value, 'A', 'Value should be "A"')
        self.assertEqual(struct_symbol.type.value, 'struct', 'Type should be "struct"')
        self.assertIsNotNone(struct_symbol.inner_scope, 'Inner scope should not be None')
        self.assertRangesEqual(struct_symbol.range, Range((3, 1), (3, 2)))

        symbol = self.get_symbol(struct_symbol.inner_scope, 'name')
        self.assertEqual(symbol.value, 'name', 'Value should be "name"')
        self.assertEqual(symbol.type.value, 'char', 'Type should be "char"')
        self.assertRangesEqual(symbol.range, Range((2, 9), (2, 13)))
        self.assertIsNotNone(symbol.dimension, 'Dimension should not be None')
        self.assertEqual(symbol.dimension.value, '32', 'Dimension should be "32"')

    def test_dont_parse_variable_declarations_outside_a_struct(self):
        source_text = """float d;"""
        parse_tree = parse(source_text)

        self.assertEqual(len(parse_tree.errors), 3, 'Three errors should be present')


if __name__ == '__main__':
    unittest.main()
