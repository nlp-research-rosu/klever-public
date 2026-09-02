# Trust-boundary discovery

## Canonical inventory

The sole inventory authority is `/reference/rule-inventory.json`, with
`inventory_sha256`:

```text
2ba24efa71b132a7ac64fee85b3a68a5cdfa4cf4871a1b444364b99fc18a7951
```

It contains three rules, in `VERIFICATION`, and all three appear once in
`trust-boundary.json` in the canonical order. Every canonical `attributes`
array is empty, so the inventory contains no rule carrying `simplification`.

## Classification analysis

All three rules are `DEFINITION` clauses for the total proof-local function
`scanHappy(IntSeq, Int, Int, Int)`:

| Canonical rule | Classification | Reason |
|---|---|---|
| `rule-c81ca83083d7457acd8bc03869be055c6f82860af5fcb6ab0df7413577ec1931` | `DEFINITION` | Base clause: the summary of an empty remaining sequence is `true`. |
| `rule-424ad9bede59bccdcf23851333637603f57a311d80fcb5fef99140e39aae7991` | `DEFINITION` | Warm-up clause for `I < 2`: consume the head and advance the stored history without yet imposing a complete-window condition. |
| `rule-738ed76d501e1fe77a5aa4c3808cc7f2254b9f6b94e6b2a6378b84afed317e55` | `DEFINITION` | Steady-state clause for `I >= 2`: define the current window's pairwise-distinct condition and recurse on the tail. |

These rules have the proof-term head `scanHappy`; they do not match a `<k>`
cell, replace a Python construct, observe operational state, or bypass any
fixed-semantics step. They therefore are not `OPERATIONAL_RULE`.

The cases are structurally defining rather than additional facts. The empty
and constructor patterns are disjoint; for a constructor, `I <Int 2` and
`I >=Int 2` are disjoint and exhaustive. Both recursive cases descend from
`iCons(C, REST)` to `REST`. Consequently none is a `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

Stage 1 `prove.sh` lines 19–22 compile `verification.k` with all three
`scanHappy` rules already present, and lines 23–25 then run `kprove` against
that compiled definition. No earlier command proves any exact rule statement
against a module that omits it. Therefore Stage 1 provides no evidence meeting
the required ordering for `PROVED_DERIVED_LEMMA`.

Stage 1 does separately prove the `SPEC.loop-invariant` reachability claim as
part of the complete proof, and `PROOF.md` records the resulting `#Top`.
However, that claim is not a rule in the canonical inventory and does not turn
any of the three preloaded recurrence equations into a separately proved
derived lemma.

## Domain-lemma set

The domain-lemma set is empty.

The operational-rule set is also empty for this local verification-module
inventory. Operational Python behavior comes from the supplied imported
reference semantics, while the canonical local closure contains only the three
defining `scanHappy` equations.
