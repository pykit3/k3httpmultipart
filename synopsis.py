import os

import k3fs

import k3httpmultipart

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

    # get http request headers; make_headers() computes Content-Length
    multipart = k3httpmultipart.Multipart()
    res_headers = multipart.make_headers(fields)

    print(res_headers)

    # output:
    # {
    #    'Content-Type': 'multipart/form-data; boundary=75d42525e65d4cf3ba7e1fdbc9ec9787',
    #    'Content-Length': 258,
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
