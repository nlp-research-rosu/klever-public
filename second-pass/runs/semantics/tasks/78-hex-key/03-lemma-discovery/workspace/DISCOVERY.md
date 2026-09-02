# Trust-boundary discovery

The canonical inventory declares eight rules in `HEX-KEY-VERIFICATION`. All
eight are classified as `DEFINITION`. The first two expand named macro terms
to the exact translated Python statement trees. The remaining six define
mathematical summaries or structural helpers through equations and
recurrences:

- `isPrimeHexCode` defines membership in the fixed code sequence for
  `2`, `3`, `5`, `7`, `B`, and `D`.
- `primeHexBit` converts that predicate to a numeric indicator.
- The two `hexCount` rules define its empty case and constructor recurrence.
- The two `finalDigit` rules define its empty case and constructor recurrence.

No inventory rule is an `OPERATIONAL_RULE`: none of the eight rules advances
or observes the K machine configuration. The macro rules only name syntax
trees, while the function rules compute proof summaries.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 `prove.sh` compiles `verification.k`, containing all eight inventory
rules, before its sole `kprove spec.k` invocation. It does not first prove any
inventory rule against a module from which that exact rule is absent, nor does
it subsequently introduce a proved rule. The `loop-lemma` in `spec.k` is a
reachability claim proved during that invocation, not a canonical inventory
rule or a reusable rule introduced after a separate proof. The recorded
`kprove.out` contains `#Top`, establishing the claims but not the required
proof-before-rule ordering for any inventory entry.

## Domain lemmas

The domain-lemma set is empty. No additional mathematical fact is trusted as
a `DOMAIN_LEMMA`; the mathematical helper rules in the inventory are
definitions of the summaries used by the claims.
