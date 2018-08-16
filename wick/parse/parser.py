import copy

from collections import namedtuple
from types import MethodType
from typing import Callable, List, Union

from .common import Range
from .lexer import new_lexer

lexer = None


class Context:
    token = None
    symbol_table = {}
    scope = None
    symbols = []
    errors = []
    comments = []


Diagnostic = namedtuple('Diagnostic', ['range', 'severity', 'message'])
Program = namedtuple('Program', ['ast', 'scope', 'symbols', 'errors', 'comments'])


class Object:
    @staticmethod
    def create(prototype):
        """Creates a new object from the given prototype"""

        return copy.deepcopy(prototype)


class Symbol:
    def __init__(self):
        self.reserved = False
        self.arity = ''
        self.scope = None
        self.value = ''
        self.range = Range((-1, -1), (-1, -1))

    def nud(self) -> 'Symbol':
        """Null denotation parse.

        Does not care about symbols to the left. Used for parsing literals
        variables and prefix operators.
        """

        self.error('Undefined')

    def led(self, left: 'Symbol') -> 'Symbol':
        """Left denotation parse.

        Used for parsing infix and suffix operators.

        Args:
            left: The Symbol to the left
        """

        self.error('Missing operator')

    def error(self, message: str, range: Range=None):
        """Reports an error

        Args:
            message: The message to report

            range: The associated range
        """

        self._diagnostic(message, 1, range)

    def warn(self, message: str, range: Range=None):
        """Reports a warning

        Args:
            message: The message to report

            range: The associated range
        """

        self._diagnostic(message, 2, range)

    def _diagnostic(self, message: str, severity: int=4, range: Range=None):
        """Report diagnostic info

        Args:
            message: The message to report

            severity: The severity of the diagnostic. Lower is more severe.

            range: The associated range
        """

        range = range or self.range

        Context.errors.append(Diagnostic(
            range,
            severity,
            message
        ))


MaybeSymbol = Union[Symbol,None]


class Scope:
    def __init__(self, parent_scope: 'Scope'=None):
        self.definitions = {}
        self.parent = Context.scope or parent_scope
        Context.scope = self

    def define(self, symbol: Symbol, type: Symbol) -> Symbol:
        """Defines the given symbol in the current scope.

        Transforms a name token into a variable token.

        Args:
            symbol: The Symbol to define.

            type: The type of the Symbol. This is also a Symbol.

        Returns:
            A Symbol
        """

        s = self.definitions.get(symbol.value)

        if s:
            symbol.warn(f'Already defined: {symbol.value}')

        else:
            self.definitions[symbol.value] = symbol

        symbol.reserved = False
        symbol.nud = MethodType(itself, symbol)
        symbol.led = None
        symbol.std = None
        symbol.lbp = 0
        symbol.scope = Context.scope
        symbol.type = type

        return symbol

    def find(self, symbol: Symbol) -> Symbol:
        """Finds the definition of a name

        Args:
            symbol: The Symbol to find

        Returns:
            A Symbol
        """

        current_scope = self

        while True:
            p = current_scope.definitions.get(symbol)

            if p:
                return current_scope.definitions.get(symbol)

            current_scope = current_scope.parent

            if not current_scope:
                p = Context.symbol_table.get(symbol)

                if p:
                    return p

                return Context.symbol_table.get('(name)')

    def push(self, scope: 'Scope'):
        """Opens a Scope and sets the given scope as the Context.scope.

        This will not change the parent of the given scope.

        Args:
            scope: The Scope to push
        """

        if scope.parent != Context.scope:
            raise Exception('Bad scope pushed')

        Context.scope = scope

    def pop(self):
        """Closes a Scope and sets Context.scope to Context.scope.parent."""
        Context.scope = self.parent

    def reserve(self, symbol: Symbol):
        """Indicate that the given symbol is a reserved word.

        Args:
            symbol: The Symbol to reserve
        """

        d = self.definitions.get(symbol.value)

        if d:
            if d.reserved:
                return

            if d.arity == 'name':
                symbol.error('Already defined')

        self.definitions[symbol.value] = symbol
        symbol.reserved = True

    def is_global(self) -> bool:
        """Determine if this is the global scope

        Returns:
            True if self is the global scope
        """

        return self.parent is None


