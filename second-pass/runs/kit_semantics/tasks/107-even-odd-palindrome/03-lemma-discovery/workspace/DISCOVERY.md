# Trust-boundary discovery

## Canonical basis

The launcher-generated `/reference/rule-inventory.json` is the exhaustive
canonical inventory used for this classification. It reports:

- schema version `2`;
- inventory SHA-256
  `bd6baa11540644d109e6d3516ace2adf5c7c318407fb921dfed4acc5a6ffaf79`;
- verification module `VERIFICATION`;
- verification SHA-256
  `466c7679d2f2c6cd7a3d3b9a04c583d518d0920cc9d070b4e41226adb9d26748`;
- exactly one rule.

The classification follows the inventory order and includes its sole
`source_rule_id` exactly once. Imported reference-semantics rules were not added
because they are not entries in the canonical local verification-module
inventory.

## Rule classification

| Source rule ID | Classification | Reason |
|---|---|---|
| `rule-85e70a4588ebd4cc7fa9900b762e8c8d4075fa1ebbdfda530c9ea390b0a2029a` | `DEFINITION` | The rule is the single exhaustive equation for the nullary symbol `solutionClosure()`. Its right-hand side is a concrete `closureVal` containing the translated parameter list, nested `If`/`Return` body, and definition location. It defines a named proof term; it has no cell pattern, does not observe or rewrite an executing configuration, and states no additional reusable mathematical fact. |

The canonical attributes array for this rule is empty. In particular, no
inventoried rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k`, with the
`solutionClosure()` equation already present, and then proves `spec.k` against
that compiled definition. It does not first prove the exact equation against a
module that omits it. The later proof commands are expected-failure
postcondition and body-mutation probes; neither proves the rule's exact
statement. Consequently, Stage 1 contains no evidence satisfying the required
lemma-first ordering for any inventoried rule.

## Operational and domain lemmas

There are no `OPERATIONAL_RULE` entries: the only local rule defines a value and
does not supply an execution or observation transition.

The `DOMAIN_LEMMA` set is empty. No additional trusted mathematical fact is
present in the canonical inventory.

## Completeness checks

- Canonical rule count: `1`.
- Classified rule count: `1`.
- Duplicate `source_rule_id` values: `0`.
- Missing canonical rule IDs: `0`.
- Extra rule IDs: `0`.
- Classification values used: only the allowed value `DEFINITION`.
