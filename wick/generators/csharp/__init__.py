from collections import namedtuple

from jinja2 import Environment, PackageLoader

from . import filters


Generator = namedtuple('Generator', ['generate', 'generate_project'])


def get_generator(language):
    if language.lower() in ['csharp', 'c#']:
        return Generator(
            generate=get_generator_for_template('fileio.cs'),
            generate_project=generate_project
        )

    if language.lower() in ['csharp-test', 'c#-test']:
        return Generator(
            generate=get_generator_for_template('test.cs'),
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
            loader=PackageLoader('wick.generators.csharp', 'templates')
        )

        env.filters['pascalcase'] = filters.pascal_case

        template = env.get_template(template_name)

        return template.render(program=program)

    return generate


def generate_project(program, out_directory):
    import os

    module_path = os.path.join(out_directory, f'{filters.pascal_case(program.name)}.cs')

    env = Environment(
        loader=PackageLoader('wick.generators.csharp', 'templates')
    )

    env.filters = {**env.filters, **filters.filters}

    with open(module_path, 'w') as file:
        template = env.get_template('fileio.cs')
        file.write(template.render(program=program))