class Define:
    """Namespace for defining language constructs"""

    @staticmethod
    def symbol(id: str, bp: int=0) -> Symbol:
        """Defines a symbol with the given id and left binding power.

        Args:
            id: Symbol id

            bp: Left binding power

        Returns:
            A Symbol
        """

        s = Context.symbol_table.get(id)

        if s:
            if bp >= s.lbp:
                s.lbp = bp

        else:
            class C(Symbol):
                pass

            C.__qualname__ = f'{id.capitalize()}Symbol'
            C.__name__ = C.__qualname__

            s = C()
            s.id = id
            s.value = id
            s.lbp = bp
            Context.symbol_table[id] = s

        return s

    @staticmethod
    def infix(id: str, bp: int, led: Callable[[Symbol], Symbol]=None) -> Symbol:
        """Defines an infix operator.

        Args:
            id: Symbol id

            bp: Left binding power

            led: Left denotation parsing function

        Returns:
            A Symbol
        """

        symbol = Define.symbol(id, bp)

        if not led:
            def led(self, left):
                self.first = left
                self.second = Parse.expression(bp)
                self.arity = 'binary'

                return self

            symbol.led = MethodType(led, symbol)

        else:
            symbol.led = MethodType(led, symbol)

        return symbol

    @staticmethod
    def infixr(id: str, bp: int, led: Callable[[Symbol], Symbol]=None) -> Symbol:
        """Defines a right-associative infix operator.

        Args:
            id: Symbol id

            bp: Left binding power

            led: Left denotation parsing function

        Return:
            A Symbol
        """

        symbol = Define.symbol(id, bp)

        if not led:
            def led(self, left):
                self.first = left
                self.second = Parse.expression(bp - 1)
                self.arity = 'binary'

                return self

            symbol.led = MethodType(led, symbol)

        else:
            symbol.led = MethodType(led, symbol)

        return symbol

    @staticmethod
    def prefix(id: str, nud: Callable[[], Symbol]=None) -> Symbol:
        """Defines a prefix operator.

        Args:
            id: Symbol id

            nud: Null denotation parsing function

        Returns:
            A Symbol
        """

        symbol = Define.symbol(id)

        if not nud:
            def nud(self):
                Context.scope.reserve(self)
                self.first = Parse.expression(70)
                self.arity = 'unary'

                return self

            symbol.nud = MethodType(nud, symbol)

        else:
            symbol.nud = MethodType(nud, symbol)

        return symbol

    @staticmethod
    def assignment(id: str) -> Symbol:
        """Defines an assignment expression.

        Args:
            id: Symbol id

        Returns:
            A Symbol
        """

        def led(self, left):
            self.first = left
            self.second = Parse.expression(9)
            self.assignment = True
            self.arity = 'binary'

            return self

        return Define.infix(id, 10, led)

    @staticmethod
    def statement(id: str, std: Callable[[], Symbol]) -> MaybeSymbol:
        """Defines a statement.

        Args:
            id: Symbol id

            std: Statement denotation parse
        """

        symbol = Define.symbol(id)
        symbol.std = MethodType(std, symbol)

        return symbol


class Parse:
    """Namespace for parsing language constructs"""

    @staticmethod
    def advance(id: str=None) -> Symbol:
        """Create a new Symbol from the token stream.

        This new symbol will also be set as Context.token. An optional token id
        can be provided to verify the id of the current token.

        Args:
            id: Expected id of current token. Will report an error on mismatch.

        Returns:
            A Symbol
        """

        global lexer

        if id and Context.token.id != id:
            Context.token.error(f'Expected: "{id}" Actual: "{Context.token.id}"')

        next_token = lexer.lex()

        if not next_token:
            Context.token = Context.symbol_table.get('(end)')
            Context.token.range = Range((-1, -1), (-1, -1))

            return Context.token

        value = next_token.value
        arity = next_token.type

        if arity == 'name':
            prototype_object = Context.scope.find(value)

        elif arity == 'operator':
            prototype_object = Context.symbol_table.get(value)

            if not prototype_object:
                next_token.error(f'Unknown operator: "{value}"')

        elif arity == 'number':
            ff = Context.symbol_table.get(arity)

            arity = 'literal'
            prototype_object = Context.symbol_table.get('(literal)')

            if ff:
                prototype_object.type = ff

        elif arity == 'type':
            arity = 'type'
            prototype_object = Context.scope.find(value)

        elif arity == 'comment':
            Context.comments.append(next_token)
            return Parse.advance(id)

        else:
            next_token.error(f'Unexpected token: "{next_token.id}"')

        Context.token = Object.create(prototype_object)
        Context.token.value = value
        Context.token.arity = arity
        Context.token.range = next_token.range

        if not Context.token.scope and Context.token.arity == 'name':
            Context.token.scope = Context.scope

        if Context.token.scope and Context.token.scope != Context.scope:
            Context.token.scope = Context.scope

        Context.symbols.append(Context.token)

        return Context.token

    @staticmethod
    def expression(rbp: int) -> Symbol:
        """Parses an expression.

        Args:
            rbp: Right binding power

        Returns:
            A Symbol
        """

        current_token = Context.token
        Parse.advance()
        left = current_token.nud()

        while rbp < Context.token.lbp:
            current_token = Context.token
            Parse.advance()
            left = current_token.led(left)

        return left

    @staticmethod
    def statement() -> MaybeSymbol:
        """Parses a statement.

        Returns:
            A Symbol
        """
        current_token = Context.token

        if hasattr(current_token, 'std'):
            Parse.advance()
            Context.scope.reserve(current_token)

            return current_token.std()

        expression = Parse.expression(0)

        if not expression:
            current_token.error('Bad expression statement.')

        return None

    @staticmethod
    def statements() -> List[Symbol]:
        """Parses a sequence of statements.

        Returns:
            Symbol
        """
        parsed_statements = []

        while True:
            if Context.token.id == '}' or Context.token.id == '(end)':
                break

            statement = Parse.statement()

            if statement:
                parsed_statements.append(statement)

        return parsed_statements

    @staticmethod
    def block() -> Symbol:
        current_token = Context.token
        Parse.advance('{')

        return current_token.std()


