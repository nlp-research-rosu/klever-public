# Submitted-program constructor and rule mapping

This mapping is based on the trustedly regenerated `solution.mpy` and the fresh
scratch copy of the supplied semantics.

| Program constructor/effect | Declaration | Material execution rules | Review decision |
|---|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:61`, `semantics/core.k:124` | `core.k:125-127` loads and sequences statements left-to-right | Sound for the submitted module; no statement is skipped. |
| `FuncDef`, `Params`, closure binding | `syntax.k:52,57,60`, `functions.k:8` | `functions.k:14`, `call.k:69`, `functions.k:63-64,78,80,85` | The real body is stored in a closure, the integer argument is bound, return discards only the active callee suffix, and `#pop` restores the saved caller continuation/state. |
| `Name` lookup | `syntax.k:12`, `core.k:130` | `core.k:131-132,152` | Lexical lookup selects the explicit `count_up_to` binding and all local variable bindings. No proof rule pins a name independently of the environment. |
| `Int`, `Bool` literals | `syntax.k:9-11` | `core.k:194-195` | Exact mathematical integers and booleans. |
| `Assign(Name, ...)` | `syntax.k:41` (`strict(2)`) | `controls.k:9`; cell-write priority rule at `controls.k:12` is inapplicable because this ordinary frame has no `$cells` binding | RHS is evaluated before the scope update; state effects match the program. |
| `If` and truthiness | `syntax.k:48` (`strict(1)`), `core.k:199` | `controls.k:51-54`, `core.k:200,202` | Guards evaluate first and choose exactly one branch; this program uses Bool results and the `prime` Bool local. |
| `While` | `syntax.k:44`, `controls.k:65` | `controls.k:77-81,85` | Guard re-evaluates every iteration; true executes body then loop label, false terminates. The auxiliary claims anchor exact `#while(condition, body)` terms after real semantic steps. |
| `Compare` / `CmpOp` | `syntax.k:30,32` | evaluation contexts `operators.k:15-16`; dispatch `operators.k:17`; Int cases `int.k:22-27` | Left then right operand evaluation and exact `<`, `<=`, and `==` mathematical-Int comparisons. |
| `BinOp("+",...)` | `syntax.k:14` (`seqstrict(2,3)`) | `operators.k:12`; `int.k:9` | Left-to-right evaluation and exact integer addition for both loop increments. |
| `BinOp("%",...)` | same | `operators.k:12`; `int.k:15,19-20` | Python-style modulo. Every reached divisor is at least 2, so no zero-divisor exception is abstracted. |
| `ListExpr` and allocation | `syntax.k:16`, `list.k:13` | `list.k:14-15`; `core.k:117-121`; `core.k:186,189-191,213-219` | Elements evaluate left-to-right and each literal allocates at fresh `heapLoc`; entry starts at location 0. |
| `Attribute`, `Call`, argument order | `syntax.k:27-28`, `core.k:185-186`, `call.k:19` | `call.k:16,20-21,24,52-58`; `core.k:189-191` | The receiver/callee is evaluated before arguments. `isMutMethod("append")` preserves the receiver reference so the list mutator rule, not a dereferenced-value oracle, executes. |
| `list.append` mutation | `list.k:18` | `list.k:19-20,53-55` | Writes `valSeqConcat(old, [candidate])` at the selected heap location and returns `noneV`; the following `Expr` discards only that value. |
| expression statement | `syntax.k:51` (`strict`) | `controls.k:48` | Call side effect happens before the resulting `noneV` is discarded. |
| `Return` and call-frame control | `syntax.k:49` (`strict`) | `functions.k:78,85`; call setup `call.k:69-76` | The returned heap reference is preserved and the callee frame is removed; heap and monotone heap location survive. |

No program constructor maps to `float.k`, `sort.k`, `dict.k`, `set.k`,
`subscript.k`, comprehension, range/iterator, string-method, or other opaque
facilities. Those fixed-baseline declarations are inventoried separately and
have no symbol or control dependency on any positive claim or postcondition.
