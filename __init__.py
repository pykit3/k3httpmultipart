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


def __getattr__(name: str) -> str:
    # importlib.metadata takes about 20 ms to import, so it is loaded only
    # when __version__ is read
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib.metadata import version

    return version("k3httpmultipart")
