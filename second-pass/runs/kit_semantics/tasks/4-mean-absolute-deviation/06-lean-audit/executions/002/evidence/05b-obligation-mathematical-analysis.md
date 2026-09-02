# Mathematical analysis of generated obligations

## Conjunct-level lowering

The independently classified domain set is the ordered three-rule set
`97b321…`, `92241e…`, `6f2599…`. The obligation map contains exactly one
conjunct for each ID in that order, with no duplicate or extra ID.

1. `97b321…` lowers
   `#Ceil({V:Val}:>Float) => (isFloat(V) = true #And #Ceil(V))` to the
   equivalence between `Option.isSome` for the Float projection and
   `isFloat(inj(V)) = true ∧ True`. The `True` is the exact lowering of
   `#Ceil(V)` for an already well-sorted `V : Val`; it is not a separate
   top-level obligation and does not replace or weaken the load-bearing
   `isFloat` condition.
2. `92241e…` quantifies the original `V : Val` and `A : Float`, carries the
   exact `isFloat(V) = true` guard, injects `A` into the first Val operand,
   and equates dynamic `applyBin "+"` with injected
   `addF(A, projectFloat(V))`.
3. `6f2599…` analogously preserves the original `M : Float`, `V : Val`,
   guard, operand order, subtraction operator, and injected
   `subF(projectFloat(V), M)` result.

All three equations are directly relevant to projecting symbolic float-list
elements and executing the addition/subtraction in the two source loops. None
is the source program's final mean-absolute-deviation postcondition, and none
is irrelevant padding. The generated target is their right-associated
conjunction and has the independently recomputed definition hash
`5c021c8f0c4cb38fc323789aa10d96159c82d20b4b6f7cabf3d22516570efdda`.

## Carrier-level lowering failure

The conjunct text is not enough to establish an exact translation. The
quantifier type `SortVal` generated at Stage 4 is a strict subset of frozen K
`Val`: frozen K has `str(IntSeq) : Str < Iterable < Val`, while generated Lean
has no `SortStr`, no `str` constructor, and no Str injection into Iterable or
Val. Evidence `17-stage4-carrier-projection.txt` reconstructs the exact
generation-time projection and exhibits the missing carrier member.

Consequently, the apparent `∀ (V : SortVal)` in each conjunct does not range
over the original rule's full `V : Val` domain. Most decisively, the projection
definedness equivalence for rule `97b321…` omits every frozen string value.
This is a weakened obligation even though its source-rule ID, span, conjunct
hash, and manifest binding are internally consistent. Stage 4 therefore fails
the mathematical source-rule/obligation identity requirement.
