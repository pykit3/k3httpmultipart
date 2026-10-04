# k3httpmultipart

[![Action-CI](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3httpmultipart/badge/?version=stable)](https://k3httpmultipart.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3httpmultipart)](https://pypi.org/project/k3httpmultipart)

This module provides some util methods to get multipart headers and body.

k3httpmultipart is a component of [pykit3] project: a python3 toolkit set.




# Install

```
pip install k3httpmultipart
```

# Synopsis

```python
import os

import k3fs

import k3httpmultipart

# http request headers
headers = {"Content-Length": 1200}

# http request fields
file_path = "/tmp/abc.txt"
k3fs.fwrite(file_path, "123456789")
with open(file_path) as f:
    fields = [
        {
            "name": "aaa",
            "value": "abcde",
        },
        {"name": "bbb", "value": [f, os.path.getsize(file_path), "abc.txt"]},
    ]

    # get http request headers
    multipart = k3httpmultipart.Multipart()
    res_headers = multipart.make_headers(fields, headers=headers)

    print(res_headers)

    # output:
    # {
    #    'Content-Length': 1200,
    #    'Content-Type': 'multipart/form-data; boundary=75d42525e65d4cf3ba7e1fdbc9ec9787',
    # }

    # get http request body reader, from the same object so that the body
    # uses the boundary in the headers
    body_reader = multipart.make_body_reader(fields)
    data = list(body_reader)

    print(b"".join(data).decode("utf-8"))

    # output:
    # --75d42525e65d4cf3ba7e1fdbc9ec9787
    # Content-Disposition: form-data; name=aaa
    #
    # abcde
    # --75d42525e65d4cf3ba7e1fdbc9ec9787
    # Content-Disposition: form-data; name=bbb; filename=abc.txt
    # Content-Type: text/plain
    #
    # 123456789
    # --75d42525e65d4cf3ba7e1fdbc9ec9787--
```

#   Author

Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>


[pykit3]: https://github.com/pykit3