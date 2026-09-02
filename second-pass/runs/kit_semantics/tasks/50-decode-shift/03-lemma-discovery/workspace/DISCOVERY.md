# Trust-boundary discovery

## Canonical inventory

The sole rule source for this classification was
`/reference/rule-inventory.json`. Its copied inventory digest is:

`6a12a2f6c846652079e924de9ebe4396c9acfdc86d2c7106bad8a7d7d4e616b0`

The inventory contains six rules, all in module `VERIFICATION`. Each canonical
`source_rule_id` appears once in `trust-boundary.json`, in the same order as
the inventory. None of the six rules carries the `simplification` attribute.

## Classification result

All six rules are `DEFINITION`:

- `decodeCode` is an unconditional equation naming the inverse character-code
  calculation.
- `encodeCode` is an unconditional equation naming the prompt's forward
  character-code calculation.
- The two `decodeAcc` rules are the disjoint base and constructor cases of a
  structurally recursive mathematical summary.
- The two `lowerCodes` rules are the disjoint base and constructor cases of a
  recursively defined input-domain predicate.

These rules rewrite only named mathematical terms. None matches a `<k>` cell,
reads or writes configuration state, selects a program binding, changes
control, observes execution, or replaces a fixed-semantics operation.
Consequently, there are no `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no canonical rules classified as `PROVED_DERIVED_LEMMA`.

The Stage 1 `prove.sh` first compiles `verification.k`, with all six inventory
rules already present, into `verification-kompiled`. It then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Stage 1 `PROOF.md` records that this command printed `#Top` and exited 0.
However, that ordering proves the claims under a definition already containing
all six rules. It does not first prove the exact statement of any inventory
rule against a module that omits that rule, so it cannot justify
`PROVED_DERIVED_LEMMA` for any of them.

`spec.k` contains the separately checked `character-inverse` and
`loop-invariant` reachability claims, as well as the target `decode-shift`
claim. These claims are proof evidence, but they are not rules in the canonical
inventory and do not correspond exactly to an inventory rule admitted only
after its proof. The expected-failure mutation probes likewise establish no
derived inventory rule.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical rule adds a separate trusted
mathematical fact beyond the defining equations and recurrences above.
