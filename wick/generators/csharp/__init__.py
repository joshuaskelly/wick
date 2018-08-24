from collections import namedtuple

from jinja2 import Environment, PackageLoader

from . import filters


Generator = namedtuple('Generator', ['generate_project'])


def is_valid_language(language):
    return language.lower() in ['csharp', 'c#']


def get_generator(language):
    if is_valid_language(language):
        return Generator(
            generate_project=generate_project
        )


def generate_project(program, out_directory):
    import os

    module_path = os.path.join(out_directory, f'{filters.pascal_case(program.name)}.cs')

    env = Environment(
        loader=PackageLoader('wick.generators.csharp', 'templates')
    )

    env.filters = {**env.filters, **filters.filters}

    with open(module_path, 'w') as file:
        template = env.get_template('main.jinja2')
        file.write(template.render(program=program))
