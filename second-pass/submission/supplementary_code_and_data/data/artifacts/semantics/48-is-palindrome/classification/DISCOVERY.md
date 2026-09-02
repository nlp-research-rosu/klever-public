# Trust-boundary discovery

The canonical inventory contains one rule from the local `VERIFICATION`
module:

- `rule-f5ed2b78f37cc7987423ef2f718f88456d091c4c95e893898cf03b437c6f3d3e`
  is classified as `DEFINITION`. It defines the named Boolean proof term
  `palindrome(IS)` by expansion to equality of `IS` with the supplied
  semantics' negative-step string-slice summary. It is an equation defining
  the contract term, not an execution rule or an additional mathematical
  fact. The rule has no `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1's `prove.sh` first compiles
`verification.k` into `verification-kompiled` and then runs `kprove spec.k`
against that compiled definition. Consequently, the sole inventoried rule was
already present during the proof; Stage 1 does not prove its exact statement
against a module from which the rule is absent.

## Domain lemmas

The domain-lemma set is empty. The local verification-module closure adds no
trusted mathematical facts beyond the named contract definition described
above.
