def count_upper(s):
    count = 0
    even = True
    ch = ""
    for ch in s:
        count += even and ch in "AEIOU"
        even = not even
    return count


assert count_upper("aBCdEf") == 1
assert count_upper("abcdefg") == 0
assert count_upper("dBBE") == 0
assert count_upper("") == 0
assert count_upper("AEIOU") == 3
assert count_upper("AaEeIiOoUu") == 5
