from . import document


def generate(parse_tree):
    """Generate Markdown text

    Args:
        parse_tree: A ParseTree object to generate text for

    Returns:
        The Markdown text
    """

    return document.generate_source(parse_tree)
