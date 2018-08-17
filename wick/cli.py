#!/usr/bin/env python3

"""Wick

Usage:
    wick <source> [--language=<lang>]
    wick -h | --help
    wick --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    --language=<lang>  Desired source code language [default: python]
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

    with open(source_file) as file:
        result = wick.generate(file.read(), uri=source_file, language=language)
        print(result)

    sys.exit(0)


if __name__ == '__main__':
    main()