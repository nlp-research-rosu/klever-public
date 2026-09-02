# Trust-boundary rule classification

## Canonical inventory

The exhaustive canonical inventory is
`/reference/rule-inventory.json`. It identifies verification module
`VERIFICATION`, carries inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and contains zero rule entries:

```json
"rules": []
```

Consequently, `trust-boundary.json` contains an empty `rules` array. This
classifies every canonical `source_rule_id` exactly once, in inventory order,
because there are no canonical rule IDs to classify.

## Classification explanation

All four classification sets are empty:

- **DEFINITION:** none.
- **OPERATIONAL_RULE:** none.
- **PROVED_DERIVED_LEMMA:** none.
- **DOMAIN_LEMMA:** none.

In particular, the domain-lemma set is empty.

The mounted Stage 1 `verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It adds no equation, recurrence, macro expansion, structural helper,
operational rule, simplification rule, or mathematical lemma. Rules in the
supplied reference semantics are not added to this classification: the
launcher-generated canonical inventory is explicitly exhaustive for this
task, and it contains no entries.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` compiles `verification.k` and runs:

- the target reachability claim in `spec.k`;
- an expected-failure false-result claim in `spec-vacuity.k`; and
- an expected-failure body-mutation claim in `spec-body-mutation.k`.

None of those claims proves the exact statement of a reusable rule that is
subsequently installed into a module containing that rule. `prove.sh` has no
earlier bridge-free lemma proof followed by a later build that adds a
corresponding rule. The finalized Stage 1 `PROOF.md` independently records
that there are no proof-local extensions. Therefore no Stage 1 artifact
supports a `PROVED_DERIVED_LEMMA` classification.

## Simplification-rule check

The canonical inventory contains no rules carrying the `simplification`
attribute. Thus there is no simplification rule requiring classification as
`DEFINITION` or `DOMAIN_LEMMA`.
