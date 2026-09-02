# K proof trust-boundary discovery

The canonical inventory identifies 10 rules in the local `VERIFICATION`
module closure. Each is classified exactly once in `trust-boundary.json`, in
the inventory's original order.

## Definitions

Seven rules are definitions:

- `rule-62ed89db83ac9521d185c3efa101e7178564396966b30641c489bd6e0da25b21`
  and
  `rule-5f7d67ec7de6f261bc639a5357fe24c0755d69896737437ce4a6460d8c904b01`
  are the empty-map and extension equations for the locally introduced
  `freshScopes` structural summary.
- `rule-9389ac349c7264d24779fe506309eca98bcd5f175d2c68b09ee24d4612d2cd90`,
  `rule-6a85e13e9e00989679ee454ab9a6312358f25a6af6f49da2f2cfaea3756357f4`,
  and
  `rule-e42c4c16b30b74db12ec47f2e2a59c4d1e568e5aff8fe56aef128de15f5b614b`
  expand the named body, module, and closure proof terms.
- `rule-a24b2678e0b18c55695f70b54faddde8407de9768d019653098bb326e564557a`
  and
  `rule-91e33937d50f2f1a09154fc22d8b5577e75677533363d7a9391ff2152f58497f`
  are the zero equation and positive recurrence defining `baseDigits`. These
  are the two rules carrying `simplification`, and both are classified as
  `DEFINITION`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains three rules:

- `rule-437465420fc6223721ad7c1f90c24fba6434c7a8d0b69e9c65c7139faac9cb24`
  supplies the unproved connection from `freshScopes(L, S)` to
  `L in_keys(S) == false`.
- `rule-746c49465cb8335d005b3a331b93eb26bdf586974933b9d025250760d4d0c29d`
  supplies the unproved fresh-key Map-update normalization.
- `rule-82f2c726c84180f9e0c75a16a31dd3a15476f84ccb4dacad03db18bcaca52fda`
  supplies the unproved corresponding Map-deletion normalization.

These are reusable mathematical facts about the allocator invariant and
finite maps, rather than definitions of their left-hand symbols or ordinary
Python execution rules.

## Proved derived lemmas and operational rules

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` compiles
`verification.k` with all 10 inventory rules already present and then invokes
`kprove spec.k`. It contains no earlier proof command against a module from
which any inventory rule is absent, and there is no separate proof artifact
showing exact statement correspondence. The successful claims therefore do
not establish the required proof-before-use ordering for any reusable rule.

There are also no `OPERATIONAL_RULE` entries in this local verification-module
inventory. Imported MPY operational semantics are outside this inventory;
the local rules consist only of named definitions and the three additional
domain facts above.
