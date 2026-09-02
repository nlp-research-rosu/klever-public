# Differential input scope

The reviewer-authored `differential_test.py` checks:

- the two documented examples;
- empty, singleton, zero-product, negative, mixed-sign, and arbitrary-precision
  integer boundary cases; and
- every list of length 0 through 5 over the pool `[-3, -1, 0, 1, 2, 5]`.

The script constructs this set deterministically, imports the trusted canonical
and candidate functions from separate scratch modules, compares returned
values and exceptions, and checks that neither implementation mutates its
input.
