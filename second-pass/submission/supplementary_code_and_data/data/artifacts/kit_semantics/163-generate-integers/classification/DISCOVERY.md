# Trust-boundary discovery

## Canonical scope

The classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory of the local verification-module closure. Its
`inventory_sha256` is
`3d466cb6625fb9c3bf00b56d4b753370f1ae5da4550698bf12d5415a2784b6ea`.
The inventory contains four rules, all from module `VERIFICATION`, and none
carries the `simplification` attribute.

## Classifications

All four rules are `DEFINITION`:

1. `rule-e485812b492df1e2d627d73dd057ca7d00d04af511b2dc7bdd89e5e026812d48`
   is the unconditional defining equation for the total summary function
   `inClosedSpan`.
2. `rule-8e0942964d5eb30f25988841f3b2b7d776f3c0a617ec8af6602e2863e4e471e1`
   is the `true` constructor case of the total structural helper `keepDigit`.
3. `rule-1ca5229dc152dfa3dcd21aa4974e7959fd9ec785342863588027006c39579132`
   is the complementary `false` constructor case of `keepDigit`. The two
   Boolean cases are disjoint and exhaustive.
4. `rule-1d4a13583c5d0924f771db5d1584f01d12bfcbce0077644a396fa7bf3d6fa6e8`
   is the unconditional finite defining equation for `expectedDigits`, built
   from the preceding summary functions in ascending digit order.

These rules define mathematical postcondition terms. None matches a
configuration cell, advances execution, observes runtime state, or replaces a
fixed-semantics program step, so the `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` compiles `verification.k` with all four
inventory rules already present and then proves `SPEC.generate-integers`.
Its two additional `kprove` commands run expected-failure mutation probes.
There is no command that first proves the exact statement of any inventory
rule against a module from which that rule is absent. The mounted `PROOF.md`
likewise identifies the rules as definitional summaries and records no
derived-lemma proof phase. Consequently, the
`PROVED_DERIVED_LEMMA` set is empty.

## Domain lemmas

The domain-lemma set is empty. No canonical rule states an additional trusted
mathematical fact: every rule is part of the exhaustive defining equations for
`inClosedSpan`, `keepDigit`, or `expectedDigits`.
