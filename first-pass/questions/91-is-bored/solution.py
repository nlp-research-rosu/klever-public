# solution.py — canonical 1-function shape: the single-pass scan (the
# sanctioned re.split workaround) lives directly in is_bored.
# Single-scan rewrite of `re.split(r'[.?!]\s*', S)` then counting fragments whose
# first two chars are "I " (capital-I then space).  No regex, no genexp: one left-to-right
# pass with a 4-state machine, written as a PURE if/elif chain (no continue, no fall-through,
# no char temporaries) so each iteration is one atomic dispatch over ord(S[i]) comparisons.
# WS (ASCII \s) = codes 9..13 and 28..32; DELIM = '.', '?', '!' = codes 46, 63, 33.
#   phase: 0=fragment start, 1=second char of fragment, 2=fragment body,
#          3=consuming the whitespace/delimiter run right after a delimiter
#   cand : 0=fragment so far is not "I ", 1=saw leading 'I', 2=matched "I "
def is_bored(S):
    count = 0
    phase = 0
    cand = 0
    i = 0
    n = len(S)
    while i < n:
        if phase == 3 and (ord(S[i]) == 46 or ord(S[i]) == 63 or ord(S[i]) == 33 or (9 <= ord(S[i]) and ord(S[i]) <= 13) or (28 <= ord(S[i]) and ord(S[i]) <= 32)):
            phase = 3
        elif ord(S[i]) == 46 or ord(S[i]) == 63 or ord(S[i]) == 33:
            if cand == 2:
                count = count + 1
            cand = 0
            phase = 3
        elif phase == 3 or phase == 0:
            cand = 1 if ord(S[i]) == 73 else 0
            phase = 1
        elif phase == 1:
            cand = 2 if (cand == 1 and ord(S[i]) == 32) else 0
            phase = 2
        i = i + 1
    if cand == 2:
        count = count + 1
    return count
