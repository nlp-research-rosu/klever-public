# Trust-boundary discovery

The canonical inventory hash is
`248228e8fdfc6e33e8b384cf6ee6d6599339e96ceb0bed8b684817fefeffc574`.
It contains nine rules in the closure of `COUNT-UP-TO-WITH-OUTER`.

## Definitions

The first seven rules are `DEFINITION`:

- The three `noDivisor` rules are its terminal-empty, divisor-found, and
  recursive-non-divisor equations.
- The two `appendIfPrime` rules define its false and true branches.
- The two `primesAcc` rules are its terminating equation and recurrence.

These rules introduce the mathematical summaries used by the proof. They are
equations or recurrences, not separately established facts about execution.
The inventory contains no rule with the `simplification` attribute.

## Staged loop evidence and exact correspondence

Stage 1 deliberately stages two loop claims:

1. `prove.sh` compiles `COUNT-UP-TO-BASE`, which does not contain the inner
   loop summary, and runs `kprove` on
   `COUNT-UP-TO-INNER-LOOP-SPEC`.
2. It then compiles `COUNT-UP-TO-WITH-INNER`, which does not contain the outer
   loop summary, and runs `kprove` on
   `COUNT-UP-TO-OUTER-LOOP-SPEC`.

The loop bodies, state updates, result summaries, and arithmetic
preconditions in those claims correspond to the cores of the subsequently
added rules. However, the mounted claims do not establish the exact reusable
rule statements:

- Each claim fixes the `-1` scope to `builtinsScope`; each rule instead
  matches `scope(BI:Map, root)` for an arbitrary `BI`.
- Each claim fixes `scopeLoc`, `heapLoc`, `ret`, and `exc` and constrains the
  stack; the rules omit those cells and therefore apply while arbitrary values
  in those cells are preserved.

The reusable rules are thus strictly more general than the claims evidenced
by `prove.sh`. Under the required exact-statement criterion, neither can be
classified as `PROVED_DERIVED_LEMMA`, even though their comments call them
theorems and the proof commands are ordered before their use.

Accordingly:

- `rule-3e4c9acccabad57e7ba8e25c78b46534c3490b6a4643e19530860adcfcd9f03e`
  is a `DOMAIN_LEMMA`.
- `rule-61fd7317a61776818f367054e0c73dd9601ffc1ed75d9f4c6442d0f67fa51cb5`
  is a `DOMAIN_LEMMA`.

There are no inventoried rules that qualify as separately proved
`PROVED_DERIVED_LEMMA`, and there are no `OPERATIONAL_RULE` classifications.
The domain-lemma set is not empty; it consists exactly of the two loop-summary
rules above.
