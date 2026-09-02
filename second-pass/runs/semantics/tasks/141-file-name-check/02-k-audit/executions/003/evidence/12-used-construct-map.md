# Submitted-program construct map

This maps every constructor in regenerated `solution.mpy` to the selected
supplied semantics and identifies proof-local preemption.

| Submitted constructor / effect | Declaration | Fixed execution path | Proof-local effect |
|---|---|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `semantics/syntax.k` | `core.k` `#loadAll` and `functions.k` definition binding | `runFileNameCheck` constructs the exact function closure directly; constructor JSON identity is recorded in `09-program-term-pinning.log` |
| `Expr(Str(...))` docstring | `semantics/syntax.k` | `str.k` literal conversion, then `controls.k` discards the value | Executes normally |
| `Name` | `semantics/syntax.k` | `core.k` `#look` walks the concrete function scope, module scope, and builtins | Executes normally; count receiver binding is already a `boundMethodV` when bridged |
| `Call`, argument order | `semantics/syntax.k` | `call.k` `#callee`, `core.k` `#evalArgs`, then `#applyK` | Count calls are intercepted only after receiver and argument evaluation |
| `Attribute(...,"count")` | `semantics/syntax.k` | `call.k` creates `boundMethodV`; `methods.k` `applyMethod`/`cntSub` computes the result | `verification.k:19` priority 40 replaces `applyMethod`/`cntSub` by opaque `charCount` |
| `len(file_name)` | `semantics/syntax.k` | `call.k` builtin dispatch; `builtins.k` `seqLen`; `core.k` `isLen` | Executes normally |
| `Subscript(...,0)` | `semantics/syntax.k` | `subscript.k` `applyIndex`, `normIdx`, `intSeqAt` | `verification.k:27` priority 40 returns opaque `headCode`; its length guard makes the real access in-bounds but does not fix the returned code |
| `ord(...)` | `semantics/syntax.k` | `call.k` builtin dispatch; `builtins.k` one-character `ord` | Executes normally on the bridged one-character string |
| `Slice(UnaryOp("-",Int(4)),NoBound,NoBound)` | `semantics/syntax.k` | `operators.k`/`int.k` evaluate `-4`; `subscript.k` evaluates bounds and uses `doSlice`/`buildIS` | `verification.k:34` priority 40 preempts the complete slice and returns opaque `suffix4` |
| Three suffix `Compare("==",...)` nodes | `semantics/syntax.k` | `operators.k` dispatch; `str.k` code-sequence equality | `verification.k:42,48,54` priority 40 return independent opaque `suffixIs` flags |
| Integer `Compare` nodes | `semantics/syntax.k` | `operators.k`; `int.k` comparison rules | Execute normally |
| `UnaryOp("not",...)` | `semantics/syntax.k` | `operators.k`; `bool.k`/`core.k` truthiness | Executes normally |
| `BoolOp("and"/"or",...)` | `semantics/syntax.k` | `bool.k` left-to-right short-circuit rules | Executes normally, but consumes opaque-derived booleans |
| Nested integer `BinOp("+",...)` | `semantics/syntax.k` | strict left-to-right evaluation; `int.k` addition | Executes normally, summing ten opaque `charCount` results |
| `Assign` | `semantics/syntax.k` | `controls.k` updates only the active function scope | Executes normally |
| `If` | `semantics/syntax.k` | strict condition evaluation; `controls.k` `#branch` | Executes normally, with branch values supplied by opaque-derived computations |
| `Return` and call cleanup | `semantics/syntax.k` | `functions.k` `retV`, `#pop`; `call.k` frame allocation | Executes normally and restores all claimed cells |

There are no loops, comprehensions, heap allocations, mutable objects,
exceptions, imports, helper-function calls, or auxiliary loop claims in the
submitted program. The six proof-local priority bridges read and write only
the `<k>` cell; the displaced fixed operations are pure. Their fatal gap is
value fidelity: no bridge-free theorem or equations connect any returned
observation to `cntSub`, `intSeqAt`, `doSlice/buildIS`, or string equality.
