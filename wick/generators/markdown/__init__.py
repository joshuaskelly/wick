import os

from collections import namedtuple

from . import document


Generator = namedtuple('Generator', ['generate_project'])


def is_valid_language(language):
    return language.lower() in ['markdown']


def get_generator(language):
    if is_valid_language(language):
        return Generator(
            generate_project=generate_project
        )


def generate_project(program, out_directory):
    doc_path = os.path.join(out_directory, f'{program.name}.md')

    with open(doc_path, 'w') as file:
        file.write(document.generate_source(program))
