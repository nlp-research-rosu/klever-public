# Independent operational-bridge judgment

Both generated target parameters are bound only to
`rule-1136bead…`, the definedness lemma for `seqLen` under `isStrV`.
The theorem constrains definedness, not the numeric length, so the parameter
definitions require a separate operational audit.

## `isStrV`

The candidate definition is at `Proof.lean` lines 6–8. It returns `true`
exactly for `SortVal.inj_SortStr` and `false` for every other `SortVal`
constructor. This matches frozen `builtins.k` lines 293–297:

- `isStrV(str(_:IntSeq)) => true`
- the `owise` `Val` case returns `false`.

It also matches the generated operational equations in `Func.lean` lines
19–24. The generated `Inj SortIterable SortVal` instance canonicalizes an
iterable-wrapped string to `SortVal.inj_SortStr`; a raw, noncanonical nested
constructor is handled by the K `owise`/generated fallback and the candidate
returns `false` on that adversarial shape.

## `seqLen?`

The candidate definition is at `Proof.lean` lines 35–50, with helpers at lines
10–32. It is an exact option-valued model of frozen `seqLen`:

- direct string and set values use constructor recursion on `IntSeq`, matching
  total `isLen`;
- list and tuple values use constructor recursion on `ValSeq`, matching total
  `vsLen`;
- ranges use the same three guarded `rangeLen` equations: positive/nonempty,
  negative/nonempty, and the corresponding empty cases;
- step zero yields `none`, matching the absence of a frozen `rangeLen` rule;
- every value kind not covered by a frozen `seqLen` rule yields `none`.

In both nonempty range branches the numerator and denominator are positive,
so Lean integer division agrees with the frozen `/Int` result on the rule
domains. The definitions are structurally recursive and do not depend on the
proof theorem, generated axioms, or a hard-coded test value.

## Adversarial and counterfactual checks

`operational-bridge-adversarial.log` records:

- string/non-string discrimination: `true`, `false`;
- string lengths `0` and `2`;
- list, tuple, and set lengths `2`;
- positive and negative range lengths `3`;
- empty positive and negative ranges `0`;
- zero-step range `none`;
- raw noncanonical nested string: `isStrV = false`, `seqLen? = none`.

The same Lean audit file machine-checks three counterfactuals:

1. constant-false `isStrV` plus constant-`none` `seqLen?` proves the generated
   target vacuously;
2. an implementation that returns hard-coded `some 0` for every string also
   proves the target because only definedness is constrained;
3. honest `isStrV` paired with constant-`none` `seqLen?` is refuted on the empty
   string.

These mutations demonstrate that build success is insufficient. The actual
candidate is not one of those convenient models: it distinguishes constructors,
computes different ground lengths, handles range guards, and follows every
frozen `seqLen` equation.
