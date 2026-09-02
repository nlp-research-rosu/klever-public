# K declaration inventory summary

Inventory contains **949** declarations. The complete statement text and per-record review disposition are in `k-declaration-inventory.jsonl` and `k-declaration-inventory.tsv`.

## Counts by source class

- PROOF_LOCAL: 19
- SUPPLIED_BASELINE: 928
- TARGET_CLAIM: 2

## Counts by declaration kind

- claim: 2
- configuration: 1
- context: 5
- rule: 709
- syntax: 232

## Attribute/tag counts

- concrete: 35
- function: 151
- macro: 4
- no-evaluators: 22
- owise: 27
- priority: 45
- symbol: 25
- total: 114

## Counts by file

| File | Counts |
|---|---|
| `reference-semantics/semantics/assert.k` | rule=3 |
| `reference-semantics/semantics/bool.k` | context=1, rule=13 |
| `reference-semantics/semantics/builtins.k` | rule=137, syntax=38 |
| `reference-semantics/semantics/call.k` | rule=21, syntax=3 |
| `reference-semantics/semantics/comprehension.k` | rule=7, syntax=3 |
| `reference-semantics/semantics/concrete.k` | rule=16, syntax=5 |
| `reference-semantics/semantics/controls.k` | rule=34, syntax=3 |
| `reference-semantics/semantics/core.k` | configuration=1, rule=46, syntax=37 |
| `reference-semantics/semantics/dict.k` | rule=28, syntax=12 |
| `reference-semantics/semantics/float.k` | rule=121, syntax=34 |
| `reference-semantics/semantics/functions.k` | rule=15, syntax=4 |
| `reference-semantics/semantics/int.k` | rule=16, syntax=1 |
| `reference-semantics/semantics/iter.k` | syntax=1 |
| `reference-semantics/semantics/list.k` | rule=27, syntax=5 |
| `reference-semantics/semantics/methods.k` | rule=75, syntax=27 |
| `reference-semantics/semantics/operators.k` | context=2, rule=10 |
| `reference-semantics/semantics/range.k` | rule=6, syntax=2 |
| `reference-semantics/semantics/set.k` | rule=12, syntax=6 |
| `reference-semantics/semantics/sort.k` | rule=19, syntax=6 |
| `reference-semantics/semantics/str.k` | rule=28, syntax=5 |
| `reference-semantics/semantics/subscript.k` | context=2, rule=40, syntax=15 |
| `reference-semantics/semantics/syntax.k` | syntax=16 |
| `reference-semantics/semantics/tuple.k` | rule=21, syntax=4 |
| `spec.k` | claim=2 |
| `verification.k` | rule=14, syntax=5 |

## Interpretation

Every supplied-semantics declaration is accepted only at the selected trusted `SUPPLIED_SEMANTICS` level after recursive byte/type integrity checking. This does not bless any `verification.k` extension. Every proof-local declaration has an individual decision in the complete inventory. Opaque/no-evaluator supplied symbols are inventoried but are unused by `solution.mpy`.
