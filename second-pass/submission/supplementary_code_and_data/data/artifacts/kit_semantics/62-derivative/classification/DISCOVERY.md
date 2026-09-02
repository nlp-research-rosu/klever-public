# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`. Its embedded
`inventory_sha256` is
`0d47ff2367ef2c6bf87c730b4ca6f2d2c6d07dfa5c78f5d7fc08aad9fbf67f69`.
It contains five rules, all in the single local verification module
`VERIFICATION`. `trust-boundary.json` preserves their canonical order and
classifies each `source_rule_id` exactly once.

## Classifications

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-82fd85d7d877438e349407a829d1e35806842c5943d9c0f294aa58ed3173779c` | `DEFINITION` | Empty-sequence base equation for the recursive `derivAcc` summary. |
| 2 | `rule-51a3749a6415a476a599f9f4b4d86298466c83cbf2e19efd98a63953ec251c03` | `DEFINITION` | Guarded nonpositive-index recurrence for `derivAcc`. |
| 3 | `rule-699bb53c2b20d45244efa55313af6891bd44df240c352ce9088ca451eccca62c` | `DEFINITION` | Guarded positive-index recurrence for `derivAcc`, including the next fixed-semantics multiplication term. |
| 4 | `rule-69d164c2333b75d39789a2087d0efc8310446075e2ed8ca85aaa99880622898f` | `DEFINITION` | Empty-sequence base equation for the structural `noRefsVS` predicate. |
| 5 | `rule-cdffeaf04d811ef623fa1b34b1412c6bea8d70a043f5ca0aa93d9bec48680e9a` | `DEFINITION` | Recursive cons equation for `noRefsVS`. |

The first three rules carry `simplification`. Each is classified as
`DEFINITION`, as required: together they define `derivAcc` by empty, skipped
index, and appended-product cases. They simplify occurrences of the named
mathematical summary and do not match a `<k>` execution configuration.

The two `noRefsVS` rules are also definitions. Although the predicate occurs in
the proof's input-domain precondition, these equations introduce its structural
meaning; they do not assert a further fact about a previously defined domain.

No inventory rule is an `OPERATIONAL_RULE`. None has an execution construct,
observation context, or configuration cell on its left-hand side. In
particular, mentioning the fixed `applyBin` term on the right-hand side of the
positive `derivAcc` recurrence does not intercept or replace execution.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`;
that compiled definition already contains all five canonical rules. It then
runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The target output is `#Top`, but this proves the reachability claims using the
definition that already contains the five rules. The later vacuity and body
mutation commands use that same compiled definition. Stage 1 contains no prior
`kprove` command against a module with any canonical rule removed, and no
artifact proves an exact reusable rule statement before admitting that rule.
Accordingly, neither comments nor successful target execution justify a
`PROVED_DERIVED_LEMMA` classification.

The `derivative-loop` item in `spec.k` is a reachability claim, not a rule in
the canonical inventory, so it is outside the required rule classification.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule adds a trusted mathematical fact beyond a named recursive
definition. In particular, `noRefsVS` defines the domain predicate itself, and
the `derivAcc` equations define the result summary; none is a separately
assumed theorem used to close the proof.
