import hashlib


def string_to_md5(text):
    if not text:
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()


empty_result = string_to_md5("")
example_result = string_to_md5("Hello world")
abc_result = string_to_md5("abc")
