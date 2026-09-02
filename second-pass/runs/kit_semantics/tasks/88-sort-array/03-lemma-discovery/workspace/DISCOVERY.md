# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with canonical
inventory SHA-256
`79bcb25ad216ecb707ec3f1dc4591a1afb03ed9a778f0fa2d7bd947b49333a50`.
It contains four rules in inventory order, all from the mounted Stage 1
`VERIFICATION` module. The mounted `verification.k` hash matches the
inventory's recorded verification hash.

## Classifications

All four rules are classified as `DEFINITION`.

1. `rule-61708f547727d7aa918ad6bf8a016e92b25d1ccd0e36098b415347016593af3e`
   is the empty-sequence base equation for `intVals`.
2. `rule-cfcac90169b6a7cd2244c88675990844903b2aaec267489c942ae4ccd2156521`
   is the recursive `intVals` constructor equation. It embeds the integer head
   as a value and recursively embeds the tail.
3. `rule-a9f37c1eb33efeb535d72a822b8dfc6ea4e900fe284743e255793a6456e2a7e8`
   is the empty-sequence base equation for the `nonNegative` predicate.
4. `rule-758572a581b5030cc9404c6609e8681bf8bd5aa4744ae6307a1a2074351c15c9`
   is the recursive definition of `nonNegative`, checking the head and
   recurring on the structurally smaller tail.

These are equations defining two named proof-side terms over the complete
`IntSeq` constructor set. They do not observe or advance a Python execution
configuration, so none is an `OPERATIONAL_RULE`. Although `nonNegative` is
used to describe the theorem's input domain, its two rules define that
predicate; they do not add an independent mathematical fact.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` compiles `verification.k` and proves the target
claims `SPEC.empty` and `SPEC.nonempty`, followed by negative mutation probes.
It does not first prove the exact statement of any inventory rule against a
module from which that rule is absent. No inventory rule therefore satisfies
the required evidence ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact, and no rule carries the `simplification` attribute.
