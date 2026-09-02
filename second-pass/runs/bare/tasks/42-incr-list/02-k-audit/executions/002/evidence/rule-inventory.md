# Exhaustive local declaration and rule inventory

This inventory covers every local declaration and rule in the immutable
candidate sources `semantic.k`, `verification.k`, and `spec.k`. Imported
built-ins are listed separately as trust boundaries.

## `semantic.k`: syntax and configuration

`MPY-SYNTAX` imports `INT-SYNTAX` and `STRING-SYNTAX` and declares:

1. `Program ::= Module(Stmts)`.
2. `Stmts ::= List{Stmt, ""}` (including generated empty/list-unit syntax).
3. `Params ::= Params(Strings)`.
4. `Strings ::= List{String, ","}`.
5. `Stmt ::= FuncDef(String, Params, Stmts)`.
6. `Stmt ::= Assign(Exp, Exp)`.
7. `Stmt ::= For(Exp, Exp, Stmts)`.
8. `Stmt ::= Return(Exp)`.
9. `Exp ::= Name(String)`.
10. `Exp ::= Int(Int)`.
11. `Exp ::= ListExpr(Exps)`.
12. `Exp ::= BinOp(String, Exp, Exp)`.
13. `Exps ::= List{Exp, ","}`.

`MPY` imports that syntax plus built-in `INT`, `LIST`, and `MAP`. It declares:

1. `PyVal ::= pyInt(Int)`.
2. `PyVal ::= pyList(List)`.
3. `PyVal ::= #incPrefix(List, Int) [function, total]`.
4. `Result ::= noResult | result(PyVal)`.
5. `IterVal ::= noIter | iter(String, PyVal)`.
6. `KItem ::= #init(Program, PyVal)`.
7. `KItem ::= #exec(Stmts)`.
8. `KItem ::= #for(List, Int, String, Stmts)`.
9. `KItem ::= #bind(String, PyVal)`.
10. `KItem ::= #return(PyVal)`.
11. `PyVal ::= #eval(Exp, Map, IterVal) [function, total]`.
12. `PyVal ::= #add(PyVal, PyVal) [function, total]`.
13. `PyVal ::= #at(List, Int) [function, total]`.
14. `List ::= #evalExps(Exps, Map, IterVal) [function, total]`.
15. `List ::= #asList(PyVal) [function]`.

There are no locally declared macros, aliases, priorities, or `functional`
attributes. The configuration contains exactly `<k>`, `<env>`, `<iter>`, and
`<result>` inside `<mpy>`. The initial term is
`#init($PGM:Program,$ARGS:PyVal)` with empty environment, `noIter`, and
`noResult`. Every cell is read or written by at least one used rule.

The `[total]` declarations are not established by exhaustive equations:
`#incPrefix` only reduces at index zero; `#eval` omits missing names and
unsupported operators; `#add` omits mixed values; and `#at` omits negative and
out-of-bounds indices. Those gaps do not occur during ordinary concrete
execution of this integer-list program, but they do occur in the submitted
symbolic theorem because its `L:List` precondition does not constrain elements.

## `semantic.k`: 23 rules

| ID | Lines | Rule | Static assessment |
|---|---:|---|---|
| S1 | 56-58 | Exact `#init` for `incr_list(l)` installs `l` and executes the captured body. | Sound and target-specific. |
| S2 | 60 | Empty `#exec` becomes `.K`. | Sound. |
| S3 | 62-64 | Assignment evaluates the RHS in the old environment, then updates the named binding. | Sound for pure supported expressions. |
| S4 | 66-69 | `for X in E` evaluates `E` once, converts it to a list, and starts at index zero before the remaining statements. | Sound for the target's `pyList` iterable. |
| S5 | 71-73 | `Return(E)` discards remaining statements and starts `#return` with the evaluated value. | Sound for target-level return. |
| S6 | 75-78 | If `I < size(L)`, bind item `I`, execute the body, and increment `I`. | Sound; sequencing matches the submitted loop. |
| S7 | 80-81 | If `I >= size(L)`, finish the loop. | Sound; disjoint from S6 and exhaustive for integer indices. |
| S8 | 83-84 | `#bind` writes the loop binding into `<iter>`. | Target-adequate, though not a reusable Python scope model. |
| S9 | 86-87 | `#return(V)` discards a continuation and writes `result(V)` when the result cell was empty. | Sound for the only reachable top-level return; broader than the target context. |
| S10 | 97 | A name equal to the `<iter>` name reads the iterator value. | Sound on target-reachable states. |
| S11 | 98 | A name in the map reads the map value. | Sound on target-reachable states. S10/S11 overlap with different RHSs if the same name occurs in both stores, but the submitted control flow never inserts `"value"` in `<env>` or `"result"` in `<iter>`. |
| S12 | 99 | Integer expression becomes `pyInt`. | Sound. |
| S13 | 100 | List expression evaluates elements and wraps `pyList`. | Sound for pure expressions. |
| S14 | 101-102 | `BinOp("+",...)` evaluates both expressions and applies `#add`. | Sound because supported expressions are pure; no source-visible evaluation-order distinction remains. |
| S15 | 104 | Empty expression list becomes `.List`. | Sound. |
| S16 | 105-106 | Nonempty expression list evaluates head then tail. | Sound for the target. |
| S17 | 108 | Integer addition. | Sound, using unbounded mathematical integers as Python's relevant model. |
| S18 | 109 | List concatenation. | Sound for immutable semantic lists. |
| S19 | 110-114 | Special simplification: adding an exact increment singleton to `#incPrefix(L,I)` becomes `#incPrefix(L,I+1)`. | Illegitimate result-bearing operational bridge. It is unguarded, preempts evaluation of nested `#at/#add`, and has no bridge-free universal connection theorem. |
| S20 | 116 | `#asList(pyList(L)) = L`. | Sound. |
| S21 | 117 | Index zero of a nonempty list returns its head. | Sound. |
| S22 | 118-119 | Positive index recursively decrements through the list. | Sound; it visibly sticks out of bounds. |
| S23 | 121 | `#incPrefix(_L,0) = pyList(.List)`. | Truthful base equation, but insufficient to define positive prefixes without S19. |

