# Trust-boundary classification

The exhaustive canonical inventory contains one rule:
`rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1`.
It expands `expectedSumProduct(IS)` into a pair whose components are the
`sumInts(IS)` and `productInts(IS)` mathematical summaries. This is a named
postcondition expansion, so it is classified as `DEFINITION`.

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The sole
rule defines a proof term; it does not execute or observe a program step.

There are no separately proved derived lemmas. In particular, Stage 1
`prove.sh` compiles `verification.k` with this rule already present and then
proves the main claim in `spec.k`. It does not first prove this rule's exact
statement against a module from which the rule is absent, so that command is
not evidence for a `PROVED_DERIVED_LEMMA` classification.

The domain-lemma set is explicitly empty. The inventory's only rule is a
definition, not an additional trusted mathematical fact.
