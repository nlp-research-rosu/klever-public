# Material constructor-to-rule map

The source term is the byte-identical trusted regeneration recorded in
`02-translation.log`. Line references below are to the clean scratch copy under
`/tmp/audit-work/candidate-src`.

| Submitted/source construct | Declaration | Material rules and evaluation mechanism |
|---|---|---|
| `Module(Stmts)` | `reference-semantics/semantics/syntax.k:61` | Initial configuration and `#loadAll` in `core.k:49-60,124-127`; `FuncDef` binding in `functions.k:14-16`. The independently run module-load witness reaches the exact module binding used by `SPEC.target`. |
| `FuncDef("fix_spaces", Params("text"), BODY)` | `syntax.k:53`, `syntax.k:57-60` | `functions.k:14-16` installs `closureVal(("text", .ParamNames), BODY, 0)`. |
| Statement sequence / `.Stmts` | `syntax.k:56` | `core.k:126-127` evaluates the head statement then the tail and consumes the empty sequence. |
| `Assign(Name(...), Expr)` | `syntax.k:41 [strict(2)]` | Generated strictness evaluates the RHS; `controls.k:9-11` writes the active scope. The cell-writing priority rule is excluded because the pinned local scope has no `"$cells"` entry. |
| `Str("...")` | `syntax.k:13` | `str.k:13-17` converts the program's ASCII literals to `IntSeq`. Every literal used here is ASCII. |
| `Name("...")` | `syntax.k:12` | `core.k:130-154` starts lookup and returns the nearest pinned binding. Every material lookup is present in the exact module/local scope, so parent fallback and cell-deref rules are not used. |
| `For(Name("char"), Name("text"), BODY)` | `syntax.k:45 [strict(2)]` | Generated strictness evaluates `text` once; `controls.k:69,71-74` creates and advances `#loop`; `str.k:8-10` yields one-character strings; `tuple.k:31-34` writes `char`; `controls.k:85` continues with the next iterator state. |
| `If(test, then, else)` | `syntax.k:49 [strict(1)]` | Generated strictness evaluates the test; `controls.k:51-54` uses `truthy`; `core.k:200` maps the resulting Bool to itself. |
| `Compare(..., CmpOp("=="|"!=", ...))` | `syntax.k:30-32` | Left/right contexts and dispatch are `operators.k:14-17`; string equality/inequality are `str.k:25-26`. |
| `BinOp("+", left, right)` | `syntax.k:15 [seqstrict(2,3)]` | Generated strictness fixes left-to-right evaluation; `operators.k:12` dispatches; `str.k:20-24` performs code-sequence concatenation. |
| `AugAssign(Name(...), "+", Expr)` | `syntax.k:44 [strict(3)]` | Generated strictness evaluates the RHS; `controls.k:20-23` reads and updates the active binding with `applyBin`; `str.k:20-24` implements the string addition. The heap-ref priority case is excluded by the exact string bindings. |
| `Return(BinOp(...))` | `syntax.k:50 [strict]` | Generated strictness evaluates the result; `functions.k:78-90` records it, discards the remainder of the callee computation, restores the caller environment/stack/scope location, and yields the value. |
| Entry `Call(Name("fix_spaces"), str(CS))` | `syntax.k:28` | `call.k:19-21` evaluates callee before arguments; `core.k:185-191,214-215` evaluates the one argument; `call.k:69-75` allocates the exact closure frame; `functions.k:63-66` binds `text`; the body then executes through the rules above. No proof-local `Call` interception exists. |
| Direct input `str(CS:IntSeq)` | `core.k:13,15,18-28` | It is already a `Val`/`Iterable`; no string-literal parser is involved. `str.k:8-10` consumes one `iCons` per loop step. |
| `#fixSpacesBody`, `#fixSpacesLoopBody` | `verification.k:7,24 [function,total]` | One unconditional equation each expands to the exact submitted constructor tree. `04-kprove-pinning-compare-v2.log` machine-checks the full expansions. These aliases name syntax and do not skip execution. |

## Per-file rule disposition

