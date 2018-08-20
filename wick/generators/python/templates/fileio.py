import struct
{% for struct in program.structs %}
class {{ struct.name }}:
    """{{ struct.description|indent }}"""

    format = '<{{ struct.properties|formatstring }}'
    size = struct.calcsize(format)

    __slots__ = (
    {%- for property in struct.properties %}
        '{{ property.name -}}'{{ "," if not loop.last -}}
    {% endfor %}
    )

    def __init__(self,
    {%- for property in struct.properties %}
                 {{ property.name }}{{ "," if not loop.last -}}
    {% endfor %}):
    {%- for property in struct.properties %}
        self.{{ property.name }} = {{ property.name -}}
    {% endfor %}

    @classmethod
    def write(cls, file, {{ struct.name|lower }}):
        {{ struct.name|lower }}_data = struct.pack(cls.format,
        {%- for property in struct.properties %}
                            {{ struct.name|spaces }}{{ struct.name|lower }}.{{ property.name }}{{ "," if not loop.last -}}
        {% endfor %})

        file.write({{ struct.name|lower }}_data)

    @classmethod
    def read(cls, file):
        {{ struct.name|lower }}_data = file.read(cls.size)
        {{ struct.name|lower }}_struct = struct.unpack(cls.format, {{ struct.name|lower }}_data)

        return {{ struct.name }}(*{{ struct.name|lower }}_struct)
{% endfor %}