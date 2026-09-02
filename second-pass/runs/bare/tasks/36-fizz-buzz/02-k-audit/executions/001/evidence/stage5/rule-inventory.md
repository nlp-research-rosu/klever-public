# Exhaustive local declaration and rule inventory

Files audited: `/candidate/semantic.k` and `/candidate/verification.k`. There
are no candidate helper `.k` files beyond these and `spec.k`.

## Imports and configuration

- `semantic.k:1` requires the installed K builtin `domains.md`.
- `MPY-SYNTAX` imports `INT-SYNTAX`, `BOOL-SYNTAX`, and `STRING-SYNTAX`.
- `SEMANTIC` imports `MPY-SYNTAX`, `INT`, `BOOL`, `STRING`, and `MAP`.
- `verification.k` requires `semantic.k`; `VERIFICATION` imports `SEMANTIC`.
- The configuration has wrapper `<fizz>` and exactly four state cells:
  `<k>` (current translated program/computation), `<input>` (integer `N`),
  `<env>` (map of local names to integers), and `<result>` (integer, initially
  zero). There is no heap, call stack, exception, output, or allocation cell.

## Local syntax productions

| ID | Location | Declaration/production | Attributes | Used by submitted program? |
|---|---|---|---|---|
| SYN-01 | semantic.k:8 | `Program ::= Module(Stmts)` | none | yes |
| SYN-02 | semantic.k:10 | `Stmts ::= List{Stmt,""}` | list | yes |
| SYN-03 | semantic.k:11 | `Stmt ::= FuncDef(String,Params(String),Stmts)` | none | yes |
| SYN-04 | semantic.k:12 | `Stmt ::= Assign(Expr,Expr)` | none | yes |
| SYN-05 | semantic.k:13 | `Stmt ::= While(Expr,Stmts)` | none | yes |
| SYN-06 | semantic.k:14 | `Stmt ::= If(Expr,Stmts,Stmts)` | none | yes |
| SYN-07 | semantic.k:15 | `Stmt ::= Return(Expr)` | none | yes |
| SYN-08 | semantic.k:17 | `Expr ::= Name(String)` | none | yes |
| SYN-09 | semantic.k:18 | `Expr ::= Int(Int)` | none | yes |
| SYN-10 | semantic.k:19 | `Expr ::= Bool(Bool)` | none | runtime result only |
| SYN-11 | semantic.k:20 | `Expr ::= BinOp(String,Expr,Expr)` | none | yes (`+`, `%`, `//`) |
| SYN-12 | semantic.k:21 | `Expr ::= Compare(Expr,CmpOp)` | none | yes |
| SYN-13 | semantic.k:22 | `Expr ::= BoolOp(String,Expr,Expr)` | none | yes (`or`) |
| SYN-14 | semantic.k:23 | `CmpOp ::= CmpOp(String,Expr)` | none | yes (`<`, `>`, `==`) |
| KITEM-01 | semantic.k:39 | `assignTo(String)` | none | assignment continuation |
| KITEM-02 | semantic.k:40 | `binLeft(String,Expr)` | none | binary evaluation |
| KITEM-03 | semantic.k:41 | `binRight(String,Int)` | none | binary evaluation |
| KITEM-04 | semantic.k:42 | `compareLeft(String,Expr)` | none | comparison evaluation |
| KITEM-05 | semantic.k:43 | `compareRight(String,Int)` | none | comparison evaluation |
| KITEM-06 | semantic.k:44 | `orElse(Expr)` | none | short-circuit `or` |
| KITEM-07 | semantic.k:45 | `ifThenElse(Stmts,Stmts)` | none | conditional continuation |
| KITEM-08 | semantic.k:46 | `whileBody(Expr,Stmts)` | none | loop continuation |
| KITEM-09 | semantic.k:47 | `returnValue` | literal | return continuation |
| FUN-01 | verification.k:8 | `digitSevens(Int):Int` | `function,total` | yes, specification/invariants |
| FUN-02 | verification.k:9 | `fizzContribution(Int):Int` | `function,total` | yes, specification/invariants |
| FUN-03 | verification.k:10 | `fizzFrom(Int,Int):Int` | `function,total` | yes, final result |
| FUN-04 | verification.k:11 | `fizzEnd(Int):Int` | `function,total` | yes, final `i` |
| MACRO-01 | verification.k:42 | `Stmt ::= INNER-LOOP` | `macro` | exact inner-loop alias |
| MACRO-02 | verification.k:50 | `Stmt ::= OUTER-LOOP` | `macro` | exact outer-loop alias |

