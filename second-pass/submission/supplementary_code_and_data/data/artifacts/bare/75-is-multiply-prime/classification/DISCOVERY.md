# Trust-boundary discovery

The canonical inventory contains one rule:
`rule-42e3d1013e958ee69b67f3151bd6928b3cf7deebc75764f9d52633a30ba4514c`.

It is classified as `DEFINITION` because it is the defining equation for
`isThreePrimeProductBelow100`, the mathematical summary used directly in the
proof target. Its right-hand side gives the finite characterization appropriate
to the stated input bound; it does not supply an additional fact about an
independently defined summary.

There are no separately proved derived lemmas. Stage 1's `prove.sh` first
compiles `definition.k`, whose import closure already contains this verification
rule, and then proves the final claim in `spec.k` against that compiled
definition. It does not first prove the rule's exact statement against a module
that omits the rule, so there is no `PROVED_DERIVED_LEMMA` evidence to report.

There are no `OPERATIONAL_RULE` entries in the canonical inventory.

The domain-lemma set is empty. The canonical inventory contains no
`DOMAIN_LEMMA` rules.
