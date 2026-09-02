# Trust-boundary discovery

The canonical inventory has SHA-256
`50a312a7b1d384afc035db8b18aec0130d8781eb9fdd063798f093ac0523f7d4`
and contains four rules, all in module `VERIFICATION`. Each canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order.

## Classification

All four rules are `DEFINITION`:

- `rule-0b1487f16122d27497d8c2b109033346786d2ad1ea565f1e4e43ff7b63a74ee6`
  is the empty-sequence base equation for `deleteAcc`.
- `rule-9958ef1e5cedad6393d09ebbc3c826f504a56323dc84f7f28b3c814045e0cd23`
  is the `iCons` structural recurrence for `deleteAcc`.
- `rule-ec000690c3aa4109db5bb6cc52464e7d8893560fc3144e4db5d63ff5b9da171c`
  is the empty-sequence base equation for `reverseDeleteAcc`.
- `rule-d31842da509f8fdf40a424d203025312d80e1fea7bb96b8b765027072309de32`
  is the `iCons` structural recurrence for `reverseDeleteAcc`.

The two base/step pairs define total named summaries over the two constructors
of `IntSeq`. Their recursive cases descend from `iCons(X, XS)` to `XS`; their
conditionals specify whether the current character is omitted or accumulated.
They rewrite only the named summary terms and do not match the K configuration,
program syntax, continuation, environment, or state cells. They are therefore
definitions rather than operational rules or additional mathematical facts.

None of the four canonical rules carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` compiles `verification.k` with all four rules already
present, then proves the reachability claims in `spec.k`. It does not first
prove any canonical rule's exact statement against a module that excludes that
rule. The `reverse-delete-loop` reachability claim is described in
`PROOF.md` as a derived loop circularity, but it is a claim in `spec.k`, not a
rule in the canonical inventory, so it is not classified here.

The positive Stage 1 evidence is `proof-positive.out`, containing `#Top` for
the combined `spec.k` proof. The mutation outputs establish discrimination of
the target claims, but neither is evidence of the required exclude-then-prove
ordering for any inventory rule.

## Other classification sets

The `OPERATIONAL_RULE` set is empty: the inventory contains no rule describing
ordinary program execution or observation.

The `DOMAIN_LEMMA` set is explicitly empty: no additional trusted mathematical
fact is present in the canonical verification-module rule inventory.
