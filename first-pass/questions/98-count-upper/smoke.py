def count_upper(s):
    count = 0
    i = 0
    c = ""
    code = 0
    for c in s:
        code = ord(c)
        if i % 2 == 0:
            if code == 65 or code == 69 or code == 73 or code == 79 or code == 85:
                count = count + 1
        i = i + 1
    return count


# HumanEval/98 test cases (the dataset `check`); returns an int.
assert count_upper("aBCdEf") == 1
assert count_upper("abcdefg") == 0
assert count_upper("dBBE") == 0
assert count_upper("B") == 0
assert count_upper("U") == 1
assert count_upper("") == 0
assert count_upper("EEEE") == 2
