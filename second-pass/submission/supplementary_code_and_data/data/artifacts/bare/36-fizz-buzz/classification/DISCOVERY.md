# Trust-boundary discovery

The canonical inventory contains 13 rules from the local `VERIFICATION` module closure. They divide into 12 definitions and one domain lemma. There are no inventory rules classified as `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA`.

## Definitions

The ten equations for `fizzEnd`, `digitSevens`, `fizzContribution`, and `fizzFrom` are classified as `DEFINITION`:

- The two `fizzEnd` branches define the final outer-loop index for negative and nonnegative inputs.
- The three `digitSevens` equations define the base case and decimal-digit recurrence used to count sevens in one integer.
- The three `fizzContribution` equations define whether an integer contributes its `digitSevens` count based on divisibility by 11 or 13.
- The two `fizzFrom` equations define the empty-interval base case and the recurrence accumulating contributions over `[I, N)`.

The `INNER-LOOP` and `OUTER-LOOP` rules are also `DEFINITION`. They are macro expansions—explicitly a definitional category—naming the exact translated loop ASTs used in the reachability claims. They do not assert additional facts about execution.

## Separately proved derived lemmas

There are no separately proved derived lemmas. In particular, `prove.sh` first compiles `verification.k` itself as module `VERIFICATION` and only afterward runs `kprove spec.k` against that compiled definition. It does not first prove any inventory rule against a module from which that rule is absent, so no rule has the ordering and exact-correspondence evidence required for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The integer-addition associativity simplifier

```k
rule (A +Int B) +Int C => A +Int (B +Int C) [simplification]
```

is classified as `DOMAIN_LEMMA`. It is an additional algebraic fact used to right-associate symbolic sums so that loop-invariant expressions close. It is present during compilation and is not separately proved by `prove.sh`.

The domain-lemma set is **not empty**: it contains exactly this one associativity rule.
