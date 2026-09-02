# Trust-boundary discovery

The canonical inventory contains one rule, in module `VERIFICATION`.

`rule-c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9`
is classified as `DEFINITION`. It is the defining equation for
`primeHexCount(S)`: the named contract summary expands to the sum of the
occurrence counts for `2`, `3`, `5`, `7`, `B`, and `D`. It is an equation
introducing a mathematical summary, not an execution rule or an additional
mathematical fact.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` compiles
`verification.k` into `verification-kompiled` before running:

```text
kprove spec.k --definition verification-kompiled --spec-module HEX-KEY-SPEC
```

Thus the inventoried rule is already present in the definition used by the
proof. There is no earlier proof against a module omitting that rule, and no
later exact rule installation that could justify `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The inventory contains no trusted additional
mathematical fact and no rule carrying the `simplification` attribute.

The execution rules in `semantic.k` belong to the language model, but they are
not members of the launcher-generated canonical verification-module inventory
and therefore are not additional entries in this classification file.
