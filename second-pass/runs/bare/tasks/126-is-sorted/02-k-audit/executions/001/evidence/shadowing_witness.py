def is_sorted(lst):
    # The generator target intentionally shadows the parameter.  Python
    # evaluates the iterable from the outer scope, but the element expression
    # sees the per-item integer as `lst`, so `.count` raises AttributeError.
    # The second generator captures the outer parameter, causing the trusted
    # translator to emit the CellVars shape accepted by the generated grammar.
    return all(lst.count(lst) <= 2 for lst in lst) and all(
        lst.count(x) <= 2 for x in lst
    )
