# Trust-boundary discovery

## Result

The canonical inventory hash is
`cfcda43d802cd76ff5b47b744bbe3c51d030a222ce2c55bad170611d9840faa4`.
The inventory contains 10 rules, all from module `VERIFICATION`, and every
canonical `source_rule_id` is classified exactly once in inventory order.

Classification totals:

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The domain-lemma set is empty.

## Classification method

I treated `/reference/rule-inventory.json` as exhaustive and canonical. I did
not add imported reference-semantics rules, K claims, generated backend rules,
or alternative formulations that do not occur in that inventory.

All 10 inventory entries have empty attribute lists. In particular, no
inventory rule carries `simplification`. Every left-hand side is headed by one
of the proof-local function symbols `nestedStep`, `nestedScan`,
`bracketInput`, or `nestedResult`. None matches a configuration cell, Python
AST term, continuation, environment, or observable execution state. The rules
therefore define named mathematical summaries and domain predicates rather
than model program execution.

The five `nestedStep` equations are the guarded cases of one DFA transition
definition. Their guards partition early states, middle states, and the
absorbing completed state. The two `nestedScan` equations are the base and
constructor cases of structural recursion over `IntSeq`. The two
`bracketInput` equations structurally define the bracket-only input predicate.
The final `nestedResult` equation names the Boolean obtained by scanning from
state 0 and testing for state 4. These are all `DEFINITION`.

No inventory rule is an `OPERATIONAL_RULE`: ordinary Python execution is
provided by the mounted reference semantics, whose rules are outside this
canonical local verification-module inventory.

No inventory rule is a `DOMAIN_LEMMA`: none asserts an extra algebraic,
ordering, collection, or other mathematical fact used to close the proof.
Each right-hand side is instead the defining case or recurrence for its
left-hand-side symbol.

## Separately proved derived lemmas

There are no separately proved derived rules.

Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k` as
module `VERIFICATION`; that file already contains all 10 canonical rules. It
then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Thus the positive target proof is checked against a definition containing
every inventoried rule. Stage 1 does not first prove the exact statement of any
rule against a module omitting that rule, and it does not later import a
separately established rule. The negative mutation probes also use the same
already-compiled definition and do not establish reusable rules.

`SPEC.loop` is a reachability claim used as a circularity in `spec.k`, not a
canonical rule entry. Its Stage 1 proof status therefore does not justify
classifying any of the 10 inventoried equations as
`PROVED_DERIVED_LEMMA`.

## Rule-by-rule explanation

The following rows preserve canonical inventory order.

| Canonical source rule | Classification | Reason |
|---|---|---|
| `rule-d3f0b3b96e611b41d2e8c331de464a83b4e68e55a3a9ef80c85072283e3a52e6` | `DEFINITION` | Defines the early-state increment on code 91. |
| `rule-5235cdc16e73a4af8cde1dbf5b49f86ee7f418aed9aca6ae1e221671c623b08b` | `DEFINITION` | Defines the complementary early-state no-change case. |
| `rule-2632b098e390f757cdbc95d8a688555d956e3ba1ea0c29d982f03ab021c4c38a` | `DEFINITION` | Defines the middle-state increment on code 93. |
| `rule-20a7c7c6a34063a9caf1231ef507ed100c405cf13773a8407bb758e23da8a956` | `DEFINITION` | Defines the complementary middle-state no-change case. |
| `rule-97fd5a94cf85ea0ea85838319221cb4b69e04384d7611ccab77c11e40b315cdd` | `DEFINITION` | Defines completed states as absorbing. |
| `rule-93dce5c554493a3aaf098de0b0f849282a9eeabdbd187be97413f28507e3f9f9` | `DEFINITION` | Defines the empty-sequence base case of `nestedScan`. |
| `rule-51cb2a9f32f1e0f28c99c7bb9ba96fa06a420bfc0ff59247b5dfae9db1d39768` | `DEFINITION` | Defines the constructor recurrence of `nestedScan`. |
| `rule-86c81c4e83f334a250f0f7cd6a3d696ef3dd176482dc7252a0d002fb835aa66c` | `DEFINITION` | Defines the empty-sequence base case of `bracketInput`. |
| `rule-ae46ad4c111fd8416f3da10532e15c6d50824884fc7bba26f2ddee8a60b4c781` | `DEFINITION` | Defines the constructor recurrence of `bracketInput`. |
| `rule-b4ad6b97ec2791a39b26f63843ed3879c0a6a47ab5790df412ba95eca8a70c12` | `DEFINITION` | Defines `nestedResult` in terms of `nestedScan`. |
