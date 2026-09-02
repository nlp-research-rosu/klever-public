# Differential input manifest

The executable input generator is `differential_test.py`.

- Documented examples: `[]` and `[1, 2, 3, 4]`.
- Named boundary cases: `[0]`, `[1]`, `[-1]`, `[2]`, `[-2]`,
  `[0, 0]`, `[1, 0]`, `[0, 1]`, `[-2, 0, 5]`, `[2, -3]`,
  `[-10**100, 10**100]`, and
  `[10**100, 10**100, -(10**100)]`.
- Exhaustive small cases: every list of length 0 through 5 over
  `(-3, -1, 0, 1, 2, 4)`.
- Deterministically generated cases: Python `random.Random(8008)`, 500 lists;
  each length is drawn uniformly from 0 through 32 and each element uniformly
  from -1,000,000 through 1,000,000.

This exercises the canonical loop's zero-iteration, first-iteration, and
multi-iteration boundaries, plus zero/one multiplicative identities, sign
changes, arbitrary-precision integers, and representative longer lists. The
submitted implementation has no conditional branches.
