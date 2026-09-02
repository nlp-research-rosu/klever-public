# Trust-boundary discovery

The canonical inventory has SHA-256
`e8965936389b130da83ca966c8f2d352ba5819829004bcaf84d4d910698449b8`
and contains eight rules, all from the local `VERIFICATION` module. Each
canonical `source_rule_id` appears once in `trust-boundary.json`, in inventory
order.

## Classification result

All eight rules are classified as `DEFINITION`.

- `rotateWith` has one unconditional equation defining the normalized value of
  a rotation update.
- `cycScan` has an empty-sequence base equation and an `iCons` structural-step
  equation defining a Boolean fold.
- `finalRotation` has empty and nonempty structural equations defining the
  final rotation summary.
- `finalChar` has empty and nonempty structural equations defining the final
  loop-target summary.
- `cycPattern` has one unconditional equation defining the top-level summary
  by initializing `cycScan`.

These rules rewrite only newly declared mathematical summary symbols. None
matches a `<k>` cell or another operational configuration, and none observes or
changes execution-model state. Therefore the `OPERATIONAL_RULE` set is empty.
The inventory reports no `simplification` attribute on any rule.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as `VERIFICATION`; that
file already contains all eight inventoried rules. It then runs:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Consequently, the successful Stage 1 proof checks the reachability claims with
all eight rules already in the compiled definition. It does not first prove
the exact statement of any inventoried rule against a module that omits that
rule. The two later Stage 1 commands use `spec-vacuity.k` and
`spec-body-mutation.k` as expected-failure probes; they likewise do not prove
any inventoried rule in a rule-free module. The loop claim in `spec.k` is proof
evidence for the program/summary connection, but it is a claim rather than one
of the canonical inventoried rules and does not establish the required
rule-absent ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No canonical rule adds a separate trusted
mathematical fact: every rule is an equation or structural recurrence defining
one of the newly declared summary terms.
