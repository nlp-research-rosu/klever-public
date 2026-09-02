# Exhaustive local K inventory and soundness decisions

This inventory covers the submitted `semantic.k`, `verification.k`, and
`spec.k`. There are no generated helper K files besides these. Imports from the
K distribution are treated as the named low-level trust boundary, not as local
rules.

## Syntax and configuration

| ID | Location | Declaration | Use and decision |
|---|---|---|---|
| S1 | `semantic.k:7` | `Pgm ::= Module(Function)` with `symbol(moduleAst)` | Represents the translated module. Declarative only; exact submitted root constructor is covered. |
| S2 | `semantic.k:8` | `Function ::= FuncDef(String, Params, Stmt)` with `symbol(funcDefAst)` | Represents the one submitted function. Declarative only. |
| S3 | `semantic.k:9` | `Params ::= Params(String)` with `symbol(paramsAst)` | Represents the sole formal parameter. Declarative only. |
| S4 | `semantic.k:10` | `Stmt ::= Return(Expr)` with `symbol(returnAst)` | Covers the submitted sole statement. Declarative only. |
| S5 | `semantic.k:12` | `Expr ::= Name(String)` with `symbol(nameAst)` | Covers all submitted `Name` nodes. Declarative only. |
| S6 | `semantic.k:13` | `Expr ::= Int(Int)` with `symbol(intAst)` | Covers the submitted threshold literal. Declarative only. |
| S7 | `semantic.k:14` | `Expr ::= ListComp(Expr, CompFor)` with `symbol(listCompAst)` | Covers the submitted comprehension. Declarative only. |
| S8 | `semantic.k:15` | `Expr ::= Compare(Expr, CmpOp)` with `symbol(compareAst)` | Covers the submitted comparison. Declarative only. |
| S9 | `semantic.k:16` | `CompFor ::= CompFor(Expr, Expr, Expr)` with `symbol(compForAst)` | Covers the sole generator and filter. Declarative only. |
| S10 | `semantic.k:17` | `CmpOp ::= CmpOp(String, Expr)` with `symbol(cmpOpAst)` | Covers the submitted `>` comparison. Declarative only. |
| S11 | `semantic.k:20` | `PyList ::= nil` with `symbol(nil), constructor` | Free empty integer-list constructor; sound but restricts the modeled source domain. |
| S12 | `semantic.k:21` | `PyList ::= cons(Int, PyList)` with `symbol(cons), constructor` | Free integer-list constructor; arbitrary finite length, order, and duplicates are represented. Floats and other terminating Python numeric inputs are not. |
| C1 | `semantic.k:29-33` | `<py><k>$PGM:Pgm</k><input>$INPUT:PyList</input></py>` | Explicit entry-harness configuration. It has no heap, output, exception, or call stack; none is needed for the exact pure integer-list program, but this is not a general Python module configuration. |
| S13 | `semantic.k:36` | `KItem ::= eval(Expr, Map)` with `symbol(eval)` | Internal evaluation form. Not a function, total symbol, or opaque oracle. |
| S14 | `semantic.k:42` | `PyList ::= asList(KItem)` with `function, symbol(asList)` | Partial typed projection. No `total` declaration. Its sole actual use receives a `PyList`. |
| S15 | `semantic.k:56` | `PyList ::= filterGt(PyList, Int)` with `function, symbol(filterGt)` | Result-bearing recursive summary. No `total` declaration, but R4-R6 exhaust its declared `PyList × Int` domain. |

There are no local `total`, `functional`, `simplification`, `concrete`,
`owise`, `priority`, or opaque-symbol declarations. The `symbol` attributes
give stable K labels and do not assert semantic truth.

## Ordinary semantic and functional rules

