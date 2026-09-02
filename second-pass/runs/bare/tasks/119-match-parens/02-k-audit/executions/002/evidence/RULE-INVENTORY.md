# Exhaustive local K declaration and rule inventory

Source scope: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no other candidate `.k` helper files. Imported
K builtin modules are listed as trust boundaries, not expanded into this local
inventory.

## Local declarations

| File:lines | Declaration(s) and attributes | Audit decision |
|---|---|---|
| `semantic.k:6` | `Pgm ::= Module(Stmts)` | Source module constructor; used and faithfully loaded. |
| `semantic.k:8-10` | list sorts `Stmts`, `Strings`; `Params(Strings)` | Faithful constructor grammar for the submitted term. |
| `semantic.k:12-14` | `Stmt ::= FuncDef \| If \| Return` | Exactly the submitted statement forms. |
| `semantic.k:16-20` | `Exprs`, `CmpOps`, `CmpOp`, `Bound`, `Slice` | Faithful supporting constructor grammar. |
| `semantic.k:22-31` | `Expr ::= Name \| Int \| Bool \| Str \| ListExpr \| BinOp \| Compare \| Subscript(index) \| Subscript(slice) \| Call` | Enumerates every expression form in `solution.mpy`; no used form is absent. |
| `semantic.k:44-46` | inductive `PString ::= .PString \| lp PString \| rp PString` | Sound representation of finite strings over the promised alphabet. |
| `semantic.k:48-50` | `PyString ::= parens(PString) \| yesString \| noString` | Sound disjoint representation for admissible inputs and the two outputs. |
| `semantic.k:52-57` | `Value ::= intVal \| boolVal \| strVal \| listVal \| closure`; `Values` | Sufficient runtime values. |
| `semantic.k:61` | verification-only `Expr ::= PStr(PString)` | Not emitted by the translator; supplies arbitrary finite parenthesis inputs to the universal claim. Its evaluation rule is inventoried below. |
| `semantic.k:63-84` | all continuation `KItem`s: `exec`, `eval`, binary/compare/index/slice/list/call continuations, `invoke`, `choose`, return/call frames, `launch`, `invokeEntry` | Explicit evaluation/control machinery; each used item has rules below. |
| `semantic.k:86-88` | functions `chars`, `pconcat`, `ptail` | `chars` and `pconcat` are defined below. `ptail` has no equation and is an unused partial/opaque symbol; no claim or execution path mentions it. |
| `semantic.k:89-92` | functions `literalString`, `stringPlus`, `stringHead`, `stringTail` | Equations below are partial outside the submitted subset and fail visibly there. |
| `semantic.k:93-94` | functions `valueEq`, `pstringEq` | Truthful equations for every value combination reached by this program. |
| `semantic.k:101-108` | configuration `<k>`, `<input>`, `<env>`, `<functions>`, `<result>` | All cells are read or written. Calls preserve the caller map through a continuation; no heap or I/O is used. |
| `semantic.k:110` | `Result ::= noResult \| Value` | Faithful result-cell state. |
| `verification.k:6` | `Pgm ::= solutionProgram` | Definitional handle; exact expansion inventoried below. |
| `verification.k:9` | `balanced(PString,Int) [function]` | Fully covered by four disjoint equations below; no `[total]` declaration is used. |
| `verification.k:10` | `contractAnswer(PString,PString) [function]` | Covered by a true branch and `[owise]`; no `[total]` declaration is used. |
| `spec.k:8-13` | universal entry claim | Result-constraining, satisfiable, and unrestricted over finite `PString`s, but its closure relies on invalid operational bridges and an inadequate CPython model. |
| `spec.k:16-21` | prompt `"Yes"` example claim | Satisfiable and result-constraining. |
| `spec.k:23-28` | prompt `"No"` example claim | Satisfiable and result-constraining. |

There are no local `[total]`, `[functional]`, `[simplification]`, or
`[concrete]` declarations/rules. The only explicit priorities are the two
`[priority(40)]` operational bridges in `verification.k:25-65`. The only
`[owise]` rule is `contractAnswer` at line 20.

