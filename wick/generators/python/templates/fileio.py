import struct
{% for struct in program.structs %}
class {{ struct.name }}:
    """{{ struct.description|indent }}

    Attributes:
        {%- for property in struct.members %}
        {{ property.name }}: {{ property.description }}{{ '\n' if not loop.last -}}
        {%- endfor %}
    """

    format = '<{{ struct.members|formatstring }}'
    size = struct.calcsize(format)

    __slots__ = (
    {%- for property in struct.members %}
        '{{ property.name -}}'{{ "," if not loop.last -}}
    {% endfor %}
    )

    def __init__(self,
    {%- for property in struct.members %}
    {%- set outerloop = loop %}
    {%- for expanded_property in property.unpack %}
                 {{ expanded_property.name }}{{ ',' if not loop.last or not outerloop.last -}}
    {% endfor %}
    {%- endfor %}):
    {%- for property in struct.members %}
        self.{{ property.name }} = {% for expanded_property in property.unpack %}
            {{- expanded_property.name -}}{% if property.type == 'char' and property.length > 1 %}.split(b'\x00')[0].decode('ascii') if type({{ property.name }}) is bytes else name{% endif %}{{ ', ' if not loop.last -}}
        {% endfor %}
    {%- endfor %}

    @classmethod
    def write(cls, file, {{ struct.name|lower }}):
        {{ struct.name|lower }}_data = struct.pack(cls.format,
        {%- for property in struct.members %}
                            {{ struct.name|spaces }}{{ '*' if property.length > 1 and property.type != 'char' }}{{ struct.name|lower }}.{{ property.name }}{{ ".encode('ascii')" if property.type == 'char' and property.length > 1 }}{{ ',' if not loop.last -}}
        {% endfor %})

        file.write({{ struct.name|lower }}_data)

    @classmethod
    def read(cls, file):
        {{ struct.name|lower }}_data = file.read(cls.size)
        {{ struct.name|lower }}_struct = struct.unpack(cls.format, {{ struct.name|lower }}_data)

        return {{ struct.name }}(*{{ struct.name|lower }}_struct)
{% endfor %}