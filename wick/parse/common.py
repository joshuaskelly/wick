class Position:
    def __init__(self, line:int, character:int):
        self.line = line
        self.character = character

    def __iter__(self):
        return iter([self.line, self.character])


class Range:
    def __init__(self, start, end):
        self.start = Position(*start)
        self.end = Position(*end)

    def contains(self, position: Position):
        if position.line < self.start.line:
            return False

        elif position.line > self.end.line:
            return False

        elif position.character < self.start.character:
            return False

        elif position.character > self.end.character:
            return False

        return True
