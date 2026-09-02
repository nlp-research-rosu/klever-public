# Independent Stage 3 classification

The trusted `/reference/tools/k_rule_inventory.py` inventory reconstruction
found one local verification module (`VERIFICATION`) and ten rules.  The
recomputed ordered inventory, source spans, normalized source hashes,
`source_rule_id` values, and inventory hash are in
`02-inventory-reconstruction.log`.

| Index | Source span | Short identity | Independent classification | Reason |
|---:|---:|---|---|---|
| 0 | 8 | `rule-62ed89…` | `DEFINITION` | Empty-map base equation for the locally introduced `freshScopes` structural summary. |
| 1 | 9–10 | `rule-437465…` | `DOMAIN_LEMMA` | Unproved consequence of `freshScopes`: the allocator's next location is absent from the scope map. |
| 2 | 11–12 | `rule-5f7d67…` | `DEFINITION` | Recursive constructor equation for the `freshScopes` summary over the exact predecessor location and a `Scope` value. |
| 3 | 17–18 | `rule-746c49…` | `DOMAIN_LEMMA` | Unproved finite-map identity rewriting fresh-key update to a singleton binding plus the old map. |
| 4 | 19–20 | `rule-82f2c7…` | `DOMAIN_LEMMA` | Unproved finite-map deletion identity for a fresh singleton binding. |
| 5 | 24–43 | `rule-9389ac…` | `DEFINITION` | Defines the named `changeBaseBody` proof term as the translated function-body syntax tree. |
| 6 | 46–49 | `rule-6a85e1…` | `DEFINITION` | Defines `solutionModule` by wrapping the named body in module/function constructors. |
| 7 | 52–53 | `rule-e42c4c…` | `DEFINITION` | Defines the named `changeBaseClosure` proof value. |
| 8 | 58 | `rule-a24b26…` | `DEFINITION` | Zero equation of the mathematical `baseDigits` recurrence. |
| 9 | 59–64 | `rule-91e339…` | `DEFINITION` | Positive quotient/remainder recurrence for `baseDigits`. |

There are seven definitions and three true domain lemmas.  There are no
ordinary operational rules in this local verification module and no
`PROVED_DERIVED_LEMMA`: Stage 1 does not first prove any of these exact rules
against a module omitting it.  Both `[simplification]` rules are definitions,
so the simplification constraint is satisfied.

The three domain lemmas are relevant rather than generic decoration.  Frozen
`call.k` lines 69–74 allocate a new `scope(.Map, parent(DEFL))` at `NEWL` by
map update and increment the allocator; `functions.k` lines 63–66 update that
frame while binding parameters; lines 85–90 delete the callee frame when
popping it.  Recursion repeats this lifecycle.  The absence, update, and
deletion facts are therefore exactly the map facts needed to preserve and
consume the `freshScopes` invariant in the source proof.  The `baseDigits`
definitions directly state the source program's zero case and positive
quotient/remainder recursion.

This independent classification agrees entry-for-entry with the protected
Stage 3 manifest.  It does not validate the later Lean encoding of the
classified rules.
