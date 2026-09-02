# Exhaustive source-level K inventory and soundness decisions

Scope: the scratch copy contains exactly `semantic.k`, `verification.k`, and
`spec.k` as K sources. There are no generated helper K files. Candidate-built
definitions were excluded. Line numbers below refer to those scratch source
copies, which are byte copies of the candidate sources.

## Local syntax and configuration inventory

| ID | Source | Declaration (all alternatives enumerated) | Role and decision |
|---|---|---|---|
| D1 | `semantic.k:9` | `Module ::= Module(Stmt)` `[symbol(Module)]` | Exact outer constructor used by `solution.mpy`; sound. |
| D2 | `semantic.k:10` | `Params ::= Params(String,String)` `[symbol(Params)]` | Exact two-parameter constructor used by this program; sound minimal coverage. |
| D3 | `semantic.k:12-13` | `Stmt ::= FuncDef(String,Params,Stmt) [symbol(FuncDef)] \| Return(Expr) [symbol(Return)]` | Covers both statement constructors used; no statement sequencing is needed by this one-return program. |
| D4 | `semantic.k:15-19` | `Expr ::= Name(String) [symbol(Name)] \| Call(Expr,Expr) [symbol(Call)] \| BinOp(String,Expr,Expr) [symbol(BinOp)] \| Subscript(Expr,Expr) [symbol(Subscript)] \| Slice(Bound,Bound,Bound) [symbol(Slice)]` | Exactly covers every expression constructor in `solution.mpy`; sound minimal grammar. |
| D5 | `semantic.k:20` | `Bound ::= Expr \| NoBound [symbol(NoBound)]` | Represents the lower expression and omitted upper/step in the used slice. |
| D6 | `semantic.k:22-24` | `Val ::= intVal(Int) \| listVal(List) \| noResult` | Integer/list values plus output sentinel; sufficient for the program. |
| D7 | `semantic.k:35-41` | `<maximum><k>$PGM:Module ~> boot</k><args>$ARGS:List</args><env>.Map</env><out>noResult</out></maximum>` | Explicit state: computation, input arguments, local environment, result. No heap/I/O cell is needed for this pure return-value program. |
| D8 | `semantic.k:43` | `KItem ::= boot \| finish(Val)` | Entry and return continuations; sound for the selected entry model. |
| D9 | `semantic.k:56` | `Val ::= eval(Expr,Map)` `[function]` | Partial evaluator for exactly the used expressions. |
| D10 | `semantic.k:67-70` | `Val ::= sortedVal(Val) \| lengthVal(Val) \| subtractVal(Val,Val) \| suffixVal(Val,Val)`, each `[function]` | Typed helper layer; all reachable cases from valid inputs have equations. |
| D11 | `semantic.k:76-78` | `List ::= sortInts(List) \| insertInt(Int,List) \| dropInts(Int,List)`, each `[function]` | Ascending insertion sort and prefix removal. |
| D12 | `verification.k:8` | `List ::= maximumSpec(List,Int)` `[function]` | Definitional mathematical summary used only in the postcondition; it does not rewrite the program control state. |

Attribute census: ten constructor alternatives carry `[symbol(...)]`; nine
function symbols carry `[function]` (`eval`, four typed value helpers, three
list helpers, and `maximumSpec`). There are no local `[total]`, `[functional]`,
`[opaque]`, `[priority]`, `[simplification]`, `[concrete]`, strictness, macro,
or anywhere rules. Thus there is no hidden totalization, oracle, priority
preemption, or proof-only simplifier to justify.

## Rule and claim inventory

