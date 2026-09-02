# Static mapping and rule dispositions

The exhaustive declaration-level inventory is `rule-inventory.log`. This file
records the relevance and disposition applied to every inventoried source file,
then expands every candidate-local declaration individually.

## Actual `solution.mpy` construct mapping

| Submitted construct | Syntax | Executing fixed-semantics rules |
|---|---|---|
| `Module(FuncDef(...))` | `syntax.k:53,61` | `core.k:124-127` loads/sequences the module; `functions.k:14-16` binds exactly `closureVal(PNS,BODY,L)`. The symbolic entry starts after this deterministic loader step with that exact closure prebound. |
| `Call(Name("f"), Int(N))` | `syntax.k:9,12,28` | `core.k:131-154,194`; `call.k:20-21,69-75`; `functions.k:63-66,78-90`. Callee and arguments evaluate left-to-right, a frame is allocated, the parameter is bound, and return restores the caller. |
| `Assign(Name(...), ...)` | `syntax.k:41` | Strict RHS evaluation from the syntax attribute, then `controls.k:9-11`. |
| `ListExpr()` | `syntax.k:17` | `list.k:13-15`, `core.k:189-191,117-121,217-219`; this allocates the returned list at heap location 0. |
| `Int(0)`, `Int(1)`, `Int(2)` | `syntax.k:9` | `core.k:194`. |
| `While(Compare(...), BODY)` | `syntax.k:46` | `controls.k:65-67,77-82,85`; a true guard executes the body and returns to the literal `#while`, while a false guard exits. |
| `Compare(Name("i"), "<=", Name("n"))` | `syntax.k:30,32` | Evaluation contexts `operators.k:15-17`, integer comparison `int.k:23`, and name lookup `core.k:131-154`. |
| Integer `AugAssign` with `*` and `+` | `syntax.k:44` | Strict RHS then `controls.k:20-23`; arithmetic is `int.k:9,14`. |
| `BinOp("%", i, 2) == 0` | `syntax.k:15,30,32` | Left-to-right binop strictness, `operators.k:12,15-17`, `int.k:15,19-20,26`. The reachable divisor is the literal 2. |
| `If(...)` | `syntax.k:49` | Strict condition then `controls.k:51-54`; the Boolean result uses `core.k:199-205`. |
| `result.append(value)` | `syntax.k:28-29,52` | Attribute becomes a bound method (`call.k:16`); generic call/argument evaluation is `call.k:20-24` and `core.k:189-191`; the in-place heap update is `list.k:53-55`; `Expr` discards `noneV` via `controls.k:48`. |
| `Return(Name("result"))` | `syntax.k:50` | Name lookup plus `functions.k:78-90`, returning the allocated reference while preserving its heap object. |
| Sequence append algebra | `core.k:14`; `list.k:18` | `list.k:19-20` defines finite `ValSeq` concatenation. |

No float, string, set, tuple, subscript, comprehension, range, sort, dict, MD5,
or other opaque result-bearing symbol occurs in the submitted program or in a
reachable proof-local result term.

## Supplied-semantics file disposition

The candidate tree was byte-identical to the trusted supplied tree. Therefore
the 928 declarations from these files are fixed semantics, not candidate proof
extensions. Every file was read in full. For used files, the relevant rules are
expanded above and agree with the submitted Python execution. For unused files,
their constructors cannot be reached from the submitted AST or its pinned
integer/list values, so they cannot contribute to claim closure.

