# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`88adbf942eb1c766f28585672f908061a5c3385bad356f21790fe5db810b2d20`.
It contains six rules in the local `VERIFICATION`-module closure. The output
preserves that order and classifies every canonical `source_rule_id` once.

## Classification summary

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-fef3abb92ec888abf14e3bf9a2fd8f282df0e342c4122d6cd092d876bcb85646` | `DEFINITION` | Guarded base clause for `sequenceAcc`. |
| 2 | `rule-43f49722bb57ff9eafcc5227f4b4353cd12742df4bb56c784efe6e413736cdbf` | `DEFINITION` | Guarded recursive clause defining one accumulator step. |
| 3 | `rule-d55499ddc47bd6adf4d30b16fdbd3314a5db1919e0074fd704e4bfe2e4543f7c` | `DEFINITION` | Symbolic exposure of the exact same base equation as inventory position 1. |
| 4 | `rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc` | `DOMAIN_LEMMA` | Inductive fold used to normalize a successor summary back to the preceding summary; it is not separately proved before use. |
| 5 | `rule-02288b5620299a0a1ac5b02b112560d2ffdd21df6457ef2054ea9f3746dbef3b` | `DEFINITION` | Negative-input clause for `stringSequenceCodes`. |
| 6 | `rule-975c7f6f0a3b75ffe8b642274c4103c08f2594d0bccd1678e974201218b3ab16` | `DEFINITION` | Nonnegative-input clause for `stringSequenceCodes`. |

There are no local `OPERATIONAL_RULE` classifications. Every inventoried rule
rewrites a mathematical summary term; none matches a K configuration cell,
program AST execution step, call, continuation, or observation.

## Simplification rules

All four rules carrying `simplification` satisfy the required classification
restriction:

- The concrete base and recursive clauses are `DEFINITION`.
- The symbolic base is also `DEFINITION` because its statement is identical to
  the base defining equation; the second copy changes applicability during
  symbolic simplification but adds no new mathematical assertion.
- The inductive fold is `DOMAIN_LEMMA`. It is a distinct reverse-oriented
  proof helper, not a defining clause needed to give `sequenceAcc` its
  base/recursive meaning. Its mathematical justification is the recurrence,
  but the mounted evidence does not machine-check the exact fold before
  importing it into the target proof.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The ordering in `/reference/k-proof/prove.sh` is decisive:

1. Lines 23–26 compile `/reference/k-proof/verification.k` into
   `verification-kompiled`; that module already contains all six canonical
   rules, including the symbolic base and inductive fold.
2. Lines 27–29 then run the first positive `kprove` command against that
   compiled definition.
3. Lines 34–40 run negative mutation probes against the same definition; they
   do not prove either simplification rule.

No Stage 1 artifact first proves the exact statement of any reusable rule
against a module that omits that rule. The prose derivations in
`/reference/k-proof/PROOF.md` are useful mathematical rationales, but they do
not meet the required proof-ordering and exact-correspondence test.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc`
  — the inductive `sequenceAcc` fold simplification.

Consequently, the finalized K proof is conditional on this fold equality as a
trusted mathematical fact in addition to the definitions and the supplied
operational semantics.