S19's false-behavior witness uses any nonempty intended integer list and
`I = size(L)`. Python indexing `L[I]` is out of bounds, and S21/S22 leave
`#at(L,size(L))` stuck. Nevertheless S19 rewrites the surrounding symbolic
term to `#incPrefix(L,size(L)+1)`. The machine evidence is:

- `stage5-rule-witness-positive.log`: the fabricated successor claim closes
  with `#Top`;
- `stage5-rule-witness-control.log`: the direct out-of-bounds operation is
  stuck with `WarnStuckClaimState`;
- `stage5-rule-witness-ground.log`: substituting the satisfying intended input
  `L=[pyInt(1)]` exposes competing normalization and does not establish the
  successor.

This is also an overlap at `I=0`: S23 can first reduce the abstract accumulator
to an ordinary empty list, after which S18 produces an ordinary singleton;
S19 can instead replace the outer addition by a positive opaque
`#incPrefix`. No confluence or connection theorem equates those normal forms.

## `verification.k`

Imports are `MPY`, `BOOL`, `K-EQUAL`, and `MAP-SYMBOLIC`. There are no new
syntax declarations or claims and exactly two simplification rules:

| ID | Lines | Rule | Static assessment |
|---|---:|---|---|
| V1 | 13-15 | Equality of `#incPrefix(L,I)` and `#incPrefix(L,J)` is replaced by equality of `I` and `J`. | Injectivity is mathematically true for actual valid prefixes because lengths differ, but here it is an additional axiom about an incompletely defined opaque function and depends on the missing S19 connection. |
| V2 | 17 | `0 <= size(L)` becomes `true`. | Sound ordinary mathematics for a K list. |

There are no priority rules. Both local rules have `[simplification]`.

## `spec.k`

There are no syntax or function declarations and exactly two reachability
claims:

| ID | Lines | Claim | Static assessment |
|---|---:|---|---|
| C1 | 8-33 | `for-invariant`: from index `I`, accumulator `#incPrefix(L,I)`, and `0 <= I <= size(L)`, execute the exact remaining target loop and return; post-state accumulator/result are `#incPrefix(L,size(L))`. | A circular loop summary. It closes only in the theory containing S19 and is not a bridge-free connection theorem for S19. |
| C2 | 36-62 | `incr-list-correct`: execute the exact submitted constructor program on arbitrary `L:List`; post-state result is `#incPrefix(L,size(L))`; depends on C1. | Program term is pinned, but the post-state is a proof-local opaque value rather than the concrete `pyList` result. |

## Used-construct coverage map

| Submitted constructor | Declaration | Execution rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | Program/function syntax | S1 |
| statement list | `Stmts` list syntax | S2-S7 |
| `Assign` | statement syntax | S3 |
| `For` | statement syntax | S4, S6-S8 |
| `Return` | statement syntax | S5, S9 |
| `Name("l")`, `Name("result")`, `Name("value")` | expression syntax | S10-S11 |
| `Int(1)` | expression syntax | S12 |
| `ListExpr` | expression syntax | S13, S15-S16 |
| `BinOp("+",...)` | expression syntax | S14, S17-S19 |
| Python input/output lists | `pyList(List)` | S18, S20-S22 |

Every submitted construct has a concrete rule path. Missing semantics for other
Python constructs is outside the generated-semantics scope and is not a defect.

## Imported trust boundary

The proof trusts K's built-in mathematical `Int`, Boolean operations, K
`List` concatenation/`size`, finite `Map` update/lookup, K sequence, equality,
symbolic map support, reachability circularity, and the Haskell backend. Those
are ordinary low-level boundaries. S19, V1, and `#incPrefix [total]` are local,
task-specific, result-bearing additions and are not part of that acceptable
boundary.