The exhaustive declaration/rule listing is `04-rule-inventory.tsv` (26 files,
1,122 declarations, including every one of the 709 source/proof-local rules and
both claims).

| File | Material to this proof | Static disposition |
|---|---|---|
| `semantics/syntax.k` | Yes | The listed constructors and strictness/sequence attributes match the regenerated term and establish the evaluation orders shown above. Unused grammar alternatives are inert. |
| `semantics/core.k` | Yes | Material configuration, sequencing, scope lookup, call-argument evaluation, Bool truthiness, and list helpers preserve the cells stated in the claims. Heap/cell, other truthiness, and collection helper rules have constructor/guard domains disjoint from the pinned path. |
| `semantics/iter.k` | Yes | Only declares the iterator protocol; the string and loop modules supply all used steps. |
| `semantics/str.k` | Yes | String iteration, ASCII literals, concatenation, and equality are exhaustive on the used domains and agree with code-sequence mathematics. Substring/order rules are unused. |
| `semantics/operators.k` | Yes | Material `BinOp` and `Compare` dispatch follows generated strictness. Heap-ref priority rules are excluded by the exact string-valued path. |
| `semantics/controls.k` | Yes | Name assignment, string augmented assignment, branches, and string `for` control match the body. Imports, while/break/continue, and ref consumers are unreachable from the submitted term. |
| `semantics/functions.k` | Yes | Exact module closure creation, parameter binding, explicit return, and frame restoration are used. Annotated-closure/cell rules are constructor-disjoint. The semantics' stated no-escaping-closure limitation is irrelevant to this first-order function. |
| `semantics/call.k` | Yes | Generic callee-first/argument-next dispatch and the ordinary closure call are used. Builtin/method/ref/annotated-closure alternatives are constructor-disjoint. |
| `semantics/tuple.k` | Yes, one rule family | Only `#bindTgt(Name,V)` is used by the `for`; tuple iteration/unpacking and ref cases are disjoint. |
| `semantics/range.k`, `int.k`, `bool.k`, `float.k`, `set.k`, `list.k`, `subscript.k`, `comprehension.k`, `methods.k`, `builtins.k`, `sort.k`, `assert.k`, `dict.k`, `concrete.k` | No material operation | Their ordinary, guarded, priority, `owise`, concrete, total, and opaque declarations are all enumerated in the TSV. The submitted term contains none of their triggering constructors/operations except module imports. Their documented approximations and opaque symbols therefore do not influence control, state, or the result of either positive claim. LLVM-only `concrete.k` is not imported by the Haskell proof module. |
| `verification.k` | Yes | All 14 equations are reviewed individually below: two exact AST aliases; three exhaustive `pendingSpace` cases; three exhaustive structurally descending `resultAfter` cases; three exhaustive structurally descending `pendingAfter` cases; two exhaustive structurally descending `charAfter` cases; and one unconditional `fixedSpaces` equation. The two `[simplification]` tags mark truthful non-space defining equations, not extra axioms. There are no priority rules, operational bridges, or opaque symbols. |
| `spec.k` | Yes | The loop claim is a fixed-semantics circularity over the exact loop head and arbitrary preserved continuation. The target pins the exact reachable module binding, all call-frame state, and `str(fixedSpaces(CS))`. |

## Proof-local equation checks

- `pendingSpace`: guards `P == "__"`, `P == "-" and P != "__"`, and the
  complement of both are pairwise disjoint and exhaustive. The results are
  respectively `"-"`, `"-"`, and `P + "_"`, exactly the nested branch.
- `resultAfter`: empty, head `32`, and head `C != 32` are pairwise disjoint and
  exhaustive over `IntSeq`; each recursive rule removes one input constructor.
  The non-space equation uses `R + (P + char)`, matching the translated AST.
- `pendingAfter`: the same constructor partition and descent; a non-space
  resets the pending sequence.
- `charAfter`: empty preserves the prior target and a constructor updates it to
  the last one-character string; recursion strictly descends.
- `fixedSpaces`: concatenates the exact final completed and pending sequences.
  It is a pure summary whose value is connected to real loop execution by
  `SPEC.loop-invariant`.
