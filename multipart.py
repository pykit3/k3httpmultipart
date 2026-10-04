import copy
import uuid
from collections.abc import Iterator

import k3mime


class MultipartError(Exception):
    # The base class of the other exceptions in this module. It is a subclass of `Exception`
    pass


class InvalidArgumentTypeError(MultipartError):
    # A subclass of `MultipartError` Raise if the type of value is not a str or a list or the type of value[0] is not a string, string reader, file reader or file object
    pass


class Multipart:
    """

    :param block_size: It represents the size of each reading file
    :param boundary: a placeholder that represents out specified delimiter
    """

    def __init__(self, block_size=1024 * 1024):
        self.block_size = block_size

        self.boundary = uuid.uuid4().hex

        self.delimiter = f"--{self.boundary}"
        self.terminator = f"--{self.boundary}--"

    def make_headers(self, fields, headers=None):
        """
            Return a header according to the fields and headers

            :param fields: is a list of the dict, and each elements contains `name`, `value` and `headers`,
        `headers` is an optional argument
                -   `name`:
                It's a string that represents field's name

                -   `value`:
                The value represents field's content. The type of value can be a string or a
                list, string indicates that the field is a normal string, However, there are
                three arguments of list: `content`, `size` and `file_name`

                    -   `content`:
                    The type of `content` can be string, reader, file object
                        The string type refers to the user want to upload a string. It takes the
                    string as the field body

                        The reader type refers to a generator. To read the contents of generator as
                    the field body

                        The file object type refers to a file object, To read the contents of file
                    as the field body

                    -   `size`
                    `size` refers to the length of the content in bytes, a string is counted after
                    UTF-8 encoding. When the type of `content` is a string, size can be None

                    - `file_name`
                    `file_name` is an optional argument, if `file_name` is None, that indicates
                    that `content` is uploaded as a normal field, whereas, the field as a file

                -   `headers`:
                a dict, key is the `field_header_name`, value is the `field_header_value`,
                it contains user defined headers and the required headers, such as
                'Content-Disposition' and 'Content-Type'
            :param headers: a dict of http request headers, key is the `header_name`, value is the
        `header_value`.  It's a default argument and its default value is None
            :return: a dict that represents the request headers
        """

        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)

        headers["Content-Type"] = f"multipart/form-data; boundary={self.boundary}"

        if "Content-Length" not in headers:
            headers["Content-Length"] = self._get_body_size(fields)

        return headers

    def make_body_reader(self, fields):
        """
        Return a body according to the fields

        :param fields: refer to the explanation above fields
        :return: a generator that yields the multipart request body as `bytes`, a string is encoded as UTF-8
        """

        for f in fields:
            reader, _fsize, headers = self._standardize_field(f["name"], f["value"], f.get("headers", {}))

            yield self._get_field_header(headers)

            for buf in reader:
                if isinstance(buf, str):
                    buf = buf.encode("utf-8")
                yield buf

            yield b"\r\n"

        yield self.terminator.encode("utf-8")

    def _standardize_field(self, name, value, headers):
        if isinstance(value, str):
            reader = self._make_str_reader(value)
            fsize = len(value.encode("utf-8"))
            self._set_content_disposition(headers, name)

            return reader, fsize, headers

        elif isinstance(value, list):
            reader, fsize, fname = self._standardize_value(value)

            self._set_content_disposition(headers, name, fname)
            if fname is not None:
                headers.setdefault("Content-Type", k3mime.get_by_filename(fname))

            return reader, fsize, headers

        raise InvalidArgumentTypeError(f"type of value {type(value)} is invalid")

    def _standardize_value(self, value):
        reader, fsize, fname = (value + [None, None])[:3]

        if isinstance(reader, type(open)):
            reader = self._make_file_reader(reader)

        elif isinstance(reader, str):
            reader = self._make_str_reader(reader)
            fsize = len(value[0].encode("utf-8"))

        elif isinstance(reader, Iterator):
            pass

        else:
            raise InvalidArgumentTypeError(f"type of value[0] {type(value[0])}is invalid")

        return reader, fsize, fname

    def _get_field_size(self, field):
        _reader, fsize, headers = self._standardize_field(field["name"], field["value"], field.get("headers", {}))

        field_headers = self._get_field_header(headers)

        return len(field_headers) + fsize + len("\r\n")

    def _get_body_size(self, fields):
        body_size = 0

        for f in fields:
            body_size += self._get_field_size(f)

        return body_size + len(self.terminator)

    def _get_field_header(self, headers):
        field_headers = [self.delimiter]

        field_headers.append("Content-Disposition: " + headers.pop("Content-Disposition"))

        for k, v in headers.items():
            field_headers.append(k + ": " + v)

        field_headers.extend([""] * 2)

        return "\r\n".join(field_headers).encode("utf-8")

    def _make_file_reader(self, file_object):
        while True:
            buf = file_object.read(self.block_size)
            if buf == "":
                break
            yield buf

    def _make_str_reader(self, data):
        yield data

    def _set_content_disposition(self, headers, name, fname=None):
        if fname is None:
            headers["Content-Disposition"] = f"form-data; name={name}"
        else:
            headers["Content-Disposition"] = f"form-data; name={name}; filename={fname}"
