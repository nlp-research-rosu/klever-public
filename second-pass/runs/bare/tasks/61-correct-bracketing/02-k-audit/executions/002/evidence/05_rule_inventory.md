# Exhaustive local declaration and rule inventory

Line references are to the immutable candidate source as copied under
`/tmp/audit-work/61-correct-bracketing-audit/candidate/`.

## Local syntax and state

`semantic.k` declares all of the following productions:

- `Pgm`: `Module(Stmts)` and the audit/entry wrapper
  `Run(Pgm,String,String)` (lines 10–11).
- `Stmts`: the empty-separator `List{Stmt,""}` declaration (line 13), including
  its generated list unit and concatenation constructors.
- `Params`: `Params(String)` (line 14).
- `Stmt`: `FuncDef(String,Params,Stmts)`,
  `Assign(Expr,Expr)`, `For(Expr,Expr,Stmts)`,
  `If(Expr,Stmts,Stmts)`, and `Return(Expr)` (lines 16–20).
- `Expr`: `Name(String)`, `Int(Int)`, `Bool(Bool)`, `Str(String)`,
  `BinOp(String,Expr,Expr)`, and `Compare(Expr,CmpOp)` (lines 22–27).
- `CmpOp`: `CmpOp(String,Expr)` (line 29).
- `Value`: `intVal(Int)`, `boolVal(Bool)`, and `strVal(String)` (lines 39–41);
  `Value` is a subsort of `Expr` (line 42).
- `Function`: `function(Params,Stmts)` (line 44).
- Ten continuation `KItem`s: `invoke`, `assignTo`, `ifBranch`, `binLeft`,
  `binRight`, `compareLeft`, `compareRight`, `forStart`, `forLoop`, and
  `returnNow` (lines 46–55).

`verification.k` adds exactly two productions:

- zero-argument `solutionProgram : Pgm [function,total]` (line 9);
- `bracketSpec(Int,String) : Bool [function,total]` (line 30).

There are no local `functional`, `opaque`, `macro`, `strict`, `seqstrict`,
`priority`, `owise`, `anywhere`, or `concrete` declarations.  There are no
local priority rules.  The only local simplification rules are the four
`bracketSpec` equations below.

The configuration (semantic.k lines 57–62) has exactly:

- `<k>` for the current `Pgm`/computation;
- `<functions>` for function-name to function-body bindings;
- `<env>` for the active function's local bindings.

Every non-`k` cell is read or written.  No heap, I/O, exception, allocation, or
call-stack cell exists; the submitted program uses none of those effects and
has one top-level call.

## Ordinary semantic rules (semantic.k)

| ID | Lines | Rule role and complete judgment |
|---|---:|---|
| S01 | 65–66 | `Run(Module(SS),F,INPUT)` sequences module loading before `invoke(F,strVal(INPUT))`. Correct binding/evaluation order for the submitted one-module entry call. |
| S02 | 67 | `Module(SS) => SS`. Exposes the module statement list; exact for this IR. |
| S03 | 68 | Empty `Stmts` at the computation head becomes `.K`; correct list sequencing unit. |
| S04 | 69 | A statement head is executed before its tail; correct left-to-right statement order. |
| S05 | 71–72 | `FuncDef` installs/overwrites `F` with its exact params/body. The only definition is selected correctly. |
| S06 | 74–76 | `invoke` requires the selected map binding, installs the exact body, and resets locals to the single parameter. Exact for this non-nested one-argument call. |
| S07 | 79 | `Int(I) => intVal(I)`. Truthful literal injection. |
| S08 | 80 | `Bool(B) => boolVal(B)`. Truthful literal injection. |
| S09 | 81 | `Str(S) => strVal(S)`. Truthful literal injection. |
| S10 | 82–83 | `Name(X)` looks up the unique map value. Correct for every reachable lookup. |
| S11 | 85 | Begins `BinOp` by evaluating the left operand. |
| S12 | 86 | After the left value, evaluates the right operand while retaining the left. |
| S13 | 87 | Applies imported arbitrary-precision integer addition, with operands in the original left/right order. |
| S14 | 88 | Applies imported arbitrary-precision integer subtraction as left minus right. |
| S15 | 90 | Begins `Compare` by evaluating its left operand. |
| S16 | 91–92 | Evaluates the comparator after the left and retains the left. |
| S17 | 93–94 | Integer `==` returns the imported integer equality Boolean. |
| S18 | 95–96 | String `==` returns the imported string equality Boolean. |
| S19 | 99 | `Assign(Name(X),E)` evaluates `E` before mutation. |
| S20 | 100–101 | Existing-key assignment replaces exactly `X`; state footprint is only `<env>`. |
| S21 | 102–104 | Absent-key assignment inserts exactly `X`, guarded by `X` not in the map. Its guard is disjoint from S20. |
| S22 | 106 | `If` evaluates its guard before either branch. |
| S23 | 107 | A true Boolean guard selects only `THEN`. |
| S24 | 108 | A false Boolean guard selects only `ELSE`; guard cases are disjoint/exhaustive over reachable Booleans. |
| S25 | 110 | `Return(E)` evaluates `E` before returning. |
| S26 | 111 | A return value discards the complete active continuation and becomes the sole `<k>` result. This exactly models both early and final return in the single top-level call; no caller frame exists in the submitted program. |
| S27 | 115 | `For(Name(X),E,BODY)` evaluates the iterable before loop setup. |
| S28 | 116–117 | Existing loop target is initialized to `""`, then the loop starts. It is overwritten before every nonempty iteration. |
| S29 | 118–120 | Absent loop target is inserted as `""`, with a guard disjoint from S28. |
| S30 | 121 | Empty remaining string terminates the loop. |
| S31 | 122–127 | For an existing target and nonempty string, bind its first character, execute the exact body, then recurse on the suffix. |
| S32 | 128–134 | Same iteration step for an absent target; the absence guard is disjoint from S31. In the submitted path S29 has already inserted the target, so S31 is the recurring rule. |

