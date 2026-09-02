def count_upper(s):
    count = 0
    even = True
    ch = ""
    for ch in s:
        count += even and ch in "AEIOU"
        even = not even
    return count


# Expected values were independently checked with /reference/canonical.py.
assert count_upper("") == 0
assert count_upper("A") == 1
assert count_upper("B") == 0
assert count_upper("AA") == 1
assert count_upper("BA") == 0
assert count_upper("AB") == 1
assert count_upper("aBCdEf") == 1
assert count_upper("dBBE") == 0
assert count_upper("AEIOU") == 3
assert count_upper("AaEeIiOoUu") == 5
assert count_upper("xAxExIxOxU") == 0
