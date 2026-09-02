# Trust-boundary discovery

## Canonical scope

The sole classification source is
`/reference/rule-inventory.json`. Its `inventory_sha256` is
`aae99af3f9847ce2ab92c4c7c79358ecfcde2abeaa10a418c3fd084758889f0e`,
and it contains 10 rules from the local `VERIFICATION` closure. The mounted
`verification.k` SHA-256 is
`9696cfcae2e2436114cda643ad130cf607767bf60afd368c0a63ddbe9a1c863b`,
which matches the inventory's `verification_sha256`.

Every canonical `source_rule_id` appears exactly once in
`trust-boundary.json`, in inventory order. No rules imported from the supplied
semantics were added beyond the canonical list.

## Classification summary

| Classification | Count | Rule set |
|---|---:|---|
| `DEFINITION` | 9 | Four macro equations; two `allInts` equations; two `collectAcc` equations; one `byLengthVS` equation |
| `OPERATIONAL_RULE` | 0 | Empty |
| `PROVED_DERIVED_LEMMA` | 0 | Empty |
| `DOMAIN_LEMMA` | 1 | `rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430` |

The four macro rules are definitions because they expand named proof syntax
into fixed AST-constructor terms. The `allInts`, `collectAcc`, and
`byLengthVS` rules are base equations or structural recurrences defining
mathematical summaries. None is an ordinary execution or observation rule, so
the `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` compiles `verification.k` at lines 25–29 before any proof
command. The resulting definition already contains every canonical rule,
including the `applyCmp` simplification rule. The later commands at lines
47–56 prove the loop and target specifications against that definition. No
earlier command proves the exact simplification statement against a module
that omits it, and no rule-free connection module or exact corresponding claim
is present in the mounted evidence. The mutation probes establish
non-vacuity/body sensitivity, not the simplification rule itself.

Consequently, the Stage 1 comment calling the rule a “Derived
sort-refinement lemma” and the prose derivation in `PROOF.md` do not satisfy
the required proof ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430`
  (`verification.k`, lines 75–78).

This rule carries the `simplification` attribute and adds a guarded
sort-refinement fact for `applyCmp`. It is not a definition of a new summary
symbol, recurrence, macro, or named proof term. Because the target proofs run
with the rule already installed and Stage 1 supplies no prior exact proof
without it, the fact remains in the trusted mathematical domain boundary.

No other canonical rule carries `simplification`, and the remaining nine rules
are definitional equations. Thus there are no additional domain lemmas.
