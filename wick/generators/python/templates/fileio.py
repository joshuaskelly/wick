import struct
{% for struct in program.structs %}
class {{ struct.name }}:
    """{{ struct.description|indent }}

    Attributes:
        {%- for property in struct.properties %}
        {{ property.name }}: {{ property.description }}{{ '\n' if not loop.last -}}
        {%- endfor %}
    """

    format = '<{{ struct.properties|formatstring }}'
    size = struct.calcsize(format)

    __slots__ = (
    {%- for property in struct.properties %}
        '{{ property.name -}}'{{ "," if not loop.last -}}
    {% endfor %}
    )

    def __init__(self,
    {%- for property in struct.properties %}
    {%- set outerloop = loop %}
    {%- for expanded_property in property.unpack %}
                 {{ expanded_property.name }}{{ "," if not loop.last or not outerloop.last -}}
    {% endfor %}
    {%- endfor %}):
    {%- for property in struct.properties %}
        self.{{ property.name }} = {% for expanded_property in property.unpack %}
            {{- expanded_property.name -}}{{ ", " if not loop.last -}}
        {% endfor %}
    {%- endfor %}

    @classmethod
    def write(cls, file, {{ struct.name|lower }}):
        {{ struct.name|lower }}_data = struct.pack(cls.format,
        {%- for property in struct.properties %}
                            {{ struct.name|spaces }}{{ '*' if property.length > 1 and property.type != 'char' }}{{ struct.name|lower }}.{{ property.name }}{{ ',' if not loop.last -}}
        {% endfor %})

        file.write({{ struct.name|lower }}_data)

    @classmethod
    def read(cls, file):
        {{ struct.name|lower }}_data = file.read(cls.size)
        {{ struct.name|lower }}_struct = struct.unpack(cls.format, {{ struct.name|lower }}_data)

        return {{ struct.name }}(*{{ struct.name|lower }}_struct)
{% endfor %}