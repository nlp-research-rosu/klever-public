# Reviewer rule inventory

Scope: the candidate's `semantic.k` and `verification.k`. `spec.k` contributes
eight reachability claims but no semantic or proof-extension rule.

## Syntax and symbol declarations

| ID | File:line | Declaration | Attributes / review |
|---|---|---|---|
| S01 | semantic.k:7 | `Module ::= Module(Stmts)` | Program root; used. |
| S02 | semantic.k:9 | `Stmts ::= List{Stmt,""}` | Statement sequencing; used. |
| S03 | semantic.k:10 | `Strings ::= List{String,","}` | Parameter lists; used. |
| S04 | semantic.k:11 | `Params(Strings)` | Used with one parameter. |
| S05 | semantic.k:13-16 | `Stmt ::= FuncDef \| Assign \| If \| Return` | All four are used. |
| S06 | semantic.k:18 | `Exprs ::= List{Expr,","}` | Zero/one argument lists used. |
| S07 | semantic.k:19 | `CmpOps ::= List{CmpOp,","}` | Singleton comparisons used. |
| S08 | semantic.k:21-27 | `Expr ::= Name \| Str \| Int \| Attribute \| Call \| Compare \| BinOp` | All but `Int` occur in `solution.mpy`; `Int` is unused but harmless. |
| S09 | semantic.k:29 | `CmpOp(String,Expr)` | `!=` and `in` used. |
| S10 | semantic.k:37-41 | `Value ::= VStr \| VInt \| VBool \| VList \| VAttr` | Runtime values; all used. |
| S11 | semantic.k:42 | `iteValue` | `[function]`; two equations R17-R18. |
| S12 | semantic.k:44 | `eval` | `[function]`; equations R01-R08. |
| S13 | semantic.k:45 | `call` | `[function]`; equations R09-R12. |
| S14 | semantic.k:46 | `add` | `[function]`; equation R13. |
| S15 | semantic.k:47 | `compare` | `[function]`; equations R14-R15. |
| S16 | semantic.k:48 | `asBool` | `[function]`; equation R16. |
| S17 | semantic.k:77-78 | `Outcome ::= normal \| returned` | Explicit normal/return control. |
| S18 | semantic.k:79 | `iteOutcome` | Symbolic conditional outcome. |
| S19-S21 | semantic.k:80-82 | `exec`, `execStmt`, `execRest` | `[function]`; equations R19-R26. |
| S22 | semantic.k:100 | `isWhitespace` | `[function,total]`; equation R27. |
| S23-S24 | semantic.k:106-107 | `pySplitWhitespace`, `splitWhitespaceAt` | `[function]`; equations R28-R33. |
| S25-S26 | semantic.k:129-130 | `joinValues`, `joinValuesTail` | `[function]`; equations R34-R37. |
| S27 | semantic.k:140 | `pySplitOn` | `[function]`; equations R38-R39. |
| S28 | verification.k:7 | `Function ::= closure(Params,Stmts)` | Selected function body. |
| S29 | verification.k:8 | `findFunction` | `[function]`; equations R40-R41. |
| S30-S32 | verification.k:9-11 | `invoke`, `outcomeValue`, `runProgram` | `[function]`; equations R42-R45. |
| S33 | verification.k:30 | `solutionAST` | `[function]`; exact program equation R46. |
| S34 | verification.k:83 | `oddLetterCount` | `[function,total]`; equation R47. |
| S35 | verification.k:99 | `containsWhitespace` | `[function,total]`; equation R48. |
| C01 | verification.k:103 | `<k> runProgram($PGM,$INPUT) </k>` | Only observable cell; sufficient for this pure one-function program. |

There are no local `[functional]`, `[simplification]`, `[simplifier]`,
`[priority]`, `[owise]`, `[anywhere]`, or macro declarations; no local opaque
symbol lacks equations on the submitted program's paths.

## Rules

