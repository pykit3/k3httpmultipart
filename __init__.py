from importlib.metadata import version

__version__ = version("k3httpmultipart")

from .multipart import (
    InvalidArgumentTypeError,
    Multipart,
    MultipartError,
)

__all__ = [
    "InvalidArgumentTypeError",
    "Multipart",
    "MultipartError",
]
