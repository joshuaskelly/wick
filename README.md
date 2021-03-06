# [![wick](https://raw.githubusercontent.com/joshuaskelly/wick/master/.media/logo.svg?sanitize=true)](https://github.com/JoshuaSkelly/wick)

# wick

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)]() [![PyPI version](https://badge.fury.io/py/wick.svg)](https://pypi.python.org/pypi/wick) [![Build Status](https://travis-ci.org/joshuaskelly/twitch-observer.svg?branch=master)](https://travis-ci.org/joshuaskelly/twitch-observer)

wick is a Python command line tool that automatically generates file I/O source code for working with binary data.

## Why?
I was working on a project that involved reverse engineering file formats and I found that most data structures tend to be composed of several simpler data structures. I also noticed that the simpler structures were all very boilerplate. So I created this tool to write the simple structures for me, and I can do the more interesting work of composing them into the larger structure.

## Supported Target Languages
- C#
- JavaScript
- Python

## Installation

```shell
$ pip install wick
```

## Usage

```shell
$ wick example.h Python
```

## What _exactly_ does it do?

Let's walk through a concrete example.

Say we have binary data that is a sequence of records that are represented by a string name and an integer id. First we create a record.h file that contains a C struct representation of this data:

```C
// record.h

// Simple Record
struct Record {
    // Record name
    char name[64];

    // Record id.
    unsigned char id;
};
```

Then we run `wick` on the file:

```shell
$ wick record.h Python
```

Which will then create a record.py file whose contents look like:

```python
# record.py
import struct


class Record:
    """Simple Record object

    Attributes:
        name: Record name

        id: Record id.
    """

    format = '<64sB'
    size = struct.calcsize(format)

    __slots__ = (
        'name',
        'id'
    )

    def __init__(self,
                 name,
                 id):
        self.name = name.split(b'\x00')[0].decode('ascii') if type(name) is bytes else name
        self.id = id

    @classmethod
    def write(cls, file, record):
        record_data = struct.pack(cls.format,
                                  record.name.encode('ascii'),
                                  record.id)

        file.write(record_data)

    @classmethod
    def read(cls, file):
        record_data = file.read(cls.size)
        record_struct = struct.unpack(cls.format, record_data)

        return Record(*record_struct)

```

Then we can import this code into Python and _do work_.

### Read Data
```python
with open(path, 'rb') as file:
    rec = Record.read(file)
```

### Write Data
```python
with open(path, 'wb') as file:
    rec = Record(b'name', 0)
    Record.write(file, rec)
```

### Unpack Lots of Data
```python
import struct

# Assuming the file only contains Record data
with open(path, 'rb') as file:
    recs = [Record(*chunk) for chunk in struct.iter_unpack(Record.format, file.read())]
```

## Contributing
Have a bug fix or a new feature you'd like to see in wick? Send it our way! Please make sure you create an issue that addresses your fix/feature so we can discuss the contribution.

1. Fork this repo!
2. Create your feature branch: `git checkout -b features/add-javascript-code-generator`
3. Commit your changes: `git commit -m 'Implemented Javascript code generator'`
4. Push the branch: `git push origin add-javascript-code-generator`
5. Submit a pull request.
6. Create an [issue](https://github.com/joshuaskelly/wick/issues/new).

## License
MIT

See the [license](./LICENSE) document for the full text.
