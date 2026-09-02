# Trust-boundary discovery

The canonical inventory identifies one rule in the local verification-module closure. This report classifies that rule only; the mounted reference semantics are outside the canonical inventory supplied for this stage.

## Classification

| Source rule ID | Classification | Reason |
| --- | --- | --- |
| `rule-64ab866119ef68aee7112f09de97735afd57399d3ba18fb6463d8b22a673c966` | `DEFINITION` | The rule expands the named proof entry term `#sameChars(S0, S1)` into a call of the constructor-level solution closure with `str(S0)` and `str(S1)`. It therefore defines a structural proof-harness term and introduces no independent mathematical fact. |

The inventory records no `simplification` attribute on this rule. There are no rules classified as `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` first compiles `verification.k` as `SAME-CHARS-VERIFICATION`; that compiled module already contains the inventory rule. It then runs `kprove spec.k` against that definition. There is no earlier proof command that proves the exact rule statement against a module from which the rule is absent. Consequently, the Stage 1 evidence does not meet the required ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The sole local rule is a definition of the proof entry term, so no additional mathematical fact is trusted to close the K proof.

## Coverage

`trust-boundary.json` uses canonical inventory hash `c1534c6113c88c0bb5b2530edcf8c3dbb61b692426c714be2d9eb96085fc2610` and lists the inventory's one `source_rule_id` exactly once, in inventory order.
