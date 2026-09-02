# Trust-boundary discovery

The exhaustive canonical inventory contains one rule:
`rule-9c0f13f3d959c4d25eeabaa331cdf4ff8c0471110b739b101cee0ce8e9d29e31`.
It is classified as `PROVED_DERIVED_LEMMA`.

## Separately proved derived lemma

The inventoried rule in `verification.k` is the reusable form of the
`loop-invariant` claim in `loop-lemma-spec.k`. The claim and rule have the same
loop control, program and input cells, environment bindings, and result
`VInt(scan(L, IS, A))`. The rule additionally carries `priority(40)`, which
controls its use once installed and does not introduce a different statement.

The Stage 1 ordering in `prove.sh` establishes the required proof boundary:

1. It compiles `verification-core.k` as module `VERIFICATION-CORE`. That module
   contains the semantic and summary definitions but not the inventoried rule.
2. It runs `kprove loop-lemma-spec.k` against
   `verification-core-kompiled`, proving the matching `loop-invariant` claim.
3. Only after that proof does it compile `verification.k`, which installs the
   proved statement as the inventoried rule for the final `spec.k` proof.

Thus the classification rests on both exact statement correspondence and
proof-before-installation evidence, rather than on the source comment alone.

The inventory contains no rules with the `simplification` attribute. It also
contains no `DEFINITION` or `OPERATIONAL_RULE` entries. The domain-lemma set is
explicitly empty.
