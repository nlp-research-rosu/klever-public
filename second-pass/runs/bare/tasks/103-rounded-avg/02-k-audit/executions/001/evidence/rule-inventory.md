# Exhaustive local K declaration and rule inventory

Scope: the scratch copies of `semantic.k`, `verification.k`, and `spec.k`.
There are no other candidate-authored `.k` source files. Imported K standard
library modules are recorded as trust boundaries, not candidate-local rules.

## `semantic.k`: syntax and configuration

| ID | Lines | Declaration / alternatives | Use in submitted `solution.mpy` |
|---|---:|---|---|
| S1 | 9 | `Module ::= Module(Stmts)` | Root constructor |
| S2 | 10 | `Stmts ::= List{Stmt,""}` | Function body, then/else bodies |
| S3 | 11–13 | `Stmt ::= FuncDef(...) \| If(...) \| Return(...)` | All three alternatives used |
| S4 | 15 | `Params ::= Params(Strings)` | Two formal names |
| S5 | 16 | `Strings ::= List{String,","}` | `"n","m"` |
| S6 | 18–23 | `Expr ::= Int \| Name \| UnaryOp \| BinOp \| Compare \| Call` | All six alternatives used |
| S7 | 24 | `Exprs ::= List{Expr,","}` | One argument to each builtin call |
| S8 | 25 | `CmpOp ::= CmpOp(String,Expr)` | `">", Name("m")` |
| S9 | 26 | `CmpOps ::= List{CmpOp,","}` | Single comparison operator |
| S10 | 39–42 | `PyVal ::= intVal \| boolVal \| ratVal \| binVal` | Runtime values; all reached |
| S11 | 43 | `Result ::= noResult \| result(PyVal)` | Initial and final result |
| S12 | 45–49 | `KItem ::= boot \| exec \| execStmt \| choose \| doReturn` | Control terms; all reached |
| F1–F6 | 51–56 | `[function]` declarations `eval`, `unary`, `binary`, `compare`, `callBuiltin`, `roundValue` | Expression evaluation |
| C1 | 58–63 | `<py><k>boot($PGM,$N,$M)</k><env>.Map</env><result>noResult</result></py>` | Complete modeled state |

No declaration has `[total]`, `[functional]`, `[opaque]`, a priority
attribute, or a simplification attribute. No local evaluation-context
attributes (`strict`/`seqstrict`) occur.

## `semantic.k`: operational and functional rules

| ID | Lines | Rule summary | Static judgment |
|---|---:|---|---|
| R1 | 67–69 | Boot the sole `rounded_avg` definition and bind its two formal names to `N,M`. | Sound for the exact submitted module. It reads `<k>`, replaces `.Map`, and leaves `<result>` unchanged. |
| R2 | 71 | `exec(.Stmts) => .K`. | Sound empty-list termination. |
| R3 | 72 | `exec(S REST) => execStmt(S) ~> exec(REST)`. | Sound left-to-right statement sequencing. Disjoint from R2. |
| R4 | 74–76 | Evaluate an `If` condition under the current environment, then `choose`. | Sound for the pure expressions used here. |
| R5 | 77 | True choice executes the then-list. | Sound; disjoint from R6. |
| R6 | 78 | False choice executes the else-list. | Sound; disjoint from R5. |
| R7 | 80–81 | Evaluate a `Return` expression, then `doReturn`. | Sound for the modeled top-level function. |
| R8 | 82–83 | A `PyVal` before `doReturn` discards the remaining function continuation and writes the result. | Sound on both real return paths. The only reachable continuation is the remainder of this function body; the rule models Python’s abrupt return and changes no other modeled state. |
| R9 | 85 | Evaluate an integer literal. | Sound. |
| R10 | 86 | Look up a present name in the map. | Sound for the unique bindings `"n"` and `"m"`; missing names remain visibly stuck. |
| R11 | 87 | Delegate unary expression evaluation to `unary`. | Sound on the used pure operand. |
| R12 | 88–89 | Delegate binary expression evaluation to `binary`. | Evaluation order is not explicit, but both used operands are pure; no observable order difference exists in this program. |
| R13 | 90–91 | Delegate a single comparison to `compare`. | Sound for the used one-link comparison. |
| R14 | 92 | Evaluate a one-argument named builtin call, then `callBuiltin`. | Sound for the nested pure calls `round(...)` and `bin(...)`; unsupported bindings/call shapes stay stuck. |
| R15 | 94 | Integer unary minus. | Sound. |
| R16 | 95 | Integer addition. | Sound and uses unbounded K integers, matching Python integer addition. |
| R17 | 96–97 | Model Python `/` on two integers as exact `ratVal(I,J)`. | **Materially unsound as a model of the real Python operation used by the program.** CPython `/` produces binary64 or raises. Intended-domain witness: `I=18014398509481986,J=2` arises from `n=m=9007199254740993`; K preserves exact `9007199254740993`, but CPython produces `9007199254740992.0`. At `n=m=10**400`, CPython raises `OverflowError` while K produces a value. |
| R18 | 98 | Integer greater-than. | Sound. |
| R19 | 99 | Dispatch `round` to `roundValue`. | Structurally sound, but it receives the unsound exact-rational abstraction introduced by R17. |
| R20 | 100 | Dispatch `bin(intVal(I))` to `binVal(I)`. | Acceptable only as an abstract representation contract for Python’s external builtin; it does not itself return a K `String`. It is result-bearing and all program postconditions depend on that representation bridge. |
| R21 | 104–105 | Exact positive-denominator rational below half rounds to floor. | Mathematically sound for the declared exact `ratVal`, guard disjoint from R22–R24. |
| R22 | 106–107 | Exact rational above half rounds to floor plus one. | Mathematically sound for exact `ratVal`, disjoint guard. |
| R23 | 108–111 | Exact half with even floor rounds down. | Mathematically sound ties-to-even for exact `ratVal`, disjoint guard. |
| R24 | 112–115 | Exact half with odd floor rounds up. | Mathematically sound ties-to-even for exact `ratVal`, disjoint guard. |

