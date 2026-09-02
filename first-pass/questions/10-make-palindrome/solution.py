# solution.py — canonical 2-function shape (docstrings omitted). is_palindrome's
# slice-equality takes the sanctioned two-pointer index loop (sticky ok, no
# early exit — diff-tested); make_palindrome is near-verbatim canonical with
# the REAL is_palindrome call in the while and the real slices.


def is_palindrome(string):
    lo = 0
    hi = len(string) - 1
    ok = True
    while lo < hi:
        if string[lo] != string[hi]:
            ok = False
        lo = lo + 1
        hi = hi - 1
    return ok


def make_palindrome(string):
    if not string:
        return ''
    beginning_of_suffix = 0
    while not is_palindrome(string[beginning_of_suffix:]):
        beginning_of_suffix += 1
    return string + string[:beginning_of_suffix][::-1]
