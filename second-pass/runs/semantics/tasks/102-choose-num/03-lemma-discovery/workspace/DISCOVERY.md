# Trust-boundary discovery

The canonical inventory has two rules, both in
`CHOOSE-NUM-VERIFICATION`, and each is classified exactly once.

- `rule-c03e276aa838c9ccf89f1a02a5355f619fd9394ba2274696d4c6c3b5f6c8c047`
  is a `DEFINITION`. Its equation defines the named summary
  `largestEvenInRange(X, Y)` using `Y - pyMod(Y, 2)` and an interval-membership
  test. It is a definitional expansion, not an independently asserted
  mathematical lemma.
- `rule-322c7434385e18d731b0a8f9faaae283673f25cd14302a2d02662c6bb69252e0`
  is an `OPERATIONAL_RULE`. It turns the verification-only `#chooseNum(X, Y)`
  command into execution of a closure whose statements match the translated
  `choose_num` body. This is program injection/observation machinery in the
  verification model.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications. Stage 1's `prove.sh`
first compiles `verification.k` as `CHOOSE-NUM-VERIFICATION`, which already
contains both inventoried rules, and then runs `kprove spec.k` against that
compiled definition. The claims in `spec.k` prove the function behavior, but
there is no earlier proof command against a module omitting either rule and no
later import of an exact proved rule statement. Therefore Stage 1 provides no
proof-before-import evidence for a separately proved derived lemma.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. Neither inventoried rule is an additional
trusted mathematical fact: one is a named definition and the other is an
operational execution wrapper. The inventory also contains no rule carrying
the `simplification` attribute.
