# Reviewer rule and declaration inventory

Line numbers refer to the clean scratch copies, which are byte copies of the
candidate sources. The numbered source record is `17_numbered_sources.log`.

## `semantic.k`: local declarations

| Lines | Declaration | Attributes / role | Audit judgment |
|---|---|---|---|
| 1–25 | `MPY-SYNTAX` importing integer, Boolean, and string syntax | Syntax module | The submitted term uses only the declared subset. |
| 6 | `Program ::= Module(Stmts)` | Constructor syntax | Used by `solution.mpy`; faithful to the translator output. |
| 9 | `Stmts ::= List{Stmt, ""}` | Empty-separated list | Used for function bodies, branches, and module statements. |
| 10–12 | `Stmt ::= FuncDef \| Return \| If` | Constructor syntax | Exactly the three statement forms used. |
| 14–15 | `Params`, `Ids` | Comma-separated parameter strings | One- and two-parameter forms are used. |
| 17–22 | `Expr ::= Int \| Bool \| Name \| BinOp \| Compare \| Call` | Constructor syntax | Exactly the expression constructors used. |
| 23–24 | `CmpOp`, `Exprs` | Comparison pair and comma-separated arguments | Used by every comparison and call. |
| 27–32 | `SEMANTIC` imports syntax, map, integer, and Boolean domains | Semantic module | The imported K primitives form part of the trust boundary. |
| 33 | `Function ::= function(Params, Stmts)` | Runtime function value | Stores exact submitted parameters and bodies. |
| 35–37 | `KItem ::= #invoke \| #branch \| #finish` | Internal control terms | Sufficient for this tail-call-only program. |
| 39–42 | `Expr ::= #eval \| #lookup \| #bin \| #cmp` | All four marked `[function]`; none `[total]` | Each used ground case is covered. Unused types/operators stop rather than fabricate. |
| 43 | `Exprs ::= #evalArgs` | `[function]`, not total | Only arities one and two are covered and those are the only used arities. |
| 44 | `Map ::= #bind` | `[function]`, not total | Only one/two parameters are covered and those are the only used arities. |
| 46–52 | `<py>` configuration with `<k>`, `<functions>`, `<env>`, `<result>` | Entry appends `#invoke("is_prime", Int($N))`; `$N: Int` | Pins the formal input to all K integers. State is sufficient for the modeled pure program but has no Python call-stack/recursion-depth component. |

There are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
or opaque declarations. There is one priority attribute, inventoried below.

## `semantic.k`: every local rule

| Line(s) | Rule | Reads / writes and control | Audit judgment |
|---|---|---|---|
| 54 | `Module(SS) => SS` | Replaces the module at the front of `<k>`; frames continuation | Faithfully starts the translated statement list. |
| 56 | `(S SS) => S ~> SS` | Orders statement execution left-to-right | Faithful for all submitted blocks. |
| 57 | `.Stmts => .K` | Removes an empty block | Faithful list termination. |
| 59–60 | `FuncDef` | Removes declaration; updates `<functions>[F <- function(P,B)]` | Faithful for the two unique top-level definitions. |
| 62–65 | `#invoke` | Reads selected function; replaces `<env>` with parameter binding; starts body | Binding/body/arguments are exact for the submitted calls. Environment restoration and a call stack are omitted; all actual calls are syntactic tail returns, so restoration is not observably needed for the submitted cases. |
| 66–67 | `If` | Reads `<env>` and evaluates its guard into `#branch` | Guard expressions are pure, so eager functional evaluation preserves order observably. |
| 68 | true `#branch` | Selects then-block | Correct. |
| 69 | false `#branch` | Selects else-block | Correct. |
| 73–74 | `Return(Call(Name(F),ES)) ~> _ => #invoke(...)` | Reads `<env>`, evaluates arguments, discards the entire continuation; `[priority(40)]` | Correct branch/value behavior for each submitted syntactic tail call, and priority properly preempts the general return rule. **Materially unfaithful to the real CPython program over the formal all-`Int` domain:** it is an unbounded stack-free tail jump, whereas CPython allocates recursive frames and raises `RecursionError`. Witnesses `N=1000003` and `N=1022117` satisfy the entry domain; real `solution.py` raises, while this rule chain reaches `Bool(true)` and `Bool(false)`, respectively (`15_differential_with_recursion_boundary.log`, `16_k_recursion_gap.log`). |
| 75–76 | `Return(E) ~> _ => #finish(#eval(...))` | Reads `<env>` and discards remaining function-block computation | Correct for submitted Boolean returns. It overlaps the tail-call return syntactically, but priority 40 selects the specialized rule. |
| 77–78 | `#finish(V)` | Empties `<k>` and writes `<result>` | Correct for the modeled top-level/tail-call execution. |
| 80 | `#lookup(X, X |-> V REST) => V` | Reads a map | Correct; every used name is present in its exact binding. |
| 82 | `#eval(Int(I),_) => Int(I)` | Pure literal evaluation | Correct. |
| 83 | `#eval(Bool(B),_) => Bool(B)` | Pure literal evaluation | Correct. |
| 84 | `#eval(Name(X),RHO) => #lookup(X,RHO)` | Pure local lookup | Correct for `n` and `d`. Function-position names are handled by the specialized tail-call rule rather than this rule; the submitted names select exact top-level bindings. |
| 85–86 | `#eval(BinOp(OP,L,R),RHO)` | Evaluates both pure operands and dispatches | Submitted operands have no effects/exceptions, so the lack of an explicit sequencing continuation is harmless here. |
| 87–88 | `#eval(Compare(...))` | Evaluates both pure operands and dispatches | Correct for every submitted single comparison. |
| 90 | `#bin("+",Int(I),Int(J))` | K arbitrary-precision addition | Matches Python integers on used inputs. |
| 91 | `#bin("*",Int(I),Int(J))` | K arbitrary-precision multiplication | Matches Python integers. |
| 92–93 | `#bin("%",Int(I),Int(J))` if `J != 0` | K truncating remainder | Every actual divisor has `J>=2`; on that domain this matches Python remainder. Division by zero visibly stops and is unreachable in the submitted flow. |
| 95 | `#cmp("<",...)` | Integer less-than | Correct. |
| 96 | `#cmp(">",...)` | Integer greater-than | Correct. |
| 97 | `#cmp("==",...)` | Integer equality | Correct. |
| 99 | one-argument `#evalArgs` | Evaluates one pure argument | Used only indirectly by the one-parameter binder at the initial invocation, which is supplied directly; rule is truthful. |
| 100–101 | two-argument `#evalArgs` | Evaluates the two pure arguments | Used by helper tail calls; value is correct. |
| 103 | one-parameter `#bind` | Creates one map entry | Correct for `is_prime`. |
| 104–105 | two-parameter `#bind` | Creates two map entries | Correct for `no_divisor`; parameter names are distinct. |

