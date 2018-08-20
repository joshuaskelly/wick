import io
import unittest

import {{ program.name|snakecase }}


class Test{{ program.name|capitalize }}ReadWrite(unittest.TestCase):
    def setUp(self):
        self.buff = io.BytesIO()

    {% for struct in program.structs %}
    def test_{{ struct.name|snakecase }}(self):
        {%- for property in struct.properties %}
        {{ property.name }} = 0
        {%- endfor %}

        expected = {{ program.name|snakecase }}.{{ struct.name }}(
        {%- for property in struct.properties %}
            {{ property.name }}{{ "," if not loop.last -}}
        {% endfor %}
        )

        {{program.name | snakecase}}.{{struct.name}}.write(self.buff, expected)
        self.buff.seek(0)


        actual = {{ program.name|snakecase }}.{{ struct.name }}.read(self.buff)

        {% for property in struct.properties -%}
        self.assertEqual(expected.{{ property.name }}, actual.{{ property.name }}, '{{ property.name|capitalize }} values should be equal')
        {% endfor %}
    {% endfor %}