R21–R24 cover the used domain `D=2`, positive numerator. Their `<`, `>`, and
`==` half tests partition it, and the two parity guards partition the equality
case. They do not repair R17’s loss of CPython binary64 behavior.

## `verification.k`

| ID | Lines | Declaration or rule | Class and judgment |
|---|---:|---|---|
| VF1 | 9–21 | `[function] roundedAvgProgram` and its sole equation to a `Module(...)` constructor tree. | Definitional constant. Fresh `kast` parsing gives byte-identical KORE for this RHS and submitted `solution.mpy`; it does not replace the body with an answer. |
| VF2 | 26, 28–29 | `[function] renderBinary`; `binVal(I) => "0b" + unsignedBits(I)` for `I>=0`. | Result observer. Correct for the intended nonnegative successful results; depends on VF3–VF5. |
| VF3 | 27, 30 | `[function] unsignedBits`; `unsignedBits(0) => "0"`. | Correct base case. |
| VF4 | 31 | `unsignedBits(1) => "1"`. | Correct base case; disjoint from VF3 and VF5. |
| VF5 | 32–33 | For `I>=2`, recurse on `I/2` and append `I%2`. | Correct, decreasing, and covers all remaining nonnegative integers. |

There are no `[total]`, `[functional]`, `[opaque]`, priority, ordinary
execution-bypass, or `[simplification]` declarations in `verification.k`.
The three functions are partial outside the domains needed by this program.

## `spec.k`

The eleven positive claims are: `reversed`, `integral-midpoint`,
`half-even-down`, `half-even-up`, four fixed program examples, and three fixed
rendering examples. There are no helper claims, circularities, loop summaries,
lemmas, or proof-local rewrite rules. The four universal claim guards partition
all positive `N,M`: reversed; valid even sum; valid odd sum with even floor;
valid odd sum with odd floor.

## Construct-to-rule coverage

`Module/FuncDef/Params/Stmts` map to S1–S5 and R1–R3; `If/Compare/Name/CmpOp`
map to S3, S6, S8–S9 and R4–R6, R10, R13, R18; `Return/UnaryOp/Int` map to S3,
S6 and R7–R9, R11, R15; nested `Call/Name/BinOp/Int` map to S6–S7 and R9–R10,
R12, R14, R16–R17, R19–R24. Every constructor in `solution.mpy` therefore has
a declaration and a reached rule. The defect is semantic fidelity of the
reached division/rounding path, not missing construct coverage.
