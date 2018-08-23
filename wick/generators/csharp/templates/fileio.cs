using System;
using System.IO;
using System.Text;

namespace {{ program.name|pascalcase }} {
    {% for struct in program.structs %}
    {#- Class statement -#}
    // {{ struct.description }}
    public class {{ struct.name|pascalcase }} {
        {#- Class members #}
        {% for property in struct.members -%}
        public {{ property|csharptype }} {{ property.name }};
        {% endfor %}
        public const int Size = {{ struct.size }};

        public {{ struct.name|pascalcase }} (
            {%- for property in struct.members -%}
                {{ property|csharptype }} {{ property.name }}{{ ", " if not loop.last}}
            {%- endfor -%}) {
            {%- for property in struct.members %}
            this.{{ property.name }} = {{ property.name }};
            {%- endfor %}
        }

        public static {{ struct.name|pascalcase }} Read(BinaryReader reader) {
            {#- Read data -#}
            {%- for property in struct.members %}
            {{ property|csharptype }} {{ property.name }} = {{ "" }}
            {%- if property.length == 1 and property.type -%}
            reader.{{- property|readermethod }}();
            {%- endif -%}
            {#- Read arrays -#}
            {%- if property.length > 1 and property.type != 'char' -%}
            new {{ property|csharptype(True) }};
            for (int index = 0; index < {{ property.length }}; index++) {
                {{ property.name }}[index] = reader.{{ property|readermethod }}();
            }
            {%- endif -%}
            {#- Read strings -#}
            {% if property.length > 2 and property.type == 'char' -%}
            Encoding.ASCII.GetString(reader.ReadBytes({{ property.size }})).TrimEnd('\0');
            {%- endif -%}
            {%- endfor %}

            {# Return new Object -#}
            return new {{ struct.name|pascalcase }}(
            {#- Constructor Args -#}
            {%- for property in struct.members -%}
            {{ property.name }}{{ ", " if not loop.last}}
            {%- endfor %});
        }

        public static void Write(BinaryWriter writer, {{ struct.name|pascalcase }} {{ struct.name|lower }}) {
            {% for property in struct.members -%}
            {% if property.type == 'char' and property.length > 1 -%}
            writer.Write(Encoding.ASCII.GetBytes({{ struct.name|lower }}.{{ property.name }}.Substring(0, Math.Min({{ property.length }}, {{ struct.name|lower }}.{{ property.name }}.Length)).PadRight({{ property.length }}, '\0')));
            {#- Write array data -#}
            {%- elif property.length > 1 -%}
            {%- if not loop.first -%}
            {{ '' }}
            {%- endif %}
            for (int index = 0; index < {{ property.length }}; index++) {
                writer.Write({{ struct.name|lower }}.{{ property.name }}[index]);
            }
            {#- Write data -#}
            {% else %}
            writer.Write({{ struct.name|lower }}.{{ property.name }});
            {%- endif %}
            {%- endfor %}
        }
    }

    public static class {{ struct.name|pascalcase }}ReadWriteExtensions {
        public static {{ struct.name|pascalcase }} Read{{ struct.name|pascalcase }}(this BinaryReader reader) {
            return {{ struct.name|pascalcase }}.Read(reader);
        }

        public static void Write(this BinaryWriter writer, {{ struct.name|pascalcase }} {{ struct.name|lower }}) {
            {{ struct.name|pascalcase }}.Write(writer, {{ struct.name|lower }});
        }
    }
    {%- endfor %}
}