The only local priority is `[priority(40)]` on the specialized return-call rule.
It resolves its overlap with the default-priority general-return rule in favor
of the call rule. There are no local semantic simplification rules.

## `verification.k`: every local declaration and rule

| Lines | Extension | Class / domain | Audit judgment |
|---|---|---|---|
| 9–10 | `noDivisor(Int,Int)`, `prime(Int)` | `[function]`, not total; result-bearing definitional summaries | No opaque value is introduced. The equations below determine every use. |
| 12–13 | `noDivisor(N,D) => true` if `D*D>N` | Definitional equation | True characterization of an exhausted divisor search from positive `D`. Helper uses `N,D>=2`. |
| 14–15 | `noDivisor(N,D) => false` if `D*D<=N` and `D dividesInt N` | Definitional equation | Matches the program's positive-divisor remainder test. K defines `D dividesInt N` as `(N %Int D)==0`; see `18_builtin_integer_contract.log`. |
| 16–17 | recurse at `D+1` if within bound and nondividing | Definitional equation | Truthful, strictly increasing on the helper domain, disjoint from the other two guards. |
| 19–20 | `prime(N)=>false` if `N<2` | Definitional equation | Matches source and ordinary primality convention. |
| 21–22 | `prime(N)=>noDivisor(N,2)` if `N>=2` | Definitional equation | Guards are exhaustive/disjoint; the mathematical bridge to primality is the standard finite-divisor argument, but is not separately proved in K. |
| 27–29 | `noDivisorFunction`, `isPrimeFunction`, `solutionProgram` | `[function]`, not total; definitional names | These name concrete syntax and do not replace execution. |
| 31–43 | equation for `noDivisorFunction()` | Exact submitted helper term | Byte-translated source and submitted MPY agree; body is executed by fixed local rules. |
| 45–53 | equation for `isPrimeFunction()` | Exact submitted entry term | Same. |
| 55–73 | equation for `solutionProgram()` | Exact submitted whole-program term | Static constructor-by-constructor match with `solution.mpy`; it expands before operational execution. |

The three guards of `noDivisor` are pairwise disjoint and exhaustive because
integer order partitions `D*D>N` from `D*D<=N`, and Boolean divisibility
partitions the latter. The two `prime` guards are disjoint and exhaustive.
There are no ordinary operational bridges, priority rules, simplification
rules, `[total]`, `[functional]`, `[concrete]`, or opaque symbols in
`verification.k`.

## `spec.k`: claims

| Lines | Claim | Plain-language contract and judgment |
|---|---|---|
| 8–16 | `helper-correct` | For every K integer `N>=2,D>=2`, invoking the exact stored helper from any environment/result terminates in the modeled semantics with result `Bool(noDivisor(N,D))`; final environment is existential. It is a real recursive circularity and closes alone. |
| 19–28 | `is-prime-correct` | For every K integer `N`, expand the exact submitted program, invoke `is_prime(N)`, consume `<k>`, install the exact two functions, and change the initial result to `Bool(prime(N))`; final environment is existential. It constrains the returned Boolean and depends on the helper circularity. The proof set closes, but the all-integer result is not a theorem about real CPython because of the recursion witness. |

## Construct-to-rule coverage for `solution.mpy`

| Used construct | Declaration | Operational coverage |
|---|---|---|
| `Module` | `semantic.k:6` | rule 54 |
| juxtaposed statement blocks / empty blocks | 9 | rules 56–57 |
| `FuncDef` | 10 | rules 59–60 |
| `If` | 12 | rules 66–69 |
| `Return` | 11 | rules 73–78 |
| `Int`, `Bool`, `Name` | 17–19 | rules 80, 82–84 |
| `BinOp` for `+`, `*`, `%` | 20 | rules 85–86, 90–93 |
| `Compare` / `CmpOp` for `<`, `>`, `==` | 21, 23 | rules 87–88, 95–97 |
| `Call(Name(...),...)` with two arguments | 22, 24 | specialized rule 73–74, rules 100–101, 104–105 |
| parameter lists of arity one and two | 14–15 | rules 103–105 |

Every submitted constructor is declared and has a reachable rule path. No rule
fabricates an unconstrained result or encodes a task answer. The disqualifying
issue is instead a concrete semantic mismatch: the modeled recursive control
transition eliminates the real Python stack and exception behavior over inputs
that the universal formal claim includes.
