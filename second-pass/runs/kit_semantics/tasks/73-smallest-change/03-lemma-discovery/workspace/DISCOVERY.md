# Trust-boundary discovery

The canonical inventory has SHA-256 `3f2d6f96e2fde04bddd98fb0e5cc6357e5f39a29c219ed0264215d821bec45b9` and contains 14 rules in the local `VERIFICATION` closure. All 14 are classified once and in canonical order in `trust-boundary.json`.

## Classification result

- Ten rules are `DEFINITION`: the four fresh constructor/macro symbols (`smallestLoopBody`, `smallestBody`, `smallestDef`, and `fixedBuiltins`), both structural equations for the fresh `allInts` predicate, the defining equation for fresh `halfLen`, the defining equation for fresh `pairDiff`, and both guarded recurrence equations for fresh `mismatchCount`.
- One rule is `OPERATIONAL_RULE`: the local `#branch`/`AugAssign` rule updates the execution configuration and preserves the arbitrary continuation and residual scope map.
- Zero rules are `PROVED_DERIVED_LEMMA` under the required exact-statement test.
- Three rules are `DOMAIN_LEMMA`: the whole-loop summary bridge, the comparison-definedness `#Ceil` simplification, and integer-addition reassociation.

The two rules carrying the `simplification` attribute are classified as required: the equation of the fresh `halfLen` symbol is a `DEFINITION`, while integer-addition reassociation is a `DOMAIN_LEMMA`. The `#Ceil` rule is also a `DOMAIN_LEMMA` because it states a fact about `#Ceil`, `applyCmp`, and sequence operations defined outside the verification module rather than defining a fresh symbol.

## Separately proved derived-lemma evidence

No canonical source rule qualifies as a separately proved derived lemma.

`prove.sh` does run `kprove branch-connection-spec.k` against `BRANCH-CONNECTION`, a module importing only the supplied `MPY` semantics, and `branch-connection-proof.log` records `#Top`. That spec proves separate true-guarded and false-guarded branch paths. The installed canonical branch rule is instead one unguarded rule whose update contains a Boolean conditional. Because no earlier claim has the identical installed statement, this evidence does not satisfy the exact-correspondence requirement; the installed rule is classified by its operational role.

`prove.sh` next runs `kprove loop-connection-spec.k` against `LOOP-CONNECTION`, which imports `VERIFICATION-BASE` but does not contain the later whole-loop rule in `VERIFICATION`; `loop-connection-proof.log` records `#Top`. The proved claim, however, quantifies arbitrary accumulator `C` and index `I`, assumes the additional bound `0 <=Int I`, and returns the generalized accumulator-plus-summary result. The installed canonical rule fixes the accumulator and index to zero, omits that bound, and has the specialized result. The proved claim therefore strictly generalizes rather than identically matches the installed rule, so the canonical rule is a `DOMAIN_LEMMA`, not a `PROVED_DERIVED_LEMMA`.

Neither the comparison-definedness simplification nor integer-addition reassociation is first proved by an exact bridge-free claim in `prove.sh`.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791` — whole-loop summary bridge;
- `rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526` — comparison-definedness fact; and
- `rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4` — integer-addition associativity.
