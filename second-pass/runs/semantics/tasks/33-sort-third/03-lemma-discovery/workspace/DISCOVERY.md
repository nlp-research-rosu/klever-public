# Trust-boundary discovery

The canonical inventory contains 11 rules, all from the local `VERIFICATION`
module. Every inventory rule is classified as `DEFINITION`. None rewrites an
execution configuration or observes operational state; the first four expand
named terms for the translated program, and the remaining seven define the
mathematical summary and structural helpers used by the specification.

| Inventory rule | Classification | Basis |
| --- | --- | --- |
| `rule-30f896f4a78788a4df1bfd241f27a89c6a07e729eefa54e20e31be5cceb2c6bb` | `DEFINITION` | Expansion of the named loop-body statement term. |
| `rule-21093175dbb8f2943626cf550979b0da747b2af38d29798aa0321b8a05e4bb0c` | `DEFINITION` | Expansion of the named function-body statement term. |
| `rule-7c593d3abb10208b9212ec827fa30fc4ff49f3dfa4acc1d6d12a35777a7a8b39` | `DEFINITION` | Expansion of the named closure term. |
| `rule-10b3747ff64f7edc5c2b2739b560b4381fc410dad54630e3f5c2a3f0a1b3d3de` | `DEFINITION` | Expansion of the named translated-module term. |
| `rule-6bf57cc70b116bf57d62cb53019c3bc3a8afd519690929ee08b6bb00a2334384` | `DEFINITION` | Conditional selector equation for stride-three indices. |
| `rule-d67c9157105f75b20f186a8416a8374e66a206669477ae93c784de085518a12d` | `DEFINITION` | Complementary selector equation for preserved indices. |
| `rule-265d11e00e4fbf524925232abb23c7127d163ff9a4a0fb40c8dd70453168070e` | `DEFINITION` | Base equation of the output fold. |
| `rule-48d8e0a8b82574ed851e8ab7b2c422bde84aba1f278d3e73a9ee43b27ebff908` | `DEFINITION` | Recursive equation of the output fold. |
| `rule-5003da3d7156c8d67318d1d506c428d29a27f6057012a2b10ef5b4a0bc66f7a0` | `DEFINITION` | Base equation of the last-loop-value helper. |
| `rule-7b6f7fc609a2303132cffc76dbf0fb13227389bda8ad1906153b016750d88a66` | `DEFINITION` | Recursive equation of the last-loop-value helper. |
| `rule-784a582d08c3bf5c89efdcf597adcf9e84c7d8e69114ac1324c993790561826b` | `DEFINITION` | Initialization equation for the top-level output summary. |

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1's `prove.sh` compiles `verification.k` with all 11 inventory rules
already present, then invokes `kprove spec.k` once. That command proves the
`sort-third-loop` and `sort-third-correct` claims, but neither claim is a rule
in the canonical inventory. There is no Stage 1 command that first proves the
exact statement of an inventory rule against a module lacking that rule and
then reuses it, so the required ordering and exact-correspondence evidence is
absent for every inventory rule.

## Other classifications

The `OPERATIONAL_RULE` set is empty: the inventory contains no ordinary
execution or observation rule.

The `DOMAIN_LEMMA` set is explicitly empty. No additional mathematical fact is
introduced by the local verification module beyond its defining equations and
recurrences.

No inventory rule carries the `simplification` attribute.