| File/module | Relevance to this proof | Disposition for every inventoried declaration |
|---|---|---|
| `semantics.k` / `MPY`, `MPY-KRUN` | Assembly/import boundary | Trusted supplied assembly; proof imports `MPY`, runtime imports `MPY-KRUN`. |
| `syntax.k` / `MPY-SYNTAX` | Used | Declarations match every submitted AST node as mapped above. |
| `core.k` / `MPY-CORE` | Used | Configuration, allocation, lookup, literals, argument order, truthiness, and finite sequence helpers are consistent with the executed program. |
| `operators.k` / `MPY-OPERATORS` | Used | Contexts impose the needed evaluation order; integer cases dispatch without an overlapping reachable domain. |
| `int.k` / `MPY-INT` | Used | `+`, `*`, `%`, `<=`, and `==` agree with Python on reachable positive `i` and divisor 2. |
| `list.k` / `MPY-LIST` | Used | Empty-list allocation, finite concatenation, and in-place `append` preserve the heap and return `noneV` as required. |
| `controls.k` / `MPY-CONTROLS` | Used | Assignment, integer augmentation, conditional, while-loop continuation, and expression discard match control flow. |
| `functions.k` / `MPY-FUNCTIONS` | Used | Exact closure binding, parameter binding, return, stack, environment restoration, and escaping heap reference match the claim cells. |
| `call.k` / `MPY-CALL` | Used | Callee/argument evaluation and exact `closureVal` invocation execute the submitted body; no problem-local interception exists. |
| `bool.k` | Only fixed support | No candidate-local or opaque result enters the proof; reachable Boolean guard values are handled by fixed truthiness. |
| `methods.k` | Declaration/import support | `append` is handled directly in `list.k`; other methods are unreachable. |
| `builtins.k` | Registry/import support only | No builtin call is reachable from the submitted body. Opaque MD5 is unreachable. |
| `assert.k`, `concrete.k` | Runtime harness only | Included only in the fresh LLVM smoke execution, not the proof definition. |
| `iter.k`, `range.k`, `float.k`, `str.k`, `set.k`, `tuple.k`, `subscript.k`, `comprehension.k`, `sort.k`, `dict.k` | Unused by submitted AST and proof result | Fixed supplied declarations are inert for this proof. All listed opaque float/sort symbols are unreachable. |

The fixed semantics has 45 priority rules, 35 concrete-only rules, 26
`owise` rules, and multiple `total` declarations; the exact inventory is in
`rule-inventory.log` and the flagged declarations are in
`special-declarations.log`. None is a candidate-local priority rule or
operational bridge.

## Candidate-local `verification.k` declarations

| Location | Declaration | Class and soundness decision |
|---|---|---|
| `verification.k:8-9` | `outputOK(...)[function,total]` | Transparent definitional postcondition, not an operational rule. `total` leaves malformed/nonmatching arguments underspecified, but supplies no equation making them true; both symbolic mutations get stuck on the unmet `outputOK`. |
| `verification.k:10-11` | Empty suffix when `I>N` | Sound base case: exactly no indices remain. |
| `verification.k:12-16` | Even-step suffix equation | Sound recurrence: emitted value is `F*I`, then factorial and triangular accumulators become `F*I` and `T+I`. |
| `verification.k:17-22` | Odd-step suffix equation | Sound recurrence: emitted value is `T+I`, with the same accumulator updates. The even/odd guards are disjoint and exhaustive for integer `I` because the divisor is 2. |
| `verification.k:25-27` | Concatenation associativity simplification | Sound for finite constructor `ValSeq`, by induction on the left sequence. |
| `verification.k:28-29` | Right identity simplification | Sound for finite constructor `ValSeq`, by induction on the left sequence. Its overlap with associativity has the same normal result. |
| `verification.k:32-35` | Left-cancellation of equal concatenations | Sound for finite free sequences, by induction on the common prefix. |
| `verification.k:36-38` | `P = P++A` implies `A=[]` | Sound for finite sequences: length gives `len(P)=len(P)+len(A)`, hence `len(A)=0`. |

There are no candidate-local opaque symbols, priority rules, operational
bridges, ordinary execution rewrites, or `functional` declarations. The only
ordinary candidate rules define the postcondition; the four other local rules
are simplifications. Exhaustive small finite-sequence checks are preserved in
`local-algebra-check.log`; the universal decisions above rest on the stated
inductions, not on those finite tests.