| ID | Source | Complete rule/claim summary | Classification and decision |
|---|---|---|---|
| R1 | `semantic.k:45-48` | Exact `Module(FuncDef("maximum",Params("arr","k"),BODY)) ~> boot` becomes `BODY`; exactly two typed args bind `arr` and `k` into the empty environment. | Entry operational rule. It executes, rather than replaces, the submitted body. It is intentionally a direct entry harness instead of general Python function-object/call semantics. Sound for this exact program and invocation model. |
| R2 | `semantic.k:50-51` | `Return(E)` becomes `finish(eval(E,RHO))`, reading the current environment. | Return operational rule. The used expression is pure, so functional evaluation does not lose state or exceptional effects on the intended integer-list domain. |
| R3 | `semantic.k:53-54` | `finish(V)` empties `<k>` and writes `V` over `noResult`. | Return completion. Preserves args/env and writes only the result cell; sound. |
| R4 | `semantic.k:57` | `eval(Name(X),(X |-> V) REST) => V`. | Environment lookup. K maps have unique keys, so the matching binding is unambiguous. |
| R5 | `semantic.k:58-59` | `eval(Call(Name("sorted"),E),RHO) => sortedVal(eval(E,RHO))`. | Built-in `sorted` semantics for the fixed unshadowed call. Exact solution defines no `sorted` binding; on integer lists the helper below is faithful. |
| R6 | `semantic.k:60-61` | `eval(Call(Name("len"),E),RHO) => lengthVal(eval(E,RHO))`. | Built-in list length for the fixed unshadowed call; faithful on represented lists. |
| R7 | `semantic.k:62-63` | `eval(BinOp("-",LEFT,RIGHT),RHO) => subtractVal(eval(LEFT,RHO),eval(RIGHT,RHO))`. | Integer subtraction. Operand order is not operationally observable here because both operands are pure. |
| R8 | `semantic.k:64-65` | `eval(Subscript(BASE,Slice(START,NoBound,NoBound)),RHO) => suffixVal(eval(BASE,RHO),eval(START,RHO))`. | Models the only used slice `[START:]`. The claim ensures `START = size(L)-K` lies in `[0,size(L)]` for intended inputs, exactly the covered suffix behavior. |
| R9 | `semantic.k:71` | `sortedVal(listVal(L)) => listVal(sortInts(L))`. | Truthful typed wrapper. |
| R10 | `semantic.k:72` | `lengthVal(listVal(L)) => intVal(size(L))`. | Uses trusted K finite-list `size`; truthful. |
| R11 | `semantic.k:73` | `subtractVal(intVal(I),intVal(J)) => intVal(I -Int J)`. | Uses trusted mathematical integer subtraction; truthful. |
| R12 | `semantic.k:74` | `suffixVal(listVal(L),intVal(N)) => listVal(dropInts(N,L))`. | Truthful wrapper for in-range nonnegative `N`, the only reachable intended case. |
| R13 | `semantic.k:79` | `sortInts(.List) => .List`. | Insertion-sort base; truthful. |
| R14 | `semantic.k:80-81` | `sortInts(ListItem(I) REST) => insertInt(I,sortInts(REST))`. | Structural recursion on a smaller finite integer list. By induction and R15-R17 it yields an ascending permutation. |
| R15 | `semantic.k:83` | `insertInt(I,.List) => ListItem(I)`. | Insertion base; truthful. |
| R16 | `semantic.k:84-86` | Insert `I` before head `J` when `I <=Int J`. | Maintains ascending order and multiset; truthful. |
| R17 | `semantic.k:87-89` | Retain head `J` and recurse when `I >Int J`. | Maintains ascending order and multiset. Its guard is disjoint from and, with R16, exhaustive over K integers. |
| R18 | `semantic.k:91` | `dropInts(0,L) => L`. | Prefix-drop base; truthful. |
| R19 | `semantic.k:92-94` | For `N > 0`, consume an integer head and recurse with `N-1`. | Structural descent; truthful for `0 < N <= size(L)`. Deliberately partial for negative/out-of-range/non-integer-list inputs, none of which is used by an intended satisfying entry state. |
| R20 | `verification.k:9-10` | `maximumSpec(L,K) => dropInts(size(L)-K,sortInts(L))`. | Definitional summary, not an operational bridge. For an ascending list of length `n` and `0<=K<=n`, dropping `n-K` leaves a sorted length-`K` suffix; every removed element is no greater than every retained element. This is exactly the maximum-`K` multiset. |
| C1 | `spec.k:6-23` | Exact submitted `Module(...) ~> boot` with two args and empty env/output reaches `.K`, the bound env, and `listVal(maximumSpec(L,K))`, requiring `0<=K<=size(L)`. | Sole positive entry claim. The RHS has no fresh/free result variable and is equality-constraining. Fresh build proves it with exit 0 and `#Top`; the false mutation separately tests discrimination. |

## Used-construct coverage map

Every constructor in the byte-regenerated `solution.mpy` has both a declaration
and a path to behavior:

- `Module`, `FuncDef`, `Params` -> D1-D3 and R1.
- `Return` -> D3 and R2-R3.
- `Subscript` plus `Slice(...,NoBound,NoBound)` -> D4-D5 and R8/R12/R18-R19.
- `Call(Name("sorted"),Name("arr"))` -> D4, R4-R5, R9, R13-R17.
- `Call(Name("len"),Name("arr"))` -> D4, R4, R6, R10.
- `BinOp("-",...,Name("k"))` -> D4, R4, R7, R11.
- String and integer/list/map built-ins -> standard K domains imported from
  `domains.md`, `INT`, `STRING`, `LIST`, `MAP`, and `BOOL`.

No used constructor is handled by a catch-all, fabricated result, opaque term,
or proof-specific operational rewrite.

## Cross-cutting soundness checks

- **Overlap and guards.** Constructor patterns separate all `eval` equations.
  Empty/nonempty list patterns separate sort/insert/drop bases. R16 and R17 are
  disjoint and exhaustive because integer order partitions `I<=J` versus
  `I>J`. R18 and R19 are disjoint. There are no competing priorities.
- **Coverage and descent.** The evaluator is intentionally partial for unused
  AST nodes and types. On finite integer lists satisfying the claim, sort,
  insertion, and drop cover all reachable terms and recurse structurally.
  No symbol is declared total.
- **Binding and calls.** The only bindings are the exact parameters `arr` and
  `k`; name lookup retrieves them. `sorted` and `len` are fixed built-ins in
  the submitted source with no shadowing definition. General Python rebinding
  is outside this minimal semantics.
- **State and allocation.** The generated Python expression has no input
  mutation: `sorted` and slicing create new lists. The K model preserves the
  `arr` environment binding and returns a logical new result. Object identity
  and allocation are omitted but are not observable in the stated result.
- **Control and exceptions.** The direct-entry boot rule, return, and finish
  cover the only control path. Valid integer-list inputs cannot raise from the
  modeled sort, length, subtraction, or in-range slice. No loop/helper claim or
  abrupt control bridge exists.
- **Specification meaning.** R13-R17 are insertion sort by an ordinary
  induction; R18-R19 remove a prefix; R20 therefore denotes the requested
  sorted maximum-`K` list. The K reachability proof itself establishes equality
  with that definitional expression, but does not contain a separate
  machine-checked theorem of the English “maximum” characterization. That is a
  documented intent-bridge limitation, not a false equation.

## Soundness-witness conclusion

No inventoried rule was labeled unsound, so no false-conclusion witness is
asserted. The narrower evidence gaps are: the English maximum characterization
is justified by the induction above rather than a separate K theorem; the
formal claim does not encode the prompt's length/value bounds or an explicit
“every `ListItem` is `Int`” representation predicate; and maximum-length K CLI
tests hit an external parser kill before execution. None makes a false
conclusion provable on the intended finite integer-list domain.
