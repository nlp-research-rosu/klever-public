# Exhaustive local K inventory

This inventory covers every local declaration and rule in the submitted
`semantic.k` and `verification.k`, plus the five reachability claims in
`spec.k`. Imported `domains.md` modules are recorded as a trust boundary rather
than re-inventoried. Line numbers refer to the candidate source.

## Syntax and configuration

| ID | Lines | Declaration | Use and review |
|---|---:|---|---|
| S01 | semantic.k 3–12 | `Bracket ::= lbr \| rbr`; `BString ::= .BString \| Bracket BString` | Inductive encoding of exactly finite bracket-only inputs. |
| S02 | 13 | `Module ::= Module(Stmts)` | Parses the submitted module root. |
| S03 | 14–15 | comma-separated `Strings`; `Params(Strings)` | Parses the one string parameter. |
| S04 | 17–18 | comma-separated `CmpOps`; `CmpOp(String,Expr)` | Parses the submitted singleton comparisons. |
| S05 | 20–25 | `Expr ::= Name \| Int \| Bool \| Str \| BinOp \| Compare` | Exactly the expression constructors in `solution.mpy`; unused alternatives remain ordinary syntax. |
| S06 | 27–32 | juxtaposed `Stmts` list; `Stmt ::= FuncDef \| Assign \| For \| If \| Return` | Exactly the statement constructors in the submitted AST. |
| S07 | 41–45 | `Val`, `Result`, and `Function` constructors | Runtime values, optional result, and stored function body. Constructors are not opaque. |
| S08 | 47–48 | `KItem ::= start(BString) \| iterate(String,BString,Stmts)` | Internal call and loop continuations. |
| S09 | 50–56 | `<py>` configuration containing `<k>`, `<functions>`, `<env>`, `<result>` | All cells are used; there is no heap, I/O, exception, or call stack because the submitted one-function subset does not require them. |
| S10 | 74–77 | `eval`, `add`, `compare`, `getVal`, each `[function]` | Pure expression evaluators. None is declared `[total]`; every application reachable from the submitted program is covered. |
| S11 | 102 | `choose(Val,Stmts,Stmts) [function]` | Covered for both reachable Boolean values. |
| S12 | 120 | `getString(Val) [function]` | Covered for the only reachable string value. |
| V01 | verification.k 8 | nullary `loopBody [function,total]` | Exact, fully covered definitional AST fragment. |
| V02 | 20 | nullary `solutionBody [function,total]` | Exact, fully covered definitional AST fragment. |
| V03 | 26 | nullary `theSolution [function,total]` | Exact, fully covered definitional module AST. |
| V04 | 33 | `scan(Int,BString) [function,total]` | Result-bearing reference function, not an execution bridge. Rules cover every theorem-reachable state 0–3 but not other `Int` values; the global `total` annotation is therefore over-broad. |

There are no local `[functional]` declarations distinct from the functions
above, no opaque symbols, no priority rules or `owise` rules, no strictness
attributes, no simplification rules, and no macros.

## Ordinary semantic rules in `semantic.k`

| ID | Lines | Rule | Soundness review |
|---|---:|---|---|
| R01 | 59 | `Module(SS) => SS` | Begins module loading with its statement list. |
| R02 | 60 | nonempty `Stmts` list `=> S ~> SS` | Left-to-right statement sequencing. |
| R03 | 61 | `.Stmts => .K` | Empty sequence terminates. |
| R04 | 63–64 | `FuncDef` updates `<functions>` and vanishes | Stores the exact parameters/body. The submitted program has one definition, so overwrite/order issues do not arise. |
| R05 | 66–70 | `start(BS) => BODY`; bind `"string"` and replace environment | Selects the loaded exact `is_nested` binding. Entry execution starts with an empty environment. |
| R06 | 79 | `eval(Name(X),ENV) => getVal(ENV[X])` | Faithful lookup; all used names are bound. |
| R07 | 80 | `getVal(V:Val) => V` | Type projection for successful lookup. |
| R08 | 81 | integer literal evaluation | Exact unbounded K/Python integer value. |
| R09 | 82 | Boolean literal evaluation | Exact. |
| R10 | 83 | string literal `"["` to one-character `lbr` string | Exact on the used literal. |
| R11 | 84 | string literal `"]"` to one-character `rbr` string | Exact; harmless though unused by this AST. |
| R12 | 85 | `BinOp("+",...)` through `add` | Both operands are pure; exact on used integer operands. |
| R13 | 86–87 | singleton `Compare` through `compare` | Exact for all submitted comparisons; no chained comparison is used. |
| R14 | 89 | integer `add` | Ordinary integer addition. |
| R15 | 91 | integer `==` | Ordinary integer equality. |
| R16 | 92 | integer `<` | Ordinary integer ordering. |
| R17 | 93–94 | `lbr == lbr => true` | Exact. |
| R18 | 95–96 | `lbr == rbr => false` | Exact. |
| R19 | 97–98 | `rbr == lbr => false` | Exact. |
| R20 | 99–100 | `rbr == rbr => true` | Exact. |
| R21 | 103 | `choose(true,THEN,_) => THEN` | Exact branch selection. |
| R22 | 104 | `choose(false,_,ELSE) => ELSE` | Exact branch selection; guards are constructor-disjoint from R21. |
| R23 | 107–108 | assignment to `Name(X)` | Evaluates against the old environment and updates exactly one binding. |
| R24 | 110–112 | `If` becomes the selected statement list | Expressions are pure, so meta-level `eval` preserves the submitted evaluation and control behavior. |
| R25 | 116–118 | `For(Name(X),E,BODY)` becomes `iterate`; prebind `X` to empty | The iterable is evaluated in the old environment, as Python requires. Prebinding differs from Python on an empty iterable, but the submitted post-loop code never reads `bracket` and `Return` clears the environment, so this cannot alter any theorem-observable state or result. |
| R26 | 121 | `getString(strVal(BS)) => BS` | Exact projection on the reachable iterable. |
| R27 | 123 | empty `iterate => .K` | Exact loop termination. |
| R28 | 124–126 | left-bracket iteration | Binds the one-character loop value, executes the body, then recurs on the suffix. |
| R29 | 127–129 | right-bracket iteration | Same for a right bracket; R28/R29 are constructor-disjoint. |
| R30 | 133–136 | `Return(E) ~> REST => .K`; clear functions/environment; set result | Correct early-return control for this single-call semantics. Every submitted return expression is pure and bound. Clearing the entire continuation is exactly the required non-local effect, and all observable cells match the claims. |

