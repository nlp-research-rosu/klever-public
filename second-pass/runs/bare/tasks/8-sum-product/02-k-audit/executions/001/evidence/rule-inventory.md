# Exhaustive local declaration and rule inventory

Scope: the fresh source copies of `semantic.k`, `verification.k`, and `spec.k`.
There are no generated helper K source files.

## Syntax, configuration, and attributes

| ID | Source | Declaration | Attributes / role | Audit result |
|---|---|---|---|---|
| D01 | `semantic.k:3-12` | Sort heads `Module`, `Stmt`, `Stmts`, `Expr`, `Params`, `Strings` | Abstract-syntax categories | Sufficient for every constructor in `solution.mpy`. |
| D02 | `semantic.k:14` | `Module(Stmts)` | `[symbol(Module)]` | Exact outer constructor used by the translator. |
| D03 | `semantic.k:15` | `Stmts ::= List{Stmt, ""}` | `[symbol(Stmts)]`; generated empty/sequence list productions | Represents the ordered top-level statement sequence; `.Stmts` and cons/sequence are used by R02-R03. |
| D04 | `semantic.k:16` | `Strings ::= List{String, ","}` | `[symbol(Strings)]` | Parses the two imported names and single `prod` name. Runtime import payload is abstracted by R04. |
| D05 | `semantic.k:18-23` | `ImportFrom`, `FuncDef`, `Return` | Constructor symbols | Exactly the statement constructors in the submitted term. |
| D06 | `semantic.k:25` | `Params(String)` | `[symbol(Params)]` | Exact one-parameter form used by the program. |
| D07 | `semantic.k:27-31` | `Name`, `TupleExpr`, `Call` | Constructor symbols | Exactly the expression constructors used by the body. |
| D08 | `semantic.k:39-41` | Sort `Ints`; `.Ints`; `Int "," Ints` | `[symbol(noInts)]`, `[symbol(consInts)]` | Finite integer-list model, including empty and nonempty cases. |
| D09 | `semantic.k:43-46` | Sort `PyVal`; `PyInt`, `PyList`, `PyTuple` | Constructor symbols | Models precisely the integer, list, and tuple values required by the formal domain/result. |
| D10 | `semantic.k:48-50` | Sort `Closure`; `Closure(String, Expr)` | Constructor symbol | Stores the one parameter and pure return expression used by the exact function. |
| D11 | `semantic.k:52-54` | `#exec(Stmts)`, `#invoke(String, PyVal)` | KItem constructor symbols | Internal control terms; both are eliminated on real executions. |
| D12 | `semantic.k:56` | `sumInts(Ints):Int` | `[function, total]` | R14-R15 are disjoint, structurally descending, and cover all `Ints`. |
| D13 | `semantic.k:57` | `productInts(Ints):Int` | `[function, total]` | R16-R17 are disjoint, structurally descending, and cover all `Ints`. |
| D14 | `semantic.k:58` | `eval(Expr, Map):PyVal` | `[function]`, deliberately not total | All exact-program uses are covered by R07, R09-R11; unsupported calls remain visibly unreduced. |
| D15 | `semantic.k:59` | `sumValue(PyVal):PyVal` | `[function]`, not total | Exact use receives a `PyList` and is covered by R12. |
| D16 | `semantic.k:60` | `productValue(PyVal):PyVal` | `[function]`, not total | Exact use receives a `PyList` and is covered by R13. |
| D17 | `semantic.k:61` | `lookupValue(Map, String):PyVal` | `[function]`, not total | Exact use has a present one-entry binding and is covered by R08. |
| D18 | `semantic.k:63-69` | `<python>` with `<k>`, `<input>`, `<functions>`, `<result>` | Initial values `$PGM`, `$INPUT`, `.Map`, `.K` | Minimal state is adequate: the exact program has no mutation, heap, exceptions, I/O, or allocation. |
| D19 | `verification.k:7` | `expectedSumProduct(Ints):PyVal` | `[function, total]` | V01 is unguarded and covers every `Ints` value. |

There are no local `[functional]` declarations, simplification rules,
`[concrete]` rules, priority attributes, fresh variables, or opaque
result-bearing symbols.

## Operational rules and function equations

