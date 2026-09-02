# solution.py — proof rewrite of HumanEval/156 int_to_mini_roman.
# Behavior-identical to canonical.py (canonical UNCHANGED); differential-tested vs the
# canonical over the WHOLE documented domain 1..1000 (0 mismatches, see PROOF.md).
#
# REDESIGN: the canonical's greedy nested-while over a 13-entry value table blows up
# symbolically (the prior proof ground for hours).  Replaced by the CLOSED FORM over the
# decimal digits of `number` (valid because 1 <= number <= 1000):
#   thousands t = number // 1000        (0 or 1)
#   hundreds  h = (number // 100) % 10   (0..9)
#   tens      e = (number // 10)  % 10   (0..9)
#   units     u = number % 10            (0..9)
# Each place has a FIXED lowercase Roman pattern per digit (the standard subtractive
# tables); the result is the concatenation M[t] + H[h] + T[e] + U[u].  No loop — four
# constant-table lookups + three string concats.  Built directly in lowercase, so the
# canonical's trailing `.lower()` is unnecessary.
def int_to_mini_roman(number):
    M = ['', 'm']
    H = ['', 'c', 'cc', 'ccc', 'cd', 'd', 'dc', 'dcc', 'dccc', 'cm']
    T = ['', 'x', 'xx', 'xxx', 'xl', 'l', 'lx', 'lxx', 'lxxx', 'xc']
    U = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix']
    return M[number // 1000] + H[(number // 100) % 10] + T[(number // 10) % 10] + U[number % 10]
