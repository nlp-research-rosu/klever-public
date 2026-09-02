# K proof trust-boundary discovery

## Canonical scope

This classification uses `/reference/rule-inventory.json` as the exhaustive
inventory of the local verification-module closure. Its canonical
`inventory_sha256` is
`e967335267fe43883ba33230aa4151fb286d4237327166d38f9c73941c614d2b`.
The inventory contains 11 rules, all from `VERIFICATION`, and
`trust-boundary.json` preserves their canonical order.

The classification totals are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

## Rule classifications

| Inventory position | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-d39c65c361a04494ea4bbc0d7da105a5e581cf169c07c502ff73be17a3291eae` | `DEFINITION` | `overlapLength` is a pure equation defining the interval-overlap summary. |
| 1 | `rule-9ba556783237da1b35ba406043b46667d41336798e2d73985610f972d35ace31` | `DEFINITION` | This is the true-flag base equation for `scanHasDivisor`. |
| 2 | `rule-8c03a8287d60d83cb1f7b1e3e939abef2b3a70e6e9b849b699f9a92c0c04da47` | `DEFINITION` | This totalizing equation normalizes a scan starting below 2 to start at 2. |
| 3 | `rule-cbdf8169fcc3ad7f374ff7043b01e95fdd8553e9e71602765a1cb6bc2be276f6` | `DEFINITION` | This is the empty-range base equation at or beyond `N`. |
| 4 | `rule-7aa9640fdd3d0a7fae00e8405951aeef3032f94eac83b2986db8444d7a440970` | `DEFINITION` | This is the defining divisor-found case. |
| 5 | `rule-9d883d30e3dc643451f9c6b495149a2825d220410cfb6af1b0eaa6667da1097d` | `DEFINITION` | This is the recursive non-divisor case that advances the scan index. |
| 6 | `rule-5464006d80f33f5fc975672d11f260f30dc67367228f691333955f474bcc16f3` | `DEFINITION` | This `[simplification]` rule repeats the position-1 defining equation exactly, apart from proof-control attributes. |
| 7 | `rule-5397c59dca3c3fdbd353b530e08c7ce17c5d56052c9dfc863b7725bda7f01106` | `DEFINITION` | This `[simplification]` rule repeats the position-3 defining equation exactly, apart from proof-control attributes. |
| 8 | `rule-b538396a9a5a6ab14036d6fd6bbae17ed3358e6c9a6e0611c302001e4e358333` | `DEFINITION` | This `[simplification]` rule repeats the position-4 defining equation exactly, apart from proof-control attributes. |
| 9 | `rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4` | `DOMAIN_LEMMA` | This `[simplification]` rule reverses the position-5 recurrence so a post-iteration `scanHasDivisor(false, N, D + 1)` folds to the invariant at `D`. It is an additional mathematical fact in the proof theory, and Stage 1 does not separately prove it before use. |
| 10 | `rule-983202dd3d105fa6a5f593a9222e54e761e7c2e4313c4ea910e8029a732a355f` | `DEFINITION` | `primeResult` is a pure equation defining the named result summary. |

The rules classified as definitions rewrite only mathematical summary terms.
None matches an MPY configuration, continuation, environment, scope, heap, or
control cell, so the canonical inventory contains no ordinary execution or
observation rule to classify as `OPERATIONAL_RULE`.

The first three `[simplification]` entries introduce no new value equation:
their left-hand sides, right-hand sides, and guards duplicate earlier
`[concrete]` defining cases. The fourth `[simplification]` entry is different:
it reverses the recursive defining orientation specifically to fold a symbolic
loop step. It is therefore recorded as trusted mathematical support rather
than as another defining case.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 ordering evidence is `/reference/k-proof/prove.sh`:

- Lines 17–20 compile the complete `/reference/k-proof/verification.k` as
  module `VERIFICATION`. That source already contains all four
  `[simplification]` rules at lines 50–63.
- Lines 21–23 then run the sole positive `kprove` command over `spec.k`
  against that already-extended compiled definition.
- Lines 33–35 run the expected-failure vacuity probe against the same complete
  definition; this is neither an earlier proof nor a proof of an inventory
  rule.
- Lines 51–58 compile the distinct mutation module and run another
  expected-failure target probe. That probe does not state or prove the exact
  proposition of any inventory rule.

The claims in `/reference/k-proof/spec.k` are two loop reachability claims and
the whole-program target claim. They do not provide an earlier, exact statement
of any canonical rule proved against a module lacking that rule. Consequently,
the Stage 1 report's informal description of the simplification rules as
"derived" is not sufficient for the stricter `PROVED_DERIVED_LEMMA`
classification required here.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-7dcc581fc2eb7b71715119443ca2ecc1192932d0a0273a3e90bd21562ae85ff4`,
  the guarded reverse-fold fact for `scanHasDivisor`.

The successful `#Top` in `/reference/k-proof/proof.out` establishes the Stage 1
claims only under the verification module that already contains this rule.
Thus that success is evidence that the proof uses the extended theory, not
evidence of an independent derivation of the fold fact.
