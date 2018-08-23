import os

from collections import namedtuple

from jinja2 import Environment, Template, PackageLoader


Generator = namedtuple('Generator', ['generate', 'generate_project'])


def get_generator(template_string, filters=None):
    def generate(program):
        return Template(template_string).render(program=program)

    def generate_project(program, out_directory):
        env = Environment()

        if filters:
            import importlib

            module = os.path.basename(filters).split('.')[0]
            spec = importlib.util.spec_from_file_location(module, filters)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            env.filters = {**env.filters, ** module.filters}

        file_path = os.path.join(out_directory, program.name)

        template = env.from_string(template_string)

        with open(file_path, 'w') as file:
            file.write(template.render(program=program))

    return Generator(
        generate=generate,
        generate_project=generate_project
    )
