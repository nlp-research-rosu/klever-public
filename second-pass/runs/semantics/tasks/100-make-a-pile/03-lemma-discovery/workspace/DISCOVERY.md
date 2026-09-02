# K proof trust-boundary discovery

The canonical inventory contains nine rules from the local
`PILE-VERIFICATION` module closure. Every `source_rule_id` is classified once,
in canonical inventory order, in `trust-boundary.json`.

## Definitions

Seven rules are `DEFINITION`:

- `pileCondition`, `pileLoopBody`, `pileBody`, `pileClosure`, and `pileModule`
  are macro expansions naming exact program or proof terms.
- The two guarded `pile(N, I)` equations are the base and recursive cases of
  the mathematical sequence summary. They define the suffix
  `[N + 2*I, ..., N + 2*(N-1)]`.

These rules introduce named representations and their equations; they do not
add independent mathematical facts about an existing operation.

## Operational rules

No canonical inventory rule is classified as `OPERATIONAL_RULE`. The ordinary
Python execution rules come from the supplied `MPY` semantics, outside this
launcher inventory. The local closure contributes only proof-term definitions,
the `pile` recurrence, and two mathematical simplifications.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 `prove.sh` first compiles `verification.k` as
`PILE-VERIFICATION`. That compiled module already contains all nine inventory
rules. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module PILE-PREFIX-SPEC
kprove spec.k --definition verification-kompiled --spec-module PILE-LOOP-SPEC
```

Both commands prove reachability claims from `spec.k`; neither first proves an
inventory rule against a module that omits that rule. Consequently, the two
successful `#Top` results do not establish any inventory entry as a reusable
proved-derived rule.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb`:
  `valSeqConcat(VS, .ValSeq) => VS`, the right-identity law.
- `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97`:
  associativity of `valSeqConcat`.

Both carry the `simplification` attribute. The supplied MPY list semantics
already defines `valSeqConcat` by recursion on its first argument, so these
rules are additional mathematical facts rather than defining equations for
the operation. They are present in the symbolic definition before either
`kprove` invocation and have no separate Stage 1 proof evidence. They are
therefore trusted `DOMAIN_LEMMA`s, regardless of the nearby comment describing
them as identities used by the proof.