## `semantic.k` rule inventory

Every local rule start line is included in the following table. A line range
lists each rule whose start line appears in that range in the declaration scan.

| Rule start line(s) | Role | Audit decision |
|---|---|---|
| 114 | `Module` starts definition loading then `launch` | Sound for the submitted module. |
| 116, 117 | empty statement execution; function definition insertion | Sound. Later definitions overwrite earlier ones as Python module bindings do for this subset. |
| 121, 123, 124 | `If` evaluation and Boolean branch choice | Sound; condition is evaluated before the selected body, then remaining statements. |
| 126, 127, 129 | return evaluation, `returned`, and discarding the current statement continuation | Sound for this control encoding. The call frame remains to restore the caller. |
| 132, 133, 134, 135 | integer, Boolean, source-string, and verification-only `PStr` evaluation | Sound on their represented values. `PStr` is an explicit proof-input bridge, not source syntax emitted by `py2mpy.py`. |
| 136, 137 | local-variable and global-function lookup | Each is truthful for a matching map. They overlap if a name is simultaneously in both maps, but submitted local names and function names are disjoint on all intended executions. |
| 139, 140 | left-to-right binary operand evaluation | Sound. |
| 141, 142, 143 | integer `+`, integer `-`, parenthesis-string `+` | Sound for the operand types reached by the program. |
| 147, 149 | one-link comparison evaluation, left then right | Sound; the submitted program contains only one-link comparisons. |
| 151, 153 | equality and integer less-than application | Sound for reached types. |
| 156, 157, 158, 161 | index evaluation, list index zero/successor, parenthesis-string index zero | Sound for the only indices 0 and list length two. Out-of-range and negative-index Python behavior is unmodeled but unreachable under the stated input shape and body. |
| 163, 165 | evaluation of the exact `[1:]` slice and string tail | Sound for the only slice in the program. |
| 167, 169, 170 | two-element list evaluation, left then right | Sound and exactly matches the input constructor used by entry claims. |
| 172, 173, 174 | one-argument call evaluation and invocation | Sound, left-to-right. |
| 175, 177, 179, 181 | two-argument call evaluation and invocation | Sound, function then first argument then second argument. |
| 185, 188 | one- and two-argument closure calls with a fresh local map | Sound in the idealized machine; the caller map is captured in `finishCall`. Collectively these rules omit CPython's finite recursion limit. |
| 192 | normal/explicit return restores the caller map | Sound for this program's calls. |
| 195, 196, 198 | entry launch, lookup of `match_parens`, and final result storage | Sound when the loaded module supplies the required binding, as the submitted module does. |
| 202, 203, 204 | convert `"Yes"`, `"No"`, or another source string | Sound on output literals and promised parenthesis inputs. Other alphabets cause `chars` to stick rather than fabricate a value. |
| 207, 208, 211 | recursively convert empty, `(`-headed, and `)`-headed strings | Disjoint and exhaustive on the promised alphabet; recursive substring shortens by one. |
| 215, 216, 217 | inductive `pconcat` | Truthful, disjoint, terminating structural recursion. |
| 218 | string addition via `pconcat` | Truthful for the only string kind used as an addition operand. |
| 220, 221 | one-character `stringHead` for `(` and `)` | Truthful for nonempty input; empty input is guarded by source control flow. |
| 222, 223 | `stringTail` for `(` and `)` | Truthful and structurally decreasing. |
| 225, 226, 227 | integer, Boolean, and parenthesis-string equality | Truthful on reached same-type operands. |
| 228, 229, 230, 231 | all equality combinations of `yesString` and `noString` | Truthful and disjoint. |
| 233-241 | all nine constructor-shape cases for `pstringEq` | Truthful, pairwise compatible, exhaustive on two `PString`s, and structurally decreasing in equal-head recursive cases. |

