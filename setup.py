# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3httpmultipart",
    packages=["k3httpmultipart"],
    version="0.1.0",
    license='MIT',
    description='This module provides some util methods to get multipart headers and body.',
    long_description="# k3httpmultipart\n\n[![Action-CI](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3httpmultipart/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3httpmultipart.svg?branch=master)](https://travis-ci.com/pykit3/k3httpmultipart)\n[![Documentation Status](https://readthedocs.org/projects/k3httpmultipart/badge/?version=stable)](https://k3httpmultipart.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3httpmultipart)](https://pypi.org/project/k3httpmultipart)\n\nThis module provides some util methods to get multipart headers and body.\n\nk3httpmultipart is a component of [pykit3] project: a python3 toolkit set.\n\n\n#   Name\n\nk3httpmultipart\n\n#   Status\n\nThe library is considered production ready.\n\n\n\n\n# Install\n\n```\npip install k3httpmultipart\n```\n\n# Synopsis\n\n```python\n\nimport os\n\nimport k3httpmultipart\nimport k3fs\n\n# http request headers\nheaders = {'Content-Length': 1200}\n\n# http request fields\nfile_path = '/tmp/abc.txt'\nk3fs.fwrite(file_path, '123456789')\nfields = [\n    {\n        'name': 'aaa',\n        'value': 'abcde',\n    },\n    {\n        'name': 'bbb',\n        'value': [open(file_path), os.path.getsize(file_path), 'abc.txt']\n    },\n]\n\n# get http request headers\nmultipart = k3httpmultipart.Multipart()\nres_headers = multipart.make_headers(fields, headers=headers)\n\nprint(res_headers)\n\n#output:\n#{\n#    'Content-Type': 'multipart/form-data; boundary=FormBoundaryrGKCBY7',\n#    'Conetnt-Length': 1200,\n#}\n\n# get http request body reader\nmultipart = k3httpmultipart.Multipart()\nbody_reader = multipart.make_body_reader(fields)\ndata = []\n\nfor body in body_reader:\n    data.append(body)\n\nprint(''.join(data))\n\n#output:\n#--FormBoundaryrGKCBY7\n#Content-Disposition: form-data; name=aaa\n#\n#abcde\n#--FormBoundaryrGKCBY7\n#Content-Disposition: form-data; name=bbb; filename=abc.txt\n#Content-Type: text/plain\n#\n#123456789\n#--FormBoundaryrGKCBY7--\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3httpmultipart',
    keywords=['python', 'multipart'],
    python_requires='>=3.0',

    install_requires=['k3fs<0.2,>=0.1.5', 'k3mime>=0.1.2,<0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