| ID | Source | Rule / equation | Classification and complete audit |
|---|---|---|---|
| R01 | `semantic.k:71-72` | `Module(SS)` schedules `#exec(SS) ~> #invoke("sum_product", V)` using `<input> V` | Entry-harness operational rule. It preserves every modeled cell and invokes only after ordered top-level execution. It is not general Python module execution, but it is exact for the task entry point pinned in the submitted module. |
| R02 | `semantic.k:74` | `#exec(.Stmts) => .K` | True empty-sequence base case. |
| R03 | `semantic.k:75` | `#exec(S SS) => S ~> #exec(SS)` | Preserves source order and reaches R02 after the finite statement list. Base/cons patterns are disjoint. |
| R04 | `semantic.k:77` | `ImportFrom(_, _) => .K` | Import abstraction. On the exact program, `typing` is runtime-irrelevant and `math.prod` is modeled by the fixed R11/R13/R16-R17 primitive path. The rule is broader than its demonstrated justification for arbitrary modules; no false result witness exists for the fixed submitted program under the intended ordinary-integer-list domain. This is recorded as an adequacy limitation, not an unsoundness finding. |
| R05 | `semantic.k:79-80` | One-return `FuncDef` stores `Closure(P,E)` in `<functions>` | Exact for the submitted one-parameter, one-`Return` function. Map update correctly installs/overwrites the named definition. Other bodies do not match and remain stuck. |
| R06 | `semantic.k:82-84` | `#invoke(F,V)` finds `Closure(P,E)`, removes the call, and writes `eval(E,P |-> V)` to an empty result cell | Exact task-call operational rule. It reads the selected binding, binds the already evaluated input value, changes only `<k>` and `<result>`, and preserves the function map/input. No return frame or suffix is discarded: the rule rewrites only `#invoke` at the front and frames the continuation. |
| R07 | `semantic.k:86` | `eval(Name(X),ENV) => lookupValue(ENV,X)` | Correct local-variable lookup path; the real body uses it only for `numbers`. |
| R08 | `semantic.k:87` | `lookupValue((X |-> V) _REST,X) => V` | Correct for a well-formed K map containing the unique key. The exact environment is the one-entry `P |-> V`. |
| R09 | `semantic.k:88-89` | Tuple evaluation maps both expressions to `PyTuple` | Correct for the two pure builtin calls. Python's left-to-right order is observationally immaterial here because neither operation changes state or raises on finite lists of ordinary integers. |
| R10 | `semantic.k:90-91` | `eval(Call(Name("sum"),A),ENV)` uses `sumValue(eval(A,ENV))` | Fixed external-primitive bridge for Python's builtin `sum` on the formal `PyList(Ints)` domain. It does not skip program-defined code. R12/R14-R15 completely define its value. |
| R11 | `semantic.k:92-93` | `eval(Call(Name("prod"),A),ENV)` uses `productValue(eval(A,ENV))` | Fixed external-primitive bridge for imported `math.prod` on the formal `PyList(Ints)` domain. R13/R16-R17 completely define its value. |
| R12 | `semantic.k:95` | `sumValue(PyList(IS)) => PyInt(sumInts(IS))` | Correct type wrapper on every reachable use. |
| R13 | `semantic.k:96` | `productValue(PyList(IS)) => PyInt(productInts(IS))` | Correct type wrapper on every reachable use. |
| R14 | `semantic.k:98` | `sumInts(.Ints) => 0` | Correct empty-sum identity. Disjoint from R15. |
| R15 | `semantic.k:99` | `sumInts(I,IS) => I +Int sumInts(IS)` | Correct recursive integer-list sum; structurally descends. |
| R16 | `semantic.k:100` | `productInts(.Ints) => 1` | Correct empty-product identity. Disjoint from R17. |
| R17 | `semantic.k:101` | `productInts(I,IS) => I *Int productInts(IS)` | Correct recursive integer-list product; structurally descends. |
| V01 | `verification.k:9-10` | `expectedSumProduct(IS) => PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))` | Definitional summary, not an execution rewrite. It is total and fixes both result components using the fully defined mathematical folds above. |

All other constructor patterns that could overlap are disjoint by constructor
or literal name. In particular, the `sum` and `prod` call equations are
disjoint; the list bases and recursive cases are disjoint; and the statement
constructors are disjoint. No guard, priority, or simplification interaction is
present.

## Claim inventory and real-program construct mapping

`spec.k` contains one unlabeled entry reachability claim and there are no
auxiliary or loop claims. Its initial `<k>` term is the submitted
`solution.mpy` term byte-for-byte after whitespace normalization. It starts
with an empty function map/result and an arbitrary `PyList(IS)`. Its
post-state consumes `<k>`, installs the exact closure, and constrains the result
to `expectedSumProduct(IS)`.

Construct-to-rule coverage for the exact program:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| `Module` and ordered statement list | D02-D03 | R01-R03 |
| Both `ImportFrom` statements | D04-D05 | R04 |
| `FuncDef`, `Params`, one `Return` | D05-D06 | R05 |
| Entrypoint invocation | D11 | R06 |
| `TupleExpr` | D07 | R09 |
| `Call(Name("sum"), Name("numbers"))` | D07 | R10, R12, R14-R15 |
| `Call(Name("prod"), Name("numbers"))` | D07 | R11, R13, R16-R17 |
| Parameter `Name("numbers")` | D07 | R07-R08 |
| Integer-list input and tuple result | D08-D09 | R12-R17, V01 |

The empty and nonempty concrete executions exercise both base and recursive
fold rules. Normal, zero-containing, negative, and arbitrary-precision inputs
all terminate with no residual control term.
