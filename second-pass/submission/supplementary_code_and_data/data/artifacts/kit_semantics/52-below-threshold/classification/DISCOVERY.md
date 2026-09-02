# Trust-boundary discovery

## Canonical scope

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256
`e3362171f152047e40ed1bad492d95d2db31b2dc70d7b9ca193761b513268845`.
It contains four rules, in the `VERIFICATION` module, and none has the
`simplification` attribute. `trust-boundary.json` preserves that inventory
order and classifies each `source_rule_id` exactly once.

Rules from supporting files that are absent from the canonical inventory are
not added to the classification. In particular, the inventory is treated as
exhaustive rather than being expanded from comments or imports.

## Classification result

All four canonical rules are `PROVED_DERIVED_LEMMA`.

Although the rules are deployed as priority-40 operational accelerators, Stage
1 does not merely assume them as verification-model execution rules. Each
rule's complete transition is first stated as a reachability claim and proved
against `loop-verification-kompiled`, whose main module is
`VERIFICATION-LOOPS` and which does not contain any of the four canonical
rules. Only after those proofs does `prove.sh` compile `verification.k` and
make the proved transitions reusable rules.

For correspondence checking, each rule was compared with its claim after
removing only the claim label, insignificant whitespace, and the rule-only
`priority(40)` scheduling attribute. Every pair matched exactly. The attribute
changes rewrite selection order, not the configuration relation established
by the claim.

## Separately proved derived lemmas

### Empty `#loop`

- Canonical rule:
  `rule-bde967b339e94e547969a2cd8447240326a9df2d66f66b5aa5718a7f875159fa`
- Matching evidence: `LOOP-SPEC.loop-empty`, `loop-spec.k` lines 6-37.
- Proof ordering: `prove.sh` lines 27-34 compiles
  `verification-loops.k` and proves `loop-empty`; the canonical rule is not
  compiled until lines 44-47.
- Proof result recorded by Stage 1: `#Top`, exit 0.

### Nonempty `#loop`

- Canonical rule:
  `rule-856b1e357a5f433ad09956ac507d9936d2c9e9e4e9d5a8f2a9fa32315eb71e6b`
- Matching evidence: `LOOP-SPEC.loop-cons`, `loop-spec.k` lines 39-71.
- The claim and rule have the same symbolic head and tail, numeric-domain
  guard, continuation, environments, scopes, heap framing, stack transition,
  return/exception state, and exit code.
- Proof ordering: the same `prove.sh` lines 27-34 command proves it before the
  canonical rule is compiled.
- Proof result recorded by Stage 1: `#Top`, exit 0.

### Empty source `For`

- Canonical rule:
  `rule-334c70388307babf11e3781429f37a3574c7ff891d86996b5621c3b1e8f92c1e`
- Matching evidence: `LOOP-SPEC.for-empty`, `loop-spec.k` lines 73-104.
- Proof ordering: `prove.sh` lines 37-41 proves the `For` claims against
  `loop-verification-kompiled`, before the canonical rule is compiled.
- The command trusts only `loop-empty` and `loop-cons`, whose exact claims the
  immediately preceding command already proved. This is staged proof
  composition, not a new unproved fact.
- Proof result recorded by Stage 1: `#Top`, exit 0.

### Nonempty source `For`

- Canonical rule:
  `rule-f9e5b4514f00b3ed026d33dbeec83015df4208cb8c2aeed1d460d93c10f63efe`
- Matching evidence: `LOOP-SPEC.for-cons`, `loop-spec.k` lines 106-138.
- The claim and rule have the same numeric-domain guard and complete
  configuration transition.
- Proof ordering and composition are the same as for `for-empty`: proof at
  `prove.sh` lines 37-41, installation only at lines 44-47.
- Proof result recorded by Stage 1: `#Top`, exit 0.

## Other classifications

There are no canonical `DEFINITION` entries. The mathematical summary
definitions used by the claims are in supporting modules but do not appear in
the exhaustive canonical inventory.

There are no canonical `OPERATIONAL_RULE` entries. The four operationally used
rules meet the stronger, evidence-based `PROVED_DERIVED_LEMMA` criterion
because their exact transitions are proved before installation.

The `DOMAIN_LEMMA` set is empty. No rule in the canonical inventory is an
additional trusted mathematical fact.
