def count_upper(s):
    count = 0
    remaining = s
    while remaining:
        count += remaining[0] in "AEIOU"
        remaining = remaining[2:]
    return count


assert count_upper("aBCdEf") == 1
assert count_upper("abcdefg") == 0
assert count_upper("dBBE") == 0
assert count_upper("") == 0
assert count_upper("AEIOU") == 3
