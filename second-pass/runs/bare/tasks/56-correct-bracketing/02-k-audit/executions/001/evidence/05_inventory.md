# Static rule inventory

Source dependency closure reviewed: `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`.  Line numbers below refer
to those immutable candidate files.  `/candidate/expanded.k` is a derived
expansion containing the K built-ins and is neither required nor imported by
the source closure; the fresh rebuild did not copy or use it.

## Local syntax declarations

`semantic.k`:

| Lines | Sort | Every local production | Attributes / use |
|---|---|---|---|
| 8-9 | `Pgm` | `Module(Stmts)`, `correctProgram()` | The first parses `solution.mpy`; the second is a proof-facing duplicate/macro. |
| 11-13 | `Stmts` | empty-separated `List{Stmt,""}`, `targetLoopBody()`, `targetTail()` | The two nullary macros are `[function,total]`. |
| 14 | `Strings` | comma-separated `List{String,","}` | Function parameter list. |
| 16 | `Params` | `Params(Strings)` | Used by the function definition. |
| 18-22 | `Stmt` | `FuncDef`, `Assign`, `For`, `If`, `Return` | All five occur in `solution.mpy`. |
| 24-29 | `Expr` | `Name`, `Int`, `Bool`, `Str`, `BinOp`, `Compare` | All six occur in `solution.mpy`. |
| 31 | `CmpOp` | `CmpOp(String,Expr)` | Used for `==` and `<`. |
| 42 | `Value` | `IVal`, `BVal`, `SVal`, `SeqVal` | First three model real values; `SeqVal` is proof-only and cannot arise from the initial configuration. |
| 43 | `Function` | `function(Params,Stmts)` | Stored function closure without a captured environment. |
| 44 | `Store` | `emptyStore`, `bind(String,Value,Store)` | Persistent shadowing environment. |
| 45 | `Value` | `lookup(String,Store)` | `[function]`, intentionally partial for absent keys. |
| 51-63 | `KItem` | `invoke`, `functionBoundary`, `assignName`, `binopLeft`, `binopRight`, `compareLeft`, `compareRight`, `ifKont`, `forStart`, `forString`, `forBracketSeq`, `returnKont`, `finish` | Continuations; `forBracketSeq` is proof-only. |
| 73 | `Result` | `noResult`, `result(Value)` | Observable return cell. |

`verification.k`:

| Lines | Sort | Every local production | Attributes / use |
|---|---|---|---|
| 9-12 | `Bool` | `bracketSpec`, `bracketEmpty`, `bracketOpen`, `bracketNegative` | Each is `[function,total]`; mathematical string checker. |
| 28 | `BracketSeq` | `noBrackets`, `openBracket`, `closeBracket` | Proof-only free datatype representing strings over `<>`. |
| 29 | `Bool` | `bracketSeqSpec` | `[function,total]`; mathematical checker over the proof-only datatype. |

No local declaration has `[functional]`.  There are no local opaque
declarations, priorities, macros, aliases, simplification rules, or
`[concrete]` rules.  The operational sentinel `functionBoundary()` is
uninterpreted by itself but is consumed by the broad return continuation rule.

## Configuration and imports

`semantic.k:65-71` defines `<py>` with:

- `<k>` initially containing parsed `$PGM:Pgm` followed by
  `invoke("correct_bracketing", SVal($INPUT:String))`;
- `<functions>` initially `.Map`;
- `<env>` initially `emptyStore()`;
- `<result>` initially `noResult()`.

The definition imports K's `INT`, `BOOL`, `STRING`, and `MAP` modules and the
candidate `VERIFICATION` module.  The built-in integer, Boolean, string
substring/length/equality, and map-update operations are the low-level trusted
primitives.  The candidate has no heap, exceptions, output, or allocation
cells; none are needed by this submitted program.

## Every operational and definitional rule in `semantic.k`

