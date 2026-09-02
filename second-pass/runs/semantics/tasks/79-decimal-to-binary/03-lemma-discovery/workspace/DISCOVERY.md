# K proof trust-boundary discovery

The canonical inventory contains two rules, both in `VERIFICATION`.

## Classifications

- `rule-d413ecca2d0d055a04bc2f4fe8404284cf3025dc1bb61dd03e2d09244027583b` is a `DOMAIN_LEMMA`. It summarizes a property of the reference slice equations: removing two known leading character codes from a string leaves the arbitrary `IntSeq` tail. This is an additional mathematical fact used to make symbolic slicing progress.
- `rule-f0749fc6bd85fe62094ab4f801ecd2f6fd2b3797fe1fc9760ae63e8c1f50cb7e` is a `DEFINITION`. It expands the named `#runDecimalToBinary` proof term into the closure call representing the translated solution.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1 `prove.sh` compiles all of `verification.k`, including the slice-tail rule, before invoking `kprove` on the single `decimal-to-binary-correct` claim in `spec.k`. It has no earlier `kprove` command against a module lacking that rule and therefore supplies no ordering or exact-correspondence evidence for a separately proved derived lemma.

## Domain-lemma set

The domain-lemma set is **not empty**. It consists exactly of `rule-d413ecca2d0d055a04bc2f4fe8404284cf3025dc1bb61dd03e2d09244027583b`.
