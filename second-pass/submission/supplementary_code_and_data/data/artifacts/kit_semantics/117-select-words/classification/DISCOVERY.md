# Trust-boundary discovery

## Canonical inventory

The sole classification source was
`/reference/rule-inventory.json`, whose copied inventory hash is:

```text
b8a651c082f47c4331d73fb06595968cd0537666f9d79a596a98bb456cea6f9e
```

It contains 22 rules, all in the local `VERIFICATION` module. The output keeps
their canonical inventory order and classifies every `source_rule_id` exactly
once.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 22 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The first three rules define the proof-only statement names
`charLoopBody`, `afterCharLoop`, and `selectWordsBody` by expanding them to
their exact MPY syntax trees. They are macro-like named-term definitions. They
do not match a `<k>` cell, inspect a configuration, or add execution behavior,
so they are not operational rules.

The remaining nineteen rules all carry the `simplification` attribute. They
define the mathematical summary functions `flushSelected`, `selectScan`,
`scanAccum`, `wordAfter`, `countAfter`, and `charAfter`. Their cases are base
equations or structurally decreasing recurrences:

- `flushSelected` partitions count mismatch, equal count with an empty word,
  and equal count with a nonempty word.
- `scanAccum` partitions an empty suffix, delimiter cases, and non-space
  vowel/non-vowel cases while consuming one character in every recurrence.
- `wordAfter` and `countAfter` define the final loop-local values by consuming
  one character per recursive equation.
- `charAfter` defines the last bound loop character.
- `selectScan` composes those definitions into the final result summary.

These are equations defining proof terms and mathematical summaries, not
additional algebraic facts about previously defined operations. Therefore
every simplification rule is classified as `DEFINITION`, satisfying the
requirement that a simplification rule be either `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 evidence does not demonstrate the ordering required for
`PROVED_DERIVED_LEMMA`. In `/reference/k-proof/prove.sh`, the Haskell
definition is compiled directly from `verification.k`, which already contains
all 22 canonical rules:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

`/reference/k-proof/proof-positive.out` contains `#Top`, but that proves the
reachability claims with all inventory rules already installed. Neither
`prove.sh` nor another mounted Stage 1 artifact first proves the exact statement
of any inventory rule against a module that omits that rule. The loop
circularity in `spec.k` is a claim, not a canonical inventory rule, and does not
change this classification.

## Operational and domain-lemma sets

The operational-rule set is empty. The canonical local inventory contains no
ordinary configuration or observation rule; operational Python behavior comes
from the separately supplied reference semantics, outside this canonical local
rule inventory.

The domain-lemma set is explicitly empty. No canonical rule asserts an
additional trusted mathematical fact beyond the defining equations described
above.

No Lean statement, replacement theorem, or alternative formulation is included
in the JSON.
