import os

from collections import namedtuple

from jinja2 import Environment


Generator = namedtuple('Generator', ['generate_project'])


def get_generator(template_string, filters=None):
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
        generate_project=generate_project
    )
