# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, whose
`inventory_sha256` is
`769426b2163a87c782102e56a3bed0a12ffc57f4f5045ad2ec51f22e842de036`.
It contains four rules, all in the mounted Stage 1 `VERIFICATION` module.
`trust-boundary.json` preserves those four `source_rule_id` values in canonical
inventory order and classifies each exactly once.

## Classifications

All four canonical rules are `DEFINITION`.

1. `rule-0d84adc0fbe6fe3c0ad834b7cabaec34b6f1a14a37b1d97e6309a591d770d73e`
   is the base equation of `trialPrime`. On the defined domain `D >= 2`, it
   returns the accumulated Boolean when no candidate divisor remains.
2. `rule-f7636d5013012b53a727f7a69e19eee33049f6844171d011930dcbc50544e7b5`
   is the divisible-case recurrence of `trialPrime`. It advances the candidate
   divisor and records `false`.
3. `rule-c788496123caab512e57df64b2dd0261154d3d075835223008964c8feddfab13`
   is the nondivisible-case recurrence of `trialPrime`. It advances the
   candidate divisor and preserves the accumulator.
4. `rule-835478f853e5b3aed5797027e0534f3648fdf19cc84cf0cc5b7ef40a0675b715`
   is the wrapper equation defining `primeNat(N)` as
   `trialPrime(N, 2, N >=Int 2)`.

These rules are equations and recurrences for named mathematical summaries.
They do not match K configuration cells, execute Python constructors, observe
runtime state, or replace an operational step. Therefore none is an
`OPERATIONAL_RULE`.

The inventory records an empty attribute list for every rule, so there is no
`simplification`-attributed rule requiring a `DEFINITION` versus
`DOMAIN_LEMMA` decision.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The mounted Stage 1 `/reference/k-proof/prove.sh` first compiles
`verification.k` as module `VERIFICATION`; that file already contains all four
canonical rules. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The recorded `/reference/k-proof/positive-proof.out` contains `#Top`, but this
proves the reachability claims using a definition that already contains the
four rules. Stage 1 has no command that first proves the exact statement of any
canonical rule against a module from which that rule is absent, and no
rule-free proof artifact with exact rule correspondence. Consequently none
satisfies the required ordering for `PROVED_DERIVED_LEMMA`.

`SPEC.loop-invariant` is described in Stage 1 `PROOF.md` as a derived
reachability lemma/circularity, but it is a claim in `spec.k`, not a rule in the
canonical local verification-module inventory. It is therefore outside this
per-rule classification.

## Domain lemmas

The domain-lemma set is empty.

The `trialPrime` cases and `primeNat` wrapper define the meaning of proof terms;
they do not assert an additional reusable mathematical fact about independently
defined terms. No canonical rule therefore requires trust as a `DOMAIN_LEMMA`.
