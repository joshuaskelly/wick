import os

from collections import namedtuple

from jinja2 import Environment, Template, PackageLoader


Generator = namedtuple('Generator', ['generate', 'generate_project'])


def get_generator(template_string):
    def generate(program):
        return Template(template_string).render(program=program)

    def generate_project(program, out_directory):
        file_path = os.path.join(out_directory, program.name)

        with open(file_path, 'w') as file:
            file.write(generate(program))

    return Generator(
        generate=generate,
        generate_project=generate_project
    )
