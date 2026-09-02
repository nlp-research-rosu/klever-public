# Reviewer rule and declaration inventory

This inventory covers every candidate-local declaration in `semantic.k` and
`verification.k`. Imported K `BOOL`, `INT`, and `STRING` hooks are separately
accounted for as trusted primitives; no candidate helper K files exist.

## Local syntax

`semantic.k:10-31` declares:

1. `Exprs ::= List{Expr, ","}`.
2. `Params ::= Params(String)`.
3. Ten `Expr` constructors: `Name(String)`, `Str(String)`, `Bool(Bool)`,
   `Int(Int)`, `UnaryOp(String, Expr)`, `Attribute(Expr, String)`,
   `Call(Expr, Exprs)`, `IfExp(Expr, Expr, Expr)`,
   `GenExp(Expr, CompFor)`, and `Subscript(Expr, SliceSpec)`.
4. `CompFor ::= CompFor(Expr, Expr, Exprs)`.
5. `SliceBound ::= NoBound | Expr`.
6. `SliceSpec ::= Slice(SliceBound, SliceBound, SliceBound)`.
7. Two `Stmt` constructors: `Return(Expr)` and
   `FuncDef(String, Params, Stmts)`.
8. `Stmts ::= List{Stmt, ""}`.
9. `Program ::= Module(Stmts)`.

`semantic.k:42-45,54,58,66,70,74-75,80,87-88,104` additionally declares:

10. `PString` constructors `.PString` and `Int :: PString`.
11. Functions `pstr(String):PString` and `pstrAt(String,Int):PString`;
    neither is declared `total`.
12. Total functions `isAlpha(Int):Bool`, `toggle(Int):Int`,
    `hasAlpha(PString):Bool`, `swapCase(PString):PString`,
    `reverse(PString):PString`, `reverseAcc(PString,PString):PString`, and
    `ifPString(Bool,PString,PString):PString`.
13. Partial functions `evalBool(Expr,PString):Bool` and
    `evalString(Expr,PString):PString`.
14. `Result ::= noResult | PString`.

`verification.k:8` declares the total function
`expected(PString):PString`.

There are no candidate-local `[functional]` declarations, opaque symbols,
priorities, strictness declarations, simplification rules, macros, aliases, or
local syntax precedence groups.

Unused-but-declared source constructors are `Str`, `Bool` as an ordinary
expression except for the generator sentinel, and `Int` except below unary
minus. Generated-semantics mode permits such unused declarations; they do not
need operational rules because the submitted AST never requests their
standalone evaluation.

## Configuration and construct coverage

`semantic.k:106-111` has exactly three cells under `<humanEval>`:
`<k>` for the submitted `Program`, `<input>` for its already supplied
`PString` argument, and `<result>` initially `noResult`. The program is pure, so
the absence of heap, output, exception, and mutable-environment cells is
reasonable only for the exact submitted body.

The submitted `solution.mpy` maps as follows:

| Submitted constructor | Declaration | Operational rule |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | lines 11, 28-31 | whole-program rule, lines 113-115 |
| `IfExp` | line 20 | `evalString(IfExp...)`, lines 96-97 |
| `Call(Name("any"), GenExp(...))` | lines 13, 19, 21 | `evalBool`, lines 90-94 |
| `Attribute(...,"isalpha")`, `CompFor`, `Bool(true)` | lines 15, 18, 24, 16 | same `evalBool` rule |
| `Call(Attribute(Name("s"),"swapcase"),...)` | lines 13, 18 | swapcase bridge, line 98 |
| `Subscript`, `Slice`, `NoBound`, `UnaryOp("-",Int(1))` | lines 17, 21, 25-26, 16 | reverse-slice bridge, lines 99-102 |

Thus every submitted constructor parses and reaches a rule, but the rules'
value fidelity must still be checked against Python.

## Exhaustive rule assessment

1. **`pstr(S) => pstrAt(S,0)` (line 47).** Definitional entry into the
   concrete-input converter; it is not used by the symbolic claim.
2. **`pstrAt` base (lines 48-49).** Mathematically consistent with the selected
   K `lengthString` hook when the index reaches the hook's measured length.
3. **`pstrAt` step (lines 50-51).** Intended as a Python-string-to-code-point
   bridge, but it is not faithful for all non-ASCII K strings. Fresh execution
   on `pstr("αΒ")` produces input `206::177::206::146`, the UTF-8 bytes, not
   Unicode code points `945::914`; see `stage5-pstr-multibyte-witness.log`.
   This makes the comment at lines 1-3 and concrete bridge false. It is not used
   by the symbolic claim, but it invalidates generated-semantics concrete
   fidelity.
