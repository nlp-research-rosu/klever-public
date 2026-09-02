# Trust-boundary discovery

## Canonical scope

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory. Its copied inventory digest is:

```text
ed9455742263e4ffcb296214aa731ac41511e0935ee388f6e3e45782ae9df00f
```

The inventory has 14 rules, all from module `VERIFICATION`. Each canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 4 |

The seven rules carrying `concrete` are the guarded recursive and base
equations for `factRun`, `totalRun`, and `resultRun`; they are
`DEFINITION`s. Three `simplification` rules repeat the corresponding
`I > N` base equations with identical left-hand sides, right-hand sides, and
guards, so those are also `DEFINITION`s.

No inventoried rule matches a K configuration cell or executes/observes a
source-language construct. Consequently, the `OPERATIONAL_RULE` set is empty.

## Domain lemmas

The domain-lemma set is **not empty**. It contains these four reverse-step
simplification rules:

- `rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7`
  folds `factRun(I+1,N,F*I)` to `factRun(I,N,F)` under `I <= N`.
- `rule-5aa051dcb3d8aa1545bc998933e91b5adea53c25b6565ff7e8213e15b8ba1b66`
  folds `totalRun(I+1,N,T+I)` to `totalRun(I,N,T)` under `I <= N`.
- `rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7`
  folds the even-index advanced `resultRun` term under the even guard.
- `rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac`
  folds the odd-index advanced `resultRun` term under the odd guard.

These rules express the reverse equalities of the defining recurrences, but
they are oriented specifically to close symbolic circularity. Under the
benchmark classifications, they are additional mathematical facts unless
Stage 1 first proves their exact statements without having them available.
That prerequisite is not met, so they are `DOMAIN_LEMMA`s rather than
`PROVED_DERIVED_LEMMA`s.

## Separately proved derived lemmas

There are **no separately proved derived lemmas**.

The mounted `/reference/k-proof/prove.sh` first compiles
`verification.k`—including all 14 canonical rules—into
`verification-kompiled`. It then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Thus both positive proofs already have every reverse-step simplification
available. `spec.k` proves the loop invariant and the function-correctness
claim; it does not state or prove any of the four exact reverse-step rules in a
module excluding those rules. The vacuity and body-mutation commands reuse the
same compiled definition and are negative probes, not prior lemma proofs.

Stage 1 `PROOF.md` calls the reverse-step rules “derived lemmas” and gives a
paper justification from symmetry of the recurrences. That documentation is
not the ordering evidence required for `PROVED_DERIVED_LEMMA`: no Stage 1
`kprove` command first establishes an exact reverse-step statement against a
rule-free definition.

## Trust-boundary consequence

The target proof is conditional on the four `DOMAIN_LEMMA` equalities in
addition to the supplied semantics and the ten summary definitions. This
classification does not introduce an alternative theorem or replacement
statement; it records only the canonical K rules and their proof status.