| ID | Lines | Rule / role | Static judgment |
|---|---|---|---|
| S1 | 47 | Lookup matching head binding. | Correct for the shadowing store. |
| S2 | 48-49 | Skip a nonmatching head binding. | Correct; guard is disjoint from S1.  Lookup is intentionally stuck if absent. |
| S3 | 75 | Execute `Module(SS)` as `SS`. | Correct for this one-module IR. |
| S4 | 76-82 | Expand `targetLoopBody()`. | Exact textual AST of the two statements in the translated loop body.  Nullary total function with one equation. |
| S5 | 83-84 | Expand `targetTail()`. | Exact translated final return.  Nullary total function with one equation. |
| S6 | 88-94 | Expand `correctProgram()`. | Expands to the submitted AST only through S4/S5 macros.  The duplicate is currently extensionally identical, but no K claim or build dependency connects it to the bytes of `solution.mpy`. |
| S7 | 95 | Sequence a nonempty statement list. | Correct left-to-right list execution. |
| S8 | 96 | Consume `.Stmts`. | Correct empty-list behavior. |
| S9 | 98-99 | Register a function in `<functions>`. | Correct for the single submitted definition. |
| S10 | 101-103 | Invoke a one-argument function and reset the environment. | Correct for the sole top-level call; does not model nested-call environment restoration. |
| S11 | 105 | Wrap integer literal as `IVal`. | Correct. |
| S12 | 106 | Wrap Boolean literal as `BVal`. | Correct. |
| S13 | 107 | Wrap string literal as `SVal`. | Correct. |
| S14 | 108-109 | Resolve a name through `lookup`. | Correct for all reads in the submitted program, whose names are bound. |
| S15 | 111 | Evaluate assignment RHS before store update. | Correct. |
| S16 | 112-113 | Bind evaluated assignment value. | Correct shadowing assignment for this program. |
| S17 | 115 | Begin binary operation with left operand. | Correct left-to-right order. |
| S18 | 116 | After left value, evaluate right operand. | Correct. |
| S19 | 117 | Integer addition. | Correct via K unbounded integers; Python integers are also unbounded. |
| S20 | 118 | Integer subtraction. | Correct. |
| S21 | 120 | Begin comparison with left operand. | Correct left-to-right order. |
| S22 | 121-122 | After left value, evaluate comparison RHS. | Correct. |
| S23 | 123-124 | String equality. | Correct on the intended ASCII alphabet. |
| S24 | 125-126 | Integer equality. | Correct. |
| S25 | 127-128 | Integer less-than. | Correct. |
| S26 | 130 | Evaluate an `If` guard first. | Correct. |
| S27 | 131 | Select true branch. | Correct and disjoint from S28. |
| S28 | 132 | Select false branch. | Correct. |
| S29 | 134-135 | Evaluate `For` iterable first. | Correct. |
| S30 | 136-137 | Dispatch real `SVal` strings to `forString`. | Correct. |
| S31 | 138-139 | Dispatch proof-only `SeqVal` values to `forBracketSeq`. | Internally coherent, but it creates an alternate execution domain not reachable from `$INPUT:String`; no connection theorem relates it to S30. |
| S32 | 140-141 | End an empty string loop. | Correct. |
| S33 | 142-145 | Bind first string character, run body, recurse on suffix. | Correct for intended ASCII `<`/`>` strings; guards S32/S33 partition strings and the suffix shortens. |
| S34 | 146 | End an empty proof-only sequence loop. | Correct for its declared datatype. |
| S35 | 147-149 | Interpret `openBracket(BS)` as a `<` iteration. | Correct by the candidate's chosen datatype interpretation. |
| S36 | 150-152 | Interpret `closeBracket(BS)` as a `>` iteration. | Correct by that interpretation. |
| S37 | 154 | Evaluate return expression first. | Correct. |
| S38 | 155-156 | Discard `_REST:K` after `returnKont` and enter `finish`. | Correct on every reachable return of this one top-level function, where discarding the remaining loop/tail and `functionBoundary` models abrupt return.  It is over-broad for nested calls or an observable caller continuation, which the target does not use; this is a scope gap, not an intended-domain false-result witness. |
| S39 | 157-158 | Store the returned value and terminate. | Correct for the sole call. |

Rules S1-S39 are ordinary K rules/equations; none is a priority or
simplification rule.  S4 and S5 define `[function,total]` symbols.  S1/S2
define the non-total `lookup` function.

