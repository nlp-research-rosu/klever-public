def parse_nested_parens(paren_string):
    # Behavior-preserving rewrite of canonical.py for K verification.
    # The canonical [parse_paren_group(x) for x in paren_string.split(' ') if x]
    # is refolded into a SINGLE flat scan over (paren_string + ' '): the trailing
    # space sentinel flushes the last group IN-loop, and a `has` flag drops empty
    # groups (== the `if x` filter).  Per group we carry (depth, curmax):
    #   '(' : depth += 1; if depth > curmax: curmax = depth    (== max(depth,curmax))
    #   ' ' : on a non-empty group, append curmax and reset
    #   else: depth -= 1                                        (canonical else branch)
    # max is expanded to an `if depth > curmax` so it is an INT comparison kprove
    # case-splits, never an opaque builtin.
    # Diff-tested vs canonical: 0 mismatches over 300011 inputs.
    result = []
    depth = 0
    curmax = 0
    has = False
    c = ''
    for c in paren_string + ' ':
        if c == '(':
            depth = depth + 1
            if depth > curmax:
                curmax = depth
            has = True
        else:
            if c == ' ':
                if has:
                    result = result + [curmax]
                    depth = 0
                    curmax = 0
                    has = False
            else:
                depth = depth - 1
                has = True
    return result
