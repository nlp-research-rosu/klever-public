# Reviewer rule and declaration inventory

This inventory is reconstructed from the immutable candidate sources. “Sound”
below means sound for every use made by the submitted constructor program,
unless a broader scope is stated. Built-in K collections, booleans, and
unbounded integers are imported primitives rather than local rules.

## Local syntax and attributes

| ID | Location | Declaration / constructors | Attributes and audit |
|---|---|---|---|
| D01 | `semantic.k:6` | `Program ::= Module(Stmts)` | Submitted module wrapper; used and covered. |
| D02 | `semantic.k:9` | `Stmts ::= List{Stmt,""}` | Generates empty, singleton, and juxtaposition forms; all are used. |
| D03–D05 | `semantic.k:10-12` | `Stmt ::= FuncDef(...) \| Return(...) \| If(...)` | Exactly the three submitted statement constructors. |
| D06 | `semantic.k:14` | `Params ::= Params(Ids)` | Used for one- and two-argument functions. |
| D07 | `semantic.k:15` | `Ids ::= List{String,","}` | Only arities one and two are semantically bound. |
| D08–D13 | `semantic.k:17-22` | `Expr ::= Int \| Bool \| Name \| BinOp \| Compare \| Call` | Exactly the submitted expression constructors. |
| D14 | `semantic.k:23` | `CmpOp ::= CmpOp(String,Expr)` | Used for `<`, `>`, `==`. |
| D15 | `semantic.k:24` | `Exprs ::= List{Expr,","}` | Submitted calls use arities one and two. |
| D16 | `semantic.k:33` | `Function ::= function(Params,Stmts)` | Internal function closure without a Python frame or globals object. |
| D17–D19 | `semantic.k:35-37` | `KItem ::= #invoke \| #branch \| #finish` | Internal control forms. `#invoke`/`#finish` expose the material no-frame abstraction discussed below. |
| D20–D23 | `semantic.k:39-42` | `Expr ::= #eval \| #lookup \| #bin \| #cmp` | All four are `[function]`, none `[total]`; equations cover all actual calls. |
| D24 | `semantic.k:43` | `Exprs ::= #evalArgs(...)` | `[function]`, not `[total]`; covers actual arities one and two. |
| D25 | `semantic.k:44` | `Map ::= #bind(...)` | `[function]`, not `[total]`; covers actual arities one and two. |
| D26–D27 | `verification.k:9-10` | `Bool ::= noDivisor(Int,Int) \| prime(Int)` | `[function]`, neither `[total]`; algorithmic mathematical summaries. |
| D28–D30 | `verification.k:27-29` | `Function ::= noDivisorFunction() \| isPrimeFunction()`; `Program ::= solutionProgram()` | `[function]`, not `[total]`; exact constructor abbreviations, not oracles. |

There are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
or opaque declarations. The sole local priority is S09 `[priority(40)]`.

## Configuration

`semantic.k:46-52` has only the state exercised by the submission:
`<k>` starts with the parsed `Program` followed by `#invoke("is_prime",
Int($N))`; `<functions>`, `<env>`, and `<result>` start as `.Map`, `.Map`, and
`Bool(false)`. The cells support definitions, current local bindings, and the
observable return value. There is no call-stack/frame cell and no exception
cell. That omission is material for this recursive Python submission.

## Operational and equational rules

