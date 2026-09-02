# Independent differential input scope

The executable input generator is `differential_test.py`. Its fixed inputs are
the two documented examples; empty and minimum-positive lists; a passing
single-digit boundary; each of the five even-character rejection branches;
odd-only, duplicate, ordering, forbidden-digit-position, and large-integer
cases. It then deterministically adds:

- every singleton positive integer from 1 through 10,000;
- reversed sliding windows over that interval, including duplicates; and
- 1,000 pseudorandom finite lists using seed 104104, lengths drawn cyclically
  from `[0, 1, 2, 3, 7, 20, 50]`, values in `1..10**18`, and deterministic
  duplicate insertion.

The trusted oracle is `/reference/canonical.py:unique_digits`; the implementation
under audit is `/candidate/solution.py:unique_digits`. Both receive fresh list
copies for each case.
