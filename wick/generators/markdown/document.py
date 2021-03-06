import os

from . import common
from . import elements


class DataMemberTable(elements.Table):
    def __init__(self, members):
        super().__init__(('Offset', 'Size', 'Type', 'Description', 'Notes'))

        total_bytes = sum([p.size for p in members])
        hex_width = max(4, len(hex(total_bytes)))
        current_bytes = 0

        for prop in members:
            offset = common.to_hex(prop.offset, hex_width)
            size = prop.size
            type = common.get_type_string(prop)
            description = prop.name
            note = prop.description

            self.add_entry((
                offset,
                size,
                type,
                description,
                note
            ))

            current_bytes += size


class Document:
    def __init__(self):
        self._elements = []

    def add(self, element):
        self._elements.append(element)

    def __str__(self):
        return '\n'.join([str(e) for e in self._elements])


def generate_section(struct):
    doc = Document()
    doc.add(elements.H2(struct.name))

    if struct.description:
        doc.add(elements.PlainText(struct.description))

    if struct.members:
        doc.add(elements.BlankLine())
        doc.add(DataMemberTable(struct.members))

    return doc


def generate_source(parse_tree):
    doc = Document()

    if parse_tree.uri:
        filename = os.path.basename(parse_tree.uri)
        filename = filename.split('.')[0].capitalize()
        doc.add(elements.H1(filename))
        doc.add(elements.BlankLine())

    for struct in parse_tree.structs:
        doc.add(generate_section(struct))
        doc.add(elements.BlankLine())

    result = str(doc)
    return result
