# Exact Lean proof obstruction

The three writable trust parameters in `Proof.lean` have been replaced by
their total meanings from the frozen K source:

- map composition concatenates the association-list representation;
- `_|->_` constructs a singleton association list;
- `addAccSpec` implements the four recurrence rules in `verification.k`.

The selected base now has executable definitions for the relevant map hooks,
which fixes the earlier map-lookup obstruction.  The exact target nevertheless
is not derivable from the generated `Rewrites` relation.

## State mismatch

The target is the Stage 3 `DOMAIN_LEMMA`
`rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589`.
That K rule is an atomic abstraction: it replaces the loop by
`Return(addAccSpec(...))` while leaving the complete scopes cell unchanged.
It was intentionally omitted from `Base/Klean85Add/Rewrite.lean`; the only
occurrence of `addAccSpec` in that relation is the unrelated
`VERIFICATION_KLEAN_EXPORT_kxExport1` constructor.

Ordinary execution cannot establish the exact rule.  For every nonempty
input, `Rewrites._3ff423b` exposes `#bindTgt(Name("value"), head)` and the
generated assignment constructors update the `"value"` binding.  The body
then assigns `"odd_index"` to its negation and may update `"total"`.
Consequently, after one iteration the scopes cell is not the unchanged
initial scopes cell required by the fixed target.  No operational constructor
restores those bindings.

For example, a singleton input necessarily changes `"odd_index"` from
`false` to `true` and `"value"` from `0` to the input head, whereas the target
requires both to remain `false` and `0`.

## Remaining relevant hook gap

Even a target corrected to describe the final scopes would still need a
behavior theorem or definition for `«_%Int_»`; it remains a bare
`Option SortInt` axiom in `Base/Klean85Add/Func.lean:80`, and `pyMod` calls it
when processing an odd-index element.

The generated base retains 82 trusted axiom declarations: 41 generic hook
declarations in `Prelude.lean` and 41 generated hook declarations in
`Func.lean`.  The polymorphic generic `choiceAx` declarations make the base
logically explosive, so the target can be made to compile by an unrelated
`Empty` elimination.  That is expressly forbidden by the task and was not
used.

An honest completion requires either:

1. retaining the frozen domain rule as a trusted `Rewrites` constructor; or
2. changing the fixed target to the operationally reachable final scopes,
   adding the missing well-formed-map assumptions and `%Int` behavior, and
   proving the resulting loop invariant.
