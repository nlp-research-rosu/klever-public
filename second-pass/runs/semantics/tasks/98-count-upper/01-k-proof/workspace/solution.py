def count_upper(s):
    count = 0
    even = True
    ch = ""
    for ch in s:
        count += even and ch in "AEIOU"
        even = not even
    return count
