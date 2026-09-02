# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the exhaustive inventory used for this
classification. Its copied `inventory_sha256` is
`134928cdbb2e86afcf7d1b87d805c043d37ffcf38c6f9991d2d17f482d832a24`.
It lists two rules, both in `VERIFICATION`, in the order preserved by
`trust-boundary.json`.

Imported reference-semantics rules are not added to this local classification:
they have no canonical `source_rule_id` in the launcher-generated inventory.

## Rule classifications

| Inventory position | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-1f493419665e264916f30ab5358e05eef39549f5227088474c1ff240d5e27abe` | `DEFINITION` | `hexCount(.IntSeq) => 0` is the base equation defining the mathematical summary on the empty sequence. |
| 2 | `rule-7d9e21c1ff4818429cf5dfabc65f7730ee1b9f46e3a11cc4a89558f5cd957c74` | `DEFINITION` | The `iCons` equation is the structurally recursive defining case: it contributes the head's fixed-semantics membership indicator and recurses on the tail. |

The cases are disjoint and cover the two constructors of `IntSeq`. Neither
rule rewrites a Python execution configuration, and neither states an
additional algebraic fact beyond defining `hexCount`. The inventory records no
attributes on either rule, so there are no `simplification`-attributed rules to
classify.

Canonical-rule totals:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

## Separately proved derived lemma

Stage 1 contains one separately proved reusable derived lemma:
`SPEC.hex-loop`, the reachability claim at `spec.k` lines 6–37. It is a claim,
not a rule in the canonical verification-module inventory, so it is documented
here but no extra entry is added to `trust-boundary.json`.

The mounted Stage 1 evidence demonstrates the required ordering and exact
correspondence:

1. `prove.sh` lines 21–24 build `verification-kompiled` from
   `verification.k`. That module contains the two `hexCount` definitions and
   does not contain an operational rule corresponding to `SPEC.hex-loop`.
2. `prove.sh` lines 26–29 run `kprove` on the exact label
   `SPEC.hex-loop` alone, with no `--trusted` option.
3. `PROOF.md` lines 152–159 record that this command printed `#Top` and exited
   0.
4. Only afterward, `prove.sh` lines 31–35 prove the entry claim while including
   the exact same `SPEC.hex-loop` label and passing
   `--trusted SPEC.hex-loop`.

Thus the reusable loop result is first machine-checked against a definition
that does not already contain it as a rule, then reused unchanged. No other
Stage 1 claim has this pattern: `SPEC.hex-key` is the target claim, and the
mutation claims are expected-failure validation probes.

## Domain lemmas

The domain-lemma set is empty. No canonical rule is an additional trusted
mathematical fact, and no unproved helper is promoted to
`PROVED_DERIVED_LEMMA`.
