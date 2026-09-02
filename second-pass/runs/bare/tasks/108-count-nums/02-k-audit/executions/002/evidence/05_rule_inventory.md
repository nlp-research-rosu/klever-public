# Exhaustive local K inventory and assessment

Line references are to the immutable candidate. `Used` means exercised by
`solution.mpy`; “model-sound” means sound for the idealized, unbounded
integer/list machine represented by the configuration. This inventory does not
inventory imported K domain rules.

## Syntax and configuration

| ID | Location | Declaration(s) | Used and assessment |
|---|---|---|---|
| S01-S08 | `semantic.k:8-15` | Empty sort declarations `Program`, `Stmt`, `Stmts`, `Expr`, `Params`, `Cmp`, `Index`, `Bound` | All except only the unused generality of some alternatives are needed as constructor-tree sorts; sound. |
| S09 | `semantic.k:17` | `Module(Stmts) : Program`, symbol `Module` | Used; exact translator constructor. |
| S10-S11 | `semantic.k:19-20` | `Stmt < Stmts`; `Stmt Stmts : Stmts`, symbol `StmtsCons` | Used for the two top-level functions; sound constructor representation. |
| S12 | `semantic.k:22` | `Params(String)` | Used for one-argument functions. |
| S13-S15 | `semantic.k:24-27` | `FuncDef`, `If`, `Return` | All used. |
| S16-S23 | `semantic.k:29-36` | `Int`, `Name`, `ListExpr`, `UnaryOp`, `BinOp`, `Compare`, `Call`, `Subscript` | All used. |
| S24 | `semantic.k:38` | `CmpOp` | Used for `<`, `>`, `==`. |
| S25-S26 | `semantic.k:39-40` | `Expr < Index`; `Slice` | Both used (`Int(0)` and `[1:]`). |
| S27-S28 | `semantic.k:41-42` | `Expr < Bound`; `NoBound` | Used by `Slice(Int(1), NoBound, NoBound)`. |
| S29-S30 | `semantic.k:44-45` | Empty value sorts `Value`, `VList` | Used. |
| S31-S33 | `semantic.k:46-48` | `IntV`, `BoolV`, `ListV` | All used. |
| S34-S35 | `semantic.k:49-50` | `VNil`, `VCons(Int,VList)` | Used; represents every finite integer list. |
| S36-S41 | `semantic.k:52-57` | Six `list` macros, arities zero through five | Test-only input sugar; truthful but not the formal-domain bound. |
| S42-S45 | `semantic.k:78-81` | Sorts and constructors `Function/function`, `Frame/frame` | Used for function bindings and caller environments. |
| S46-S57 | `semantic.k:83-94` | KItems `invoke`, `finishK`, `callK`, `returnK`, `ifK`, `unaryK`, `binLeftK`, `binRightK`, `compareLeftK`, `compareRightK`, `subscriptK`, `indexK` | All are used control markers; no opaque KItem. |
| CFG | `semantic.k:96-102` | `<mpy>` with `<k>`, `<funs>`, `<env>`, `<stack>` | State components are all read or written. `$PGM` is a `Program`; `$ARG` is a `Value`. Crucially, `<stack>` is an unbounded mathematical K `List` and has no CPython recursion-limit state. |
| VS01-VS04 | `verification.k:9-10,44,50` | Macros `digitBody`, `countBody`, `solutionProgram`, `solutionFuns` | Compile-time naming only. Fresh `kast --expand-macros` proves `solutionProgram` is constructor-identical to submitted `solution.mpy`. |
| VS05 | `verification.k:58-59` | `signedDigitSum(Int) : Int [function,total,symbol]` | Definitional summary, not an execution rewrite. |
| VS06 | `verification.k:73-74` | `countPositive(VList) : Int [function,total,symbol]` | Definitional summary, not an execution rewrite. |
| VS07 | `verification.k:75-76` | `boolToInt(Bool) : Int [function,total,symbol,smt-hook ite]` | Definitional Boolean characteristic function; trusted SMT-hook corresponds to its exhaustive equations. |

There are no local `[priority]`, `[simplification]`, `[concrete]`,
`[anywhere]`, or opaque declarations.

## `semantic.k` rules

