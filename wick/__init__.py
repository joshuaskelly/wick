__version__ = '0.6.4'

from . import generators
from . import parser


def generate_project(source, language, outdir, uri='', template=None, filters=None):
    """For the given C struct source code, generate source code to read and
    write that data in the given language. The resulting source code will be
    written to disk at the location specified by outdir.

    Args:
        source: C source text that only contains structs with simple types.

        language: The target language to generate code for.

        outdir: The target directory to write generated files.

        uri: An optional file URI for the source text.

        template: The template to use for code generation. If provided the
            language argument will be ignored.

        filters: An optional path to a Python module file that has a "filters"
            dictionary attribute.
    """

    if template:
        generator = generators.factory.from_template(template, filters)

    else:
        generator = generators.factory.from_language(language)

    return generator.generate_project(parser.parse(uri, source), outdir)