S28/S29 have one exact-Python intermediate-state variance.  Witness:
`brackets == ""`. Python executes zero iterations and never binds local
`bracket`; K binds `"bracket" |-> strVal("")` before S30.  The variable is dead
after the loop, no expression reads it, the returned Boolean is unchanged, and
all entry claims existentially abstract the final local map.  Thus this does
not enable a false return-property conclusion for any intended input, but it is
a documented language-fidelity limitation.

For S31/S32, `substrString(S,0,1)` is the current character and
`substrString(S,1,lengthString(S))` is the strict suffix.  Prompt inputs are
ASCII parentheses, so K/Python text-index differences outside that alphabet
cannot affect the target theorem.  The 108-run concrete comparison exercised
empty, one-character, both branches, early return, nested loops, and long
strings without a mismatch.

## Verification-local equations (verification.k)

| ID | Lines | Class and judgment |
|---|---:|---|
| V01 | 9–23 | `solutionProgram` is a definitional summary, not an operational bridge. Its sole unguarded equation covers its zero-argument domain. K-parser comparison found its complete RHS constructor-identical to trusted regeneration. |
| V02 | 32 | Base equation: on the empty suffix, accept exactly when `N == 0`. Truthful. |
| V03 | 33–36 | Nonempty suffix beginning with `(` removes one character and increments `N`. Truthful, strictly descending in string length. |
| V04 | 37–39 | Nonempty non-`(` suffix at `N == 0` returns false, matching early rejection. Truthful. |
| V05 | 40–44 | Nonempty non-`(` suffix at `N > 0` removes one character and decrements `N`. Truthful, strictly descending. |

V02–V05 are `[simplification]` equations and a result-bearing definitional
summary.  Their guards are pairwise disjoint: empty/nonempty, first character
`(`/not `(`, and depth `0`/`>0`.  Both recursive equations strictly shorten
the string.  They completely cover every state reachable from `N >= 0`.

The `[total]` attribute on `bracketSpec` is broader than its equations:
`N < 0`, nonempty, first character not `(` has no equation.  Concrete witness
`bracketSpec(-1, ")")` remains unconstrained/stuck; the reachability probe
rejects a fixed `false` conclusion.  This gap cannot be reached from the loop
claim's `N >= 0` precondition and does not contribute to any entry proof.

There are no opaque result symbols and no operational bridge that replaces a
program construct.  `bracketSpec` is connected to fixed execution by the
separately proved universal `SPEC.loop` claim over all `N >= 0` and all
`String` suffixes; `SPEC.main` reuses that exact proved claim.

## Claims (spec.k)

- `SPEC.loop` (lines 9–32): exact real loop body and exact final-return
  continuation; requires `N >= 0`; returns exactly
  `boolVal(bracketSpec(N,S))`; final locals alone are existential.
- `SPEC.main` (lines 34–40): exact `Run(solutionProgram,...)` from empty maps;
  all K strings are admitted; return is exactly
  `boolVal(bracketSpec(0,S))`.
- Four ground example claims (lines 42–61): exact return Booleans for `"("`,
  `"()"`, `"(()())"`, and `")(()"`.

No claim has a free or unconstrained return value.  The existential variables
occur only in final `<functions>`/`<env>` cells.

## Submitted-constructor coverage

Every constructor in `solution.mpy` has syntax and an execution path:

- `Module`, `FuncDef`, `Params`, and statement-list sequencing: S02–S06.
- `Assign`, `Name`, `Int`: S07, S10, S19–S21.
- `For`: S27–S32.
- `If`, `Compare`, `CmpOp`, `Str`: S09, S15–S18, S22–S24.
- `BinOp("+")` and `BinOp("-")`: S11–S14.
- `Return` and `Bool(false)`: S08, S25–S26.

The claim-only `Run` wrapper is S01.  No used constructor is modeled by an
oracle, fabricated result, or unexercised catch-all.

## Imported trust boundary

The definition imports K's `INT`, `BOOL`, `STRING`, `MAP`, and `K-EQUAL`
modules.  Trusted operations that affect the result are arbitrary-precision
integer `+`, `-`, comparisons/equality; Boolean connectives; string equality,
length, substring; and finite-map lookup/update/membership.  These are fixed K
built-ins, outside the program-defined code and outside the candidate's local
proof extensions.  The backend, parser, and reachability/circularity machinery
are also trusted.
