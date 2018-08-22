import re
import unittest

import wick


class TestFormatStrings(unittest.TestCase):
    def test_char(self):
        source = """
struct A {
    char c;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<c'

        self.assertEqual(actual, expected)

    def test_signed_char(self):
        source = """
struct A {
    signed char sc;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<b'

        self.assertEqual(actual, expected)

    def test_unsigned_char(self):
        source = """
struct A {
    unsigned char uc;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<B'

        self.assertEqual(actual, expected)

    def test_short(self):
        source = """
struct A {
    short s;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<h'

        self.assertEqual(actual, expected)

    def test_unsigned_short(self):
        source = """
struct A {
    unsigned short us;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<H'

        self.assertEqual(actual, expected)

    def test_int(self):
        source = """
struct A {
    int i;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<i'

        self.assertEqual(actual, expected)

    def test_unsigned_int(self):
        source = """
struct A {
    unsigned int ui;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<I'

        self.assertEqual(actual, expected)

    def test_long(self):
        source = """
struct A {
    long l;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<l'

        self.assertEqual(actual, expected)

    def test_unsigned_long(self):
        source = """
struct A {
    unsigned long ul;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<L'

        self.assertEqual(actual, expected)

    def test_long_long(self):
        source = """
struct A {
    long long ll;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<q'

        self.assertEqual(actual, expected)

    def test_unsigned_long_long(self):
        source = """
struct A {
    unsigned long long ull;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<Q'

        self.assertEqual(actual, expected)

    def test_float(self):
        source = """
struct A {
    float f;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<f'

        self.assertEqual(actual, expected)

    def test_double(self):
        source = """
struct A {
    double d;
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<d'

        self.assertEqual(actual, expected)

    def test_unsigned_char_array(self):
        source = """
struct A {
    unsigned char uc[4];
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<4B'

        self.assertEqual(actual, expected)

    def test_string(self):
        source = """
struct A {
    char s[32];
};
"""
        source_text = wick.generate(source)
        actual = re.search("format = '(<.*)'", source_text).group(1)
        expected = '<32s'

        self.assertEqual(actual, expected)


class TestArrays(unittest.TestCase):
    def test_char(self):
        source = """
struct A {
    unsigned char c[4];
};
"""
        source_text = wick.generate(source)
        source_text_simple = re.sub('\s+', ' ', source_text)

        # Verify constructor call args
        constructor_pattern = 'def __init__\(self,\s+((?:[\w]+,\s+)*(?:[\w]+))\):'
        actual = re.search(constructor_pattern, source_text_simple).group(1)
        expected = 'c_0, c_1, c_2, c_3'

        self.assertEqual(actual, expected)

        # Verify constructor body
        actual = re.search("self.\w+ = ((?:[\w]+, )*(?:[\w]+))", source_text).group(1)
        expected = 'c_0, c_1, c_2, c_3'

        self.assertEqual(actual, expected)

        # Verify write method unpacks correctly
        struct_pack_pattern = 'struct.pack\(cls.format,\s+(.\w+.\w+)'
        actual = re.search(struct_pack_pattern, source_text_simple).group(1)
        expected = '*a.c'

        self.assertEqual(actual, expected)

    def test_string(self):
        source = """
struct A {
    char c[16];
};
"""
        source_text = wick.generate(source)
        source_text_simple = re.sub('\s+', ' ', source_text)

        # Verify constructor call args
        constructor_pattern = 'def __init__\(self,\s+((?:[\w]+,\s+)*(?:[\w]+))\):'
        actual = re.search(constructor_pattern, source_text_simple).group(1)
        expected = 'c'

        self.assertEqual(actual, expected)

        # Verify constructor body
        actual = re.search("self.(\w)+ = (\w).split\(b'.x00'\)\[0\].decode\('ascii'\) if type\((\w+)\) is bytes else (\w+)", source_text).groups()
        expected = 'c', 'c', 'c', 'c'

        self.assertEqual(actual, expected)

        # Verify write method unpacks correctly
        struct_pack_pattern = 'struct.pack\(cls.format,\s+(\w+.\w+)'
        actual = re.search(struct_pack_pattern, source_text_simple).group(1)
        expected = "a.c"

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
