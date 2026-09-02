# Independent Stage 3 classification

Frozen verification module closure: `VERIFICATION` only. `MPY` is imported from
the supplied semantics but is not a module defined locally in `verification.k`.
The trusted inventory reconstructs six local rules, all carrying
`[simplification]`.

## Operational comparison

The source loop updates

```
result := chr(48 + x % base) + result
x := x // base
```

while `x > 0`. In the supplied K semantics:

- integer `%` is `pyMod(I1,I2)`;
- integer `//` is `(I1 - pyMod(I1,I2)) /Int I2`;
- `chr(I)` is the one-code sequence `str(iCons(I,.IntSeq))` on the relevant
  ASCII range;
- string `+` is ordered `seqConcat`; and
- the while rule executes the body and loops only when the comparison is
  truthy.

Thus one loop iteration prepends code `48 + pyMod(N,B)` to the current result
and recurs at exactly `(N - pyMod(N,B)) /Int B`. For `N > 0, B >= 2`, this
quotient is nonnegative and strictly smaller than `N`. The target precondition
`2 <= B < 10` also keeps the generated digit codes in `48..56`, satisfying the
supplied `chr` guard.

## Per-rule judgment

1. `rule-a83520...f994`, lines 11--13: **DEFINITION**. This is the terminating
   `baseAcc` case for nonpositive remaining magnitude. Its left-hand side is a
   fresh pure function term, not a program/control term.
2. `rule-efae06...f474`, lines 15--17: **DEFINITION**. This is a disjoint
   totalization branch for positive magnitude and invalid bases below 2. It is
   outside the theorem domain, asserts no source/postcondition fact, and does
   not replace execution.
3. `rule-ecc726...d39a`, lines 19--25: **DEFINITION**. This is the recursive
   `baseAcc` equation and exactly mirrors one operational loop step. Its guard
   is disjoint from the other `baseAcc` cases and its recursive argument
   descends for the target domain.
4. `rule-fdf775...8118`, lines 30--31: **DEFINITION**. This defines the zero
   branch of the named `changeBaseCodes` summary as code 48, matching the
   program's early return `"0"`.
5. `rule-245f4d...1d41`, lines 33--35: **DEFINITION**. This defines the positive
   branch by starting `baseAcc` with the empty accumulator, matching empty
   `result` and no sign.
6. `rule-6eaa18...6abd`, lines 37--40: **DEFINITION**. This defines the negative
   branch by prefixing code 45 and running the same recurrence on `-N`, matching
   the sign assignment and magnitude negation.

The three guards for each function are pairwise disjoint and collectively
cover all integers. None of the six rules has a `<k>` cell, matches `Call`,
`While`, assignment, return, an environment, or any other operational state.
None states an additional arithmetic/base-representation property: each is an
equation whose left-hand side is one of the two freshly declared summary
functions. Therefore none is an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or
`DOMAIN_LEMMA`.

Independent classification result: six `DEFINITION`; zero
`OPERATIONAL_RULE`; zero `PROVED_DERIVED_LEMMA`; zero `DOMAIN_LEMMA`.
