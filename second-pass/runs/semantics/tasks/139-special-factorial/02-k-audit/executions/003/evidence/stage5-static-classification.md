# Static rule classification

This classification accompanies the exhaustive 936-sentence lexical table in
`stage5-rule-inventory.log`. The table covers 229 local syntax declarations, one
configuration, five contexts, 699 rules, and two claims across all 24 supplied
semantics sources plus `verification.k` and `spec.k`. It found 109 `total`
declarations, 147 `function` declarations, 45 priority-bearing sentences, 26
`owise` sentences, 35 concrete equations, 22 `no-evaluators` declarations, and
no `functional` or `simplification` declarations.

## Classification scheme

- **USED/Faithful**: exercised by the exact submitted term and faithful to the
  intended Python behavior and full configuration footprint.
- **DEFINITIONAL/Valid**: a terminating mathematical or structural definition;
  guarded equations cover the uses relevant to this theorem.
- **FIXED/Irrelevant**: part of the launcher-supplied fixed semantics but cannot
  head-match any exact program operation or proof-local summary in this theorem.
  It has no branch, value, state, exception, or control influence here.
- **FIXED/Opaque, irrelevant**: an explicit supplied-semantics trust boundary
  (`no-evaluators`, or equivalent under-specification) with no dataflow to this
  theorem.
- **CLAIM/Checked**: a reachability claim checked by the fresh all-claims proof.

No candidate-local operational bridge, simplification, priority rule, opaque
symbol, or unconstrained result-bearing oracle exists.

## Exact program construct map

| Program constructor | Declaration | Material rules | Classification |
|---|---|---|---|
| `Module`, statement juxtaposition | `syntax.k:56,61` | `core.k:124-127` | USED/Faithful: module statements execute left-to-right. |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` | USED/Faithful: binds the exact body as a closure in module scope 0. |
| `Assign(Name, ...)` | `syntax.k:41 [strict(2)]` | `controls.k:9-18` | USED/Faithful: RHS first, then current-frame update; cell priority is disjoint on this plain frame. |
| `Int`, `Name` | `syntax.k:9,12` | `core.k:130-154,194` | USED/Faithful: literal value and lexical lookup along parent scopes. |
| `While` / internal `#while` | `syntax.k:46`, `controls.k:65-67` | `controls.k:77-82,85` | USED/Faithful: reevaluates the guard, executes the body, and repeats; false exits without altering the continuation. |
| `Compare` / `CmpOp("<=")` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:23` | USED/Faithful: left then right evaluation and mathematical integer `<=`. |
| `AugAssign("*")`, `AugAssign("+")` | `syntax.k:44 [strict(3)]` | `controls.k:20-31`; `int.k:9,14` | USED/Faithful: RHS lookup precedes update. The sequential body makes `result` read the newly updated `factorial`. |
| `Call` | `syntax.k:28` | `call.k:20-21,69-75`; `functions.k:63-66` | USED/Faithful: evaluates callee then arguments, allocates a frame, binds `n`, and executes the exact closure body. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` | USED/Faithful: records the return value, discards the remaining callee continuation, pops the frame, restores caller state, and exposes the value to the caller's `Assign`. |
| `#loadAll` and initial/final cells | `core.k:49-60,124-127` | the rules above | USED/Faithful: heap, stack, exception, return, and exit-code cells remain exactly as claimed. |

The only priority/`owise` selection on this path is generic `Call` routing
(`call.k:20 [owise]`), after the fixed syntactic interceptors are inapplicable.
The 45 explicit priority sentences concern heap references, cells, mutations,
special methods, math calls, asserts, and concrete keyed sorting; none can match
the exact integer-only, plain-frame program states. Their specialized domains
are narrower than their fixed fallback rules.

## Proof-local inventory

| Extension | Class | Domain and coverage | Validity and influence |
|---|---|---|---|
| `factorial(Int) [function,total]` | Definitional summary | `N <= 0` and `N > 0` are disjoint and exhaustive. Positive recursion decreases by one; the theorem uses arguments `>= 0`. | Valid definition of factorial on the used domain, extended to 1 on nonpositive integers. It affects the invariant and final summary but replaces no program execution. |
| `factorial(N) => 1` | Defining equation | `N <= 0` | True by the stated extension; used at `I=1`. |
| `factorial(N) => factorial(N-1)*N` | Defining equation | `N > 0` | Standard recurrence with strict descent. |
| `specialFactorial(Int) [function,total]` | Definitional summary | `N <= 0` and `N > 0` are disjoint and exhaustive. Positive recursion decreases by one. | Valid product recurrence; it affects the invariant and entry postcondition but replaces no program execution. |
| `specialFactorial(N) => 1` | Defining equation | `N <= 0` | Empty-product base, used at `I=1`. |
| `specialFactorial(N) => specialFactorial(N-1)*factorial(N)` | Defining equation | `N > 0` | Exactly `1! * ... * N!`; multiplication commutativity equates it with the prompt's reversed display. |

There are no proof-local overlaps, missing guards, opaque symbols,
`simplification` equations, concrete-only rules, or priorities.

## Reachability claims

- `special-factorial-loop` is CLAIM/Checked. It is not an operational bridge:
  it starts at the real internal `#while` control term and symbolically executes
  the exact guard and three exact body statements. It quantifies over the full
  suffix `CONT` and frames every omitted cell. The entry invocation establishes
  its state with `N > 0`, `I=1`, `factorial=factorial(0)=1`, and
  `result=specialFactorial(0)=1`. On exit it establishes
  `factorial=factorial(N)`, `result=specialFactorial(N)`, and `i=N+1`.

