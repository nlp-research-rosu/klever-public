# K proof trust-boundary discovery

The canonical inventory identifies 18 rules in the local `VERIFICATION`
module and has inventory SHA-256
`0d5fe23d9dedd3ad555afbe0aa1bed145a5c21efee172628c5584122321912a3`.
The mounted `verification.k` hashes to the inventory's recorded verification
SHA-256,
`cff7fa18bbc3131014865e83f3d8ab7fb295dbf5c309646b1cf45f6d7d6aae7f`.

## Classification summary

- 15 `DEFINITION` rules: the three translated-program macros, the `intsVS`
  embedding equations, and the equations/recurrences for `nextRolling`,
  `rollingAcc`, `firstAfter`, `maximumAfter`, and `numberAfter`.
- 2 `OPERATIONAL_RULE` rules: the priority-40 `#iterNext` observations for the
  empty and nonempty `intsVS` representations. These extend execution of the
  verification representation through the existing iterator protocol; they
  do not assert a separate mathematical theorem.
- 0 `PROVED_DERIVED_LEMMA` rules.
- 1 `DOMAIN_LEMMA` rule:
  `rule-49d35612d63bf56fdd624a16c30b97a62ddbf196c0acb5a07976bc8b31be1a41`,
  whose statement is `firstAfter(_IS:IntSeq, false) => false`.

The domain-lemma set is **not empty**. The `firstAfter` shortcut is
mathematically derivable by induction from the empty and nonempty structural
equations, but it is itself present in `VERIFICATION` when that module is
compiled. Stage 1 contains no earlier proof of its exact statement against a
definition omitting it, so it remains a trusted mathematical fact for this
proof.

## Separately proved derived lemmas

There are no separately proved derived rules in the canonical inventory.
Stage 1 `prove.sh` first runs:

```sh
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Only after compiling all 18 inventoried rules into that definition does it run:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Thus no inventoried rule is first proved against a module that excludes the
rule and then reused with exact correspondence. `spec.k` does contain the
reachability claim `rolling-max-loop` alongside `rolling-max-correct`, but the
loop claim is not a rule in the local verification-module inventory and is not
staged by `prove.sh` as a proved rule before compilation. It therefore provides
no `PROVED_DERIVED_LEMMA` classification for an inventoried source rule.

No inventory rule carries the `simplification` attribute, so the special
restriction on such rules is satisfied vacuously.
