# Trust-boundary discovery

## Canonical inventory

The sole inventory authority was `/reference/rule-inventory.json`.

- Schema version: 2
- Inventory SHA-256:
  `1858c992ef1e9a6b842e6b7d36b1e30b8abe0e686374e68b1766d4f9cb1e3824`
- Canonical rule count: 33
- Verification-module closure represented by the inventory: `VERIFICATION`

Every canonical `source_rule_id` appears exactly once in
`trust-boundary.json`, in canonical inventory order. No Stage 1 artifact was
edited or copied.

## Classification method

I used `DEFINITION` only for primary equations, structural recurrences, exact
body expansions, and primary cases defining proof-local summaries or named
proof terms.

I used `DOMAIN_LEMMA` for simplification facts that extend an existing
operation, reverse or shortcut a primary recurrence, characterize a pre-existing
partial cast, or add an algebraic fold without an earlier rule-free proof of
that exact statement.

There are no `OPERATIONAL_RULE` entries. The inventory contains no ordinary
configuration-cell execution rule; the four body rules name syntax and leave
execution to the imported reference semantics.

There are no `PROVED_DERIVED_LEMMA` entries. The reason is evidentiary rather
than nominal: Stage 1 `prove.sh` first kompiles the complete `verification.k`
and then runs both `spec.k` and `spec-summary.k` against that compiled
definition. Both spec modules import `VERIFICATION`, so every inventory rule is
already present when those claims run. The summary log's `#Top` and
`WarnTrivialClaim` messages therefore do not establish any inventory rule in a
module from which that rule was absent. The mutation probes are expected-failure
tests and likewise do not prove an inventory rule.

Classification totals:

| Classification | Count |
|---|---:|
| `DEFINITION` | 20 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 13 |

## Rule-by-rule explanation

| Inventory position | Rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-dd2fa97c…` (`primeLoopBody`) | `DEFINITION` | Exact named MPY body expansion. |
| 2 | `rule-00b808d6…` (`scanBody`) | `DEFINITION` | Exact named MPY body expansion. |
| 3 | `rule-59e9ea73…` (`digitLoopBody`) | `DEFINITION` | Exact named MPY body expansion. |
| 4 | `rule-c3aa454c…` (`targetBody`) | `DEFINITION` | Exact translated target-body expansion. |
| 5 | `rule-8277b118…` | `DEFINITION` | Empty-sequence base case for `allInts`. |
| 6 | `rule-bb65aed9…` | `DEFINITION` | Constructor recurrence for `allInts`. |
| 7 | `rule-9e2ee339…` | `DEFINITION` | Defines `definedProjectInt` as `isInt`. |
| 8 | `rule-0312858a…` | `DOMAIN_LEMMA` | Unproved definedness characterization for the existing partial cast. |
| 9 | `rule-ced5adec…` | `DEFINITION` | Primary guarded definition of `projectIntTotal`. |
| 10 | `rule-22fa1e67…` | `DOMAIN_LEMMA` | Unproved reverse cast-to-projection simplification. |
| 11 | `rule-7191d5f6…` | `DEFINITION` | Primary Int collapse case for the projection. |
| 12 | `rule-9e1486b6…` | `DOMAIN_LEMMA` | Unproved projection-idempotence simplification. |
| 13 | `rule-835c8361…` | `DOMAIN_LEMMA` | Guarded dynamic-Val `>` dispatch fact. |
| 14 | `rule-8ca093b3…` | `DOMAIN_LEMMA` | Guarded dynamic-Val `>=` dispatch fact. |
| 15 | `rule-4175c4aa…` | `DOMAIN_LEMMA` | Guarded dynamic-Val `<` dispatch fact. |
| 16 | `rule-2dd919bc…` | `DOMAIN_LEMMA` | Guarded dynamic-Val modulo dispatch fact. |
| 17 | `rule-00073d0a…` | `DOMAIN_LEMMA` | Guarded dynamic-Val addition dispatch fact. |
| 18 | `rule-5b7a5a8c…` | `DEFINITION` | Below-domain totalization case for `primeTail`. |
| 19 | `rule-3b4a8217…` | `DEFINITION` | Completed-scan base case for `primeTail`. |
| 20 | `rule-3ad3aef2…` | `DEFINITION` | Primary recursive divisor equation for `primeTail`. |
| 21 | `rule-ca4e1410…` | `DOMAIN_LEMMA` | Unproved zero-remainder shortcut. |
| 22 | `rule-ea9bd944…` | `DOMAIN_LEMMA` | Unproved backward symbolic fold for `primeTail`. |
| 23 | `rule-b78034ba…` | `DEFINITION` | Defines `isPrime` using the lower bound and `primeTail`. |
| 24 | `rule-1ad2316f…` | `DEFINITION` | Positive defining branch for `selectPrime`. |
| 25 | `rule-1b6accb4…` | `DEFINITION` | Complementary defining branch for `selectPrime`. |
| 26 | `rule-feeddd7f…` | `DEFINITION` | Empty-sequence base case for `largestPrime`. |
| 27 | `rule-332a2264…` | `DEFINITION` | Integer-head recurrence for `largestPrime`. |
| 28 | `rule-1a849add…` | `DEFINITION` | Non-Int totalization recurrence for `largestPrime`. |
| 29 | `rule-becef0c1…` | `DEFINITION` | Nonpositive base case for `digitSum`. |
| 30 | `rule-9807cef1…` | `DEFINITION` | Primary positive decimal recurrence for `digitSum`. |
| 31 | `rule-8b14fdba…` | `DOMAIN_LEMMA` | Unproved reverse fold of the `digitSum` recurrence. |
| 32 | `rule-19a4e23f…` | `DOMAIN_LEMMA` | Unproved fold after normalizing `pyMod` to integer remainder operations. |
| 33 | `rule-4e535e95…` | `DOMAIN_LEMMA` | Unproved accumulator-lifted digit fold using integer-addition rearrangement. |

The abbreviated IDs in this explanatory table are only labels; the JSON
contains every complete canonical ID.

## Separately proved derived lemmas

None.

Stage 1 contains no command that first proves the exact statement of an
inventory rule against a module excluding that rule and only then installs it.
Accordingly, no rule was classified as `PROVED_DERIVED_LEMMA`.

## Domain-lemma trust boundary

The domain-lemma set is **not empty**. It contains these 13 canonical rules:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   — partial-cast `#Ceil` characterization.
2. `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`
   — reverse cast-to-total-projection orientation.