| ID | Location | Rule role | Assessment |
|---|---|---|---|
| R01-R06 | `59-67` | Expand `list` arities 0..5 to `ListV/VNil/VCons`. | Disjoint, exact, test-only macros. |
| R07 | `104` | Schedule the exact two-statement module. | Exact for submitted two-function module. Does not cover other statement counts, but those are unused. |
| R08 | `106-107` | Install a function binding and consume `FuncDef`. | Exact for the two top-level definitions. |
| R09 | `109` | Turn `invoke(F,V)` into argument value, call, then `finishK`. | Exact for the initial invocation in this model. |
| R10 | `110` | Consume `finishK` after a value. | Exact. |
| R11 | `112-115` | Look up function, replace call by body, bind one parameter, push caller environment. | Binding and state footprint are exact for the submitted calls in the idealized model. Together with R12, it omits CPython's finite recursion limit and resulting `RecursionError`; see witness W1 below. |
| R12 | `117-119` | On `returnK`, restore caller environment and pop frame. | Correct inverse of R11 for modeled normal return; same real-Python exception gap as R11. |
| R13-R15 | `121-123` | Evaluate `If` test, select true/false body. | Disjoint Boolean cases; exact. |
| R16 | `124` | Evaluate return expression then `returnK`. | Exact for the submitted bodies, where every return is terminal in its branch. General multi-statement function bodies are unsupported, but unused. |
| R17 | `126` | Integer literal to `IntV`. | Exact mathematical integer abstraction. |
| R18 | `127-128` | Environment lookup for `Name`. | Exact for unique map binding; every used name is bound. |
| R19 | `129` | Empty list expression to `ListV(VNil)`. | Exact. |
| R20-R21 | `131-132` | Evaluate unary expression; implement unary `-`. | Exact for used operator/type. |
| R22-R23 | `134-135` | Left-to-right binary evaluation. | Exact for used pure operands/calls and preserves recursive-call continuations. |
| R24 | `136` | Integer addition. | Exact. |
| R25 | `137-138` | Integer remainder, nonzero divisor. | Exact on all submitted executions: dividend and divisor are positive in the `%` expression. |
| R26 | `139-140` | Integer division, nonzero divisor. | Exact on all submitted executions: dividend and divisor are positive, so K `/Int` and Python `//` agree. |
| R27-R28 | `142-145` | Left-to-right comparison evaluation. | Exact for used pure operands. |
| R29-R32 | `147-154` | Exhaustive `<` and `>` true/false integer rules. | Guards are pairwise disjoint and exhaustive; exact. |
| R33-R34 | `156-159` | Empty-list equality: empty left vs empty/nonempty saved right. | Exactly covers the only used comparison `arr == []`; disjoint and exhaustive on `VList`. |
| R35 | `161` | Evaluate sole argument then call named function. | Exact binding for submitted closed top-level function map. It participates in unbounded recursion and therefore in witness W1. |
| R36 | `163` | Evaluate subscript base first. | Exact for used base. |
| R37 | `164-165` | Evaluate expression index after list base. | Exact for `arr[0]`. |
| R38 | `166` | Return head for index zero on nonempty list. | Exact and only reached after nonempty guard. |
| R39 | `167-169` | Return tail for exact slice `[1:]` on a nonempty list. | Exact for the only slice used. |

## `verification.k` rules and proof-local extensions

| ID | Location | Class | Domain and assessment |
|---|---|---|---|
| V01 | `12-26` | Macro equation | `digitBody`; exact constructor subtree, mechanically checked. |
| V02 | `28-42` | Macro equation | `countBody`; exact constructor subtree, mechanically checked. |
| V03 | `45-48` | Macro equation | `solutionProgram`; exact whole `solution.mpy` constructor, mechanically checked. |
| V04 | `51-53` | Macro equation | `solutionFuns`; exact map obtained after R07/R08. |
| V05-V07 | `61-71` | Definitional summary | `signedDigitSum`: disjoint guards `N<-9`, `N>9`, and `-9<=N<=9` cover all integers; recursive absolute magnitude decreases; equations implement the prompt's signed leading decimal digit. |
| V08-V09 | `78-79` | Definitional summary | `boolToInt`; the two Boolean constructors are disjoint and exhaustive. |
| V10-V11 | `80-82` | Definitional summary | `countPositive`; disjoint/exhaustive `VNil` and `VCons`, structural descent on finite tail. |

None of V01-V11 is an operational bridge: no verification rule rewrites a
front-of-`<k>` execution term. The result-bearing summaries occur only in
claims/postconditions and have exhaustive equations.

## `spec.k` claims

| ID | Location | Meaning and dependency |
|---|---|---|
| C01 | `8-13` | `digit_sum(N)` returns `signedDigitSum(N)` under `solutionFuns`, preserving arbitrary caller environment, stack, and continuation. Recursive circularity. |
| C02 | `16-21` | Empty `count_nums` helper returns zero. |
| C03 | `24-30` | Positive-head nonempty helper returns `countPositive`; depends on C01 and mutual C02-C04 induction over the tail. |
| C04 | `34-40` | Nonpositive-head nonempty helper returns `countPositive`; same dependencies. |
| C05 | `44-49` | Exact program plus empty invocation returns zero from clean cells. |
| C06 | `51-57` | Exact program plus positive-head nonempty invocation returns `countPositive`; depends on C01-C04. |
| C07 | `59-65` | Exact program plus nonpositive-head nonempty invocation returns `countPositive`; depends on C01-C04. |

The mutually required helper set C01-C04 and each entry with that set were
rerun by label and each closed with `#Top`. Isolated C03/C04 or C06/C07 are not
standalone lemmas because their explicit dependencies are omitted.

## False-conclusion witness W1

The prompt admits lists of integers without a size or digit bound. In the
audited CPython 3.10 runtime:

* `arr = [1] * 1200`: trusted canonical returns `1200`; submitted
  `solution.py` raises `RecursionError`.
* `arr = [10**1199]`: trusted canonical returns `1`; submitted `solution.py`
  raises `RecursionError`.

Fresh LLVM execution of R11/R12/R35 on the exact translated program instead
returns `IntV(1200)` and `IntV(1)`. Thus the generated semantics fabricates
normal returns on actual exceptional executions. This is a material real-program
soundness failure, not merely missing coverage for an unused construct.