There are no local `[functional]` declarations, `[concrete]` declarations,
opaque result symbols, freshness symbols, or priority rules. The four
`[function,total]` symbols above are fully equated below.

## Operational semantic rules

| ID | Location | Rule effect | Guard | Static judgment |
|---|---|---|---|---|
| SEM-01 | semantic.k:52-54 | Exact `Module(FuncDef("fizz_buzz",Params("n"),BODY))` loads `BODY`; binds `n=N` and initializes `count,i,x=0`. | exact module shape | Sound as the submitted task-entry harness. It is intentionally not general Python definition/call semantics. Early `x` allocation is unobservable on this program. |
| SEM-02 | semantic.k:56 | Splits a nonempty statement list to `S ~> SS`. | sort match | Correct left-to-right statement sequencing. |
| SEM-03 | semantic.k:57 | Empty statement list becomes `.K`. | none | Correct list termination. |
| SEM-04 | semantic.k:59-60 | `Name(X)` reads `X |-> I` from `<env>`. | binding exists | Correct local lookup; missing bindings get stuck rather than fabricated. |
| SEM-05 | semantic.k:62 | Assignment evaluates RHS before commit. | target is `Name` | Correct for every submitted assignment target. |
| SEM-06 | semantic.k:63-64 | Commits integer RHS to an existing map binding. | value is `Int`; binding exists | Correct for submitted locals; loader allocates every used name. |
| SEM-07 | semantic.k:66 | Begins binary operation by evaluating left operand. | none | Correct evaluation order. |
| SEM-08 | semantic.k:67 | After left integer, evaluates right and retains left. | left evaluates to `Int` | Correct evaluation order and binding. |
| SEM-09 | semantic.k:68 | `+` returns `A +Int B`. | none | Exact for Python integers on the submitted use. |
| SEM-10 | semantic.k:69-70 | `%` returns `A %Int B`. | `B != 0` | Exact for all reachable uses (`A>=0`, `B` is 10, 11, or 13). K `%Int` is truncating remainder and differs from Python for some negative operands, but no negative dividend reaches this rule in the real program. |
| SEM-11 | semantic.k:71-72 | `//` returns `A /Int B`. | `B != 0` | Exact for the only reachable use (`A=x>0`, `B=10`). K `/Int` rounds toward zero, unlike Python floor division for negative dividends; negative `x` is unreachable in the submitted program. |
| SEM-12 | semantic.k:74 | Begins comparison by evaluating left. | none | Correct evaluation order. |
| SEM-13 | semantic.k:75 | After left integer, evaluates right and retains left. | left evaluates to `Int` | Correct evaluation order. |
| SEM-14 | semantic.k:76 | `<` returns `A <Int B`. | none | Exact for submitted integer comparison. |
| SEM-15 | semantic.k:77 | `>` returns `A >Int B`. | none | Exact for submitted integer comparison. |
| SEM-16 | semantic.k:78 | `==` returns `A ==Int B`. | none | Exact for submitted integer comparison. |
| SEM-17 | semantic.k:80 | Begins binary `or` by evaluating left. | operator exactly `"or"` | Correct short-circuit order. |
| SEM-18 | semantic.k:81 | True left operand returns true without evaluating right. | left is `Bool(true)` | Correct Python `or` behavior for boolean operands used here. |
| SEM-19 | semantic.k:82 | False left operand evaluates right. | left is `Bool(false)` | Correct short-circuit behavior. |
| SEM-20 | semantic.k:84 | Evaluates `If` guard before choosing a body. | none | Correct. |
| SEM-21 | semantic.k:85 | True guard selects THEN statements. | boolean true | Correct. |
| SEM-22 | semantic.k:86 | False guard selects ELSE statements. | boolean false | Correct. |
| SEM-23 | semantic.k:88 | Evaluates `While` guard and records loop. | none | Correct. |
| SEM-24 | semantic.k:89 | True guard executes body then reconstructs the loop. | boolean true | Correct recurring control point; body precedes next guard. |
| SEM-25 | semantic.k:90 | False guard consumes loop. | boolean false | Correct. |
| SEM-26 | semantic.k:92 | Evaluates return expression then `returnValue`. | none | Correct expression-before-return order. |
| SEM-27 | semantic.k:93-94 | Integer return writes `<result>` and discards remaining top-level function computation. | integer return value | Correct abrupt return for this single top-level invocation; there is no modeled caller/stack to preserve. |

