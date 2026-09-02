def count_upper(s):
    count = 0
    remaining = s
    while remaining:
        count += remaining[0] in "AEIOU"
        remaining = remaining[2:]
    return count
