def count_upper(s):
    count = 0
    remaining = s
    while remaining:
        count += remaining[0] in "AEIOU"
        remaining = remaining[2:]
    return count


assert count_upper("") == 0
assert count_upper("A") == 1
assert count_upper("B") == 0
assert count_upper("AA") == 1
assert count_upper("BA") == 0
assert count_upper("AB") == 1
assert count_upper("AAB") == 1
assert count_upper("BAA") == 1
assert count_upper("aBCdEf") == 1
assert count_upper("abcdefg") == 0
assert count_upper("dBBE") == 0
assert count_upper("AEIOU") == 3
assert count_upper("AaEeIiOoUu") == 5
assert count_upper("BBBBBBBBB") == 0
assert count_upper("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA") == 16
