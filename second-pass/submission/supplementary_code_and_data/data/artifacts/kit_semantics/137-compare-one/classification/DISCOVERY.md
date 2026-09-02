# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is the exhaustive canonical inventory for the
local verification-module closure. It identifies module `VERIFICATION`, has
inventory SHA-256
`1cd9fe93dd4e5f480fc8b0770b4cb85ca6a17dd249f6990ca5b632e97f3c8833`,
and contains seven rules. The classification preserves those seven rules in
their canonical inventory order.

The mounted Stage 1 files were inspected read-only. In particular, the audit
checked `verification.k`, `spec.k`, `prove.sh`, `kprove.out`, `prove-run.out`,
the mutation specs and outputs, and `PROOF.md`. The inventory records an empty
attribute list for every rule, so no rule carries `simplification`.

## Rule classifications

| Canonical position | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-96a2b157eb261582571b58f8f4baca708344f5f934ab0dfd73a528a2cf06f6c3` | `DEFINITION` | Defines the nullary term `solutionModule()` as the exact `Module(...)` AST. Fixed `#loadAll`, lookup, call, binding, branch, return, and frame rules still execute the body. |
| 1 | `rule-6350669bfe107188f21ff8bcfb62369235f77456d1376006cebb32ea27e6f927` | `DEFINITION` | Defines `numericValue` as identity on `Int`. |
| 2 | `rule-cb4eededb7164c4ac333f7b361070f4e5798d337f589fa27bb6097cb9ae3ab26` | `DEFINITION` | Defines `numericValue` as identity on `Float`. |
| 3 | `rule-d42ee113ac1215c861819fe9dcefdf1fa290428f59dbaaed2952c8129135abb6` | `DEFINITION` | Defines the string case of `numericValue` using the supplied comma replacement and decimal-conversion summaries. |
| 4 | `rule-e2ace12cf9853e8f73043e00ef4021593fc0c87ff79e215abe9a4e1766c7adad` | `DEFINITION` | Defines the first guarded case of `expectedCompare`, returning `A`. |
| 5 | `rule-720e10405d2c95cf48ae7c5ffc80b5602085ca1a1b5cd84bc13950733f69d925` | `DEFINITION` | Defines the second, disjoint guarded case of `expectedCompare`, returning `B`. |
| 6 | `rule-34489340280ac69ec4b5418b1966f3a449892bb755759a19583a03a3dd033c01` | `DEFINITION` | Defines the remaining guarded case of `expectedCompare`, returning `noneV`. |

The three `numericValue` equations are constructor cases of a mathematical
summary. The three `expectedCompare` equations are pairwise-disjoint guarded
cases defining the result summary. They state what those proof-local symbols
mean; they do not rewrite an operational configuration or add an independent
ordering theorem.

`solutionModule()` is also a definition rather than an operational rule. Its
right-hand side is syntax consumed later by the imported fixed semantics. Stage
1 additionally compared execution of `solution.mpy` with execution of the
named term and obtained byte-identical final KORE configurations, but that
evidence does not change the equation's definitional character.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's positive `kprove` command proves the target claims from `spec.k`
against `verification-kompiled`, which already contains all seven inventory
rules. It does not first prove any inventory rule's exact statement against a
module from which that rule is absent. The AST-identity `cmp` is an execution
comparison, and the false-postcondition and changed-body runs are negative
validation probes; none is a separate proof satisfying the required ordering
for `PROVED_DERIVED_LEMMA`.

## Operational and domain rules

There are no local `OPERATIONAL_RULE` entries. No inventory rule matches a
`<k>` configuration, intercepts a call, changes state, or observes execution.
Ordinary execution is supplied by imported `MPY` modules, whose rules are
outside this canonical local inventory.

The `DOMAIN_LEMMA` set is empty. None of the seven rules adds a trusted
mathematical fact beyond defining `solutionModule`, `numericValue`, or
`expectedCompare`. The opaque numeric primitives discussed in the Stage 1
trust ledger belong to the supplied reference semantics and are not rules in
this canonical inventory.

## Completeness checks

- Output rule count: 7.
- Canonical inventory rule count: 7.
- Every canonical `source_rule_id` occurs exactly once.
- Output order exactly matches inventory order.
- Every classification is one of the four allowed values.
- Every rationale is nonempty.
- Top-level JSON keys are exactly `schema_version`, `inventory_sha256`, and
  `rules`; every rule object has exactly the three required keys.
- The copied inventory SHA-256 exactly matches the canonical value.
