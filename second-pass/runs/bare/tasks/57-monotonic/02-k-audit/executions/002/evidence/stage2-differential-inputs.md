# Differential input scope

The script `differential_test.py` imports `monotonic` directly from the trusted
`/reference/canonical.py` and from `/candidate/solution.py`.

Its oracle is independently written as the disjunction of:

1. all adjacent pairs satisfy `left <= right`; and
2. all adjacent pairs satisfy `left >= right`.

The explicit inputs are printed in the run log. They cover the three documented
examples, the empty list, a singleton, equal pairs, the first and second
disjunct separately, neither disjunct at a peak and a valley, duplicates, large
integers, mixed numeric values, floats, and strings.

Generated inputs are deterministic and exhaustive over these finite scopes:

- every list of length 0 through 7 over `(-2, -1, 0, 1, 2)`;
- every list of length 0 through 5 over `(-1.5, 0.0, 0.25)`; and
- every list of length 0 through 5 over `("a", "b", "c")`.

This is finite differential evidence, not a universal proof.
