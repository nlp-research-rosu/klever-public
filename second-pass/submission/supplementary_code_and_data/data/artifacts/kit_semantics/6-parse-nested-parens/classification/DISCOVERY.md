# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`f6ae86ecd9aba28a5a6fa67cf78bae5b8d0e9e654b6f39f4c9f86485764a27b3`.
It contains 37 rules, all in the sole local verification module
`VERIFICATION`. `trust-boundary.json` preserves their inventory order and
classifies every `source_rule_id` exactly once.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 37 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 37 rules are equations or structural recurrences for symbols declared as
total functions:

- Rules 0–3 expand the named AST terms `loopBody`, `afterLoop`,
  `solutionBody`, and `solutionModule`.
- Rules 4–29 define the scanner state transitions, recursive scan summaries,
  final-output construction, and the initialized `expectedDepths` result.
- Rules 30–36 define the recursive well-formed-input predicate and its
  initialized `validInput` wrapper.

These rules name program syntax or mathematical summary values. None is a
configuration-cell rewrite, observation rule, or ordinary execution step in
the verification model, so the `OPERATIONAL_RULE` set is empty. Operational
execution comes from the imported fixed `MPY` reference semantics, whose rules
are not entries in this canonical local-module inventory.

The canonical `attributes` array is empty for every entry. In particular,
there are no rules carrying the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived rules.

The Stage 1 `/reference/k-proof/prove.sh` first compiles
`verification.k`, which already contains all 37 inventory rules, and only then
runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The corresponding `/reference/k-proof/positive-proof.log` contains `#Top`.
That is evidence for the reachability claims under the already-loaded rule
set; it is not evidence that any inventory rule's exact statement was first
proved against a module omitting that rule. No earlier bridge-free proof
command, separate proof module, or exact rule-admission step appears in
`prove.sh`.

`SPEC.scan-loop` in `/reference/k-proof/spec.k` is an auxiliary reachability
claim and is checked in the positive proof run. It is not a canonical
`source_rule_id`, and Stage 1 does not convert its exact statement into a
subsequently admitted reusable rule. The vacuity and body-mutation commands are
expected-failure validation probes, not derived-rule proofs.

Accordingly, no rule is classified as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty.

The scanner and well-formedness rules are the defining equations of their
declared functions, including exhaustive guarded cases and structurally
recursive base/step equations. They do not assert an additional reusable
mathematical fact beyond those definitions, so they are `DEFINITION` rather
than `DOMAIN_LEMMA`.
