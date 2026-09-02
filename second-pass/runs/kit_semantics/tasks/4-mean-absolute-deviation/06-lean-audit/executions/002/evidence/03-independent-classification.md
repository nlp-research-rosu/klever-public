# Independent Stage 3 classification

The inventory order and source spans are those reconstructed by the trusted
`tools.k_rule_inventory.inventory_verification` run in
`02b-inventory-reconstruction-success.txt`. The classifications below were
made from the frozen rule text and supplied operational semantics, without
using the protected manifest's rationales.

| # | Source span / rule ID | Independent class | Reason |
|---:|---|---|---|
| 1 | 26–44 / `rule-0b30d37fcb1fa6f2e9d5602fd000c7184e19e2179cc09da8efcca1f73abb811e` | `DEFINITION` | `madBody` is the named macro/proof term for the exact translated source body. |
| 2 | 47 / `rule-78f2a049ece805815d21e9063a74aff75f3d53f22a84a77fea64ffc91042a363` | `DEFINITION` | Base equation for the fresh recursive domain predicate `allFloatVS`. |
| 3 | 48–49 / `rule-2a5f59dcc54d654448c496b86879b657233ccdf91d38545bb4c06ceb1ed40871` | `DEFINITION` | Tail-descending recurrence for `allFloatVS`. |
| 4 | 54–56 / `rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e` | `DOMAIN_LEMMA` | Adds the definedness characterization of the pre-existing Val-to-Float projection. It is marked `simplification`, is not an ordinary execution step, and Stage 1 does not first prove this exact equation without the rule. It is relevant because the float-list proof projects symbolic `Val` elements. |
| 5 | 57–59 / `rule-f394e6869605ba695d3a1ee914ff52207c3f62e8e1c3c99caa25ea85dac2403e` | `DEFINITION` | Guarded defining equation for the fresh named proof term `projectFloat`. |
| 6 | 60–62 / `rule-004b77064d41c5296c2b9a4939f9183460b9b84c088f3d578b78745808abb257` | `DEFINITION` | Reverse normalization orientation of the same guarded definition, naming the projection as `projectFloat`. |
| 7 | 63 / `rule-bd643f181b65c0fe3a82e3f5d4c2d3ba4e8c80c16d39267cbbeb88b6371fbbea` | `DEFINITION` | Float identity case completing the fresh `projectFloat` helper. |
| 8 | 67–70 / `rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7` | `DOMAIN_LEMMA` | Guarded equation for the pre-existing dynamic `applyBin` symbol. It restates the supplied Float dispatch after symbolic Val projection, is marked `simplification`, and is never proved rule-free first. It is directly used by the first source loop. |
| 9 | 71–74 / `rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f` | `DOMAIN_LEMMA` | Analogous guarded subtraction equation for `applyBin`; it is used by the deviation loop and is not proved rule-free first. |
| 10 | 77 / `rule-07e38f1df5e81d6a854903024c0a7ce85cdf237fa93efbb509e769c262f3bdac` | `DEFINITION` | Empty-sequence equation for the fresh sum fold. |
| 11 | 78–79 / `rule-c262061ba80c2445257ddcd2f041f47b796a7c356c25ccd0abdc0c61f65a8ab4` | `DEFINITION` | Tail-descending recurrence for the fresh sum fold. |
| 12 | 81 / `rule-e05dfca0da35f598226b9eaa3edd9657b842c4ca648929840531db77d9a1cc03` | `DEFINITION` | Empty-sequence equation for the fresh deviation fold. |
| 13 | 82–86 / `rule-86b9970d9f7bc47527162d9e7b2d0edf29e0222f21c615a73606be510fae2a55` | `DEFINITION` | Tail-descending recurrence for the fresh deviation fold. |
| 14 | 88–89 / `rule-64fc7fe46c4d3d4cba6d1895cec98deeda5e2d85a8aa58929c5d686628e20725` | `DEFINITION` | Zero-length branch defining the fresh result summary `madResult`. |
| 15 | 90–99 / `rule-07a3b4455e03279c9c5f1321b884035b05b44559041506e96c2b2c8559a8ca52` | `DEFINITION` | Complementary nonzero branch defining `madResult` from the two folds. |

There are 12 definitions, zero operational rules, zero proved-derived lemmas,
and three domain lemmas. Every rule carrying the literal `simplification`
attribute is either a definition or a domain lemma. `prove.sh` compiles all
verification rules before its only `kprove spec.k` command, so none satisfies
the required prove-first/use-later protocol for `PROVED_DERIVED_LEMMA`.