| ID | Location | Complete local match/guard and footprint | Classification and decision |
|---|---|---|---|
| R1 | `semantic.k:37-39` | At the front of `<k>`, matches `Module(FuncDef("get_positive", Params(P), Return(E)))`; reads unchanged `<input>L`; rewrites to `eval(E, P \|-> L)` and preserves the arbitrary `<k>` suffix. No guard. | Entry-harness operational bridge. It selects the named binding, binds the sole formal to the supplied `PyList`, retains the body rather than replacing it, preserves all modeled state and continuation, and is sound for the candidate harness. It is not literal Python module-import behavior; the external convention that running the module invokes the requested entry point is trusted. |
| R2 | `semantic.k:43` | `asList(L:PyList) => L`; no cell or guard. | Definitional typed projection. True on its entire match domain. Deliberately stuck on other `KItem`s; it is not marked total. |
| R3 | `semantic.k:47-52` | At the front of `<k>`, matches exactly `eval(ListComp(Name(X), CompFor(Name(X), Name(P), Compare(Name(X), CmpOp(">", Int(N))))), RHO)`; rewrites to `filterGt(asList(RHO[P]), N)` and preserves the arbitrary suffix. No cells change. | Result-bearing operational summary of the exact one-generator comprehension form. Repeated `X` enforces that element, target, and predicate refer to the same bound name; `P` selects the iterable binding. For finite integer lists, pure integer lookup/comparison has no omitted side effect or exception, and stable `filterGt` is the correct value. This rule is task-shaped and has no bridge-free K theorem against an independently fixed Python semantics; it is therefore an explicit empirical/informal semantics trust boundary, supported by transparent equations, body sensitivity, continuation testing, and 64 K/Python comparisons. No false conclusion witness exists on its declared integer-list match domain, so it is not classified as unsound. |
| R4 | `semantic.k:57` | `filterGt(nil, _N) => nil`; all integer thresholds. | Truthful base equation. |
| R5 | `semantic.k:58-59` | `filterGt(cons(I, IS), N) => cons(I, filterGt(IS,N))` when `I >Int N`. | Truthful retain-head equation. It descends structurally to `IS`. |
| R6 | `semantic.k:60-61` | `filterGt(cons(I, IS), N) => filterGt(IS,N)` when `I <=Int N`. | Truthful discard-head equation. It descends structurally to `IS`. |

R4 is disjoint from R5/R6 by constructor freeness. R5 and R6 are disjoint and
jointly exhaustive because K mathematical integers are totally ordered. Both
recursive rules strictly shorten the free list. R1, R2, and R3 have distinct
heads. There are no local priority interactions.

## Verification claims and target claims

`verification.k` declares no syntax, function, ordinary rule, priority rule,
or simplification rule. It contains three reachability claims:

| ID | Location | Precondition and postcondition | Decision |
|---|---|---|---|
| V1 | `verification.k:8-18` | Any `cons(I,REST)` integer list with `I > 0`; exact submitted program reaches `cons(I, filterGt(REST,0))`. | Sound one-head execution fact; freshly proved alone. |
| V2 | `verification.k:20-30` | Any `cons(I,REST)` integer list with `I <= 0`; exact submitted program reaches `filterGt(REST,0)`. | Sound one-head execution fact; freshly proved alone. |
| V3 | `verification.k:32-41` | Empty integer list; exact submitted program reaches `nil`. | Sound empty execution fact; freshly proved alone. |

`spec.k` likewise declares no syntax, functions, or rules. Its five entry
claims are:

| ID | Location | Precondition and postcondition | Decision |
|---|---|---|---|
| P1 | `spec.k:8-17` | Any finite `PyList` of K `Int`; exact submitted program reaches `filterGt(INPUT,0)`. | Result-constraining universal integer-list theorem; freshly proved alone. The RHS shares the input and is not free. |
| P2 | `spec.k:20-29` | First documented ground example; reaches `[2,5,6]`. | Sound ground instance; freshly proved alone. |
| P3 | `spec.k:31-40` | Second documented ground example; reaches `[5,3,2,3,9,123,1]`. | Sound ground instance; freshly proved alone. |
| P4 | `spec.k:42-51` | Empty ground input; reaches `nil`. | Sound boundary instance; freshly proved alone. |
| P5 | `spec.k:53-62` | Ground `[0,-1,-2]`; reaches `nil`. | Sound branch-boundary instance; freshly proved alone. |

The eight claim LHS program terms mechanically equal the trusted regenerated
`solution.mpy`. They are proof obligations, not local axiomatic rewrites in the
compiled `proof-kompiled` definition. Their individually selected invocations
all printed `#Top`.

## Construct coverage map

| Submitted constructor | Declaration | Behavior |
|---|---|---|
| `Module` | S1 | R1 |
| `FuncDef` | S2 | R1 exact `get_positive` selection and formal binding |
| `Params` | S3 | R1 |
| `Return` | S4 | R1 exposes its expression to `eval` |
| `ListComp` | S7 | R3 |
| `Name` | S5 | R3 binds one repeated target/element/predicate name and looks up the iterable name |
| `CompFor` | S9 | R3 |
| `Compare` | S8 | R3 |
| `CmpOp(">")` | S10 | R3 and R5/R6 using trusted K `>Int`/`<=Int` |
| `Int(0)` | S6 plus imported `INT` | R3 passes the threshold to R4-R6 |

Every constructor in the trusted regenerated program is declared and occurs in
the match of R1 or R3. Missing semantics for other translator constructors is
unused and is not counted as a defect in `GENERATED_SEMANTICS` mode.
