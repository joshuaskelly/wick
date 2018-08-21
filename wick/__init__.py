__version__ = '0.6.1'

from . import generators
from . import parser


def generate(source, uri='', language='python', template=None):
    """For the given C struct source code, generate source code to read and
    write that data in the given languge.

    Args:
        source: C source text that only contains structs with simple types.

        uri: An optional file URI for the source text.

        language: The desired language to generate code for.

        template: The template to use for code generation. If provided the
            language argument will be ignored.

    Returns:
        The generated source text
    """

    if template:
        generator = generators.factory.from_template(template)

    else:
        generator = generators.factory.from_language(language)

    return generator.generate(parser.parse(uri, source))