- `special-factorial-correct` is CLAIM/Checked. It executes the constructor-
  identical function body and constrains module `answer` to
  `specialFactorial(N)`, with `.K`, `NoExc`, exit code 0, empty heap/stack, and
  restored environment/allocation state. It depends on the loop claim as an
  inductive circularity; the fresh conjunction proof checks both.

## File-by-file disposition of the fixed supplied semantics

| Source | Inventory | Disposition |
|---|---:|---|
| `semantics.k` | wrapper only | FIXED/Irrelevant import assembly; proof imports `MPY`, not `MPY-CONCRETE`. |
| `semantics/syntax.k` | 16 syntax | USED declarations listed above are faithful; all other AST productions are FIXED/Irrelevant. |
| `semantics/core.k` | 37 syntax, 1 configuration, 46 rules | USED rules listed above are faithful. Heap/cell/keyword/list helpers are structural definitions or FIXED/Irrelevant. |
| `semantics/operators.k` | 2 contexts, 10 rules | Integer comparison dispatch is USED/Faithful; heap-reference and identity cases are FIXED/Irrelevant. |
| `semantics/int.k` | 1 syntax, 16 rules | `+`, `*`, and `<=` are USED/Faithful unbounded-integer operations. Other integer operators are DEFINITIONAL/Valid and irrelevant. |
| `semantics/controls.k` | 3 syntax, 34 rules | Assignment, augmented assignment, and while rules are USED/Faithful. Imports, conditionals, `for`, loop-control, and heap-reference rules are FIXED/Irrelevant. |
| `semantics/functions.k` | 4 syntax, 15 rules | Plain definition/call/return rules are USED/Faithful. Annotated-closure/cell rules are FIXED/Irrelevant. |
| `semantics/call.k` | 3 syntax, 21 rules | Generic call, argument order, plain closure dispatch, and parameter binding are USED/Faithful. Builtin/method/ref and annotated closure paths are FIXED/Irrelevant. |
| `semantics/assert.k` | 3 rules | FIXED/Irrelevant to the proof term; used only by the reviewer concrete driver. |
| `semantics/bool.k` | 1 context, 13 rules | FIXED/Irrelevant. Its structural short-circuit equations are consistent on their declared value model. |
| `semantics/iter.k` | 1 syntax | FIXED/Irrelevant iterator protocol declaration. |
| `semantics/range.k` | 2 syntax, 6 rules | FIXED/Irrelevant guarded integer range definitions. |
| `semantics/list.k` | 5 syntax, 27 rules | FIXED/Irrelevant list construction, iteration, equality, mutation, and membership rules. |
| `semantics/tuple.k` | 4 syntax, 21 rules | FIXED/Irrelevant tuple construction, iteration, equality, binding, and unpacking rules. |
| `semantics/str.k` | 5 syntax, 28 rules | FIXED/Irrelevant ASCII-string definitions and lexicographic helpers. |
| `semantics/set.k` | 6 syntax, 12 rules | FIXED/Irrelevant finite-code-set definitions. |
| `semantics/methods.k` | 27 syntax, 75 rules | FIXED/Irrelevant method subset. No method term is reachable from the submitted body. |
| `semantics/builtins.k` | 38 syntax, 137 rules | Only `builtinsScope` construction in `core.k` is present in the entry state; no builtin is called. All rules here are FIXED/Irrelevant, except `md5hexCodes` is explicitly FIXED/Opaque, irrelevant. |
| `semantics/subscript.k` | 2 contexts, 15 syntax, 40 rules | FIXED/Irrelevant. `valSeqAt [total]` is intentionally under-specified out of bounds/over opaque sequences and has no influence here. |
| `semantics/dict.k` | 12 syntax, 28 rules | FIXED/Irrelevant dictionary subset. |
| `semantics/sort.k` | 6 syntax, 19 rules | `sortVS` and `sortKeyVS` are FIXED/Opaque, irrelevant; remaining reverse/concrete insertion-sort plumbing is FIXED/Irrelevant. |
| `semantics/concrete.k` | 5 syntax, 16 rules | LLVM-only FIXED/Irrelevant keyed-sort/deep-equality rules, absent from the Haskell proof definition. |
| `semantics/comprehension.k` | 3 syntax, 7 macro rules | FIXED/Irrelevant source macros. |
| `semantics/float.k` | 34 syntax, 121 rules | Nineteen explicitly opaque `no-evaluators` functions and their concrete LLVM twins are FIXED/Opaque, irrelevant. All float terms are sort/head-disjoint from the submitted integer-only execution. |

## Fixed-semantics limitations that are not theorem unsoundness

The fresh compilers warn that several supplied `total` declarations are not
syntactically exhaustive over their broad carrier sorts (`mapStrVS`, `floorFI`,
`toF`, `ceilF`, and `valSeqAt`). The fixed language also intentionally models a
restricted Python subset (ASCII strings, selected methods/exceptions, opaque
sort/float/MD5 behavior). These are real trust-boundary limitations, but no such
symbol occurs in the exact program term, loop invariant, postcondition, or
path condition. Consequently there is no satisfying `n > 0` witness by which
one of them can enable a false conclusion for this theorem.

No rule that can match an intended-domain execution state encodes the task
answer, bypasses a property-bearing computation, fabricates a result, or
replaces execution with an oracle.
