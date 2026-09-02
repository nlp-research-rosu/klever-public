# Submitted construct to supplied-rule map

The line references are to the byte-identical trusted tree under
`/reference/reference-semantics/`.

| Submitted or proof term | Declaration and operational path | Audit decision |
|---|---|---|
| `Module(...)`, statement sequence | `syntax.k:61`; `core.k:124-127` | Exact module body is loaded, then statements execute left-to-right. |
| `FuncDef`, closure binding | `syntax.k:53`; `functions.k:14-16` | Binds the exact body in module scope 0. No body replacement. |
| `Call(Name("common"), ...)` | `syntax.k:28`; `call.k:20-21,69-75`; `functions.k:63-66` | Callee lookup and arguments evaluate left-to-right, a frame is pushed, and both arguments bind exactly. |
| `Assign(Name(...), ...)` | `syntax.k:41`; `controls.k:9-11` | Writes the current function scope; the higher-priority cell rule is pruned because this plain frame has no `$cells`. |
| `ListExpr()` | `syntax.k:17`; `list.k:13-15`; `core.k:117-121,189-191,217-219` | Evaluates elements left-to-right and allocates heap object 0. |
| `Int(0)` | `syntax.k:9`; `core.k:194` | Produces integer zero for the initial `item` binding. |
| `For(Name("item"), Name("l1"), body)` | `syntax.k:45`; `controls.k:69-74`; `list.k:9-10`; `tuple.k:31-38` | Evaluates the iterable once, yields left-to-right, binds `item`, executes the exact body, and returns to `#loop`. `SPEC.common-loop` is an exact circularity at that real loop head. |
| `If(BoolOp(...), append, .Stmts)` | `syntax.k:16,49`; `bool.k:16-25`; `controls.k:51-54`; `core.k:199-205` | The first comparison short-circuits the second; the branch uses Boolean truthiness. |
| `Compare(item, "in", l2)` | `syntax.k:30,32`; `operators.k:15-17,38-42`; `list.k:58-67` | Right list objects are dereferenced, then operational membership folds by K structural equality. `SPEC.member-fold` independently connects the exact fold to `memberVS`, but this disagrees with Python cross-type numeric equality: `true ==K 1` is false while Python `True == 1` is true. The preserved `[True]`/`[1]` witness makes the K execution return empty and fail the Python-correct `[True]` assertion. |
| `Compare(item, "not in", result)` | Same membership path plus `list.k:60,67` | The allocated result reference is dereferenced, membership folds, then Boolean negation applies. |
| `result.append(item)` | `syntax.k:29`; `call.k:16,20-24`; `list.k:53-55`; `list.k:18-20` | Attribute evaluation produces a bound method and the priority-40 append rule updates the same heap object by one right-appended element. |
| expression statement wrapping append | `syntax.k:52`; `controls.k:48` | The `noneV` return is discarded after the heap effect. |
| `Return(Call(Name("sorted"), Name("result")))` | `syntax.k:50`; `core.k:131-154,157-181`; `call.k:20-21,38-41`; `sort.k:18,36-37`; `functions.k:78-90` | Looks up the real builtin, dereferences the result list, allocates heap object 1 containing `sortVS`, stores that reference as the return, then restores the caller frame. |
| `sortVS` | `sort.k:18`; concrete integer rules `sort.k:20-24` | Opaque and total in symbolic proofs. This is an explicit supplied-semantics trust boundary, not a candidate proof rule. Ground execution validates insertion sorting for tested integers; the universal ascending-sort meaning remains assumed. |
| Configuration/cells | `core.k:44-60`; call/return and allocation rules above | The entry claim pins the pristine module state and final environment, scopes, two heap allocations, heap counter, empty stack, cleared return/exception state, and exit code 0. Omitted cells in helper claims are frame-completed and preserved. |

## Proof-local definitions

| Extension | Classification and justification |
|---|---|
| `commonLoopBody`, `commonBody`, `commonDefinition` | Macro-only exact syntax abbreviations. Independent KORE comparison proves `Module(commonDefinition)` is identical to the submitted `solution.mpy`; they do not rewrite runtime configurations. |
| `memberVS` | Definitional summary of the supplied K fold. Empty/cons equations are exhaustive, equality and disequality guards are disjoint, and recursion strictly shortens the sequence. Its use of `==K` faithfully summarizes the supplied semantics but inherits that semantics’ mixed-numeric mismatch with real Python. |
| `shouldAdd` | Definitional Boolean expression matching the two source conditions. |
| `commonAcc` | Definitional summary. Empty/cons cases are exhaustive and each recursive call strictly shortens `FIRST`; the true branch appends exactly once. |
| `commonSpec` | Alias for `commonAcc(FIRST, SECOND, .ValSeq)`. |
| `lastAfter` | Definitional summary of loop-target binding. Empty/cons equations are exhaustive and recursion strictly shortens the sequence. |
| `SPEC.member-fold` | Bridge-free universal connection claim from the supplied operational membership fold to `memberVS`; proved first and only then trusted downstream. |
| `SPEC.common-loop` | Exact loop-head circularity over the real target/body, arbitrary continuation, current environment/scope, and result heap cell. It summarizes only loop execution and frames all unrelated map/cells. |
| `SPEC.common-function` | Entry theorem over the exact submitted definition. It returns `ref(1)` and fixes heap object 1 to `list(sortVS(commonSpec(FIRST, SECOND)))`; it is not a free-result or implication-only claim. Because the precondition accepts arbitrary `ValSeq`, the mixed-numeric membership mismatch reaches this result and prevents the theorem from being a theorem about the real Python function on the full prompt domain. |
