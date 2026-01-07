# k3httpmultipart

[![Action-CI](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3httpmultipart/badge/?version=stable)](https://k3httpmultipart.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3httpmultipart)](https://pypi.org/project/k3httpmultipart)

HTTP multipart form data encoder for building multipart/form-data requests.

k3httpmultipart is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

```bash
pip install k3httpmultipart
```

## Quick Start

```python
import os
import k3httpmultipart

# Define form fields
fields = [
    {
        'name': 'text_field',
        'value': 'hello world',
    },
    {
        'name': 'file_field',
        'value': [open('/path/to/file.txt'), os.path.getsize('/path/to/file.txt'), 'file.txt']
    },
]

# Create multipart encoder
multipart = k3httpmultipart.Multipart()

# Get headers with Content-Type and Content-Length
headers = multipart.make_headers(fields)
# {'Content-Type': 'multipart/form-data; boundary=...', 'Content-Length': ...}

# Get body reader (generator)
body_reader = multipart.make_body_reader(fields)

# Read body content
body = ''.join(body_reader)
```

## API Reference

::: k3httpmultipart

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
