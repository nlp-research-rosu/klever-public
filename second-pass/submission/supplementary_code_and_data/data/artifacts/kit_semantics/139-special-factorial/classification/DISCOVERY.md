# Trust-boundary rule discovery

## Scope and method

`/reference/rule-inventory.json` is treated as the exhaustive canonical
inventory of the local verification-module closure. Its copied
`inventory_sha256` is
`1993002e3c6d8018cd5a567c10250d952113f008862ec1beac606f480a035d82`.
The inventory contains four rules, all from module `VERIFICATION`; each is
classified exactly once below and retained in canonical order.

The audit compared each rule's exact text and attributes with the mounted
`verification.k`, then inspected `prove.sh`, `spec.k`, `summary-test.k`,
`proof.out`, and `summary-test.out` for proof ordering and dependency evidence.
No canonical rule has the `simplification` attribute.

## Classifications

| Inventory order | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-76c9fee7d31c7b9af2772f9513ebc29daf766162032c70206947d10685c8ab71` | `DEFINITION` | Base equation of `factorialAfter`; it returns the accumulator after the index has passed the bound. |
| 2 | `rule-56984dfdcdf0ba8c027875164046db3a50319cd8bde210cf5869ac4eb5483d0b` | `DEFINITION` | Recursive equation of `factorialAfter`; it advances the index and factorial accumulator. |
| 3 | `rule-7e43f2e0797b8ac08b474026ab65d98ed66d18b24b058dc65450b65246cf00b5` | `DEFINITION` | Base equation of `productAfter`; it returns the accumulated product after the index has passed the bound. |
| 4 | `rule-110b740de92d5388806b355cf84cbe138a0ae279db89595139a60295681df25c` | `DEFINITION` | Recursive equation of `productAfter`; it advances the index and both accumulators. |

The paired guards for each function, `I >Int N` and `I <=Int N`, are disjoint
and exhaustive. The step equations are the recurrences that give the summary
symbols their meanings. Their left-hand sides are pure `factorialAfter` or
`productAfter` terms, not `<k>` configurations or source-language constructs,
so none is an `OPERATIONAL_RULE`. They state how the named folds are computed
rather than adding independent mathematical facts, so none is a
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The mounted Stage 1 `prove.sh` first compiles `verification.k` with all four
canonical rules into `verification-kompiled` and only then runs `kprove`.
Consequently, no Stage 1 command first proves the exact statement of any
canonical rule against a module that omits that rule.

`summary-test.k` does not establish the required ordering: it imports
`VERIFICATION`, so the four rules are already present while its finite ground
claims are checked. Its `#Top` output therefore validates ground reductions but
is not evidence that any rule was separately proved before admission.

Stage 1 describes the loop-invariant claim in `spec.k` as a derived lemma, but
that claim is not a rule in the canonical inventory and is therefore not added
to `trust-boundary.json`.

## Domain-lemma set

The domain-lemma set is empty.

No inventory rule is a trusted additional algebraic or domain fact. All four
rules are the base and step equations of the two proof summaries.

## Classification counts

- `DEFINITION`: 4
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
