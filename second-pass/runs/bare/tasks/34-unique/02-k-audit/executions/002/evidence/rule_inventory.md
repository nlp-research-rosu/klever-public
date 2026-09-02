# Local generated-semantics and proof-rule inventory

Scope: immutable `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. Imported K `INT` and `LIST` theories are listed separately
as trust boundaries; they are not candidate-authored rules.

## Syntax, attributes, and configuration

`MPY-SYNTAX` declares these productions:

1. `Program ::= Module(Stmts)`
2. `Stmt ::= FuncDef(String, Params, Stmts)`
3. `Stmt ::= Return(Expr)`
4. `Stmts ::= List{Stmt, ""}`
5. `Params ::= Params(Strings)`
6. `Strings ::= List{String, ","}`
7. `Expr ::= Int(Int)`
8. `Expr ::= Name(String)`
9. `Expr ::= ListExpr(Exprs)`
10. `Expr ::= Call(Expr, Exprs)`
11. `Exprs ::= List{Expr, ","}`

`MPY` declares:

12. `Val ::= VInt(Int)`
13. `Val ::= VList(List)`
14. `Val ::= VSet(List)`
15. `Val ::= apply(Program, Val) [function]`
16. `Val ::= eval(Expr, String, Val) [function]`
17. `List ::= evalExprs(Exprs, String, Val) [function]`
18. `Val ::= makeSet(Val) [function]`
19. `Val ::= sortSet(Val) [function]`
20. `List ::= dedupInts(List) [function]`
21. `List ::= removeInt(Int, List) [function]`
22. `List ::= sortInts(List) [function]`
23. `List ::= insertInt(Int, List) [function]`
24. `Val ::= run(Program, Expr) [function]`

`VERIFICATION` adds:

25. `List ::= uniqueSpec(List) [function]`

There are 11 local equational function symbols. There are no local `[total]`,
`[functional]`, `[simplification]`, `[owise]`, `opaque`, or priority
declarations. The sole state is:

`configuration <k> run($PGM:Program, $ARGS:Expr) </k>`

This pure one-cell representation is sufficient for the submitted body because
the body has one parameter, no mutation, no I/O, and one return expression. It
does not model general Python environments, heaps, exceptions, or rebinding.

## Rule-by-rule review

| ID | Source rule | Class and complete domain | Assessment |
|---|---|---|---|
| R1 | `apply(Module(FuncDef(_F, Params(X), Return(E))), V) => eval(E,X,V)` | Operational equation for a singleton module/function/parameter/return body | Truthful for the selected function in the submitted singleton module. The ignored function name is over-broad for a reusable module/binding semantics, but the claim supplies the exact `unique` binding and body. |
| R2 | `eval(Int(I),_,_) => VInt(I)` | Literal equation | Matches arbitrary-precision Python integers. |
| R3 | `eval(Name(X),X,V) => V` | One-binding lookup | Correct for the sole parameter `l`; the repeated `X` enforces exact name equality. |
| R4 | `eval(ListExpr(ES),X,V) => VList(evalExprs(ES,X,V))` | List-literal equation | Correct for the pure supported expressions. No mutation makes evaluation order observable here. |
| R5 | `eval(Call(Name("set"),E),X,V) => makeSet(eval(E,X,V))` | Builtin-call equation | Correct on ordinary builtin binding and integer-list arguments. It does not model rebinding, hashing exceptions, or noninteger equality. |
| R6 | `eval(Call(Name("sorted"),E),X,V) => sortSet(eval(E,X,V))` | Builtin-call equation | Correct on the actual `set(l)` result for integer lists. It does not model arbitrary iterables, keys, reverse order, or comparison exceptions. |
| R7 | `evalExprs(.Exprs,_,_) => .List` | Empty expression-list base | Correct. |
| R8 | `evalExprs(E:Expr,X,V) => ListItem(eval(E,X,V))` | Singleton expression list | Correct. |
| R9 | `evalExprs((E:Expr,ES:Exprs),X,V) => ListItem(eval(E,X,V)) evalExprs(ES,X,V)` | Nonempty/multiple expression list | Correct and structurally descending. Any syntactic overlap with the singleton encoding has the same right-hand result when the tail is empty. |
| R10 | `makeSet(VList(L)) => VSet(dedupInts(L))` | Set construction for represented integer lists | Correct on lists of `VInt`: retain one representative for each integer. |
| R11 | `sortSet(VSet(L)) => VList(sortInts(L))` | Sort represented set list | Correct for every `VSet` produced by R10. The raw syntax also admits synthetic `VSet` lists with duplicates, for which this broad rule would preserve duplicates; no intended source input reaches such a term. This is a representation-invariant gap, not an evidenced false conclusion on the submitted program path. |
| R12 | `dedupInts(.List) => .List` | Deduplication base | Correct. |
| R13 | `dedupInts(ListItem(VInt(I)) REST) => ListItem(VInt(I)) dedupInts(removeInt(I,REST))` | Deduplication step on integer lists | Correct: retain the head, remove every later equal integer, and recurse on a shorter list. |
| R14 | `removeInt(_, .List) => .List` | Removal base | Correct. |
| R15 | `removeInt(I,ListItem(VInt(I)) REST) => removeInt(I,REST)` | Equal-head branch | Correct and descending. |
| R16 | `removeInt(I,ListItem(VInt(J)) REST) => ListItem(VInt(J)) removeInt(I,REST) requires I =/=Int J` | Unequal-head branch | Correct. R15/R16 are disjoint and exhaustive for integers. |
| R17 | `sortInts(.List) => .List` | Insertion-sort base | Correct. |
| R18 | `sortInts(ListItem(VInt(I)) REST) => insertInt(I,sortInts(REST))` | Insertion-sort step | Correct and descending on finite integer lists. |
| R19 | `insertInt(I,.List) => ListItem(VInt(I))` | Insertion base | Correct. |
| R20 | insert before `J` when `I <=Int J` | Ordered insertion branch | Correct. |
| R21 | retain `J` and recurse when `I >Int J` | Ordered insertion branch | Correct. R20/R21 are disjoint and exhaustive for integers. |
| R22 | `run(P,ARG) => apply(P,eval(ARG,"",VList(.List)))` | Top-level pure runner | Correct for the actual ground list-literal arguments, whose evaluation does not consult the dummy binding. Over-broad for arbitrary `Name` arguments but not used that way. |
| R23 | `uniqueSpec(L) => sortInts(dedupInts(L))` | Proof-local definitional summary | Truthful for finite `VInt` lists and does not replace execution: R1–R21 reduce the submitted body to the same composition. It reuses the operational helpers, so the K theorem establishes this exact computational normal form; sortedness/uniqueness of that form follows from the audited insertion/dedup equations rather than a separate K predicate theorem. |

## Claims

1. The entry claim starts with the exact regenerated `Module(FuncDef("unique",
   Params("l"), Return(sorted(set(l)))))` constructor and `VList(L)`, with no
   side condition, and reaches `VList(uniqueSpec(L))`.
2. The ground example starts with `run` of the same exact module and the
   documented integer list, and reaches `[0,2,3,5,9,123]`.

Neither claim frames or omits another cell because the generated configuration
has only `<k>`.

## Construct coverage and trust boundary

The submitted `solution.mpy` uses `Module`, `FuncDef`, `Params`, `Return`,
`Call`, and `Name`; R1, R3, R5, and R6 cover their material behavior. Concrete
entry arguments use `ListExpr` and `Int`; R2, R4, and R7–R9 cover them.
R10–R21 cover `set`, duplicate elimination, and ascending sort. R22 connects
the configured program/argument inputs.

Trusted imports are K's `INT` and `LIST` domains: mathematical integer equality
and order, finite list constructors/matching, and their backend implementation.
The semantic bridge assumes ordinary Python builtins, integer equality/order,
and no monkeypatching. The language has no expression/value production for
Python strings, tuples, floats, or booleans, even though those include valid
inputs under the unqualified `list` source contract.
