# Static target-slice review

This is the reviewer-authored assessment of the exact rules reachable from
`SPEC.strlen`. The complete 929-item declaration/rule inventory is in
`stage5_rule_inventory.md`.

## Candidate-local theory

- `verification.k` contains only a `requires` and `imports MPY`; it declares no
  syntax, function, total/functional symbol, opaque symbol, priority rule,
  ordinary rule, simplification rule, or claim.
- `spec.k` contributes exactly one reachability claim and no helper claim,
  circularity, equation, lemma, or operational bridge.
- There are no source occurrences of `simplification` or `functional` in the
  supplied semantics, `verification.k`, or `spec.k`.

Therefore, there is no candidate-local proof extension to classify. All
operational behavior comes from the integrity-checked supplied semantics.

## Constructor and rule mapping

| Submitted constructor/control | Declaration | Reachable behavior |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:56,61` | `semantics/core.k:124-127` unwraps `#loadAll`, sequences the sole statement, and removes `.Stmts`. |
| `FuncDef("strlen", Params("string"), Body)` | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` stores `closureVal(PNS,BODY,0)` in the current module scope. |
| `Return(Expr)` | `semantics/syntax.k:50` with strict evaluation | Generated strictness evaluates its expression; `semantics/functions.k:78-90` records the result, pops the real call frame, restores the caller environment, removes the callee scope, and resumes the saved continuation. |
| `Call(Name("strlen"), Args)` | `semantics/syntax.k:28` | `semantics/call.k:19-21` evaluates the callee and arguments; `semantics/call.k:69-74` pushes a frame, creates scope 1 with parent 0, and runs the exact closure body. |
| `Name("strlen")` | `semantics/syntax.k:12` | `semantics/core.k:130-154` finds the exact closure installed in module scope 0. |
| parameter binding | `ParamNames`/`Vals` declarations in `syntax.k` and `core.k` | `semantics/functions.k:63-75` binds `"string"` to the supplied `str(CS)` in scope 1. The cell-variable priority rule is inapplicable because this is an unannotated closure with no `$cells` entry. |
| `Call(Name("len"), Name("string"))` | same `Call`/`Name` declarations | Lookup walks scope 1 → 0 → -1, where `builtinsScope` from `core.k:157-181` fixes `"len"` to `builtinV("len")`. `core.k:185-191` evaluates the one argument left-to-right. |
| builtin dispatch | `toCall`, `#applyK`, and `applyBuiltin` declarations | `semantics/call.k:31` dispatches the exact builtin value. Reference/heap priority rules do not match the direct `str(CS)` argument. |
| `len(str(CS))` | `semantics/builtins.k:17,20` | `semantics/builtins.k:21,24` rewrites `applyBuiltin("len", str(CS), .Vals)` to `seqLen(str(CS))` and then exactly to `isLen(CS)`. |
| `str(CS:IntSeq)` | `semantics/core.k:13,15,18,25,39` | It is already a model value and K result. The ASCII-only concrete `Str(String)` front-end rule in `str.k` is not used by the symbolic entry claim. |
| `isLen(CS)` | `semantics/core.k:227-229` | The empty and cons equations are constructor-disjoint, exhaustive over finite `IntSeq`, structurally decreasing, and define the number of sequence elements. |
| complete state | `semantics/core.k:49-60` | The claim pins every declared cell. The call path changes only the temporary scope/frame/return state and restores them; heap, exception, and exit code remain unchanged. |

## Control, overlap, and state assessment

1. The only call interception rules with priority are for concrete
   `math.<fn>` and `hashlib.md5` shapes. Neither matches the submitted
   `Call(Name(...), ...)` terms.
2. Generic call routing is `[owise]`, but no more-specific target shape
   applies. It evaluates the selected binding before arguments, then evaluates
   arguments left-to-right.
3. The closure-dispatch rule saves the exact caller continuation in `frame`.
   `Return` discards only the remaining callee computation before `#pop`;
   `#pop` restores the saved continuation and every modeled call-control cell.
4. Lookup priorities for closure cells require a `$cells` marker and are
   inapplicable to both the module and ordinary call scopes here.
5. The builtin reference-dereference priorities require a `ref(H)` argument and
   are inapplicable to `str(CS)`.
6. The two `isLen` rules do not overlap. Their recursion descends on the tail,
   and the `[total]` declaration is justified over the free `IntSeq`
   constructors.
7. No opaque/no-evaluator symbol, concrete-only rule, sorting primitive, float
   primitive, assertion oracle, simplification, or proof-local rule is
   reachable.
8. The only persistent state change is the required module binding
   `"strlen" |-> closureVal(...)`, which the destination states exactly.

## Exhaustive off-slice disposition

The complete inventory classifies every remaining supplied declaration and
rule as target-unreachable from the pinned configuration. This was checked by
construct/sort and control-marker reachability: those rules require a
front-of-`<k>` constructor, value sort, builtin name, method name, reference,
heap shape, loop marker, collection operator, float, dict, sort, assertion, or
concrete-only module that the submitted term and its reachable rules never
produce. They are part of the launcher-supplied fixed semantics, not
candidate-authored proof extensions. No off-slice rule can enable a conclusion
about this target result.

Some off-slice rules deliberately model only a Python subset or leave opaque
trusted operations (notably float, sorting, and MD5). This audit makes no
universal CPython-fidelity claim for those unused operations. There is no
concrete or symbolic witness on the intended `strlen` execution by which any
such rule can enable a false target conclusion, so they are not labeled
unsound under the benchmark's witness requirement.
