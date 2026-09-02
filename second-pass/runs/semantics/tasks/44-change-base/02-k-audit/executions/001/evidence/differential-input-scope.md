# Differential input scope

`differential_check.py` deterministically constructs the complete inputs:

- the three documented examples and `(x, base) = (0, 2)`;
- for each base 2 through 9, `x` at `1`, `base - 1`, `base`, `base + 1`,
  `base**2 - 1`, and `base**2`;
- the Cartesian product `x = 0..512`, `base = 2..9`;
- 256 generated cases from `random.Random(440044)`, with a uniformly selected
  bit count from 0 through 512, `getrandbits(bits)`, and a uniformly selected
  base from 2 through 9;
- `x = 2**(sys.getrecursionlimit() + 50)` at bases 2 and 9.
- the literal-prompt ambiguity probes `(-1, 2)`, `(-2, 3)`, and `(-7, 9)`;
  these are outside the proof's `X >= 0` precondition but the docstring does
  not expressly exclude them.

The script records each mismatch with the exact decimal `x`, base, and both
observable outcomes. The generator and seed in the preserved script are the
machine-readable input definition.