| ID | File:line | Rule role | Complete-domain review |
|---|---|---|---|
| R01-R03 | semantic.k:50-52 | Name lookup, string literal, integer literal | Exact for modeled values; R03 unused. |
| R04 | semantic.k:53 | Attribute receiver evaluation | Retains receiver and attribute name. |
| R05-R06 | semantic.k:54-55 | Zero/one-argument calls | Exact arities used by the program; expression calls are pure here. |
| R07 | semantic.k:56 | Integer `+` expression | Delegates to R13; only integer additions occur. |
| R08 | semantic.k:57-58 | Singleton comparison | Exact singleton form used. |
| R09 | semantic.k:60 | `str.split()` | Delegates to the explicit whitespace splitter. |
| R10 | semantic.k:61-62 | `str.split(SEP)` | Delegates to separator splitter; submitted calls use nonempty comma. |
| R11 | semantic.k:63-64 | `str.join(list[str])` | Exact list/value shape used. |
| R12 | semantic.k:65-66 | `str.count(needle)` | Trusted K nonoverlapping occurrence primitive; submitted needles are one-character ASCII. |
| R13 | semantic.k:68 | Integer addition | Exact K integer arithmetic. |
| R14-R15 | semantic.k:69-71 | String `!=` and substring `in` | Exact operations used. |
| R16 | semantic.k:72 | Boolean coercion | Conditions already have `VBool`; no broader Python truthiness is claimed. |
| R17-R18 | semantic.k:73-74 | Conditional value selection | Disjoint and exhaustive over `Bool`. |
| R19-R20 | semantic.k:84-85 | Empty/cons statement execution | Structural recursion through the real body. |
| R21-R23 | semantic.k:87-90 | Continue, propagate return, distribute continuation through symbolic branch | Preserves the result/control behavior exposed by this pure semantics. |
| R24 | semantic.k:92 | Name assignment | Evaluates RHS in old environment, then updates the name. |
| R25 | semantic.k:93 | Return | Evaluates the real expression and creates abrupt `returned`. |
| R26 | semantic.k:94-96 | If | Evaluates guard and both symbolic branch terms; exact for the program's pure expressions/statements and later selected by R17-R18. |
| R27 | semantic.k:101-104 | Single-character whitespace membership | Unconditional definition; all program calls receive a one-character substring. The declared set equals CPython 3.10 `isspace()` characters (separate evidence). |
| R28 | semantic.k:108 | Initialize whitespace scan | Starts at index 0 with empty word/output. |
| R29-R30 | semantic.k:109-112 | End scan with empty/nonempty word | Guards are disjoint and exhaustive on reachable end states. |
| R31-R33 | semantic.k:113-127 | Skip leading/run whitespace, flush word, append nonwhitespace char | Guards are disjoint/exhaustive for reachable `0 <= I < length`; index increases. |
| R34-R37 | semantic.k:131-136 | Join empty/cons list and tail | Structural, exact for lists of `VStr`. |
| R38-R39 | semantic.k:141-152 | No separator found / split at first separator | Disjoint on `findString`; recursion strictly shortens for the used nonempty comma separator. |
| R40-R41 | verification.k:13-17 | Select matching function / skip unequal function | Guards disjoint; exact binding selected from submitted module. |
| R42 | verification.k:19-20 | Invoke one-parameter closure | Binds the actual value and executes the captured body. |
| R43-R44 | verification.k:21-23 | Extract returned result / preserve symbolic branch | Exact result observation. |
| R45 | verification.k:24-25 | Run named entry point | Selects `split_words` from the supplied module. |
| R46 | verification.k:31-80 | `solutionAST` definition | Definitional program constant. Reviewer KAST comparison proves identity with submitted `solution.mpy` after empty-list-unit normalization. |
| R47 | verification.k:84-97 | `oddLetterCount` summary | Truthfully names the candidate body's sum of `b,d,...,z` counts; no execution is replaced. |
| R48 | verification.k:100-101 | `containsWhitespace` summary | Truthfully names the candidate's `join("", split()) != txt` test; no execution is replaced. |

R01-R46 are the generated fixed semantics/invocation layer. R47-R48 are
definitional summaries used only on the destination side of the universal
claim. No operational bridge bypasses a program-defined body; the body reduces
through `exec`/`eval`/`call`.

## Claims

`spec.k` has eight unconditional entry claims: one universally quantified over
all K `String` values and seven ground instances (three prompt examples plus
empty, precedence, Unicode-whitespace, and repeated-comma cases). There are no
helper, loop, invariant, or lemma claims.

