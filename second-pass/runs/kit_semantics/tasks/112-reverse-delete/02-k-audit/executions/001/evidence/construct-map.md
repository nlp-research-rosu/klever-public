# Constructor-to-semantics map for `solution.mpy`

The program term contains exactly one `Module` with one `FuncDef` and no other
top-level statement. The entry theorem starts after this inert loading prefix:
`core.k:125-127` sequences the module and `functions.k:14-16` installs
`closureVal(PNS, BODY, 0)`. Fresh concrete execution in
`03-concrete-execution.log` shows that exact closure as the only module binding.
`04-program-pinning.log` mechanically compares the regenerated function body
with the closure body in the entry claim.

| Program constructor | Declaration | Material rules / evaluation order | Review |
|---|---|---|---|
| `Module(Stmts)` | `syntax.k:61` | `core.k:124-127` | Single function definition; no skipped top-level effects. |
| `FuncDef("reverse_delete", Params, Body)` | `syntax.k:53`; `Params` at 57-60 | `functions.k:14-16` | Binds the exact parameter list/body at defining environment 0. |
| `Assign(Name, Expr)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18` | RHS first, then update current plain local scope; cell-priority leg is inapplicable because this closure has no cell metadata. |
| `Name(String)` | `syntax.k:12` | `core.k:130-154` | Looks in current local scope, then parent; all body names are present locally. |
| `Str("")` | `syntax.k:13` | `str.k:13-17` | The only literal used by the theorem is ASCII empty string, mapped to `.IntSeq`. |
| `For(Name("ch"), Name("s"), Body)` | `syntax.k:45` (`strict(2)`) | `controls.k:65-75`; `tuple.k:31-41`; `str.k:8-10` | Iterable evaluated once; each code is bound as a one-code string; body and remaining loop execute in order. |
| `If(Compare(...), Then, .Stmts)` | `syntax.k:49` (`strict(1)`) | `controls.k:51-54` | Condition is evaluated and converted with `truthy`; exactly one branch is selected. |
| `Compare(ch, CmpOp("not in", c))` | `syntax.k:30,32` | evaluation contexts and dispatch at `operators.k:14-17`; string case at `str.k:28-41` | Left then right evaluation; one-character substring membership; `notBool` selects retained characters. |
| `AugAssign(result, "+", ch)` | `syntax.k:44` (`strict(3)`) | `controls.k:20-31`; string `applyBin` at `str.k:20-24` | Evaluates `ch`, reads the local string accumulator, and appends the one-character string. Ref-priority leg cannot match. |
| `BinOp("+", ch, reversed_result)` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; `str.k:20-24` | Left-to-right string concatenation prepends the current character. |
| `Return(TupleExpr(...))` | `syntax.k:50` (`strict`) | `functions.k:77-91` | Evaluates result, records it, restores caller environment, removes callee scope, and restores the saved continuation. |
| `TupleExpr(result, Compare(...))` | `syntax.k:21` | `tuple.k:14-18`; shared argument evaluator `core.k:183-191,213-219` | Tuple fields evaluate left-to-right and become a two-element semantic tuple. |
| `Compare(result, CmpOp("==", reversed_result))` | `syntax.k:30,32` | `operators.k:14-17`; `str.k:25` | Structural `IntSeq` equality, hence true exactly when the forward and reverse accumulators agree. |

The theorem itself begins with `Call(Name("reverse_delete"), (str(S), str(C)))`.
`call.k:18-21` evaluates the binding and arguments left-to-right;
`call.k:69-75` allocates the local frame and pushes the exact continuation;
`functions.k:62-75` binds `s` then `c`; and `functions.k:77-91` returns and pops
the frame. Strings and tuples are unboxed values in this semantics, so this
program makes no heap allocation. The heap and heap counter therefore remain
unchanged.
