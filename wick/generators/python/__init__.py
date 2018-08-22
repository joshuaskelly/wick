from collections import namedtuple

from jinja2 import Environment, PackageLoader

from . import filters


Generator = namedtuple('Generator', ['generate', 'generate_project'])


def get_generator(language):
    if language.lower() == 'python':
        return Generator(
            generate=get_generator_for_template('fileio.py'),
            generate_project=generate_project
        )

    if language.lower() == 'python-test':
        return Generator(
            generate=get_generator_for_template('test.py'),
            generate_project=generate_project
        )


def get_generator_for_template(template_name):
    """Returns a generate function for the given template name"""

    def generate(program):
        """Generate Python source code

        Args:
            program: A Program object to generate code for

        Returns:
            The Python source text
        """

        env = Environment(
            loader=PackageLoader('wick.generators.python', 'templates')
        )

        env.filters['formatstring'] = filters.format_string
        env.filters['spaces'] = filters.spaces
        env.filters['snakecase'] = filters.snake_case
        env.filters['pascalcase'] = filters.pascal_case
        env.filters['testdata'] = filters.test_data

        template = env.get_template(template_name)

        return template.render(program=program)

    return generate


def generate_project(program, out_directory):
    import os

    test_dir = os.path.join(out_directory, 'tests')
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
        template = env.get_template('fileio.py')
        file.write(template.render(program=program))

    with open(test_path, 'w') as file:
        template = env.get_template('test.py')
        file.write(template.render(program=program))

