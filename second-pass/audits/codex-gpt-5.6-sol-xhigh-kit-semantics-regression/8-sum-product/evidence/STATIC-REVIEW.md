# Static soundness review ledger

This ledger accompanies `K-INVENTORY.md`. The inventory contains all 230 local
syntax declarations, 705 ordinary rules, five contexts, one configuration, and
two claims in the clean source copy. It records every complete block, guard,
attribute, and line number. The dispositions below are exhaustive:

- `SUPPLIED_BASELINE_USED_PATH_REVIEW`: inspected against the submitted
  constructor tree, the fixed operational semantics, cell changes, and Python
  behavior used by this task.
- `SUPPLIED_BASELINE_UNUSED_PATH_REVIEW`: inspected for overlap with the used
  execution slice, task-answer smuggling, and false task conclusions. These
  rules are outside the submitted program's execution slice. They are part of
  the supplied fixed semantics, not proof extensions.
- `PROOF_LOCAL_INDIVIDUAL_REVIEW`: each declaration/rule is decided separately
  below. The supplied baseline does not justify these rules.
- `TARGET_CLAIM_ADEQUACY_REVIEW`: each claim is restated and checked in
  `REVIEW.md` Stage 4.

No rule is labeled unsound. Consequently there is no unsupported unsoundness
claim requiring a false-conclusion witness. The narrower unused-totality gaps
reported below are stuckness/coverage gaps, not demonstrated false conclusions.

## Per-module rule decisions

| File | Rules | Execution-slice decision |
|---|---:|---|
| `semantics.k` | 0 | Assembly only; proof imports `MPY`, concrete build imports `MPY-KRUN`. |
| `syntax.k` | 0 | Used AST productions and strictness attributes map exactly to `solution.mpy`; unused productions do not rewrite. |
| `core.k` | 46 | Used configuration, load/sequence, literals, lookup, argument evaluation, value constructors, builtins scope, and sequence helpers preserve the stated cells and left-to-right order. Other core rules do not match the submitted term. |
| `iter.k` | 0 | Declares the iterator protocol consumed by list and `For`. |
| `list.k` | 27 | The two `#iterNext(list(...))` rules are the loop's exact empty/cons cases. List literal, equality, mutation, and membership rules do not match the submitted term. |
| `tuple.k` | 21 | `TupleExpr` uses the shared left-to-right evaluator and returns a two-element `tuple`; target binding writes `number` in the active scope. Unpacking/membership/method rules do not match. |
| `int.k` | 16 | The `+` and `*` cases are ordinary unbounded integer addition/multiplication. Other integer operators do not match. |
| `operators.k` | 10 | `BinOp` dispatch and heap dereference are not invoked directly by the two integer `AugAssign`s; no conflicting rule matches their pure `applyBin` terms. |
| `controls.k` | 34 | Plain-frame assignment, integer `AugAssign`, ignored `typing` import, `For` initialization, list iterator loop, target binding, statement sequencing, and loop continuation match the real flow. Cell/ref branches have false guards in the plain frame. |
| `functions.k` | 15 | `FuncDef`, ordinary parameter binding, `Return`, `#endcall`, and `#pop` create/remove the exact frame and restore `env`, scopes, stack, return state, and `scopeLoc`. Annotated-closure paths do not match. |
| `call.k` | 21 | Generic call lookup evaluates callee then arguments left-to-right. The ordinary closure rule binds `numbers`, saves the empty continuation, and installs the exact body. Builtin/method/annotated-closure paths do not match. |
| `bool.k` | 13 | No source Boolean operation matches; imported baseline only. |
| `float.k` | 121 | No float term matches. Duplicate mixed-number cases are outside the all-Int slice. Opaque float primitives are listed below. |
| `str.k` | 28 | No string term matches. |
| `set.k` | 12 | No set term matches. |
| `range.k` | 6 | No range term matches. |
| `subscript.k` | 40 | No subscript/slice term matches. |
| `comprehension.k` | 7 | No comprehension macro matches. |
| `methods.k` | 75 | No method term matches. |
| `builtins.k` | 137 | No builtin call occurs after the `typing` import is ignored. |
| `dict.k` | 28 | No dictionary term matches. |
| `sort.k` | 19 | No sorting term matches; its opaque sort primitives are irrelevant. |
| `assert.k` | 3 | Not part of either proof claim; used only by the independent concrete harness. |
| `concrete.k` | 16 | Imported only by `MPY-KRUN`, never the Haskell proof definition. Its deep equality/key-sort rules do not match the harness's integer tuple assertions except through ordinary equality. |
| `verification.k` | 10 | Individually justified below. |
| `spec.k` | 0 | Contains two reachability claims, not ordinary rules. |

Thus every one of the 695 supplied rules has an explicit module-row decision,
and every one of the ten proof-local rules has the individual decision below.
The complete text and attributes of each rule remain in `K-INVENTORY.md`.

## Used syntax-to-rule map