## Verification functions, simplification, and macros

| ID | Location | Rule | Coverage/overlap/termination and judgment |
|---|---|---|---|
| VER-01 | verification.k:13-14 | `fizzEnd(N)=>0` if `N<0` | Disjoint with VER-02. Correct final `i` for the program's empty negative-input loop. |
| VER-02 | verification.k:15-16 | `fizzEnd(N)=>N` if `N>=0` | Together with VER-01 covers every integer. Correct for zero and positive input. |
| VER-03 | verification.k:18-19 | `digitSevens(X)=>0` if `X<=0` | Disjoint base case. `X=0` has no digit seven; negative values are outside inner-claim use and receive a defined value. |
| VER-04 | verification.k:20-21 | `digitSevens(X)=>1+digitSevens(X/10)` if `X>0` and last digit is 7 | Correct decimal recurrence; recursive argument is nonnegative and smaller. |
| VER-05 | verification.k:22-23 | `digitSevens(X)=>digitSevens(X/10)` if `X>0` and last digit is not 7 | Disjoint from VER-04; recursive argument decreases. VER-03..05 cover all integers. |
| VER-06 | verification.k:25-26 | `fizzContribution(I)=>digitSevens(I)` if divisible by 11 | Correct first disjunct, including values divisible by both 11 and 13. |
| VER-07 | verification.k:27-28 | Same contribution if not divisible by 11 but divisible by 13 | Disjoint from VER-06; correct second disjunct. |
| VER-08 | verification.k:29-30 | Contribution zero if divisible by neither | Disjoint from VER-06/07; the three guards exhaust all integers. |
| VER-09 | verification.k:32-33 | `fizzFrom(I,N)=>0` if `I>=N` | Correct empty-interval base, including negative entry inputs where `I=0>=N`. |
| VER-10 | verification.k:34-35 | Contribution at `I` plus `fizzFrom(I+1,N)` if `I<N` | Correct `[I,N)` recurrence; measure `N-I` strictly decreases. VER-09/10 are disjoint and exhaustive. |
| VER-11 | verification.k:38 | `(A+B)+C => A+(B+C)` | `[simplification]`; true associativity over mathematical/K integers. Right-nesting decreases the number of left-nested additions and does not encode a task result. |
| VER-12 | verification.k:43-48 | `INNER-LOOP` macro expands to the exact translated inner while-loop | Compile-time alias, not an execution bridge. Expanded-KORE equality against `solution.mpy` is recorded in stage 4. |
| VER-13 | verification.k:51-59 | `OUTER-LOOP` macro expands to the exact translated outer while-loop and VER-12 | Compile-time alias, not an execution bridge. Expanded-KORE equality is recorded in stage 4. |

No rule has a priority attribute. No fresh or opaque value can influence a
branch or final result. The only proof-local normalizer, VER-11, is an ordinary
integer identity. The loop claims in `spec.k` are reachability claims rather
than operational rules in the compiled definition; the inner claim is proved
from the semantic rules, the outer claim uses the independently proved inner
claim, and the entry claim uses both independently proved loop claims.

## Used-construct coverage map

| Submitted constructor/operator | Declaration | Rules |
|---|---|---|
| `Module(FuncDef("fizz_buzz",Params("n"),...))` | SYN-01, SYN-03 | SEM-01 |
| statement lists | SYN-02 | SEM-02, SEM-03 |
| `Assign(Name(...),...)` | SYN-04, SYN-08 | SEM-05, SEM-06 plus expression rules |
| `Name`, `Int`, runtime `Bool` | SYN-08..10 | SEM-04 and value forms |
| `BinOp("+",...)` | SYN-11 | SEM-07..09 |
| `BinOp("%",...)` | SYN-11 | SEM-07, SEM-08, SEM-10 |
| `BinOp("//",...)` | SYN-11 | SEM-07, SEM-08, SEM-11 |
| `Compare` with `<`, `>`, `==` | SYN-12, SYN-14 | SEM-12..16 |
| binary `BoolOp("or",...)` | SYN-13 | SEM-17..19 |
| `If` | SYN-06 | SEM-20..22 |
| `While` | SYN-05 | SEM-23..25 |
| `Return(Name("count"))` | SYN-07 | SEM-26, SEM-27 plus SEM-04 |

Every constructor in the submitted `solution.mpy` has a declaration and a
complete reachable rule path. Unsupported syntax remains unmodeled and would
fail parsing or become visibly stuck.

