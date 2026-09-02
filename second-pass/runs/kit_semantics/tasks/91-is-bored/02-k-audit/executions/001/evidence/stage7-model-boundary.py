def is_bored(S):
    count = 0
    at_start = True
    pending_i = False
    c = ""

    for c in S:
        if c == "." or c == "?" or c == "!":
            if pending_i:
                count += 1
            at_start = True
            pending_i = False
        elif at_start:
            if c.strip() != "":
                if c == "I":
                    at_start = False
                    pending_i = True
                else:
                    at_start = False
        elif pending_i:
            if c.strip() == "":
                count += 1
            pending_i = False

    if pending_i:
        count += 1

    return count


# The supplied K model does not classify vertical tab (code 11) as whitespace,
# so its result is 0. CPython classifies it as whitespace and returns 1.
assert is_bored("I\vwork") == 0
