import hashlib


def string_to_md5(text):
    if text == "":
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()


empty_result = string_to_md5("")
digest_result = string_to_md5("Hello world")
