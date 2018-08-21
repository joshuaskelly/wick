#!/usr/bin/env python3

"""Wick

Usage:
    wick <source> [--language=<lang>] [--template=<templ>]
    wick -h | --help
    wick --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    --language=<lang>  Desired source code language [default: python]
    --template=<templ> Jinja2 template to use to generate souce. Note: If
                       provided the language option will be ignored.
"""

import os
import sys

from docopt import docopt

import wick


def main():
    """Main CLI entrypoint"""

    arguments = docopt(__doc__, version=f'wick {wick.__version__}')
    source_file = os.path.abspath(os.path.expanduser(arguments['<source>']))
    language = arguments['--language']
    template = arguments['--template']

    if template:
        template = os.path.abspath(os.path.expanduser(template))

        if os.path.exists(template):
            with open(template) as file:
                template = file.read()

    else:
        template = None

    with open(source_file) as file:
        result = wick.generate(file.read(), uri=source_file, language=language, template=template)
        print(result)

    sys.exit(0)


if __name__ == '__main__':
    main()
