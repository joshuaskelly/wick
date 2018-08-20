from collections import namedtuple

from jinja2 import Environment, PackageLoader

from . import filters


Generator = namedtuple('Generator', ['generate'])


def get_generator(language):
    if language.lower() == 'python':
        return Generator(generate=get_generator_for_template('fileio.py'))

    if language.lower() == 'python-test':
        return Generator(generate=get_generator_for_template('test.py'))


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

        template = env.get_template(template_name)

        return template.render(program=program)

    return generate

