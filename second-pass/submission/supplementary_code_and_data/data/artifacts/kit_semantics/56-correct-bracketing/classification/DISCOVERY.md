# Trust-boundary discovery

## Canonical scope

The exhaustive source of rule identities and ordering is
`/reference/rule-inventory.json`. Its embedded `inventory_sha256` is
`58de3e4264854ce375024959a6666e49997e6893c6bcfe16411f27c5f9579b3d`.
It contains seven rules, all from the mounted Stage 1 `VERIFICATION` module.
Each canonical `source_rule_id` appears exactly once in
`trust-boundary.json`, in inventory order.

The inventory contains no rule carrying the `simplification` attribute.

## Classification

All seven rules are `DEFINITION`:

- The two `bracketDelta` rules are the empty-sequence equation and structural
  recurrence defining net balance change.
- The two `bracketPrefixOK` rules are the empty-sequence equation and
  structural recurrence defining prefix nonnegativity from a supplied balance.
- The two `bracketChars` rules are the empty-sequence equation and structural
  recurrence defining the prompt's `<`/`>` character domain.
- The `bracketCorrect` rule defines the named result predicate by composing
  prefix safety with zero final delta.

These rules rewrite only named mathematical summary terms. None matches a
`<k>` cell, Python AST execution term, continuation, environment, scope, heap,
stack, return cell, exception cell, or other operational configuration.
Consequently, none is an `OPERATIONAL_RULE`.

The recurrences are definitional rather than separately admitted mathematical
facts: their empty and `iCons` cases define the summaries by structural
recursion. The final rule is likewise a direct composition defining a named
proof term. Therefore no inventory entry is a `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The mounted Stage 1 evidence does not show any inventory rule first proved
against a module that omits that exact rule. In
`/reference/k-proof/prove.sh`, lines 17–20 compile `verification.k` as the
`VERIFICATION` definition with all seven inventory rules already present.
Only afterward do lines 22–29 run the loop and complete-spec proofs against
that compiled definition. Thus those proof runs establish the claims under the
seven definitions; they do not prove any one of the seven rules before adding
it.

`SPEC.loop-inv` is a reachability claim in `spec.k`, not a canonical rule entry
in `/reference/rule-inventory.json`, so it is outside this rule-classification
array and is not relabeled as a proved derived rule.

## Domain-lemma set

The domain-lemma set is empty.

No inventory rule is an additional trusted mathematical fact used to close the
proof. The proof's mathematical vocabulary is introduced entirely through the
four named definitions above, while execution behavior comes from the supplied
reference semantics outside the launcher-defined local verification-module
inventory.
