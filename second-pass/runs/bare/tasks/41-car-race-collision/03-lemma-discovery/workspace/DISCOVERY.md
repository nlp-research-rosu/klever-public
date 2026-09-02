# Trust-boundary classification

The exhaustive canonical `/reference/rule-inventory.json` contains no rules
in the local verification-module closure. Consequently, there are no entries
to classify as `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or
`DOMAIN_LEMMA`. There are also no inventoried rules carrying the
`simplification` attribute.

There are no separately proved derived lemmas. Stage 1's `prove.sh` invokes
`kprove spec.k` against the compiled `VERIFICATION` module to prove the
top-level reachability claim, but it does not first prove a reusable rule
against a module lacking that rule and then add the exact rule to the
verification closure.

The domain-lemma set is empty.

Although the finalized `semantic.k` contains operational transition rules,
the launcher-generated inventory is authoritative and contains no rule
entries. Those semantic rules therefore are not added independently to this
classification.
