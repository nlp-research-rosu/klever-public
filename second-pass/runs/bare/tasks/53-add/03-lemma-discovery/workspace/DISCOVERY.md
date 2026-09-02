# Trust-boundary classification

The exhaustive canonical inventory contains zero rules. Consequently, there are no `source_rule_id` values to classify as `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`.

There are no separately proved derived lemmas. Stage 1's `prove.sh` compiles `VERIFICATION`, performs concrete executions, and proves the final claim in `spec.k`; it does not first prove a reusable rule against a module lacking that rule and then install the exact rule into a later module. Thus there is no Stage 1 proof evidence qualifying any rule as `PROVED_DERIVED_LEMMA`.

The domain-lemma set is explicitly empty. The definition and operational-rule sets are also empty because the canonical inventory has no entries. No rule carries the `simplification` attribute in the inventory.
