# Trust-boundary discovery

## Canonical scope

The exhaustive source for this classification is
`/reference/rule-inventory.json`, with inventory SHA-256
`c0628bc9c6a3e07fd361ebae705579a2a3cf61c51cc51b40398ddd545b5fe37b`.
It contains six rules, all from the local `VERIFICATION` module. The output
preserves their canonical order and classifies each `source_rule_id` exactly
once.

## Classification result

All six rules are `DEFINITION`.

- The first four rules are the exhaustive guarded cases and recurrence for the
  named `primeScan` mathematical summary. They match only summary terms, not K
  execution configurations, and therefore are not operational rules.
- The final two rules are the exhaustive guarded equations for the named
  `primeResult` proof term. They define the result summary directly and through
  `primeScan`.

The inventory contains no rules with the `simplification` attribute. It also
contains no rule that observes or advances Python execution, so the
`OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

The Stage 1 `/reference/k-proof/prove.sh` first compiles
`/reference/k-proof/verification.k` with all six inventory rules already
present, and then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That run proves the reachability claims and produces `#Top`, but it does not
first prove the exact statement of any inventory rule against a module that
omits that rule. The later body-mutation and vacuity commands are negative
probes, not prior proofs of reusable rule statements. Consequently, no
inventory rule satisfies the required ordering for
`PROVED_DERIVED_LEMMA`.

`SPEC.prime-loop` is a reachability claim in `spec.k`, not a rule in the
canonical verification-module inventory. It therefore receives no rule
classification here.

## Domain lemmas

The domain-lemma set is empty. None of the six rules is an additional trusted
mathematical fact used alongside a definition; each is part of the guarded
definition of `primeScan` or `primeResult`.
