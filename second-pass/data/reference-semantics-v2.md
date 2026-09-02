# Reference semantics v2 — recorded CPython-faithfulness fixes (2026-07-30)

Three approved one-fixes to `data/reference/src/semantics/` (bool.k,
builtins.k, concrete.k, core.k, float.k, int.k; +164/−14 lines):

1. bool is a subtype of int: isinstance identification, arithmetic and
   comparison promotion, krun-side numeric membership collapse.
2. Exact mixed Float/Int comparison via floor/ceil (replaces the
   intToF-rounding rules that misdecided at the 2^53 boundary).
3. Exact CPython round(F, N) via exact-fraction extraction and half-even
   integer rounding (replaces the scale-multiply algorithm with a
   machine-checked wrong-value witness).

Validated bit-exactly against CPython inside the frozen runner image:
18,004 mixed comparisons, 2,008 rounding cases, 27 identification facts,
0 mismatches; both LLVM and Haskell backends kompile; regression smoke on
unmodified passing tasks unchanged. Validation harness preserved in the
operator scratchpad (semval/).

Tree hashes:
- v1 (frozen campaign): 4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f
  preserved at `data/semantic-archive/v1/src`
- v2 (current): e017e7ddcdccc327e74147cf909748f8d5f3a5af556133d79bb556c08f867cb0

Every task records the tree hash its workspace was seeded from
(`task.json` `inputs.reference_semantics_sha256`); Stage 2 audits mount
the matching registered version via
`data/reference-semantics-versions.json` (fail-closed on unknown hashes).
The completed bare/semantics arms and all v1-generated kit-arm candidates
remain audited against v1 bytes.
