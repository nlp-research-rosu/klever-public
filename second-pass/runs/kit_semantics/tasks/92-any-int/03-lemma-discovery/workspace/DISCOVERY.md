# Trust-boundary discovery

## Canonical inventory

The sole rule source for this classification is
`/reference/rule-inventory.json`. Its embedded `inventory_sha256` is
`a8187743fcabaa841787ec6a8d9bc304dc4a1be6e3c03d3e3b0d7848487592b3`.
It contains four rules, and `trust-boundary.json` preserves their inventory
order and classifies each `source_rule_id` exactly once.

## Classifications

### Definitions

Three rules are `DEFINITION`:

- `rule-d467c351c964bfa6aa3699f282303d6447cfcf61979d2a3950f1319a2bfd3c44`
  expands the `AnyIntCall` macro to the ordinary
  `Call(Name("any_int"), ...)` proof term.
- `rule-f0f9d16c2d45c2a40f20bad1f84e2c6cdaad7928fcf033dc6b8c2ffff3f6b10d`
  expands `anyIntModuleScope` to the structural scope value that binds the
  exact submitted function closure.
- `rule-b4cd16bb262eb62089f82976d9f4fde2111bb34eaa3c93afe9502b42d0c2119a`
  defines the total mathematical summary `anySum`.

The first two are macro/structural definitions of named proof terms. The third
is an equation defining the postcondition summary. None supplies an extra fact
about an already defined mathematical operation.

### Domain lemmas

The domain-lemma set is not empty. It contains exactly:

- `rule-2337b981dde3e7f5b878ce7ffbb3f2c1c87d9b3c9777edc1dbeab1aeeba99ca5`,
  the `[simplification]` rule normalizing symbolic `boolAsInt(B)`.

This rule acts on the imported `boolAsInt` symbol and contributes a reusable
symbolic equality needed by the mixed-Boolean claims. It is not a definition of
a new summary or proof term. Under the requested policy, a simplification rule
must be either `DEFINITION` or `DOMAIN_LEMMA`; because this one adds a fact
about an existing symbol and lacks separate proof evidence, it is a
`DOMAIN_LEMMA`.

### Operational rules

The `OPERATIONAL_RULE` set is empty. The canonical local closure contains no
ordinary execution or observation rule. Program execution remains in the
imported reference semantics, which is outside this launcher-generated local
inventory.

### Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty. There is no separately proved derived
lemma and therefore no Stage 1 proof evidence satisfying that classification.

In `/reference/k-proof/prove.sh`, lines 34–40 compile `verification.k` as module
`VERIFICATION` and then run `kprove spec.k` against that compiled definition.
The `boolAsInt` simplification rule is already present in `verification.k`
lines 52–54 and is therefore included before the successful target proof.
Stage 1 does not compile a module excluding that rule, prove its exact
statement, and only then add it. The concrete run, differential test,
false-postcondition probe, and body-mutation probe also do not prove that exact
rule. Consequently, the Stage 1 comment and `PROOF.md` description calling it
derived are explanatory only and do not meet the required
`PROVED_DERIVED_LEMMA` evidence standard.

## Completeness check

The output has four entries for four canonical inventory rules, with no
duplicate or unknown identifiers. Counts by classification are:

- `DEFINITION`: 3
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 1
