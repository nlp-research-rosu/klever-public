def decode_shift(s):
    result = ""
    ch = ""
    for ch in s:
        result = result + chr(((ord(ch) - 5 - 97) % 26) + 97)
    return result


# HumanEval/50 test cases (decode_shift inverts encode_shift; codes computed offline).
assert decode_shift("mjqqt") == "hello"
assert decode_shift("fgh") == "abc"
assert decode_shift("cde") == "xyz"
assert decode_shift("btwqi") == "world"
assert decode_shift("pqjajw") == "klever"
