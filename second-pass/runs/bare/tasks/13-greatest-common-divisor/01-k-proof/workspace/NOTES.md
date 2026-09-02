# Verification notes

`semantic.k` is a small operational semantics for precisely the translated
Python subset used by `solution.mpy`: function entry, statement sequencing,
integer/name evaluation, assignment, conditionals, `while`, `%`, unary minus,
comparisons, and return.

The proof is intentionally staged. `loop-spec.k` first proves the Euclidean
loop theorem directly against the operational rules. Only after that command
succeeds does `verification.k` install the theorem as a higher-priority proof
summary. `spec.k` then proves the full translated function for arbitrary
integer inputs, with `normInt` specifying sign normalization and `gcdSpec`
specified by the Euclidean equations.
