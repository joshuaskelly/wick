#!/usr/bin/env python3

"""Wick

Usage:
    wick <source> <language> [--directory=<dir>]
    wick template <source> <template> [<filters>]
    wick -h | --help
    wick --version

Options:
    -h --help             Show this screen.
    --version             Show version.
    -d --directory=<dir>  Directory to generate project. [default: ./out]
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
    language = arguments['<language>']
    outdir = resolve_path(arguments['--directory'])

    if arguments['template']:
        template = resolve_path(arguments['<template>'])
        template = os.path.abspath(os.path.expanduser(template))

        if os.path.exists(template):
            with open(template) as file:
                template = file.read()

        filters = resolve_path(arguments['<filters>'])
        if not os.path.exists(filters):
            filters = None

        with open(source_file) as file:
            wick.generate_project_from_template(file.read(), outdir, source_file, template, filters=filters)

    else:
        with open(source_file) as file:
            wick.generate_project(file.read(), language, outdir, source_file)

    sys.exit(0)


if __name__ == '__main__':
    main()
