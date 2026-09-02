# Trust-boundary discovery

## Canonical scope

The exhaustive input is `/reference/rule-inventory.json`.

- Schema version: `2`
- Inventory SHA-256:
  `1110ead8ae73844de04448028465295b04f1002ba4a020382352cf8a2a3c3001`
- Canonical rule count: `1`
- Canonical module: `VERIFICATION`

`trust-boundary.json` preserves the sole canonical `source_rule_id` in
inventory order and classifies it exactly once. Rules and equations outside
this canonical inventory, including those in `verification-base.k` and the
supplied reference semantics, are not additional entries.

## Classification

### `rule-61aeb3d85b68b0ecbd2dd5e4ea48a3c26d762d05db0e21e48b6ed02315486851`

Classification: `PROVED_DERIVED_LEMMA`.

The rule is operational in shape because it summarizes execution of the
program's loop, but it is not installed as an unproved operational-model rule.
The mounted Stage 1 evidence establishes the required proof-before-use order:

1. `prove.sh` lines 15-18 kompile `verification-base.k` as
   `VERIFICATION-BASE`.
2. `verification-base.k` does not contain the inventoried loop rule.
3. `connection-spec.k` imports only `VERIFICATION-BASE`; its
   `CONNECTION-SPEC.loop` claim is at lines 6-43.
4. After removing only the `claim [loop]:` versus `rule` introducer and the
   rule's `priority(40)` proof-search attribute, the claim and canonical rule
   have exactly the same 37 statement lines: loop syntax, arbitrary
   continuation frame, environment and scope frames, local-state updates, and
   guard.
5. `prove.sh` lines 19-21 run that claim against
   `verification-base-kompiled`. `prove.out` line 153 records `#Top`.
6. Only afterward do `prove.sh` lines 27-30 kompile `verification.k`, which
   introduces the inventoried rule, before the target proof at lines 31-33.

The canonical rule has only the `priority(40)` attribute and does not carry
`simplification`. The priority changes rule selection, not the separately
proved statement. Because the exact rule statement is machine-checked before
the rule is present, `PROVED_DERIVED_LEMMA` is the applicable classification;
it is neither a structural definition nor an additional trusted mathematical
fact.

## Classification totals

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 1 |
| `DOMAIN_LEMMA` | 0 |

The domain-lemma set is empty.