def itself(self: Symbol) -> Symbol:
    return self


Define.symbol(',')
Define.symbol(';')
Define.symbol("{")
Define.symbol("}")
Define.symbol("[")
Define.symbol("]")

Define.symbol('(end)')
s = Define.symbol('(literal)')
s.nud = MethodType(itself, s)
s = Define.symbol('(type)')
s.nud = MethodType(itself, s)
s = Define.symbol('(name)')
s.nud = MethodType(itself, s)


def variable_std(self: Symbol):
    """Variable declaration statement denotation parse."""

    while True:
        # Ignore variables defined outside of a struct
        if Context.scope.is_global():
            return None

        current_token = Context.token

        if current_token.arity != 'name':
            current_token.error('Expected a new variable name')

        Context.scope.define(current_token, self)
        Parse.advance()

        if Context.token.id == '[':
            Parse.advance('[')
            exp = Parse.expression(0)
            Parse.advance(']')
            current_token.dimension = exp

        if Context.token.id != ',':
            break

        Parse.advance(',')
    Parse.advance(';')

    return None


Define.statement('char', variable_std)
Define.statement('unsigned char', variable_std)
Define.statement('bool', variable_std)
Define.statement('short', variable_std)
Define.statement('unsigned short', variable_std)
Define.statement('int', variable_std)
Define.statement('unsigned int', variable_std)
Define.statement('long long', variable_std)
Define.statement('unsigned long long', variable_std)
Define.statement('long', variable_std)
Define.statement('unsigned long', variable_std)
Define.statement('float', variable_std)
Define.statement('double', variable_std)


def struct_std(self: Symbol):
    """Struct statement denotation parse"""

    current_token = Context.token
    name_token = None

    if current_token.arity == 'name':
        Context.scope.define(current_token, self)
        name_token = current_token
        Parse.advance()

    if Context.token.id == ';':
        Parse.advance(';')
        current_token.inner_scope = None
        return None

    Parse.advance('{')

    Scope()
    Parse.statements()
    inner_scope = Context.scope
    Parse.advance('}')
    Context.scope.pop()

    # Handle typedef aliases
    if Context.token.arity == 'name':
        Context.scope.define(Context.token, self)

        if name_token:
            current_token.alias = Context.token
            Context.token.is_alias = True
        else:
            name_token = Context.token

        Parse.advance()

    name_token.inner_scope = inner_scope
    Parse.advance(';')

    return None


Define.statement('struct', struct_std)


def parse(source_text: str) -> Program:
    """Parses the given source text.

    Returns:
        A Program
    """

    global lexer
    lexer = new_lexer(source_text)

    Context.token = None
    Context.symbol_table = Object.create(Context.symbol_table)
    Context.symbols = []
    Context.errors = []
    Context.scope = Scope()

    Parse.advance()
    ast = Parse.statements()
    scope = Context.scope

    return Program(ast, scope, Context.symbols, Context.errors, Context.comments)
