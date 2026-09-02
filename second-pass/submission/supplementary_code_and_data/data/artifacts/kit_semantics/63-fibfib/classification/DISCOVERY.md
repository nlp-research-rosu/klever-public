# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`080f92c29f904570f666abf93dd802a1044388939b36ecd9797a9376820299d0`.
It contains six rules, all in `VERIFICATION`. Each canonical
`source_rule_id` is classified exactly once below and remains in inventory
order.

| Inventory position | Classification | Reason |
|---:|---|---|
| `rule-06e1ae240693f799ce5130532e40e2196313cdc7ac6b6067bac3cd310e9cfd53` | `DEFINITION` | Defines the `fibfibSpec` base value at index zero. |
| `rule-f91d06a620555e1485c35fdc8d70bba92bebc55eb1fadee46446005d2421e7f5` | `DEFINITION` | Defines the `fibfibSpec` base value at index one. |
| `rule-007e98cae0e9af21de6bac31ce4a143f86fee76972413486a57af84eb56fa95b` | `DEFINITION` | Defines the `fibfibSpec` base value at index two. |
| `rule-333596937108b8fb4ac5df990a0688da5577451e2655490b18f74c0ac3b1f091` | `DEFINITION` | Gives the guarded recurrence defining `fibfibSpec` for indices at least three. |
| `rule-abff69f2453cb9b7d3c8463704b5988785face92a498d2d0c64f5716c9b01a2f` | `DEFINITION` | Totalizes `fibfibSpec` for negative integers, outside the proved input domain. |
| `rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8` | `DOMAIN_LEMMA` | Adds the shifted recurrence as a simplification fact used to close the loop invariant; it is not separately proved before admission. |

## Definitions

The first five rules are equations constituting the named mathematical
summary. The first three are its base cases, the fourth is its recurrence on
the intended nonnegative domain, and the fifth is a disjoint totalization case
for negative integers. None matches a Python execution configuration or
observes operational state, so none is an `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

Stage 1 provides no proof with the required ordering. In
`/reference/k-proof/prove.sh`, the Haskell definition is compiled directly
from `/reference/k-proof/verification.k`, which already contains all six
canonical rules. The subsequent `kprove spec.k` command therefore proves the
program claims in a theory that already includes the shifted-recurrence
simplification. The negative probes reuse the same compiled definition.
Neither `prove.sh` nor another mounted Stage 1 artifact first proves the exact
simplification rule against a module from which that rule is absent. The
comment and prose calling it a derived lemma are not qualifying proof evidence.

## Domain lemmas

The domain-lemma set is **not empty**. Its sole member is
`rule-2c1e06471f4016481e42f60cdb6c9983f09da5b801cc9dc90ba306594047c7a8`.
It carries the `simplification` attribute, so the allowed classification is
`DOMAIN_LEMMA` rather than `PROVED_DERIVED_LEMMA`. Its mathematical plausibility
as a shifted form of the recurrence does not replace the benchmark's required
separate, rule-free Stage 1 proof.

## Operational rules

The canonical local verification-module inventory contains no
`OPERATIONAL_RULE` entries. The imported reference semantics is part of the
fixed model, but its rules are not present in the launcher-provided canonical
inventory and therefore are not added to this classification output.