4. **`isAlpha` (lines 55-56).** A coherent total definition of ASCII
   alphabeticity, but not Python `str.isalpha`. Witness on the intended domain:
   Python `"é".isalpha()` is true while `isAlpha(233)` is false.
5. **`toggle` uppercase (lines 59-60).** Correct ASCII case mapping on
   `65..90`.
6. **`toggle` lowercase (lines 61-62).** Correct ASCII case mapping on
   `97..122`.
7. **`toggle` fallback (lines 63-64).** Completes the local ASCII definition,
   disjointly from rules 5 and 6, but is false as a model of Python
   `swapcase`: `toggle(233)=233`, whereas `"é".swapcase()` is `"É"`
   (code point 201).
8. **`hasAlpha(.PString) => false` (line 67).** Correct base case for the local
   predicate.
9. **`hasAlpha(C::S)` (line 68).** Structurally terminating and correct
   relative to local `isAlpha`; because rule 4 is only ASCII, it is not a
   faithful model of `any(c.isalpha() for c in s)`.
10. **`swapCase(.PString)` (line 71).** Correct base case for the local
    operation.
11. **`swapCase(C::S)` (line 72).** Structurally terminating and correct
    relative to local `toggle`; because rule 7 is not Unicode swapcase, it is
    not faithful to `str.swapcase`.
12. **`reverse(S)` (line 76).** Correctly initializes a standard accumulator
    reversal over abstract `PString`.
13. **`reverseAcc(.PString,ACC)` (line 77).** Correct reversal base.
14. **`reverseAcc(C::S,ACC)` (line 78).** Correct, structurally decreasing
    reversal step. Rules 12-14 are disjoint/exhaustive for normalized abstract
    `PString` lists.
15. **`ifPString(true,THEN,_)` (line 81).** Correct true selection.
16. **`ifPString(false,_,ELSE)` (line 82).** Correct false selection. Rules 15
    and 16 are disjoint and exhaustive over `Bool`.
17. **`evalBool(any/isalpha generator,S) => hasAlpha(S)` (lines 90-94).**
    Result-bearing operational bridge. Its exact submitted-program instance is
    false over the intended Python-string domain: with
    `S=233::.PString` (`"é"`), the real generator yields true, while the rule
    yields false. The rule also ignores arbitrary `_ARGS` and `_IFS`; those
    broaden it beyond the submitted empty argument lists and `Bool(true)`
    generator sentinel. That extra overbreadth is not needed for the concrete
    witness and has no universal bridge theorem.
18. **`evalString(IfExp...)` (lines 96-97).** Pure conditional-selection
    summary. Its local equation is coherent for the submitted total branches,
    but it inherits the false test and branch-value bridges from rules 17 and
    19. No generic environment or exception semantics supports its much
    broader arbitrary-expression match domain.
19. **`evalString(s.swapcase(),S) => swapCase(S)` (line 98).**
    Result-bearing operational bridge and false on an intended input:
    `S=233::.PString` returns `233::.PString`; the real submitted Python call
    returns `"É"` (`201::.PString`). See
    `stage3-krun-direct-unicode-codepoint.log` and the Python comparison in
    `stage3-semantic-concrete-differential.log`.
20. **`evalString(s[::-1],S) => reverse(S)` (lines 99-102).** Correct over an
    abstract `PString` code-point list for the exact submitted slice. It does
    not repair the faulty `pstr` bridge; concrete `pstr("αΒ")` reverses bytes.
21. **whole-program rule (lines 113-115).** Operational bridge from the exact
    one-function `solve(s)` module to evaluating its return expression with
    the implicit `<input>`. It consumes the submitted program body and writes
    only `<result>`, so it does not bypass that body syntactically. However, it
    inherits false rules 17 and 19. Witness: with input `233::.PString`, the
    complete fresh K execution returns 233 while the submitted Python program
    returns 201.
22. **`expected(S)` (verification line 9).** Exhaustive definitional summary
    with no overlaps. It does not replace execution, but it repeats exactly the
    same `hasAlpha/swapCase/reverse` expression produced by rules 17-21. It is
    therefore not an independent connection to the prompt or canonical
    implementation and inherits their false Unicode interpretation.

All explicitly total local functions have exhaustive, non-overlapping
equations over their *local* K domains, and the recursive equations descend on
`PString`. This logical consistency explains the reconstructed `#Top`; it does
not make the operational bridges faithful to Python.
