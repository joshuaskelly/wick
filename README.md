# [![wick](.media/logo.svg)](https://github.com/JoshuaSkelly/wick)

# wick

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)]()

wick is a Python command line utility for generating File IO code from C structs.

## Installation

```shell
$ pip install wick
```

## Usage

```shell
$ wick common.h --language=python
```

## What _exactly_ does it do?

Lets say we have binary data that is a sequence of records that are represented by a string name and an integer id. We can create a simple C struct represenation of this data in record.h.

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

We then can run `wick` on record.h:

```shell
$ wick record.h --language=python
```

Which will then emit:

```python
import struct

class Record:
    """Simple Record
    
    Attributes:
        name: Record name
    
        id: Record id.
    """

    format = '<64sB'
    size = struct.calcsize(format)

    slots = (
        'name',
        'id'
    )

    def __init__(self,
                 name,
                 id):
    
        self.name = name
        self.id = id
    

    @classmethod
    def write(cls, file, record):
        record_data = struct.pack(cls.format, 
                                  record.name,
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

# Assuming the file only contains Record objects
with open(path, 'rb') as file:
    recs = [Record(*chunk) for chunk in struct.iter_unpack(Record.format, file.read())]
```

## License
MIT

See the [license](./LICENSE) document for the full text.
