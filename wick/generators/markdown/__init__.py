import os

from collections import namedtuple

from . import document


Generator = namedtuple('Generator', ['generate', 'generate_project'])


def get_generator(language):
    if language.lower() == 'markdown':
        return Generator(
            generate=generate,
            generate_project=generate_project
        )


def generate(program):
    """Generate Markdown text

    Args:
        program: A Program object to generate text for

    Returns:
        The Markdown text
    """

    return document.generate_source(program)


def generate_project(program, out_directory):
    doc_path = os.path.join(out_directory, f'{program.name}.md')

    with open(doc_path, 'w') as file:
        file.write(generate(program))
