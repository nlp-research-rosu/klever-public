# Trust-boundary discovery

The canonical inventory contains seven rules from the local `VERIFICATION`
module. Each is classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Definitions

The first three rules are `DEFINITION`s. Together they define the named
relational proof summary `outputOK`:

- the empty-sequence base case after the index has passed `N`;
- the even-index recurrence, whose next element is the updated factorial; and
- the odd-index recurrence, whose next element is the updated triangular sum.

These rules define the meaning of the proof predicate used in the claims.
They do not add execution behavior to the supplied Python semantics.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of four rules, all carrying
the `simplification` attribute:

- associativity of `valSeqConcat`;
- right identity of `valSeqConcat`;
- left cancellation of a shared prefix from a concatenation equality; and
- the consequence that `P = P ++ A` forces `A` to be empty.

These are additional algebraic facts about finite `ValSeq` concatenation.
They are not clauses defining `outputOK`, and they are not ordinary Python
execution or observation rules.

## Separately proved derived lemmas

There are **no `PROVED_DERIVED_LEMMA` rules** in the canonical inventory.

Stage 1 `prove.sh` first invokes `kprove` on the `loop-correct` claim and then
passes that claim as trusted when proving `f-symbolic`. This establishes a
claim-level proof dependency, but `loop-correct` is not one of the inventoried
K rules. More importantly, the symbolic definition is compiled from
`verification.k` before either proof command, so all seven inventoried rules
are already present during the first proof. Stage 1 contains no command that
first proves the exact statement of any inventoried rule against a module
from which that rule is absent. Consequently, comments describing the
algebraic rules as facts or cancellation helpers do not qualify them as
proved derived lemmas.

## Operational rules

There are no `OPERATIONAL_RULE` classifications. The inventory contains only
the proof-summary definition and the additional concatenation facts; ordinary
execution rules come from the supplied `MPY` semantics rather than this local
verification-module inventory.
