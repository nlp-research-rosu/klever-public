# Trust-boundary discovery

## Canonical result

The canonical inventory contains ten rules. They are classified exactly once,
in inventory order, as seven `DEFINITION` rules, one
`PROVED_DERIVED_LEMMA`, no `OPERATIONAL_RULE` rules, and two `DOMAIN_LEMMA`
rules.

The seven definitions are precisely the equations whose left-hand side is one
of the fresh symbols declared by `VERIFICATION-SYNTAX`: `cubeOf`,
`cubeSearch`, `isCubeInt`, or `iscubeClosure`. The three guarded `cubeSearch`
rules jointly define its two base outcomes and recurrence. The two guarded
`isCubeInt` rules define sign dispatch. `cubeOf` and `iscubeClosure` are direct
defining equations. None of these rules states a fact about an operation
defined outside the verification modules.

## Separately proved derived lemma

There is exactly one separately proved derived lemma:
`rule-7053976245560ebde1f9c329f37f168cf403550b3226be6fd87bc25c9c187bda`
from `connection-rule.k`.

The Stage 1 proof evidence establishes both ordering and exact correspondence:

- `prove.sh` lines 18–21 compile `verification-base.k` as
  `verification-base-kompiled`. That module does not contain the later bridge
  rule.
- `prove.sh` lines 27–29 prove `CONNECTION.search-loop` from
  `connection-spec.k` against that bridge-free definition. In command order,
  its result is the second `#Top` in `prove.log` (line 189).
- Only afterward do `prove.sh` lines 31–34 compile `connection-rule.k`, which
  introduces the reusable rule.
- The claim's reachability statement at `connection-spec.k` lines 10–47 is
  byte-for-byte identical to the rule statement at `connection-rule.k` lines
  9–46. The variables are the same `A`, `C`, and `SC`; neither form has a
  guard; and the active continuation, result, bindings, stack, and every stated
  cell transition are identical. Thus this is not a specialization of a more
  general claim and not merely a corollary. The claim label and the installed
  rule's `priority(40)` are proof/execution metadata outside the identical
  reachability statement.

The Stage 1 identity and source-connection claims are proof evidence but are
not subsequently installed as reusable canonical rules, so there are no other
`PROVED_DERIVED_LEMMA` classifications.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these two
simplification rules:

- `rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d`
  states a fact connecting externally defined integer comparison operations to
  the fresh `cubeSearch` summary at loop exit. Because its left-hand side is
  integer equality rather than a fresh verification symbol, it is not a
  definition.
- `rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2`
  states a fact about deletion by the externally defined Map update operation.
  It likewise defines no fresh verification symbol.

Both rules were already in `verification-base.k`, the module against which the
auxiliary proofs were run. Stage 1 does not first prove either exact statement
against a module that omits it. Comments describing them as derived map or
Boolean facts therefore do not qualify them as separately proved derived
lemmas. Their `simplification` attributes are consistent with the required
`DOMAIN_LEMMA` classification.

The loop bridge would ordinarily be an execution rule, but its exact statement
has the required prior proof, so it takes the more specific
`PROVED_DERIVED_LEMMA` classification. No remaining canonical rule is an
ordinary unproved execution or observation rule; hence the
`OPERATIONAL_RULE` set is empty.
