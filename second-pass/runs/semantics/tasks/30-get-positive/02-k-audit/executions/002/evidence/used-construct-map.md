# Submitted constructor-to-rule map

| Submitted constructor/control | Declaration | Executing rules in the proof path | Audit result |
|---|---|---|---|
| `Module` / `FuncDef("get_positive", Params("l"), BODY)` | `semantics/syntax.k:41,57,60,61` | `core.k:125-127`; `functions.k:14` | The entry claim begins after module loading and preinstalls the same closure. Expanded submitted and claim modules have identical KORE hashes. |
| statement sequence / `.Stmts` | `semantics/syntax.k:56` | `core.k:126-127` | Left-to-right sequencing; empty bodies terminate. |
| `Assign(Name("result"), ListExpr(.Exprs))` | `semantics/syntax.k:8,37,41` (`Assign` is strict in RHS) | `list.k:14-15`; `core.k:189-191,217-219,118`; `controls.k:9` | Allocates the empty result list at fresh heap location 0 and binds `result` to `ref(0)`. |
| `For(Name("x"), Name("l"), BODY)` | `semantics/syntax.k:41` (`For` is strict in iterable) | `core.k:131-132`; `controls.k:69,71-73,85`; `tuple.k:32`; `verification.k:30-33` | Evaluates the input once, binds each integer in order, executes the body, and preserves the continuation. |
| `If(Compare(...), APPEND, .Stmts)` | `semantics/syntax.k:30,35,41` (`If` is strict in condition) | `operators.k:15-17`; `core.k:194,200`; `int.k:24`; `controls.k:52-54` | Uses mathematical integer `> 0`; true and false branches are disjoint and exhaustive. |
| `Name("x")`, `Name("l")`, `Name("result")`, `Name("get_positive")` | `semantics/syntax.k:8` | `core.k:130-132,152` | Ordinary lexical lookup; all used names are explicitly bound in the pinned scopes. |
| `Call(Name("get_positive"), ARG)` | `semantics/syntax.k:28` | `call.k:20-21,69-76`; `core.k:189-191`; `functions.k:63-65` | Evaluates callee then argument, creates the callee frame, and binds `l`. |
| `Call(Attribute(Name("result"), "append"), Name("x"))` | `semantics/syntax.k:28-29` | `call.k:16,20-24`; `list.k:53-55`; `core.k:189-191,213-219`; `controls.k:48` | Dispatches to the list mutator, appends exactly `x` in place, returns `noneV`, then discards it as an expression statement. |
| `Return(Name("result"))` | `semantics/syntax.k:48` (`Return` is strict) | `core.k:131-132`; `functions.k:78,85-91` | Returns `ref(0)`, restores the caller frame, preserves the allocated result object, and clears `ret`. |
| `getPositiveBody` / `positiveLoopBody` | `verification.k:9-25` | macro expansion | Expansion is mechanically constructor-identical to `solution.mpy`; no operation is skipped. |
| `intVals(INPUT)` | `verification.k:29-33` | two proof-local iterator rules | Empty/cons cases are disjoint and exhaustive. Bridge-free native-list connection claims close for both complete match domains. |
| `filterPositive` / `filterPositiveBranch` | `verification.k:36-49` | five structural equations | Transparent descending recursion; Boolean branch rules are disjoint, exhaustive, and agree with `x > 0`. |
