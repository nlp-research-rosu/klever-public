# K proof trust-boundary discovery

## Canonical scope

The sole classification source is `/reference/rule-inventory.json`, whose
`inventory_sha256` is
`b2fb8d2f080192ac639ab57ac9b211ee836bb2e63f89b4d157059d4ffc931fe2`.
It contains 24 rules, in module `VERIFICATION`. The classification counts are:

- `DEFINITION`: 14
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 10

The inventory is explicitly canonical and exhaustive, so no rule outside its
24 `source_rule_id` values is added to `trust-boundary.json`.

## Definitions

The first two rules define named proof terms: `evenOddBody` expands to the
exact translated function body, and `evenOddClosure` expands to the closure
value containing that body. Neither matches a K configuration cell or bypasses
program execution.

The next twelve rules define the mathematical summary symbols:

- `evenPos(0)` and `oddPos(0)` give the zero terminator for a positive decimal
  digit recurrence.
- Their guarded `N ==Int 0` simplification variants are structural copies of
  the same base equations. They are classified as definitions, satisfying the
  requirement that simplification rules be either definitions or domain
  lemmas.
- The negative `evenPos` and `oddPos` equations totalize those symbols by
  magnitude.
- The three disjoint cases for each of `decEven` and `decOdd` define the public
  summaries at zero and on positive and negative integers.

These fourteen rules are equations or structural helpers defining named terms.
They do not state an independent execution fact or rewrite any operational
cell.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of ten simplification rules:

- two zero-magnitude equalities connecting `decEven` and `decOdd` to the
  special representation of zero;
- four sign-normalization equalities, in both orientations, connecting
  `evenPos(absInt(N))` and `oddPos(absInt(N))` with the public summaries for a
  strictly positive magnitude;
- four positive decimal-recurrence equalities, in both orientations, for the
  accumulated even and odd counts.

Unlike the function equations, these rules directly rewrite matching-logic
equality propositions to `#Top`. They are mathematical facts used to close the
symbolic loop and final result obligations. Stage 1's `PROOF.md` calls the
recurrence and sign-normalization simplifiers “proof-local mathematical facts”
and places them in the trust boundary. The base module already contains every
one of these rules when the loop theorem is proved, so Stage 1 supplies no
earlier proof of any exact canonical rule against a module from which that rule
is absent. Accordingly, none can be promoted to `PROVED_DERIVED_LEMMA`.

## Separately proved derived lemmas

No rule in the canonical inventory qualifies as
`PROVED_DERIVED_LEMMA`.

Stage 1 does separately machine-check one auxiliary reachability theorem,
`LOOP-PROOF.loop-tail` in `/reference/k-proof/spec.k`. The evidence and ordering
are:

1. `/reference/k-proof/prove.sh` lines 37–41 compile `verification.k` as module
   `VERIFICATION`, which does not contain the later operational bridge.
2. Lines 42–46 run `kprove spec.k --definition
   loop-verification-kompiled --spec-module LOOP-PROOF` and require `#Top`.
3. `/reference/k-proof/loop-proof.log` records `#Top`.
4. Only afterward, lines 54–58 compile `verification-with-lemma.k`, whose sole
   rule operationalizes that loop-tail result.

That auxiliary theorem is a `claim`, and the later operational rule belongs to
`VERIFICATION-WITH-LEMMA`; neither has a `source_rule_id` in the canonical
inventory, which names only module `VERIFICATION`. Thus the Stage 1 ordering is
real evidence for an out-of-inventory bridge, but it does not justify assigning
`PROVED_DERIVED_LEMMA` to any of the 24 canonical rules.

The other positive auxiliary result,
`IDENTITY-SPEC.translated-program-identity`, also does not create a proved
derived rule. Its proof imports `VERIFICATION`, where the `evenOddBody` and
`evenOddClosure` definition rules are already present, and its statement is a
reachability claim rather than the exact statement of either rule.

## Operational rules and simplification audit

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The named
body and closure rules construct proof terms, the summary rules define
mathematical terms, and the remaining rules simplify logical equalities; none
matches `<k>` or another operational state cell. The operational loop bridge
described above is outside the canonical inventory.

All twelve canonical rules carrying the `simplification` attribute satisfy the
required restriction: the two guarded zero equations are `DEFINITION`, and the
ten equality facts are `DOMAIN_LEMMA`. None is classified as
`OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA`.
