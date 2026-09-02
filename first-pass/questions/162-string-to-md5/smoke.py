# solution.py — canonical verbatim minus the docstring (one function; the
# hashlib.md5(...).hexdigest() chain is the trusted opaque md5hexCodes).


def string_to_md5(text):
    import hashlib
    return hashlib.md5(text.encode('ascii')).hexdigest() if text else None


assert string_to_md5('') is None
