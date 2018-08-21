from collections import namedtuple

from jinja2 import Environment, Template, PackageLoader


Generator = namedtuple('Generator', ['generate'])


def get_generator(template_string):
    def generate(program):
        return Template(template_string).render(program=program)

    return Generator(generate=generate)
