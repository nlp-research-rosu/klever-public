# solution.py — shape-faithful rewrite of canonical.py (one function; docstring
# omitted; the len-of-comprehension branch is a statement-level count loop —
# diff-tested). See DEESCAPE.md #125.


def split_words(txt):
    if " " in txt:
        return txt.split()
    elif "," in txt:
        return txt.replace(',', ' ').split()
    else:
        count = 0
        i = 0
        for i in range(len(txt)):
            if txt[i].islower() and ord(txt[i]) % 2 == 0:
                count = count + 1
        return count
