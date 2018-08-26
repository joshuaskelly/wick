__version__ = '1.1.0'

import os

from . import generators
from . import parser


def generate_project(source, language, outdir, uri):
    """For the given C struct source code, generate source code to read and
    write that data in the given language. The resulting source code will be
    written to disk at the location specified by outdir.

    Args:
        source: C source text that only contains structs with simple types.

        language: Target language to generate code for.

        outdir: Target directory to write generated files.

        uri: Source text file URI.
    """

    generator = generators.factory.from_language(language)
    _generate_project(source, outdir, uri, generator)


def generate_project_from_template(source, outdir, uri, template, filters=None):
    """For the given C struct source code, generate source code using the given
    template and filters to read and write that data. The resulting source code
    will be written to disk at the location specified by outdir.

    Args:
        source: C source text that only contains structs with simple types.

        outdir: The target directory to write generated files.

        uri: An optional file URI for the source text.

        template: The template to use for code generation. If provided the
            language argument will be ignored.

        filters: An optional path to a Python module file that has a "filters"
            dictionary attribute.
    """
    generator = generators.factory.from_template(template, filters)
    _generate_project(source, outdir, uri, generator)


def _generate_project(source, outdir, uri, generator):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    generator.generate_project(parser.parse(uri, source), outdir)