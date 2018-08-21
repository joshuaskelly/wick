import re

from collections import namedtuple
from typing import Any, Callable, Union

from .common import Position, Range


class LexError(Exception):
    pass


Rule = namedtuple('Rule', ['regex', 'callback'])
Token = namedtuple('Token', ['type', 'value', 'range'])


class Lexer:
    """A generic lexer

    Example:
        >>> l = Lexer('aab')
        >>> l.add_rule('a', lambda x: x.upper())
        >>> l.add_rule('b', lambda x: x.upper())
        >>> l.lex()
        'A'
        >>> l.lex()
        'A'
        >>> l.lex()
        'B'
        >>> l.lex()
        None
    """

    def __init__(self, program: str):
        self._program = program
        self._rules = []
        self._lexing = False

    def add_rule(self, regex: str, callback: Callable[[str], Any]):
        """Adds a rule for lexing.

        Args:
            regex: The regular expression string describing the desired lexeme

            callback: A function that processes the matched lexeme text
        """
        if self._lexing:
            raise LexError('Unable to add rules during lexing')

        # Sanitize regex. Make capturing groups non-capturing.
        regex = re.sub('\((?!\?:)', '(?:', regex)

        self._rules.append(Rule(f'({regex})', callback))

    def lex(self) -> Union[Any, None]:
        """Get the next lexeme result.

        Multiple lexemes might be processed until a result is yielded.

        Returns:
            The result of the given callback for the matching lexeme.
            None if the entire source text has been processed.
        """
        try:
            return next(self._generator)

        except AttributeError:
            self._lexing = True

            if not self._rules:
                raise LexError('Cannot lex without rules')

            def generator():
                pattern = re.compile('|'.join([r.regex for r in self._rules]))

                for matches in pattern.findall(self._program):
                    matches = (matches,) if not type(matches) == tuple else matches
                    match, rule = [pair for pair in zip(matches, self._rules) if pair[0]][0]

                    result = rule.callback(match)
                    if result:
                        yield result

                while True:
                    yield None

            self._generator = generator()

        return next(self._generator)


line = 0
character = 0
last_position = Position(line, character)
current_position = Position(line, character)


def update_position(string):
    """Updates the current position of the Lexer.

    Args:
        string: The match string being processed
    """
    global line, character, last_position, current_position
    last_position = Position(line, character)

    for c in string:
        if c == '\n':
            line += 1
            character = 0
        else:
            character += 1

    current_position = Position(line, character)


def process_lexeme(type: str=None) -> Callable[[str], Union[Token, None]]:
    """Construct a function for processing the given type

    Args:
        type: The type of the matched lexeme. If omitted the inner function
            will not return a Token.

    Returns:
        A function
    """

    def callback(lexeme: str) -> Union[Token, None]:
        """Process the given lexeme.

        Args:
            lexeme: The matched lexeme text

        Returns:
            A Token if type was provided by the outer function, otherwise None.
        """
        update_position(lexeme)

        if type:
            range = Range(last_position, current_position)
            return Token(type, lexeme, range)

    return callback


def new_lexer(program: str) -> Lexer:
    """Constructs a Lexer suitable for processing C style structs.

    Args:
        program: The source text

    Returns:
        A Lexer
    """

    global line, character, last_position, current_position
    line = 0
    character = 0
    last_position = Position(line, character)
    current_position = Position(line, character)

    lexer = Lexer(program)

    # Comments
    lexer.add_rule('\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*\/', process_lexeme('comment'))
    #lexer.add_rule('\/\/.*', process_lexeme('comment'))
    lexer.add_rule('\/\/.*(\n\s*\/\/.*)*', process_lexeme('comment'))

    # Literals
    lexer.add_rule('[0-9]+', process_lexeme('number'))

    # Types
    lexer.add_rule('\\b(char|signed char|unsigned char|bool|short|unsigned short|int|unsigned int|long long|unsigned long long|long|unsigned long|float|double)\\b', process_lexeme('type'))

    # Names
    lexer.add_rule('[A-Za-z_]+[A-Za-z0-9_]*', process_lexeme('name'))

    # Operators
    lexer.add_rule('(\[|\]|\{|\}|;|,)', process_lexeme('operator'))

    # Whitespace
    lexer.add_rule('[\s]+', process_lexeme())

    # Everything else. This is for keeping correct positioning.
    lexer.add_rule('.', process_lexeme())

    return lexer
