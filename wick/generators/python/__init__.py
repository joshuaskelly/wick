from collections import namedtuple

from jinja2 import Environment, PackageLoader

from . import filters


Generator = namedtuple('Generator', ['generate_project'])


def is_valid_language(language):
    return language.lower() in ['python']


def get_generator(language):
    if is_valid_language(language):
        return Generator(
            generate_project=generate_project
        )

    if language.lower() == 'python-test':
        return Generator(
            generate_project=generate_project
        )


def generate_project(program, out_directory):
    import os

    test_dir = os.path.join(out_directory, 'tests')
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    module_path = os.path.join(out_directory, f'{program.name}.py')
    test_path = os.path.join(test_dir, f'test_{program.name}.py')

    env = Environment(
        loader=PackageLoader('wick.generators.python', 'templates')
    )

    env.filters['formatstring'] = filters.format_string
    env.filters['spaces'] = filters.spaces
    env.filters['snakecase'] = filters.snake_case
    env.filters['pascalcase'] = filters.pascal_case
    env.filters['testdata'] = filters.test_data

    with open(module_path, 'w') as file:
        template = env.get_template('main.jinja2')
        file.write(template.render(program=program))

    with open(test_path, 'w') as file:
        template = env.get_template('test.jinja2')
        file.write(template.render(program=program))

