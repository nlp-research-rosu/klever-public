# solution.py — behavior-preserving rewrite of canonical.py (HumanEval/32).
#
# find_zero brackets a sign change (doubling loop) then bisects (halving loop) and returns the final
# `begin`.  poly and the float ops are TRUSTED opaque primitives (kprove has no float theory): the
# proof verifies the LOOP-THREADING structure (each loop folds (begin,end) via a co-inductive summary
# matching its update rules under the opaque guard case-splits) and trusts the float arithmetic + the
# root property.  PARTIAL correctness: if the loops halt, result = the summary.  poly holds canonical's
# evaluation verbatim -> solution.py == canonical.py.

import math


def poly(xs, x):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs):
    begin = -1.0
    end = 1.0
    center = 0.0
    while poly(xs, begin) * poly(xs, end) > 0.0:
        begin = begin * 2.0
        end = end * 2.0
    while end - begin > 0.0000000001:
        center = (begin + end) / 2.0
        if poly(xs, center) * poly(xs, begin) > 0.0:
            begin = center
        else:
            end = center
    return begin
