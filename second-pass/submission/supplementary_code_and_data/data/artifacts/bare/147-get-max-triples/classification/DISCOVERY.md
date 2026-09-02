# K proof trust-boundary discovery

The canonical inventory contains two rules, in the order shown in
`/reference/rule-inventory.json`. Both are classified as `DEFINITION`.

| Source rule | Classification | Reason |
| --- | --- | --- |
| `rule-5594fc18d5a757bd7bc014744a8a19e50e1ec19fb7038acbd49648528470fc16` | `DEFINITION` | The rule is an equation defining `choose3(X)`, a named mathematical summary used by the contract. |
| `rule-6d32eb21bafe6c64f6064ecdd1a030bcb2fbcfbd60c40dcdbe25253ac5f1150b` | `DEFINITION` | The rule is an equation defining `validTripleCount(N)`, the named proof target that summarizes the two residue classes. |

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` first compiles `verification.k` with
`--main-module VERIFICATION`, so both inventory rules are already present in
`verification-kompiled`. It then runs:

```sh
kprove spec.k --definition verification-kompiled
```

That command proves the program-execution claim against
`validTripleCount(N)`. It does not first prove either inventory rule against a
module omitting that rule, and therefore provides no ordering or exact
correspondence evidence that would permit `PROVED_DERIVED_LEMMA`.

## Operational and domain rules

No canonical rule is classified as `OPERATIONAL_RULE`: the inventory contains
only the two mathematical-summary equations from the local verification
module, not the execution rules from `semantic.k`.

The `DOMAIN_LEMMA` set is empty. Neither inventory rule has a `simplification`
attribute, and both rules fit the explicit `DEFINITION` category. The
mathematical connection between the natural-language triple-counting contract
and the chosen `validTripleCount` summary is explained in Stage 1 comments but
is not separately proved as an inventory rule; this does not turn either
definitional equation into a proved derived lemma.
