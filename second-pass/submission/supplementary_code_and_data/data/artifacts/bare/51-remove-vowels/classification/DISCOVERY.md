# Trust-boundary discovery

The exhaustive canonical inventory contains three rules, in the
`VERIFICATION` module. All three are classified as `DEFINITION`:

- `rule-d70a0aac3bb3b348786898ec6b394dbdace66562eea52f3eafc591f02cd22ab4`
  expands the named `removeLowerVowels` summary into deletion of `a`, `e`, `i`,
  `o`, and `u`.
- `rule-49a18c81258ea070950de54bb16d8b99c51a26b8c67538986c2c3b31a1fafa3f`
  expands the named `removeUpperVowels` summary into deletion of `A`, `E`, `I`,
  `O`, and `U`.
- `rule-cdf7c02d83c3928a7f8b88a45691a3681e2a79a579a8503bd2c19f81bb514a86`
  defines `removeVowelsSpec` by composing the two preceding summaries.

These are definitional expansions of named mathematical summaries, not
ordinary execution rules and not additional mathematical facts. None of the
three canonical entries carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first compiles
the entire `VERIFICATION` module, including all three rules, into
`verification-kompiled`. Its sole `kprove` invocation then proves `spec.k`
against that already-complete module. Consequently, Stage 1 contains no proof
of any inventoried rule against an earlier module from which that exact rule
was absent.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule states an additional
trusted mathematical fact used to close the proof.
