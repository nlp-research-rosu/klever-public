# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` has SHA-256
`de92531aa585b933c077c7b03978617a1478b0e8962fb9284eb6a300e9f8de76`
and contains six rules. `trust-boundary.json` preserves that inventory order
and classifies each `source_rule_id` exactly once.

## Classifications

| Inventory rule | Classification | Reason |
|---|---|---|
| `rule-4118d893fdb23a03019d470e2b1c6fcba5249000dd31f5eede7a49b9bb496c57` | `DOMAIN_LEMMA` | The simplification `intToF(I) => proofIntToF(I)` relates an existing supplied primitive to a fresh opaque proof term. Stage 1 calls this relation conditional trust assumption T1. It is installed before the target proof and is not independently proved. |
| `rule-8198bac7b8824309265af7441122c8de309aa29e610f052e2ef585d0cf940c16` | `DEFINITION` | Defines the nullary `triangleProgram` name by expanding it to the exact program syntax tree. |
| `rule-211b8b0393e5ae2a5e8ee78c603f8efc838adffd3c3e11440d210eb7aa3e3394` | `DEFINITION` | Defines the invalid-triangle predicate as the three side-sum comparisons. |
| `rule-563c1f5294a0f04495366f41b46928debc138e2960273a2b7233fbf30037a326` | `DEFINITION` | Defines the semiperimeter summary. |
| `rule-9e3d2b1def67f5eadfc05db79e46d7a27f186bfa84d0fcfeca76f52099eff93a` | `DEFINITION` | Defines the product used by Heron's formula. |
| `rule-0824bba9e5ff88475bdea02d8e1fe2faeda87b8b33bf10adc9aeee485a1e94c7` | `DEFINITION` | Defines the complete result summary from the invalidity predicate, Heron product, square root, and rounding operation. |

The five definitions introduce named structural or mathematical terms. None
updates a configuration cell or supplies an ordinary program-execution step,
so the canonical local inventory contains no `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`;
that module already contains all six canonical rules. It then runs `kprove`
against that compiled definition. There is no earlier positive proof against a
module omitting any candidate rule, and no evidence connecting such a prior
claim's exact statement to a later installed rule. The false-postcondition and
body-mutation commands are expected-failure probes, not proofs of reusable
rules.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-4118d893fdb23a03019d470e2b1c6fcba5249000dd31f5eede7a49b9bb496c57`
  (`intToF(I) => proofIntToF(I) [simplification]`).

Stage 1 `PROOF.md` identifies the equality represented by this rule as
conditional trust assumption T1. The concrete LLVM equation and smoke tests
are supporting evidence, but Stage 1 provides no rule-free universal K proof
of this exact simplification. It therefore remains inside the proof's trusted
mathematical boundary.

## Totals

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 1
