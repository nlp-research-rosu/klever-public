# Rule trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is the exhaustive canonical inventory for the
local verification-module closure. Its inventory digest is
`3017b8701327f8ebc811769d3af6ecf7861928f49d848164daa10a03d34e3d3b`.
It contains two rules, and `trust-boundary.json` preserves their inventory
order and classifies each exactly once.

The classification was checked against the mounted Stage 1
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`. Claims in `spec.k` are
not canonical inventory rules and therefore are not added to the JSON.

## Classifications

1. `rule-61eabb962d387664fc1888e2526053dbc025e35fe1bb15e488f84221b246fa4e`
   is `DEFINITION`. It is the guarded `N >=Int 0` equation for the declared
   total function `sumToN`, defining the summary as
   `N *Int (N +Int 1) /Int 2`. It does not match a K configuration or replace
   MPY execution.
2. `rule-dc2a2ab329f437ecc03ad7c3e85423ec0880b778f416b2bf8437887f41d0f999`
   is `DEFINITION`. It is the complementary guarded `N <Int 0` equation for
   `sumToN`, defining the empty-range result as zero. Its guard is disjoint
   from and exhaustive with the first equation's guard.

Neither rule carries the `simplification` attribute. Neither rule is an
ordinary execution or observation rule, so the `OPERATIONAL_RULE` set is
empty.

## Separately proved derived lemmas

There are no separately proved derived rules.

Stage 1 `prove.sh` first compiles `verification.k`, which already contains both
`sumToN` equations, and then proves the claims in `spec.k` against that compiled
definition. It does not first prove either rule's exact statement against a
module from which that rule is absent. Consequently, neither canonical rule
qualifies as `PROVED_DERIVED_LEMMA`.

`SPEC.sum-loop` is a proved reachability claim/circularity, but it is not a
rule in the canonical inventory and is not represented in
`trust-boundary.json`.

## Domain lemmas

The domain-lemma set is empty. Both canonical equations define the named
summary `sumToN`; the verification closure adds no separate mathematical fact
classified as `DOMAIN_LEMMA`.
