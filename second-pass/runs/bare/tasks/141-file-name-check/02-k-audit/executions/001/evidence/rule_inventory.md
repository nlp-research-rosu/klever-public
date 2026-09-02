# Exhaustive local K inventory

This inventory covers every local declaration and rule in `semantic.k`,
`verification.k`, and `spec.k`. Imports from `domains.md` are listed separately
as the external trust boundary. Line numbers refer to the submitted source.

## Syntax, configuration, and attributes

| Location | Declaration | Used by submitted AST | Audit |
|---|---|---:|---|
| `semantic.k:8` | `Program ::= Module(Stmts)` | yes | Faithful wrapper for translator output. |
| `semantic.k:10-13` | list sorts `Stmts`, `Exprs`, `CmpOps`, `Strings` | yes | Separators match translator output; empty `Stmts` is used. |
| `semantic.k:15-16` | `Params(Strings)`, `CmpOp(String,Expr)` | yes | Exact translated forms. |
| `semantic.k:18-21` | statements `FuncDef`, `Assign`, `If`, `Return` | yes | All four occur. |
| `semantic.k:23-33` | expressions `Name`, `Int`, `Str`, `Bool`, `BinOp`, `UnaryOp`, `BoolOp`, `Compare`, `Subscript`, `Attribute`, `Call` | all except `Bool` | Every used form is mapped to a rule or is pattern-matched as part of `Call`. Lack of general standalone `Attribute` evaluation is harmless for this AST. |
| `semantic.k:42-46` | `PyVal`, `Env`, `ExecResult` constructors | yes | Pure values, shadowing environment, and normal/returned/conditional results. No heap or I/O is needed. |
| `semantic.k:48-59,63,114` | 14 `[function,total,symbol]` helpers: `runProgram`, `eval`, `lookupVal`, `exec`, `continue`, `asBool`, `compareVals`, `endsWith`, `addVals`, `subscriptVal`, `boolOp`, `resultValue`, `occurrences`, `getString` | yes | Many `total` declarations are broader than their equations. The compiler reports non-exhaustive matches for all except `continue`, `endsWith`, and `occurrences`. Reachable target terms are covered, except that the `IfExec` encoding can speculatively expose an invalid empty-string subscript. |
| `semantic.k:66` | configuration `<k> runProgram($PGM,$INPUT) </k>` | yes | Only observable state is the result in `<k>`; sufficient for this pure function. |
| `verification.k:6-11` | six `[function,total,symbol]` declarations: `solutionProgram`, `digitCount`, `startsWithAsciiLetter`, `hasAcceptedSuffix`, `validFileName`, `contractResult` | yes except `validFileName` is not in the entry claim | Each has one unguarded defining equation and hence complete syntactic coverage. |
| all local source | explicit `[functional]`, priorities, `[simplification]`, ordinary proof-only rewrites, auxiliary claims, loop claims | n/a | None. `occurrences` has the sole `[concrete]` rule. `spec.k` contains the sole claim. |

The zero-argument `[symbol]` attributes trigger compiler warnings but merely
affect generated labels. They provide no logical justification.

## `semantic.k` rules

