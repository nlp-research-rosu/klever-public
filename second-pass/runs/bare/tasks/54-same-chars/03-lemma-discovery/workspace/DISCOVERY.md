# Trust-boundary discovery

The canonical inventory contains one rule:

- `rule-69aad3da8a2a2d3aa2322b5eb4234ecca7aa125148464a5fcdbec3fcfb8ad975`
  is classified as `DEFINITION`. Its equation expands the named
  `sameCharsSpec(S0, S1)` contract summary to
  `charSet(S0) ==K charSet(S1)`. This defines the mathematical observation
  used by the proof; it is neither an execution transition nor an additional
  mathematical fact.

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first runs
`kompile verification.k`, which places this rule in
`verification-kompiled`, and only afterward runs
`kprove spec.k --definition verification-kompiled`. Thus Stage 1 contains no
proof of this exact rule against a module from which the rule was absent, and
there is no separate derived-lemma proof evidence to identify.

The domain-lemma set is explicitly empty.
