# K proof trust-boundary discovery

The canonical inventory hash is
`769afab15f5d428eaaf9d32871c2abaea87d2d1409d96299a634905c782c18ea`.
The inventory contains 45 local `VERIFICATION` rules, all classified exactly
once and in canonical order in `trust-boundary.json`.

## Classification method

- `DEFINITION` covers the equations and recurrences for `trialPrime`,
  `trialDivisor`, `isPrime`, `largestPrime`, `digitAcc`, and `digitSum`, plus
  the AST and module macro expansions. The conditional rules among these that
  carry `simplification` remain defining cases of their named functions.
- `OPERATIONAL_RULE` covers rules that execute or observe the verification
  model: ordinary-frame lookup and updates, strictness-normalized execution,
  comparison and control-flow dispatch, symbolic integer-list iteration,
  target-call routing, and the bounded entry-prefix execution summary.
- `DOMAIN_LEMMA` covers the two unnamed Map-algebra simplifiers at
  `verification.k` lines 7-12. They assert canonical behavior for deleting a
  fresh explicit binding and inserting at a fresh key. They are additional
  trusted facts about Map operations, not equations defining a named proof
  helper.

Every rule carrying `simplification` is classified as either `DEFINITION` or
`DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are **no `PROVED_DERIVED_LEMMA` rules**.

Stage 1 does prove several reachability claims in a deliberate dependency
order:

1. `SPEC.prime-loop` is proved independently by `prove.sh` lines 37-41.
2. `SPEC.digit-loop` is proved independently by lines 43-47.
3. `SPEC.scan-loop` is proved by lines 49-54 while the first two claims are
   admitted as trusted dependencies.
4. `SPEC.entry-prefix` is proved by lines 56-61 while the three loop claims
   are admitted as trusted dependencies.
5. `SPEC.main-correct` is proved by lines 63-68 while the preceding four
   claims are admitted as trusted dependencies.

That evidence establishes an ordering among **claims**, but it does not meet
the required criterion for any inventoried rule. `prove.sh` kompiles
`verification.k` at lines 28-33 before the first `kprove`, so all 45 canonical
rules are already present in the proof module for every proof command. No
Stage 1 command first proves the exact statement of an inventoried rule
against a module from which that rule is absent.

In particular, comments calling rules “proof-normalization lemmas” do not make
them proved derived lemmas. The bounded entry-prefix rule
`rule-3690f6a2...` is also compiled before `SPEC.entry-prefix` is proved; the
claim is not prior evidence for adding that exact operational rule.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854`
- `rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b`

No other inventory rule is classified as a domain lemma.