3. `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`
   — projection idempotence.
4. `rule-835c8361eaef00ebfc5566f8c0006f3fcda1381710a9abd174ceefbad2243388`
   — guarded `>` dispatch.
5. `rule-8ca093b3087d53245e9e69725c16dd38aedaf276503c27b46e0be906c3caa3c4`
   — guarded `>=` dispatch.
6. `rule-4175c4aa98cddee27ede99babdafc67baf74a0b86e62935384b5f7edb34d2914`
   — guarded `<` dispatch.
7. `rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a`
   — guarded modulo dispatch.
8. `rule-00073d0ac825d52fc0b1b4501a73dd6bceabdcb61a3f09abaad5a18381411c17`
   — guarded addition dispatch.
9. `rule-ca4e141078b38af84d1adcf7e28052e43ee8b187d3f9e30e56caaee0e604ec91`
   — zero-remainder `primeTail` shortcut.
10. `rule-ea9bd944c022c45e91082fb836fb1130b2cd059d0798ab09baa25e9067fe1c06`
    — backward `primeTail` fold.
11. `rule-8b14fdbabbebf92572ac3c9cc4db1a74e817b9134daf88acb375104ce54f4c51`
    — reverse `digitSum` fold.
12. `rule-19a4e23f1d39aa90f74d31468e8e2c52b5780ea7f27054931e8584b720b2bc0a`
    — normalized `digitSum` fold.
13. `rule-4e535e9503b7ea5138b6ee785a3c03b7668867ee0f420c22b82e5ec29594b231`
    — accumulator-lifted `digitSum` fold.

These rules are trusted mathematical/sort facts in the finalized Stage 1 proof.
Stage 1's successful target proof and finite validation evidence may test their
combined consequences, but neither constitutes the required earlier,
rule-excluding proof of their exact statements.
