# JVM Parser

A Python JVM bytecode parser that reads a simple `.class` file according to the [JVM Specification (SE25)](https://docs.oracle.com/javase/specs/jvms/se25/html/index.html).

## Getting Started

### Prerequisites

- Python 3.10+

### Getting Started

```bash
javac Main.java
python jvm_parser.py
```

### Usage

```python
from jvm_parser import JVMParser

with open("Main.class", "rb") as f:
    parser = JVMParser()
    result = parser.parse(f)
    print(result)
```

### Running Tests

```bash
python -m unittest discover tests
```

## Resources

- [Chapter 4 - The class File Format](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html)
- [Chapter 6 - The JVM Instruction Set](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-6.html)
- [Chapter 2 - JVM Structure](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-2.html)