| ID | Location | Rule role | Rule-by-rule decision |
|---|---|---|---|
| S01 | `semantic.k:54` | `Module(SS) => SS` | Sound wrapper elimination. |
| S02 | `semantic.k:56` | split nonempty `Stmts` | Sound left-to-right sequencing for the list representation. |
| S03 | `semantic.k:57` | `.Stmts => .K` | Sound empty-block elimination. |
| S04 | `semantic.k:59-60` | install `FuncDef` in map | Sound for the two module-level capture-free definitions; later map update matches later-definition replacement. |
| S05 | `semantic.k:62-64` | invoke by replacing `<env>` and body | Binding/body selection is exact, but materially unsound as Python call semantics in combination with S09: it allocates no Python frame and preserves no caller frame. The concrete witness is `is_prime(1000003)`: the K run returns `Bool(true)`, whereas CPython raises `RecursionError`. |
| S06 | `semantic.k:66-67` | evaluate `If` guard | Sound for pure submitted guards. |
| S07 | `semantic.k:68` | true branch | Sound. |
| S08 | `semantic.k:69` | false branch | Sound. |
| S09 | `semantic.k:73-74` | prioritized tail-call rewrite | Materially unsound for the real Python program because each recursive `no_divisor` call is turned into a constant-space jump. At `N=1000003`, it enables the false normal-return conclusion above instead of the actual `RecursionError`. Priority makes it preempt S10; priority supplies no Python equivalence proof. |
| S10 | `semantic.k:75-76` | non-call `Return` to `#finish` | Correct returned value for this all-tail-position program below the recursion boundary. Globally context-broad because it has no caller-frame distinction; it inherits the invalid no-frame boundary but has no separate wrong-value witness on the submitted program. |
| S11 | `semantic.k:77-78` | finish and write `<result>` | Correct once `#finish` legitimately denotes entry-point completion; the model cannot establish that distinction for general calls. |
| S12 | `semantic.k:80` | map lookup | Sound under K Map uniqueness; every submitted lookup is bound. |
| S13 | `semantic.k:82` | evaluate `Int` | Sound. |
| S14 | `semantic.k:83` | evaluate `Bool` | Sound. |
| S15 | `semantic.k:84` | evaluate `Name` | Sound for the current local environment and used names. |
| S16 | `semantic.k:85-86` | evaluate `BinOp` operands then dispatch | Submitted operands are pure names/literals, so the lack of explicit effectful evaluation contexts is immaterial here. |
| S17 | `semantic.k:87-88` | evaluate comparison operands then dispatch | Sound for pure submitted operands and one comparison operator. |
| S18 | `semantic.k:90` | integer `+` | Sound via K unbounded integer primitive; matches used Python integer addition. |
| S19 | `semantic.k:91` | integer `*` | Sound via K unbounded integer primitive. |
| S20 | `semantic.k:92-93` | integer `%`, nonzero divisor | Sound for actual `D >= 2`; the guard prevents division by zero. |
| S21 | `semantic.k:95` | integer `<` | Sound via K primitive. |
| S22 | `semantic.k:96` | integer `>` | Sound via K primitive. |
| S23 | `semantic.k:97` | integer `==` | Sound via K primitive. |
| S24 | `semantic.k:99` | evaluate singleton arguments | Sound for `is_prime` invocation. |
| S25 | `semantic.k:100-101` | evaluate two arguments | Sound for helper calls; actual argument expressions are pure. |
| S26 | `semantic.k:103` | bind one parameter | Sound for the entry function. |
| S27 | `semantic.k:104-105` | bind two parameters | Sound for the helper. |
| V01 | `verification.k:12-13` | `D*D>N` summary base case | Truthful definition of the finite divisor search on the claim domain. |
| V02 | `verification.k:14-15` | divisor summary base case | Truthful on `N>=2,D>=2`; K’s `dividesInt` is `N %Int D ==Int 0`. |
| V03 | `verification.k:16-17` | advance summary to `D+1` | Truthful, disjoint from V01/V02, and descending toward V01 on the claim domain. |
| V04 | `verification.k:19-20` | `prime(N)=false` below 2 | Truthful for the integer source domain. |
| V05 | `verification.k:21-22` | `prime(N)=noDivisor(N,2)` at/above 2 | Standard trial-division characterization; guards are disjoint and cover all integers. The connection to the human word “prime” uses the ordinary divisor-below-square-root theorem, not a separate K theorem. |
| V06 | `verification.k:31-43` | `noDivisorFunction()` abbreviation | Exact submitted helper binding/body. |
| V07 | `verification.k:45-53` | `isPrimeFunction()` abbreviation | Exact submitted entry binding/body. |
| V08 | `verification.k:55-73` | `solutionProgram()` abbreviation | Exact submitted module after normalizing explicit `.Stmts` units to the external parser’s omitted empty blocks; mechanical KORE hashes match. |

V01–V08 are ordinary function equations in the compiled verification
definition. They do not replace any `Module`, `If`, arithmetic, call, or return
term during the target execution. V06–V08 supply exact terms in the claim
source and function map.

## Claims

| ID | Location | Plain-language statement and decision |
|---|---|---|
| C01 | `spec.k:8-16` | For every `N>=2,D>=2`, invoking the exact `no_divisor` binding in any surrounding function map, environment, and initial result consumes the computation and ends with `Bool(noDivisor(N,D))`. This is a valid progressive circularity: every recursive use follows concrete guard evaluation and increments `D`. |
| C02 | `spec.k:19-28` | For every K integer `N`, load the exact submitted module, invoke its exact `is_prime` binding, consume computation, and end with `Bool(prime(N))`. It depends on C01. It is result-constraining and not tautological, but—under the generated no-frame semantics—makes the false normal-return claim for the CPython witness `N=1000003`. |

