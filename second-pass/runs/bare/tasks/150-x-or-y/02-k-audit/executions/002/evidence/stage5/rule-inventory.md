# Exhaustive local K inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no other candidate `.k` helper files. Imports
from K's installed `INT`, `BOOL`, `STRING`, and `MAP` modules are standard
library primitives rather than local proof rules.

## `semantic.k`: syntax and configuration

| Lines | Declaration | Used by `solution.mpy` | Review |
|---|---|---:|---|
| 7 | `Program ::= Module(Stmts)` | yes | Faithful module constructor. |
| 9 | `Stmts ::= List{Stmt, ""}` | yes | Faithful juxtaposed statement list, including empty lists. |
| 10 | `Stmt ::= FuncDef(String, Params(Ids), Stmts)` | yes | Faithful constructor shape for the one module-level function. |
| 11 | `Stmt ::= If(Expr, Stmts, Stmts)` | yes | Faithful constructor shape. |
| 12 | `Stmt ::= While(Expr, Stmts)` | yes | Faithful constructor shape. |
| 13 | `Stmt ::= Assign(Expr, Expr)` | yes | Faithful general syntax; behavior below intentionally supports only the used `Name` target. |
| 14 | `Stmt ::= Return(Expr)` | yes | Faithful constructor shape. |
| 16 | `Ids ::= List{String, ","}` | yes | Used for exactly `("n","x","y")`. |
| 17 | `Expr ::= Int(Int)` | yes | Faithful arbitrary-precision integer literal constructor. |
| 18 | `Expr ::= Name(String)` | yes | Faithful variable reference constructor. |
| 19 | `Expr ::= BinOp(String,Expr,Expr)` | yes | Faithful constructor; rules visibly stop on unused operators. |
| 20 | `Expr ::= Compare(Expr,CmpOps)` | yes | Faithful constructor; behavior supports the used single-comparison case. |
| 21 | `CmpOps ::= List{CmpOp, ","}` | yes | The submitted term always contains exactly one comparison operator. |
| 22 | `CmpOp ::= CmpOp(String,Expr)` | yes | Faithful constructor shape. |
| 28 | `Val ::= intVal(Int) \| boolVal(Bool)` | yes | Internal value representation. |
| 30 | `KItem ::= exec(Stmts)` | yes | Statement-list continuation. |
| 31 | `KItem ::= eval(Expr)` | yes | Expression evaluation marker. |
| 32 | `KItem ::= store(String)` | yes | Assignment continuation. |
| 33 | `KItem ::= binLeft(String,Expr)` | yes | Left-to-right binary evaluation continuation. |
| 34 | `KItem ::= binApply(String,Int)` | yes | Binary application continuation holding the left integer. |
| 35 | `KItem ::= cmpLeft(String,Expr)` | yes | Left-to-right comparison continuation. |
| 36 | `KItem ::= cmpApply(String,Int)` | yes | Comparison application continuation holding the left integer. |
| 37 | `KItem ::= branch(Stmts,Stmts,Stmts)` | yes | Conditional continuation. |
| 38 | `KItem ::= whileBranch(Expr,Stmts,Stmts)` | yes | Stable recurring loop control point. |
| 39 | `KItem ::= doReturn` | yes | Abrupt function-return continuation. |
| 41–49 | `<mpy>` configuration with `k`, `env`, `n`, `x`, `y`, `result` | yes | Exactly the state needed by this closed, call-free integer program. `n/x/y` model the external call arguments; `env` models local bindings; `result` models the returned value. |

No syntax production has `macro`, `alias`, `function`, `total`, `functional`,
`simplification`, `concrete`, `priority`, `anywhere`, or `owise` attributes in
`semantic.k`.

## `semantic.k`: all 25 local operational rules

