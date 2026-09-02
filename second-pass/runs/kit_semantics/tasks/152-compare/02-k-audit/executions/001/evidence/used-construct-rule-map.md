# Used construct to supplied-semantics rule map

The exhaustive source inventory is `05a-exhaustive-source-inventory.log`.
The counts/classification are in `05b-declaration-classification.log`.

| Submitted construct or effect | Declaration and execution rules |
|---|---|
| `Module` / statement sequence | `semantics/syntax.k:61`; `semantics/core.k:124-127` |
| `FuncDef("compare", ...)` / closure binding | `semantics/syntax.k:53`; `semantics/functions.k:14-16` |
| `Params("game","guess")` / argument binding | `semantics/syntax.k:57-60`; `semantics/functions.k:63-66`; call-frame creation in `semantics/call.k:69-75` |
| `Assign(Name("result"), ListExpr())` | strict RHS in `semantics/syntax.k:41`; list evaluation/allocation in `semantics/list.k:13-15` and `semantics/core.k:117-121`; binding in `semantics/controls.k:9-11` |
| `For(..., Call(Name("zip"), ...), ...)` | strict iterable in `semantics/syntax.k:45`; loop protocol in `semantics/controls.k:65-74`; initial heap-ref dereference in `semantics/controls.k:104-108` |
| `Name("zip")`, `Name("abs")`, and other names | lookup and parent traversal in `semantics/core.k:129-154`; builtin bindings in `semantics/core.k:156-181` |
| `Call` and left-to-right arguments | `semantics/syntax.k:28`; call routing in `semantics/call.k:18-32`; argument evaluator in `semantics/core.k:183-191` |
| `zip(game, guess)` | builtin rule in `semantics/builtins.k:162-164`; iterator truncation/yield rules in `semantics/builtins.k:166-174` |
| Tuple loop target and tuple yielded by `zip` | tuple expression in `semantics/syntax.k:21`; tuple target binding/unpacking in `semantics/tuple.k:30-46` and `semantics/tuple.k:55-57` |
| `Expr(...)` effect statement | strict evaluation in `semantics/syntax.k:52`; result discard in `semantics/controls.k:46-48` |
| `Attribute(Name("result"), "append")` | strict receiver in `semantics/syntax.k:29`; bound-method creation in `semantics/call.k:15-16`; method dispatch in `semantics/call.k:23-25` |
| `result.append(value)` | mutation-specific receiver preservation in `semantics/call.k:34-67`; exact heap update in `semantics/list.k:52-55`; `valSeqConcat` equations in `semantics/list.k:18-20` |
| `score - predicted` | left-to-right strict operands in `semantics/syntax.k:15`; operator dispatch in `semantics/operators.k:10-17`; integer subtraction in `semantics/int.k:13` |
| `abs(...)` | normal builtin binding/call path above; integer absolute value in `semantics/builtins.k:43-44` |
| `Return(Name("result"))` | strict return expression in `semantics/syntax.k:50`; return, frame pop, environment restoration, and escaped heap-reference preservation in `semantics/functions.k:77-90` |

No subscript, dict, set, string, float, sort, comprehension, import, assert,
boolean branch, range, or `while` construct occurs in the submitted module.
Their declarations and rules were nevertheless included in the exhaustive
inventory and reviewed as unused supplied-semantics families.
