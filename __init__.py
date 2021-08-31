"""
#   Name

k3httpmultipart

#   Status

The library is considered production ready.

"""


__version__ = "0.1.0"
__name__ = "k3httpmultipart"

from .multipart import (
    Multipart,

    InvalidArgumentTypeError,
    MultipartError,
)

__all__ = [
    'Multipart',

    'InvalidArgumentTypeError',
    'MultipartError',
]

