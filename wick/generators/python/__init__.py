from . import prototype


def generate(parse_tree):
    """Generate Python source code

    Args:
        parse_tree: A ParseTree object to generate code for

    Returns:
        The Python source text
    """

    return prototype.generate_source(parse_tree)