| # | Lines | Rule | Complete domain / state footprint | Soundness assessment |
|---:|---:|---|---|---|
| S1 | 51–61 | Exact `Module(FuncDef("x_or_y", Params("n","x","y"), BODY))` entry | Requires singleton exact binding/body shape, empty `env`, and integer `n/x/y` cells; writes only `env`, changes `k` to `exec(BODY)` | Sound call-harness bridge for this submitted singleton module. It pins name, arity, argument order, body, and values. It does not skip the body. |
| S2 | 62 | `exec(.Stmts) => .K` | `k` only | Sound empty-list completion. |
| S3 | 63 | `exec(S SS) => S ~> exec(SS)` | `k` only | Sound left-to-right statement sequencing. |
| S4 | 65 | `If(...) => eval(COND) ~> branch(...)` | `k` only | Sound; condition is evaluated before branch selection. |
| S5 | 66 | `While(...) => eval(COND) ~> whileBranch(...)` | `k` only | Sound; exposes a stable loop control point. |
| S6 | 67 | `Assign(Name(A),E) => eval(E) ~> store(A)` | `k` only | Sound for the only used assignment target kind; unsupported targets stop. |
| S7 | 68 | `Return(E) => eval(E) ~> doReturn` | `k` only | Sound evaluation-before-return. |
| S8 | 70–71 | true `branch` | `k` only | Executes the then-list followed by the stored statement-list continuation. |
| S9 | 72–73 | false `branch` | `k` only | Executes the else-list followed by the stored statement-list continuation. |
| S10 | 75–76 | true `whileBranch` | `k` only | Executes body, then reevaluates condition and returns to the same loop-head shape. |
| S11 | 77–78 | false `whileBranch` | `k` only | Exits to the stored loop continuation. |
| S12 | 80–81 | `V ~> store(A)` | Reads `k`; updates `env[A]`; frames remaining `k` | Sound local assignment. K `Map` update overwrites or inserts exactly the named binding. |
| S13 | 83–84 | `V ~> doReturn ~> _REST => .K` | Clears the complete active `k`; requires empty `result`; writes `result=V` | Sound abrupt return for the top-level function-call harness. The program has no caller frame, cleanup, exception handler, or other observable control cell. Concrete branch-return tests exercise the discarded suffix. |
| S14 | 86 | `eval(Int(I)) => intVal(I)` | `k` only | Sound literal evaluation. |
| S15 | 87–88 | `eval(Name(A)) => V` with `A |-> V` in `env` | Reads `env`; rewrites `k` | Sound binding lookup; absent names stop rather than fabricate a value. |
| S16 | 90–91 | begin `BinOp` | `k` only | Sound left operand first. |
| S17 | 92–93 | left integer to `binLeft` | `k` only | Sound right operand second, preserving left integer. |
| S18 | 94 | integer `+` | `k` only | Sound arbitrary-precision integer addition. |
| S19 | 95 | integer `*` | `k` only | Sound arbitrary-precision integer multiplication. |
| S20 | 96–97 | integer `%`, guard right operand nonzero | `k` only | Sound on every reachable use: the divisor begins at 2 and increases. Both operands are positive at every reached `%`, so K and Python remainder agree. Division by zero stops. |
| S21 | 99–100 | begin single `Compare` | `k` only | Sound for the single-comparison terms used by the program; chained comparisons stop. |
| S22 | 101–102 | left integer to `cmpLeft` | `k` only | Sound right operand evaluation, preserving left integer. |
| S23 | 103 | integer `<` | `k` only | Sound. |
| S24 | 104 | integer `<=` | `k` only | Sound. |
| S25 | 105 | integer `==` | `k` only | Sound. |

The rules do not overlap incompatibly at any used control point. `Val`
constructors and helper continuations distinguish phases; true/false branch
rules are disjoint; operator application rules use distinct literal operator
strings; `%` is guarded against zero.

## Construct-to-rule coverage for `solution.mpy`

| Submitted construct / operation | Declaration and behavior |
|---|---|
| `Module`, exact `FuncDef`, `Params` | syntax lines 7, 10, 16; S1 |
| statement lists | syntax line 9; S2–S3 |
| outer and loop-body `If` | syntax line 11; S4, S8–S9 |
| `While` | syntax line 12; S5, S10–S11 |
| `Assign(Name(...), ...)` | syntax line 13; S6, S12 |
| `Return` (early and final) | syntax line 14; S7, S13 |
| `Int` | syntax line 17; S14 |
| `Name` | syntax line 18; S15 |
| `BinOp("*")`, `BinOp("%")`, `BinOp("+")` | syntax line 19; S16–S20 |
| `Compare` / `CmpOp("<")` | lines 20–22; S21–S23 |
| `Compare` / `CmpOp("<=")` | lines 20–22; S21–S22, S24 |
| `Compare` / `CmpOp("==")` | lines 20–22; S21–S22, S25 |

