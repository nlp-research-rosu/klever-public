# Trust-boundary discovery

## Canonical scope and method

The exhaustive source of rule identities and ordering is
`/reference/rule-inventory.json`. Its embedded inventory digest is:

```text
01ad50c6b45f648f63d18deb81f4a81f3c96e68c877d124351958a5b6a7d6c75
```

The inventory contains 10 rules, all from the local `VERIFICATION` module.
Each canonical `source_rule_id` appears exactly once in
`trust-boundary.json`, in inventory order. Imported reference-semantics rules,
K claims, and files outside the canonical local verification-module closure
were inspected as evidence but were not added to or substituted for the
canonical inventory.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 9 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

The two `allFloats` rules define a structural predicate over `ValSeq`.
`pairNear` defines a named proximity expression. The two `asFloat` rules
define an exhaustive proof-local projection/totalization. The two `rowAcc`
rules and two `outerAcc` rules are base-and-step recurrences for the nested
Boolean folds. These nine rules therefore meet the requested `DEFINITION`
criterion.

There are no canonical `OPERATIONAL_RULE` entries. In particular, the
inventoried `applyBin` rule carries the `simplification` attribute, so the
requested constraints permit only `DEFINITION` or `DOMAIN_LEMMA` for it. It
does not define a new summary or named proof term; it adds a guarded
simplification fact about the imported operational symbol `applyBin`.
Accordingly it is a `DOMAIN_LEMMA`.

## Per-rule classification

1. `rule-dc6da0bab4bb59bc7bc1f84e094e20bfb08eaabdfb63f4029d3dcd8d203f8b96`
   — `DEFINITION`: base equation for `allFloats`.
2. `rule-9e498a0552e6771e74565791899fe40f49d034087ac6ccb7f8bd852cdd51a7d5`
   — `DEFINITION`: constructor recurrence for `allFloats`.
3. `rule-1ccd7704e0d880500af6b7bbc2f25393776cecf9972be7883d55005af75dba48`
   — `DEFINITION`: abbreviation defining `pairNear`.
4. `rule-3b93d4976b7182c91d2a2f37ff4a4b4aeb87b2cae0b70e16583b7653e50137f0`
   — `DEFINITION`: Float identity branch of `asFloat`.
5. `rule-67ea2306e1ec02d05f832f6fc3d1c1df7b074395565220a88d327b4244b3dfd5`
   — `DEFINITION`: guarded non-Float totalization branch of `asFloat`.
6. `rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf`
   — `DOMAIN_LEMMA`: guarded simplification of imported `applyBin`.
7. `rule-906f23375bc3037477bb4865bd82b1acd088f6c92c84fba22886fbcdb4f2e980`
   — `DEFINITION`: base equation for `rowAcc`.
8. `rule-4e163f4813de9404688e2d18f89122e640ce937ff1c79d5b2ab228fe5b081efb`
   — `DEFINITION`: constructor recurrence for `rowAcc`.
9. `rule-9f5405faf27ef5ff3d4f3497a2b19c0aae403765801d6da99715fd17f685269c`
   — `DEFINITION`: base equation for `outerAcc`.
10. `rule-69dccad157e90642e223828bfe9d6780f595e93cc0d6e5f205e123d520ccb3da`
    — `DEFINITION`: constructor recurrence for `outerAcc`.

## Separately proved derived-lemma evidence

Stage 1 separately proves one auxiliary connection claim:
`CONNECTION-SPEC.float-subtraction` in
`/reference/k-proof/connection-spec.k`. Its proof definition,
`/reference/k-proof/connection-verification.k`, imports `MPY` and does not
import `verification.k`, so the canonical simplification rule is absent from
that proof definition. In `/reference/k-proof/prove.sh`, the connection
definition is compiled and this claim is run before the main verification
definition is compiled. `/reference/k-proof/PROOF.md` records `#Top` and exit
0 for that command.

That evidence does not make any canonical rule a
`PROVED_DERIVED_LEMMA`, because the separately proved statement is not the
exact inventoried rule. The auxiliary claim has Float-typed operands and a
direct `subF(A,B)` result. The canonical rule has Val-typed operands, an
`isFloat(A) andBool isFloat(B)` guard, `asFloat` applications on the right,
and the `simplification` attribute. The exact-correspondence requirement is
therefore not met. Comments in `verification.k` and the Stage 1 narrative do
not change that classification.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf
```

No other canonical rule is a `DOMAIN_LEMMA`.