The operational rules form an idealized, unbounded call machine. No individual
call rewrite is a false equation inside that machine, but the machine is not a
sound semantics of the real CPython program over the full source-contract
domain: it has no recursion-depth/`RecursionError` state or rule. The concrete
valid input `["(" * 498 + ")" * 498, ""]` is a false-conclusion witness for
the claimed source-language bridge. Trusted CPython 3.10.12 canonical returns
`"Yes"`; the candidate raises `RecursionError`, whereas `spec.k` claims a normal
`yesString` result for the corresponding finite `PString`.

## `verification.k` rule inventory

| Rule start line(s) | Class and role | Audit decision |
|---|---|---|
| 12 | `balanced(_,D<0) = false` | Truthful equation. Its guard is disjoint from all `D>=0` rules. |
| 13 | `balanced(.PString,D>=0) = (D==0)` | Truthful base case. |
| 14 | `balanced(lp S,D>=0) = balanced(S,D+1)` | Truthful structural recursion. |
| 15 | `balanced(rp S,D>=0) = balanced(S,D-1)` | Truthful structural recursion; the line-12 case rejects a subsequent negative depth. |
| 17, 20 | `contractAnswer` true branch and `[owise]` false branch | Truthful definition of the requested mathematical answer; guards are complementary. |
| 25-43 | priority-40 operational bridge replacing the exact `is_balanced` closure call by `boolVal(balanced(S,D))` | **Invalid/unsound over its complete match domain.** It omits `<functions>` and all other cells, accepts any continuation, and has no bridge-free universal connection theorem. With the exact closure, valid `S = lp rp .PString`, `D=0`, and `<functions>.Map</functions>`, fixed semantics gets stuck at recursive lookup of `"is_balanced"` while the bridge reaches `boolVal(true)`. See the fixed/extended witness logs. |
| 48-65 | priority-40 operational bridge replacing the exact `match_parens` closure call by `strVal(contractAnswer(A,B))` | **Invalid/unsound over its complete match domain and directly answer-encoding.** It omits the required `"is_balanced"` binding and has no bridge-free connection theorem. With two valid empty `PString`s and `<functions>.Map</functions>`, fixed semantics gets stuck at lookup while the bridge reaches `strVal(yesString)`. It is also the same summary used in the postcondition, so the proof assumes the desired caller result. |
| 69-109 | definitional `solutionProgram` expansion | Sound and body-sensitive. Trusted regeneration is byte-identical; depth-adjusted KORE configurations for parsed `solution.mpy` and one-step-expanded `solutionProgram` are byte-identical. Changing the actually executed final `Return("No")` to `Return("Yes")` makes `kprove` fail. |

The two bridge witnesses are global rule-soundness counterexamples. The actual
entry claim does load the expected function map, so those malformed-map states
are not claimed to be reachable from its precondition. On reachable entry
states, the narrower independent defect remains decisive: neither bridge has
the required bridge-free universal execution theorem, and the caller bridge
substitutes the mathematical postcondition for execution. Removing both
bridges makes the universal proof stop at the real recursive body.

## Submitted-program construct mapping

| `solution.mpy` construct | Declaration | Material behavior |
|---|---|---|
| `Module` | `semantic.k:6` | line 114, then function loading and launch |
| `FuncDef` | lines 12, 117 | closure stored in `<functions>` |
| `If` | lines 13, 121-124 | condition, branch, continuation |
| `Return` | lines 14, 126-129, 192 | return value and caller restoration |
| `Name` | line 22 | lines 136-137 |
| `Int`, `Bool`, `Str` | lines 23-25 | lines 132-134 and literal conversion |
| `ListExpr` | line 26 | lines 167-170 |
| `BinOp` | line 27 | lines 139-144 |
| `Compare`, `CmpOp` | lines 18, 28 | lines 147-154 |
| indexed and sliced `Subscript` | lines 29-30 | lines 156-165 |
| `Call` | line 31 | lines 172-193 |

Thus the generated semantics has rule coverage for every submitted constructor.
The failures are not missing used syntax: they are the missing CPython recursion
effect and the proof-only execution-replacing bridges.
