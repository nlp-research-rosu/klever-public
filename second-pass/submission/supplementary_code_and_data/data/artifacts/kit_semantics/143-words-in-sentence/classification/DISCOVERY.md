# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`:

```text
2da0b74c0f727c025741ac5cb91807cc58ba40be9a2dbd5600b8df75788bc112
```

It contains 18 rules, all in the local `VERIFICATION` module. Every canonical
`source_rule_id` is classified exactly once and in canonical order in
`trust-boundary.json`.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 18 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All six `#...` rules are macro equations that define the exact program AST.
They expand named syntax and do not perform runtime execution.

The remaining twelve rules define newly introduced proof-summary symbols:

- the two complementary equations for `primeLength`;
- the total accumulator definition `emitWord`;
- the base and recursive clauses of `scanOutput`, `scanWord`, and `scanLast`;
  and
- the composition equation for `sentenceResult`.

The equations carrying `simplification` are still definitions: they are the
base, constructor, or complementary guarded clauses of newly declared
functions. In particular, the `primeLength` rules define that predicate rather
than asserting a theorem about a pre-existing primality operator. The scan
rules are structurally descending recurrence clauses, not extra algebraic facts
about reference-semantics symbols.

No canonical rule matches a runtime configuration cell or introduces an
execution/observation transition, so the local inventory contains no
`OPERATIONAL_RULE`. Operational Python behavior is supplied by the imported
reference semantics, whose rules are outside the launcher-provided canonical
local-rule inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `/reference/k-proof/prove.sh` compiles `verification.k` with all 18
canonical rules already present:

```text
kompile verification.k ... --output-definition verification-kompiled
```

It then runs:

```text
kprove spec.k ... --claims SPEC.scan-loop
kprove spec.k ... --spec-module SPEC
```

`/reference/k-proof/proof-loop.out` and
`/reference/k-proof/proof-full.out` each contain `#Top`, but those commands
prove reachability claims against the definition that already contains every
inventory rule. They do not first prove the exact statement of any canonical
rule against a module from which that rule is absent. The body-mutant and
false-postcondition probes establish sensitivity, not the required
rule-before-admission ordering. Therefore none of the 18 entries qualifies as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty.

No inventory rule adds an independent mathematical fact over already defined
symbols. Every simplification rule is an equation or recurrence clause defining
one of the proof's own named summary functions, so each is classified
`DEFINITION` as required.
