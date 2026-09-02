# Trust-boundary discovery

The canonical inventory contains one rule, in module `VERIFICATION`:
`flipSpec(S) => pySwapCase(S)`. It is classified as `DEFINITION` because it is
the defining equation for the named contract-level summary `flipSpec`. The
right-hand side is the string-case summary supplied by the execution
semantics, so this rule introduces a name for that summary rather than an
additional mathematical fact.

The classification counts are:

- `DEFINITION`: 1
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The domain-lemma set is explicitly empty.

There are no separately proved derived lemmas. Stage 1 `prove.sh` compiles
`verification.k` before running `kprove`, and that compiled module already
contains the inventoried `flipSpec` rule. Thus Stage 1 does not demonstrate a
proof of this exact rule against a module from which it is absent, and the rule
does not qualify as `PROVED_DERIVED_LEMMA`.

The inventoried rule carries no `simplification` attribute. The output includes
the sole canonical `source_rule_id` exactly once, preserves inventory order,
and copies the canonical `inventory_sha256` exactly.
