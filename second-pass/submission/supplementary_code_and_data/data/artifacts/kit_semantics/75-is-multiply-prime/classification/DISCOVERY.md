# Trust-boundary discovery

## Canonical inventory

`/reference/rule-inventory.json` is treated as exhaustive and canonical. It
identifies `verification.k`, module `VERIFICATION`, as the complete local
verification-module closure and contains zero rules.

The canonical `inventory_sha256` is:

```text
4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

Recomputing SHA-256 over the compact canonical rules array, `[]`, produced the
same value. The mounted `verification.k` also matches the inventory's recorded
file digest,
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`.

Because the canonical inventory is empty, `trust-boundary.json` has an empty
`rules` array. This classifies every canonical `source_rule_id` exactly once
and preserves inventory order vacuously; no noncanonical entry was added.

## Classification results

| Classification | Count | Reason |
|---|---:|---|
| `DEFINITION` | 0 | The local verification closure declares no equations, recurrences, macros, or structural helpers. |
| `OPERATIONAL_RULE` | 0 | The local verification closure adds no execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable local rule exists, and Stage 1 contains no prior bridge-free proof of an exact rule followed by installation of that rule. |
| `DOMAIN_LEMMA` | 0 | The local verification closure adds no trusted mathematical fact. |

There are no inventoried rules carrying the `simplification` attribute, so the
special `DEFINITION`-or-`DOMAIN_LEMMA` restriction has no instances.

## Mounted verification module

The entire mounted local verification module is:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It contributes no local rule declarations. Its imported MPY rules belong to
the supplied reference semantics; the launcher-generated inventory explicitly
defines the local verification-module closure to contain only `VERIFICATION`
and no rules. Accordingly, this discovery does not invent classifications for
rules outside the canonical inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles the rule-free `VERIFICATION` module and
then runs:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.is-multiply-prime
```

The mounted `positive-proof.out` contains `#Top`, but that command proves the
target reachability claim. It does not prove an exact reusable rule against a
module lacking that rule, and no later build installs such a rule. The negative
vacuity and body-mutation commands likewise validate the target claim rather
than establish reusable derived rules. Therefore no inventory item could
qualify as `PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is empty.

Stage 1 closes the target claim through the supplied operational semantics and
the claim's explicit finite Boolean postcondition. The local verification
module supplies no additional mathematical rule trusted to close the proof.

## Resulting local trust boundary

The finalized proof has no rule-level additions in its local verification
module closure: no definitions, operational bridges, proved derived lemmas, or
trusted domain lemmas. Its remaining trust lies outside this canonical local
rule inventory—in particular, the supplied reference semantics and the K
toolchain identified by the Stage 1 report.
