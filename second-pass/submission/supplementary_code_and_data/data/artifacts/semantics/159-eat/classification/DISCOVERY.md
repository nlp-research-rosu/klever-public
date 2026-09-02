# Trust-boundary discovery

The canonical inventory identifies one rule in the local verification-module
closure. It is classified as `DEFINITION`.

- `rule-0f9e6b9b44ef2a0419c9cc81385d08d4b41683c3674748beb8711d590083294b`
  expands the named `eatClosure` term into the `closureVal` that embeds the
  translated parameters and function body. This is an equation defining a
  structural proof term used to initialize the symbolic execution.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` first
compiles `verification.k`, including the `eatClosure` rule, into
`verification-kompiled`. It then runs `kprove spec.k` against that compiled
definition. Thus Stage 1 contains no proof of this rule against a module that
omits it, and there is no evidence satisfying the required ordering for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The inventory contains no additional trusted
mathematical fact; its sole rule is the structural definition described above.
