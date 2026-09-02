# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`.

- Inventory schema: `2`
- Inventory SHA-256:
  `f5b69f74b12f0505988375faf85089ef4d83ccca0e2946d2e4e09f482da52564`
- Verification closure: `VERIFICATION-BASE`, then `VERIFICATION`
- Canonical rule count: `23`

`trust-boundary.json` preserves the canonical inventory order and classifies
each `source_rule_id` exactly once.

## Classification method

The first 22 rules define proof-local mathematical names:

- `isNumericVal` and `orderablePair` define domain predicates.
- The four `scanDefined` equations define a total structural recurrence over a
  `ValSeq`.
- The eleven `orderGe` equations define and totalize the proof-local comparison
  summary over all modeled value pairs.
- The five `arrangeSeq` equations define and totalize the mathematical scan
  summary used by the postcondition.

These are `DEFINITION` rules. Their right-hand sides give the cases of the
symbol named on the left, and the recursive cases descend structurally.
Although 20 of these equations carry `simplification`, that attribute changes
how K uses their definitions; it does not turn them into separately established
facts.

No canonical rule is classified as `OPERATIONAL_RULE`. The inventory is limited
to the two local verification modules: it does not include the ordinary MPY
execution rules, and the one local rule over an existing MPY observation is a
`simplification` rule that the requested classification policy requires to be
either `DEFINITION` or `DOMAIN_LEMMA`.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1 does contain relevant proof evidence:

1. `prove.sh` first compiles `verification.k` with
   `--main-module VERIFICATION-BASE` into `connection-kompiled`.
2. It then runs:

   ```text
   kprove connection-spec.k \
     --definition connection-kompiled \
     --spec-module CONNECTION-SPEC
   ```

3. `/reference/k-proof/evidence/connection-kprove.log` records `#Top` for ten
   static claims: Int-Int, Bool-Bool, Bool-Int, Int-Bool, Float-Float,
   Int-Float, Float-Int, Bool-Float, Float-Bool, and Str-Str.
4. `/reference/k-proof/connection-kompiled/mainModule.txt` confirms that those
   claims were checked against `VERIFICATION-BASE`, which excludes the final
   `VERIFICATION` rule.

That ordering is genuine bridge-free evidence, but it does not establish any
canonical inventory rule under the strict `PROVED_DERIVED_LEMMA` definition:

- The ten claims have statements of the form
  `applyCmp(">=", <static operands>) => orderGe(<static operands>)`.
- The `orderGe` inventory rules were already present in
  `VERIFICATION-BASE`, are defining equations, and are not the statements of
  those claims.
- The final inventory rule has the distinct, more general statement
  `applyCmp(">=", V:Val, W:Val) => orderGe(V, W)` under
  `orderablePair(V, W)`.
- No Stage 1 claim first proves that exact dynamic guarded statement.
- The final rule carries `simplification`, which independently excludes the
  `PROVED_DERIVED_LEMMA` classification under the requested policy.

The connection proof is therefore supporting evidence for the intended
case coverage, not an exact-statement provenance certificate for a canonical
rule.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly one rule:

```text
rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050
```

This rule rewrites the pre-existing MPY observation
`applyCmp(">=", V, W)` to the proof-local `orderGe(V, W)` under
`orderablePair(V, W)`. It does not define the left-hand symbol, so it is not a
definition. It is marked `simplification`, so it cannot be classified as an
operational rule or proved-derived lemma under the requested constraints.
Because its exact dynamic guarded statement was not first proved in Stage 1,
it is the additional mathematical fact trusted to close the target proof and
is classified `DOMAIN_LEMMA`.

## Totals

| Classification | Count |
|---|---:|
| `DEFINITION` | 22 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |
| **Total** | **23** |
