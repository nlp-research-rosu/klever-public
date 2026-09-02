# Trust-boundary discovery

## Canonical inventory

The exhaustive canonical source is
`/reference/rule-inventory.json`. It identifies `VERIFICATION` as the sole
local verification module, records inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and contains an empty `rules` array.

Accordingly, there are no canonical `source_rule_id` values to classify.
`trust-boundary.json` preserves the canonical inventory order and classifies
every inventory rule exactly once: vacuously, because the exhaustive inventory
has zero rules.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The local verification-module closure declares no equations, recurrences, macro expansions, or structural helpers. |
| `OPERATIONAL_RULE` | 0 | The local verification-module closure adds no execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable local rule is separately proved before being installed. |
| `DOMAIN_LEMMA` | 0 | No additional mathematical fact is added to close the proof. |

The canonical inventory also contains no rule carrying the `simplification`
attribute, so the required `DEFINITION`-or-`DOMAIN_LEMMA` restriction has no
instances to resolve.

## Stage 1 evidence

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It introduces no local syntax equations, rules, simplification rules, or
lemmas. Rules belonging to the supplied reference semantics are not canonical
inventory entries and therefore are not added to or reformulated in
`trust-boundary.json`.

The mounted `/reference/k-proof/prove.sh` compiles `VERIFICATION` and directly
proves `SPEC`. It does not first prove the exact statement of any reusable rule
against a module lacking that rule and then install the rule. Its later
vacuity and body-mutation commands are negative discrimination probes, not
proofs of reusable derived lemmas.

The mounted `/reference/k-proof/PROOF.md` independently records that
`verification.k` declares no proof-local functions, equations, simplification
rules, ordinary rewrites, operational bridges, trusted primitives, or
auxiliary claims.

## Derived and domain lemmas

There are no separately proved derived lemmas. Consequently, there is no Stage
1 proof command or earlier rule-free module to associate with a
`PROVED_DERIVED_LEMMA` entry.

The domain-lemma set is empty.
