# Trust-boundary discovery

## Canonical inventory

The classification source is `/reference/rule-inventory.json`, with canonical
inventory SHA-256:

```text
932e796013ca30c337145920f57c5b5c304c9fb7d35633917a2a159a409a7759
```

It contains 17 rules, all from the local verification-module closure
`VERIFICATION-SYNTAX` and `VERIFICATION`. The inventory's verification hash
`c2216fe4ac0ed219a5fc6cc7a122a8476f63aa0bb3920533801703a8fd03f6a4`
matches the mounted `/reference/k-proof/verification.k`.

Each canonical `source_rule_id` appears exactly once and remains in inventory
order in `trust-boundary.json`.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 17 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 17 rules are definitions:

- `parseMusicBody` and `parseMusicCharBody` expand named proof terms into the
  exact source-level AST executed by the fixed semantics.
- `mutatedParseMusicBody` and `mutatedParseMusicCharBody` are analogous syntax
  definitions used only by the negative body-sensitivity probe.
- The three `nextCurrent` equations and four `nextResult` equations define the
  exhaustive guarded cases of a one-character mathematical state transition.
- The base/step pairs for `scanCurrent` and `scanResult` define structurally
  recursive folds over `IntSeq`.
- The two guarded `musicResult` equations define the final result, including
  the pending whole-note flush.

None of the inventory rules matches or rewrites a K configuration cell such as
`<k>`, `<heap>`, or `<scopes>`. Consequently, none is an ordinary execution or
observation rule in the verification model, so the `OPERATIONAL_RULE` set is
empty.

No canonical rule carries the `simplification` attribute. Thus there is no
simplification-attributed rule requiring a choice between `DEFINITION` and
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles the complete `verification.k`, including
all 17 canonical rules:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Every later `kprove` command uses that already compiled
`verification-kompiled` definition. Stage 1 contains no earlier command that
proves the exact statement of any canonical rule against a module from which
that rule is absent. Therefore no rule satisfies the required ordering for
`PROVED_DERIVED_LEMMA`.

`SPEC.scan-loop` is machine-checked in Stage 1 and is described in `PROOF.md`
as a derived auxiliary reachability claim. It is a claim in `spec.k`, however,
not a rule in the canonical local verification-module inventory. It therefore
does not create a `PROVED_DERIVED_LEMMA` entry in `trust-boundary.json`.

The body-mutation and false-postcondition runs are negative validation probes;
they reject changed claims but do not first prove any canonical rule.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule asserts an extra mathematical fact used to close the proof.
The guarded transition cases, recursive folds, AST expansions, and final-result
cases define their respective proof-local symbols. They are not unproved
algebraic, ordering, collection, or semantic facts layered on top of those
definitions.
