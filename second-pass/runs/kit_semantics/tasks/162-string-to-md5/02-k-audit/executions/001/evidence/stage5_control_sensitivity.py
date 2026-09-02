import hashlib


def string_to_md5(text):
    if text == "":
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()


digest = string_to_md5("a")
after_digest = 7