| Submitted construct | Declaration | Operational path |
|---|---|---|
| `Module` and statement list | `syntax.k:56,61` | `core.k:124-127` (`#loadAll`, head/tail sequencing, empty sequence) |
| `ImportFrom("typing",...)` | `syntax.k:43` | `controls.k:35-36`; the non-`math` `owise` rule consumes it without bindings, matching annotation-only use |
| `FuncDef` / `Params` | `syntax.k:53,57` | `functions.k:14-16` installs the exact `closureVal` in module scope |
| `Assign(Name,Int)` | `syntax.k:9,12,41` | Int literal `core.k:194`; plain assignment `controls.k:9-11`; statement sequencing in `core.k` |
| `For(Name,Name,body)` | `syntax.k:45` (`strict(2)`) | lookup `core.k:130-154`; `controls.k:69-74`; list iteration `list.k:9-10`; target bind `tuple.k:31-34` |
| `AugAssign(Name,"+"/"*",Name)` | `syntax.k:44` (`strict(3)`) | RHS lookup, then `controls.k:20-23`, then `int.k:9,14` or the equivalent guarded proof-local cases |
| `Return(TupleExpr(...))` | `syntax.k:21,50` | tuple evaluator `tuple.k:14-16`; `functions.k:78-90` returns, pops the exact frame, and restores all control cells |
| `Call(Name("sum_product"),list(VS))` | `syntax.k:12,28` | `call.k:20-21,69-75`; `core.k:189-191`; `functions.k:63-66` |

The shared evaluator makes tuple elements and call arguments left-to-right. The
only state mutations on the used path are module closure installation, callee
frame allocation, binding and updating four local variables, and frame removal.
The arbitrary heap and `heapLoc` are preserved because no used construct
allocates. The returned tuple is a value, not a heap allocation.

## Configuration and control check

The single configuration (`core.k:49-60`) has `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The entry claim pins every cell. The call transition changes
`env 0 -> 1`, adds scope 1, increments `scopeLoc 1 -> 2`, and pushes
`frame(.K,0,1)`. The loop claim begins at precisely that state. `Return` stores
the tuple in `<ret>`, and `#pop` restores `env=0`, removes scope 1, restores
`scopeLoc=1`, empties the stack, clears `<ret>`, and resumes `.K`. Both claims
require `NoExc` and exit code 0. No framed or omitted state permits a proof-local
rule to fabricate a return or discard an observable continuation.

`Return(V) ~> _ => #pop` is a supplied control rule, not a proof bridge. Its
suffix is the remainder of the callee computation; the caller continuation is
stored in the frame and restored by `#pop`. For this function the loop claim
pins the exact suffix `Return(...) ~> #endcall`.

## Proof-local declarations and rules

There are three `[function,total]` declarations, ten rules, no
`[simplification]`, no `[functional]`, no priority, no `owise`, and no opaque
proof-local symbol.

1. `intsVS(.ValSeq) => true`: true by the empty all-elements predicate.
2. `intsVS(vCons(V,R)) => isInt(V) andBool intsVS(R)`: true by structural
   definition. Together the two constructor cases are total and non-overlapping.
3. `sumFrom(A,.ValSeq) => A`: the empty left fold.
4. Guarded integer `sumFrom` cons case: under `isInt(V)`, `{V}:>Int` is the
   value itself and recursion strictly shortens the sequence.
5. Guarded non-integer `sumFrom` cons case: defines totalization outside the
   theorem by skipping the element. Its guard is the exact Boolean complement
   of rule 4. It cannot affect an `intsVS` input.
6. `productFrom(A,.ValSeq) => A`: the empty left fold.
7. Guarded integer `productFrom` cons case: the multiplication fold, with the
   same valid cast and structural descent.
8. Guarded non-integer `productFrom` cons case: disjoint/exhaustive
   totalization, unreachable under the entry precondition.
9. `applyBin("+",A:Int,V:Val)` under `isInt(V)`: a derived equation for the
   supplied `applyBin("+",Int,Int)` rule. On overlap both right sides are
   `A +Int V`; it reads/writes no cell and changes no control.
10. The analogous `*` equation agrees with supplied integer multiplication.

Rules 9-10 are pure derived equations, not summaries of a program-defined
operation. Their match domain is exactly the supplied integer case after sort
refinement; they do not bypass name lookup, argument evaluation, calls,
returns, state, exceptions, or allocation. Concrete fixed-versus-extended
execution produced byte-identical complete configurations.

## Priorities, opaque symbols, totality, and overlaps

`K-INVENTORY.md` identifies all 45 priority-bearing blocks, 26 `owise` blocks,
35 concrete blocks, 110 total declarations/rules, and all ordinary rules. None
is proof-local. Used priority branches are cell/ref specializations whose guards
are false for the plain integer frame; the generic rules therefore apply.

The supplied baseline declares opaque/no-evaluator primitives for float
operations, `sortVS`, `sortKeyVS`, and `md5hexCodes`. It also has concrete-only
twins in `MPY-KRUN` where stated. None of these symbols occurs in
`solution.mpy`, either reachability claim, or a proof-local equation. They are
therefore an explicit but irrelevant supplied-semantics trust boundary for this
theorem.

The LLVM build warns that six supplied `[total]` functions have unmatched
constructor cases: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt` (notably `cellsMark`, and for `valSeqAt` empty/OOB inputs). No one of
these functions is reachable from the submitted program or the claims. The
warnings show incomplete coverage, but provide no false value equation and no
false conclusion witness on the intended input domain; they are recorded as
narrower, immaterial coverage gaps rather than unsound rules.

The supplied integer `applyBin` rules overlap the two proof-local guarded rules
only when `V` is an `Int`, and their right sides agree exactly. The fold guards
are complementary. No task-specific name or fold occurs in the supplied
baseline, and no rule encodes the requested sum/product answer.
