from . import document


def generate(parse_tree):
    return document.generate_source(parse_tree)