| # | Location | Rule(s) | Class and audit |
|---:|---|---|---|
| S1 | 64 | `occurrences(S,N) => countAllOccurrences(S,N) [concrete]` | Trusted primitive bridge to K's string library for ground strings. For the target, `N` is one of ten digits or `"."`, so non-overlapping occurrence counting agrees with Python `str.count`. On symbolic `S` it stays opaque; the theorem is parametric in the same term on execution and postcondition sides. |
| S2 | 68-71 | exact `runProgram(Module(FuncDef("file_name_check",Params("file_name"),BODY)),S)` enters `exec(BODY,Bind(...))` | Operational entry rule. It executes the submitted body rather than summarizing it. It is intentionally incomplete for other programs despite `[total]`; the target match is exact. |
| S3 | 73 | `resultValue(Returned(V)) => V` | Correct return extraction. |
| S4 | 74-75 | `resultValue(IfExec(...)) => IteVal(...)` | Symbolic conditional result. Correct for pure, total branches, but inherits the eager/partial branch defect in S12/S15. |
| S5-S6 | 77-78 | `IteVal(true/false,...)` selectors | Disjoint and exhaustive on concrete Bool; chosen result is correct. |
| S7-S8 | 79-80 | `IfExec(true/false,...)` selectors | Disjoint and exhaustive on concrete Bool; chosen execution result is correct if unchosen branch terms are not forced. |
| S9 | 82 | `exec(.Stmts,RHO) => Normal(RHO)` | Correct sequential base case. |
| S10 | 83-84 | assignment evaluates RHS in old environment, then shadows binding | Correct for target assignments and pure expressions. |
| S11 | 85 | return evaluates expression and discards remaining statements | Correct Python return control. Unused `SS` warning is intentional. |
| S12 | 86-91 | `exec(If(... ) SS,RHO) => IfExec(test, continue(then,SS), continue(else,SS))` | **Material fidelity defect.** It constructs both branch computations as function arguments instead of selecting a branch before executing it. Witness: submitted program with `S=""` should return `"No"` at the first `if`; fresh LLVM execution instead forces the later `substrString("",0,1)` and aborts. This is a false operational conclusion on the intended input domain. Haskell happens to reduce the selector lazily and returns `"No"`, exposing backend-dependent semantics. |
| S13 | 93 | `continue(Normal(RHO),SS) => exec(SS,RHO)` | Correct fall-through. |
| S14 | 94 | `continue(Returned(V),_) => Returned(V)` | Correct abrupt return. |
| S15 | 95-96 | continuation distributes into both `IfExec` branches | Value-correct for pure, total branches, but contributes to S12's speculative evaluation/backend divergence. |
| S16 | 98 | name evaluation calls `lookupVal` | Correct. |
| S17-S18 | 99-101 | hit/miss environment lookup | Guards are disjoint; recursive descent is structural. `EmptyEnv` is uncovered, but all target lookups are bound. |
| S19-S21 | 102-104 | integer/string/bool literals | Correct injections. `Bool` is unused. |
| S22 | 105-106 | binary `"+"` delegates to `addVals` | Used only for integer counts; correct. Other operators are intentionally unmodeled. |
| S23 | 107 | unary `"not"` over boolean | Correct for the used expression. |
| S24 | 108 | `BoolOp` delegates to `boolOp` | Correct dispatch. |
| S25 | 109-110 | one-comparator `Compare` delegates to `compareVals` | Exact used form; chained comparisons are absent. |
| S26 | 111-112 | subscript delegates after evaluating base/index | Correct for valid string index 0. No exception model or bounds guard exists; when S12 speculatively reaches it at `S=""`, the underlying substring is invalid. |
| S27 | 115 | `getString(VStr(S)) => S` | Correct projection. Broader `[total]` declaration is not exhaustive, but all target call receivers/arguments are strings. |
| S28 | 117-118 | built-in `len` on strings | Correct for target strings, conditional on K `lengthString` matching Python code-point length. |
| S29 | 119-120 | string `.count(nonempty-single-character)` | Correct target primitive bridge via S1. General method binding/argument evaluation is intentionally unmodeled. |
| S30 | 121-122 | string `.endswith(constant)` | Correct target primitive dispatch via S41-S42. |
| S31 | 124 | integer addition | Correct ordinary arithmetic. |
| S32 | 125-126 | string subscript via `substrString(S,I,I+1)` | Correct at target's reachable `I=0` with nonempty `S`; partial outside that domain and no Python exception is represented. Empty-string speculative witness is recorded under S12. |
| S33 | 128 | `asBool(VBool(B)) => B` | Correct projection; non-booleans intentionally unsupported. |
| S34 | 130-131 | two-operand `"and"` evaluates both operands | Same truth value as target because both used operands are total comparisons, but does not model Python short-circuit effects in general. No target-domain false result witness exists. |
| S35 | 132-133 | two-operand `"or"` evaluates both operands | Same limitation as S34; all target operands are safe comparisons. |
| S36 | 134-137 | three-operand `"or"` evaluates all three operands | Used for three `.endswith` calls, which are pure and total, so target result is correct despite missing general short-circuit behavior. |
| S37-S40 | 139-142 | integer `==`, `!=`, `>` and string `<=` | Exactly the operand/operator combinations in the AST; map directly to K mathematical operations. String comparison is a trusted built-in adequacy bridge to Python lexicographic comparison. |
| S41-S42 | 144-152 | `endsWith` length-sufficient substring equation / shorter-string `false` | Guards are disjoint and exhaustive over integer lengths. The sufficient branch uses valid indices and matches suffix semantics. |

There are no overlapping rule pairs except the deliberately disjoint lookup,
Boolean-selector, and `endsWith` pairs. There are no priorities or
simplification axioms.

## `verification.k` rules

| # | Location | Rule | Class and audit |
|---:|---|---|---|
| V1 | 13-23 | `digitCount` sums ten `occurrences` terms | Truthful definitional summary of ASCII digits. It is not an execution bridge. |
| V2 | 25-30 | `startsWithAsciiLetter` compares `substrString(S,0,1)` with ASCII ranges | Truthful only when `S` is nonempty. Its unguarded `[total]` declaration/equation is partial at `S=""`; `contractResult` intends to guard it, but S12/LLVM evaluates it anyway. This is the same recorded witness, not an additional unsupported unsoundness allegation. |
| V3 | 32-35 | `hasAcceptedSuffix` is the disjunction of `.txt/.exe/.dll` | Truthful total definition. |
| V4 | 40-45 | `validFileName` is conjunction of dot count, digit bound, nonempty start, ASCII-letter start, accepted suffix | Correct rendering of the prompt, subject to V2's partial subterm and trusted string/count primitives. It is unused by the entry claim; no K theorem connects it to `contractResult`. |
| V5 | 49-58 | `contractResult` is the rejection/acceptance decision tree | Result-constraining definitional summary that mirrors `solution.py`. It is neither fresh nor unconstrained. Its equivalence to V4 is ordinary Boolean reasoning but is not machine-checked here. |
| V6 | 62-136 | `solutionProgram` expands to the complete translated AST | Definitional program pin. Independent normalization found exact identity with regenerated `solution.mpy`; changing its successful return to `"No"` made the universal proof fail. |

## `spec.k` claim

| Location | Claim | Audit |
|---|---|---|
| `spec.k:6-8` | `<k> runProgram(solutionProgram,S:String) => contractResult(S) </k>` | No precondition: every K `String` is admitted. The sole cell is complete because the configuration has only `<k>`. The RHS is fixed by V5, not existential or tautological. There are no helper/loop claims. `kprove` closes it with `#Top`, while also warning it was trivial after definition simplification. |

## Imported trust boundary

`BOOL`, `INT`, `STRING`, and `domains.md` supply mathematical booleans and
integers, string length/comparison/slicing, and `countAllOccurrences`. These are
not candidate proof rules. Their agreement with CPython strings is an informal
language-model bridge supported only finitely by the preserved differential and
concrete tests. In particular, K's invalid-slice runtime behavior becomes
observable because candidate rule S12 speculatively evaluates a branch.
