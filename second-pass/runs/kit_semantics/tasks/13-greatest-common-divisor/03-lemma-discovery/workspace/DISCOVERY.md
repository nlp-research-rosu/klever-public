# Trust-boundary discovery

The canonical inventory `/reference/rule-inventory.json` has schema version 2,
inventory SHA-256
`eb71eadbe29655ad22f91b06153efb05bf94d9f8895ad0a721a1516e8ed11955`,
and exactly two rules. `trust-boundary.json` preserves their inventory order
and classifies each `source_rule_id` exactly once.

## Classifications

Both canonical rules are classified as `DEFINITION`.

- `rule-ac25cee0dbe61d7bbb5672f36b334215328039ce27068faf6b9672d9b4b45bad`
  is the `gcdEuclid(A, 0)` base equation. It defines the summary at a zero
  second argument as `absInt(A)`. Its `simplification` attribute changes how
  that definition is reduced during proof, but the rule still operates only
  on the named mathematical summary and does not execute or observe MPY
  program state.
- `rule-3b63b038b1412f056176447a2f40e468a644718e69d0613430286edb3756cc6e`
  is the guarded Euclidean recurrence for `gcdEuclid` when the second argument
  is nonzero. It is an equation defining the same mathematical summary, not an
  operational rule. Its guard complements the base case, and its
  `simplification` attribute is consistent with the required `DEFINITION`
  classification.

No canonical rule is an `OPERATIONAL_RULE`: the inventory contains no rule
whose left-hand side is an MPY computation or configuration. The operational
semantics is imported from the supplied reference semantics and is outside the
launcher-defined local verification-module inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k`, which already contains both
canonical rules, into `verification-kompiled`. Every subsequent `kprove`
command uses that compiled definition. Stage 1 therefore contains no proof
command that proves either exact rule statement against a module from which
that rule is absent, and no ordering evidence permits either rule to be
classified as separately proved.

The Stage 1 `SPEC.gcd-loop` and `SPEC.gcd-entry` reachability claims do print
`#Top`, but they are claims in `spec.k`, not canonical rules in
`rule-inventory.json`, and they do not establish the required rule-absent
proof ordering for either inventory entry.

## Domain lemmas

The domain-lemma set is empty. Neither canonical rule is an additional
mathematical fact layered on top of an independently defined `gcdEuclid`;
together they are the base equation and recurrence that define that summary.