## Every proof helper rule in `verification.k`

| ID | Lines | Rule / role | Static judgment |
|---|---|---|---|
| V1 | 14 | `bracketSpec` tests whether the string is empty. | Correct. |
| V2 | 15 | Empty string returns `D == 0`. | Correct. |
| V3 | 16-17 | Nonempty string tests whether its first character is `<`. | Correct; called only after V1 established nonempty. |
| V4 | 18-19 | `<` consumes one character and increments `D`. | Correct and descending in string length. |
| V5 | 20-21 | Any non-`<` character computes whether decrement is negative. | Matches the submitted Python `else` branch; intended domain contains only `>`. |
| V6 | 22 | A negative prefix returns false. | Correct. |
| V7 | 23-24 | Otherwise consume one character and decrement `D`. | Correct and descending. |
| V8 | 31 | Empty `BracketSeq` returns `D == 0`. | Correct. |
| V9 | 32 | Open constructor consumes structurally and increments `D`. | Correct and descending structurally. |
| V10 | 33-34 | Close constructor at a would-be negative depth returns false. | Correct. |
| V11 | 35-36 | Close constructor at nonnegative resulting depth recurses with `D-1`. | Correct.  Guards V10/V11 are disjoint and exhaustive over integers. |

All V1-V11 are defining equations for the five `[function,total]` symbols.
Boolean cases and the close-constructor integer guards are exhaustive and
nonoverlapping, and both recursive checkers descend.  `bracketSpec` is not used
by any claim.  `bracketSeqSpec` constrains the synthetic-domain claims.

## Construct-to-rule coverage for `solution.mpy`

| Used translated construct | Declaration | Behavioral rules |
|---|---|---|
| `Module`, statement list | `semantic.k:8,11` | S3, S7, S8 |
| `FuncDef`, `Params` | `semantic.k:16,18` | S9 |
| `Assign`, `Name` | `semantic.k:19,24` | S1, S2, S14-S16 |
| integer/Boolean/string literals | `semantic.k:25-27` | S11-S13 |
| `For` over the actual string parameter | `semantic.k:20` | S29, S30, S32, S33 |
| `If` | `semantic.k:21` | S26-S28 |
| `BinOp("+")`, `BinOp("-")` | `semantic.k:28` | S17-S20 |
| string `==`, integer `==`, integer `<` | `semantic.k:29,31` | S21-S25 |
| `Return` | `semantic.k:22` | S37-S39 |
| function call supplied by the initial configuration | `semantic.k:51,65-71` | S9, S10, S37-S39 |

Thus the concrete semantics covers every construct used by the submitted MPY
tree.  Missing behavior for absent variables, nested calls, fall-through
functions, exceptions, non-string iteration, or other Python syntax is outside
this generated minimal semantics and is not a defect for this submitted
program.

## Claims

`spec.k` contains exactly seven reachability claims:

1. `loop-zero` (`9-17`): synthetic `BracketSeq` loop at depth zero.
2. `loop-positive` (`19-30`): the same at any positive depth.
3. `universal-correctness` (`35-43`): duplicated `correctProgram()` invoked
   with proof-only `SeqVal(BS)`.
4. Concrete `SVal("<")` result false (`45-50`).
5. Concrete `SVal("<>")` result true (`52-57`).
6. Concrete `SVal("<<><>>")` result true (`59-64`).
7. Concrete `SVal("><<>")` result false (`66-71`).

The two loop claims form a mutually recursive circularity component.  The
universal claim depends on that component.  The four concrete claims execute
the string path independently.

## Static conclusion

No local equation has a demonstrated false mathematical conclusion on the
intended input domain.  The material defect is instead theorem scope and
pinning: the only universal theorem runs the proof-only S31/S34-S36 path on
`SeqVal(BS)`, whereas the actual initial configuration and submitted-program
path run S30/S32-S33 on `SVal(String)`.  No claim proves these executions
equivalent.  In addition, the entry claim executes `correctProgram()` rather
than parsing the submitted file; the separate source mutation experiment shows
that K proof closure is insensitive to the actual MPY artifact.
