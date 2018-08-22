#!/usr/bin/env python3

"""Wick

Usage:
    wick <source> [--language=<lang>] [--template=<templ>] [--outdir=<dir>]
    wick -h | --help
    wick --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    --language=<lang>  Desired source code language [default: python]
    --template=<templ> Jinja2 template to use to generate souce. Note: If
                       provided the language option will be ignored.
    --outdir=<dir>     Directory to generate project. [default: './out']
"""

import os
import sys

from docopt import docopt

import wick


def resolve_path(path):
    return os.path.normpath(os.path.abspath(os.path.expanduser(path)))


def main():
    """Main CLI entrypoint"""

    arguments = docopt(__doc__, version=f'wick {wick.__version__}')
    source_file = resolve_path(arguments['<source>'])
    language = arguments['--language']
    template = arguments['--template']
    outdir = resolve_path(arguments['--outdir'])

    if template:
        template = os.path.abspath(os.path.expanduser(template))

        if os.path.exists(template):
            with open(template) as file:
                template = file.read()

    else:
        template = None

    with open(source_file) as file:
        wick.generate_project(file.read(), outdir, uri=source_file, language=language, template=template)

    sys.exit(0)


if __name__ == '__main__':
    main()
