# K rule trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with canonical
inventory hash:

```text
5441f1019df2fff08e7d49cef4c2328a260cfe74823aaf96249b80c5cc44d8e7
```

It contains 14 rules, all in the mounted Stage 1 `VERIFICATION` module.
`trust-boundary.json` preserves their inventory order and classifies each
`source_rule_id` exactly once.

## Classification method

I inspected the canonical rule text, attributes, and source locations, then
checked the read-only Stage 1 `verification.k`, `spec.k`, `prove.sh`,
`PROOF.md`, and recorded proof output.

The classification is behavioral:

- `#fixSpacesLoopBody` and `#fixSpacesBody` are nullary equations that expand
  named proof terms to translated ASTs. The supplied semantics subsequently
  executes those ASTs, so these are definitions rather than operational rules.
- `pendingSpace`, `resultAfter`, `pendingAfter`, and `charAfter` are guarded
  or constructor-based base/recursive equations defining mathematical state
  summaries.
- `fixedSpaces` is a wrapper definition combining the two final string-state
  summaries.

No inventoried rule matches a `<k>` cell or another configuration cell, and no
inventoried rule observes or advances program execution. Consequently, the
`OPERATIONAL_RULE` set is empty.

## Simplification rules

The canonical inventory has two rules carrying `simplification`:

| Source rule | Classification | Reason |
|---|---|---|
| `rule-2474ff592cce4297eb234f57f5266cadd5c79784f4555511da449c9dc39aecd8` | `DEFINITION` | Guarded non-space recurrence for `resultAfter`; it consumes one input constructor and defines the summary's next state. |
| `rule-38a7a54771406f0fcf4f53d56873c51b354f06859365120b1441f6bd9ad3b4a8` | `DEFINITION` | Guarded non-space recurrence for `pendingAfter`; it consumes one input constructor and defines the reset state. |

The attribute controls simplifier use, but neither rule states a separate
mathematical fact beyond its function's defining recurrence. Both therefore
remain `DEFINITION`, as required for definitional simplification equations.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`,
with every one of the 14 canonical rules already included. Its later `kprove`
commands prove `SPEC.loop-invariant` and the complete `SPEC` against that
compiled definition. There is no earlier proof against a module omitting any
inventoried rule, no later admission step, and no evidence pairing a
bridge-free proof with an exact subsequently added rule. Thus no canonical
rule satisfies the required proof-before-admission ordering for
`PROVED_DERIVED_LEMMA`.

The Stage 1 reachability claim called `SPEC.loop-invariant` is proved and is
described in `PROOF.md` as a derived circularity, but it is a claim in
`spec.k`, not a rule in the canonical verification-module inventory. It
therefore receives no entry in `trust-boundary.json`.

## Domain lemmas

The domain-lemma set is empty.

Every inventoried mathematical rule is part of an exhaustive structural or
guarded definition. None is an additional algebraic, logical, or domain fact
trusted merely to close the proof. In particular, the two simplification
rules are defining recurrence cases rather than `DOMAIN_LEMMA` assumptions.

## Totals

| Classification | Count |
|---|---:|
| `DEFINITION` | 14 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 14 canonical rules are classified exactly once.