Fresh concrete tests cover: initial-if true and false, zero-iteration and
multi-iteration loops, loop-body return and final return, all three binary
operators, all three comparisons, both branch outcomes, both while outcomes,
both assignments, lookup, and return control.

## `verification.k`: symbols and all 7 equations

| # | Lines | Declaration/rule | Classification and domain | Soundness assessment |
|---:|---:|---|---|---|
| V1 | 8 | `primeFrom(Int,Int) [function]` | Definitional summary; proof uses only `D >= 2` | Not opaque and not totalized. Its value controls the loop postcondition. |
| V2 | 9–10 | `primeFrom(N,D) => true` if `N < D*D` | Equation on all integers satisfying guard | On `D >= 2`, sound: no candidate divisor at or above `D` can be at most `sqrt(N)`. |
| V3 | 11–12 | `primeFrom(N,D) => false` if `D*D <= N` and `N % D == 0` | Equation requires meaningful nonzero modulus; every proof use has `D >= 2` | Sound: `D` is a divisor in the checked interval. |
| V4 | 13–14 | recurse to `D+1` if `D*D <= N` and remainder nonzero | Equation requires meaningful nonzero modulus; every proof use has `D >= 2` | Sound: current `D` is not a divisor, so the remaining interval begins at `D+1`; `D` strictly increases. |
| V5 | 16 | `isPrime(Int) [function]` | Definitional summary over all integer `N` | Not opaque and not totalized. |
| V6 | 17–18 | `isPrime(N) => false` if `N < 2` | Equation over all integers below 2 | Sound under the ordinary integer definition of primality. |
| V7 | 19–20 | `isPrime(N) => primeFrom(N,2)` if `2 <= N` | Equation over all remaining integers | Sound: an integer `N >= 2` is composite iff it has a divisor between 2 and `floor(sqrt(N))`. |
| V8 | 22 | `chooseVal(Bool,Int,Int) [function]` | Pure result selector | Not opaque and not totalized. |
| V9 | 23 | true selector returns `intVal(X)` | All `X,Y:Int` | Sound. |
| V10 | 24 | false selector returns `intVal(Y)` | All `X,Y:Int` | Sound. |

There are three local function declarations and seven local equations (V2–V4,
V6–V7, V9–V10). There are no `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, `[priority]`, `[owise]`, `[anywhere]`, macros, aliases, opaque
symbols, fresh variables, ordinary operational bridges, or task-answer axioms
in `verification.k`.

For `D >= 2`, V2 versus V3/V4 are disjoint (`N < D²` versus `D² <= N`),
and V3 versus V4 are disjoint (`N % D == 0` versus nonzero). They cover every
used call and V4 strictly increases `D` until V2 applies. V6 and V7 partition
all integers. V9 and V10 partition `Bool`.

Narrow evidence gap: the syntax permits direct calls `primeFrom(N,D)` with
`D <= 0`, while the intended “remaining candidate divisors” meaning and the
proof only establish/use `D >= 2`. The function is not marked total, and no
target claim can produce such a call. This is not a false-conclusion witness on
the theorem's intended input domain, so it is not classified as a material
unsoundness; the reusable declaration could have been more tightly sorted or
guarded.

## `spec.k`: all reachability claims

| Module / lines | Claim inventory | Preconditions | Result constraint |
|---|---|---|---|
| `LOOP-SPEC`, 9–43 | One loop-head invariant/circularity | Exact loop-head computation and exact four-binding environment; `D >= 2`; integer `N,X,Y`; empty result | Consumes computation and sets result to `chooseVal(primeFrom(N,D),X,Y)`; final env is existential but result and input cells are constrained. |
| `SPEC`, 49–78 | Universal entry theorem | Exact submitted module term; empty env/result; arbitrary integer `N,X,Y`; no additional `requires` | Consumes computation and sets result to `chooseVal(isPrime(N),X,Y)`. |
| `SPEC`, 80–109 | Prompt example `n=7,x=34,y=12` | Same exact module and empty env/result with fixed cells | Requires `intVal(34)`. |
| `SPEC`, 111–140 | Prompt example `n=15,x=8,y=5` | Same exact module and empty env/result with fixed cells | Requires `intVal(5)`. |

No claim has a free/unconstrained result, tautological destination, implication-
only substitute, omitted program body, or framed observable cell. The
existential final environment does not weaken the returned-value property.
