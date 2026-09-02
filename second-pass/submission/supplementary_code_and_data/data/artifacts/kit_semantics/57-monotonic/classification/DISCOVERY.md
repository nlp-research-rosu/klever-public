# Trust-boundary discovery

## Canonical inventory

The exhaustive inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`635effbc5658fac7a475f0ce34b67f1d7b46f1965621f64cca3938c8fdb15f6c`.
It contains two rules from the local `VERIFICATION` module closure.
`trust-boundary.json` preserves their inventory order and classifies each
`source_rule_id` exactly once.

## Rule classifications

### `rule-9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d`

Classification: `DOMAIN_LEMMA`.

This rule carries the `simplification` attribute and normalizes the Boolean
postcondition on the short-circuit-true branch. It does not define a named
summary, recurrence, macro, or structural proof term, so it is not a
`DEFINITION`. It also has no configuration cells or execution transition, so
it is not an `OPERATIONAL_RULE`.

Stage 1 describes the rule as a Boolean-algebra lemma, but that description is
not separate proof evidence. In `/reference/k-proof/prove.sh`, lines 30–36
compile `verification.k` with this rule already present and then prove
`SPEC.monotonic`. There is no earlier `kprove` command for the exact rule
against a module that omits it. The negative mutation probes at lines 38–56
test target-result and source-body sensitivity; they do not prove this rule.
It therefore does not meet the required ordering for
`PROVED_DERIVED_LEMMA`.

### `rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4`

Classification: `DOMAIN_LEMMA`.

This complementary `simplification` rule normalizes the Boolean postcondition
on the short-circuit-false branch. Like the first rule, it is an additional
mathematical identity rather than a definition or an operational transition.

The same Stage 1 evidence applies: `prove.sh` includes this rule in the
compiled `VERIFICATION` module before the only positive target proof, and no
separate proof first establishes the exact rule without importing it. The
mutation probes do not establish its reusable mathematical statement.
Consequently it is not a `PROVED_DERIVED_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory.
Stage 1 contains no proof command that first proves either inventoried rule's
exact statement against a module from which that rule is absent.

## Domain-lemma set

The domain-lemma set is **not empty**. It consists of exactly the two canonical
rule IDs listed above. There are no inventoried `DEFINITION`,
`OPERATIONAL_RULE`, or `PROVED_DERIVED_LEMMA` entries.
