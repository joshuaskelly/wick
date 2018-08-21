import io
import unittest

import {{ program.name|snakecase }}


class Test{{ program.name|capitalize }}ReadWrite(unittest.TestCase):
    def setUp(self):
        self.buff = io.BytesIO()

    {% for struct in program.structs %}
    def test_{{ struct.name|snakecase }}(self):
        {%- for property in struct.members %}
        {{ property.name }} = {% for expanded_property in property.unpack -%}
        0{{ ", " if not loop.last -}}
        {% endfor %}
        {%- endfor %}

        expected = {{ program.name|snakecase }}.{{ struct.name }}(
        {%- for property in struct.members %}
            {{'*' if property.length > 1 and property.type != 'char'}}{{ property.name }}{{ "," if not loop.last -}}
        {% endfor %}
        )

        {{program.name | snakecase}}.{{struct.name}}.write(self.buff, expected)
        self.buff.seek(0)


        actual = {{ program.name|snakecase }}.{{ struct.name }}.read(self.buff)


        {% for property in struct.members -%}
        self.assertEqual(expected.{{ property.name }}, actual.{{ property.name }}, '{{ property.name|capitalize }} values should be equal')
        {% endfor %}
        self.assertEqual(self.buff.read(), b'', 'Buffer should be fully consumed')
    {% endfor %}
if __name__ == '__main__':
    unittest.main()