Rules R01–R30 are ordinary operational rules. None encodes whether nesting is
present, calls `scan`, or replaces execution with a summary/oracle.

## Proof-local equations in `verification.k`

| ID | Lines | Equation | Classification and review |
|---|---:|---|---|
| E01 | 9–18 | `loopBody =>` nested submitted `If` AST | Definitional summary only; exact constructor-for-constructor match to the `For` body parsed in `13-kast-submitted-program.log`. |
| E02 | 21–24 | `solutionBody => Assign; For; Return(false)` | Definitional summary only; exact submitted body and order. |
| E03 | 27–28 | `theSolution => Module(FuncDef(...solutionBody))` | Definitional program name. Together E01–E03 expand to the submitted AST; execution then uses R01–R30. |
| E04 | 35 | `scan(_, .BString) => false` | Correct: no suffix remains to complete `[[]]`; disjoint from all nonempty cases. |
| E05 | 37 | `scan(0,lbr BS) => scan(1,BS)` | First target symbol consumed. |
| E06 | 38 | `scan(0,rbr BS) => scan(0,BS)` | Right bracket ignored before the first left. |
| E07 | 40 | `scan(1,lbr BS) => scan(2,BS)` | Second left consumed. |
| E08 | 41 | `scan(1,rbr BS) => scan(1,BS)` | Right bracket ignored until the second left. |
| E09 | 43 | `scan(2,lbr BS) => scan(2,BS)` | Extra left ignored after two lefts. |
| E10 | 44 | `scan(2,rbr BS) => scan(3,BS)` | First closing right consumed. |
| E11 | 46 | `scan(3,lbr BS) => scan(3,BS)` | Extra left ignored while awaiting final right. |
| E12 | 47 | `scan(3,rbr _) => true` | Final right establishes the target; suffix is legitimately irrelevant because truth is absorbing. |

E04–E12 have disjoint constructor/ground-state patterns. Their recursion
strictly shortens `BS`, except E12 terminates immediately. They are truthful for
states 0–3. The declared first-argument sort is all `Int`, so
`scan(4,lbr .BString)` is uncovered. This is a coverage/annotation limitation,
not a false equation: the ground diagnostic in `15b-scan-totality-gap.log`
builds and gets stuck on that term rather than proving it equals `false`.
All theorem calls begin at 0 and E05–E12 preserve the set `{0,1,2,3}`.

## Reachability claims in `spec.k`

| ID | Lines | Claim | Review |
|---|---:|---|---|
| C01 | 10–21 | Loop state 0 | Exact loop head and continuation; postcondition is `scan(0,BS)`. |
| C02 | 23–34 | Loop state 1 | Same with state/result summary 1. |
| C03 | 36–47 | Loop state 2 | Same with state/result summary 2. |
| C04 | 49–60 | Loop state 3 | Same with state/result summary 3. |
| C05 | 64–68 | End-to-end `theSolution ~> start(BS)` | Empty initial maps/no result; exact final empty maps and `boolVal(scan(0,BS))`. |

C01–C04 are circular reachability invariants, not semantic rules. Their
arbitrary `ORIG` and `CUR` values are framed only where the loop body does not
inspect them. Each admits ground states (see `14-adequacy-witnesses.log`).
C05 executes E01–E03 and R01–R30; the return is fixed to `scan(0,BS)`, not an
existential or unconstrained variable.

## Used-construct coverage map

The fresh parsed AST (`13-kast-submitted-program.log`) uses:

- `Module`, `FuncDef`, `Params`, `Strings`, and `Stmts`: S02/S03/S06,
  R01–R05;
- `Assign`, `Name`, `Int`: S05/S06, R06–R08/R23;
- `For` and input `BString`: S01/S06/S08, R25–R29;
- `If`, `Compare`, `CmpOp`, `Str`, and `Bool`: S04–S06,
  R09–R11/R13/R15–R22/R24;
- `BinOp("+",...)`: S05, R12/R14;
- `Return`: S06, R30.

Thus every constructor in the submitted program has both syntax and behavior,
and no used construct is fabricated by a catch-all rule.
