# Reviewer rule inventory

This inventory covers every local declaration and rule in the candidate's
`semantic.k`, `solution-program.k`, `verification.k`, and `spec.k`. Imported K
`DOMAINS` primitives used on the proof path are listed at the end.

## `semantic.k`: syntax and configuration

- `Ids ::= List{String, ","}`, `Exprs ::= List{Expr, ","}`, and
  `Stmts ::= List{Stmt, ""}` are parser list sorts. The submitted tree uses a
  one-element parameter list, empty call-argument list, one-element function
  body, and one-element module body.
- `Params(String-list)` represents the translator's `Params`.
- `Expr` has six accepted constructors: `Name(String)`, `Str(String)`,
  `Int(Int)`, `Attribute(Expr,String)`, `Call(Expr,Exprs)`, and
  `BinOp(String,Expr,Expr)`. The submitted tree uses all except `Int`.
- `Stmt` has `Return(Expr)` and `FuncDef(String,Params,Stmts)`. Both are used.
- `Program` has `Module(Stmts)`, which is used.
- `Val` has `VStr(String)` and `VInt(Int)`. Both arise during evaluation.
- `KItem` has `invoke(String)`.
- The sole state is
  `<k> $PGM:Program ~> invoke($ARG:String) </k>`. This deliberately models a
  direct call to the one submitted pure function; no store, heap, I/O,
  exception, or call stack is represented.

## `semantic.k`: local functions and rules

There are no `[total]` or `[functional]` declarations here, no opaque
declarations, and no explicit priority rules.

1. `evalProgram(Program,String) [function]`.
   `evalProgram(Module(FuncDef("sort_numbers",Params("numbers"),Return(E))),S)
   => eval(E,S)`. The match pins the function name, one parameter, and one
   return body. It is a specialized but faithful direct-call semantics for the
   submitted shape. Unsupported shapes remain stuck.
2. `eval(Expr,String) [function]`.
   `eval(Name("numbers"),S) => VStr(S)`. Correct for the sole parameter and
   binding used by the submitted body; other names remain stuck.
3. `eval(Str(S),_) => VStr(S)`. Correct literal evaluation.
4. `eval(Int(I),_) => VInt(I)`. Correct for modeled integers, though unused by
   the submitted tree.
5. `eval(BinOp("+",E1,E2),S) =>
   addVals(eval(E1,S),eval(E2,S))`. Correct on the submitted pure string
   operands. Unsupported operand combinations remain stuck.
6. `eval(BinOp("*",E1,E2),S) =>
   multiplyVals(eval(E1,S),eval(E2,S))`. Correct on submitted
   string-times-integer operands. Evaluation order is not observable because
   every submitted operand is pure.
7. `eval(Call(Attribute(E,"count"),Str(Needle)),S) =>
   countVal(eval(E,S),Needle)`. Correct for the submitted string receiver and
   ten nonempty literal needles; unsupported call shapes remain stuck.
8. `eval(Call(Attribute(E,"strip"),.Exprs),S) =>
   stripVal(eval(E,S))`. Correct call-shape selection, but delegates to the
   over-broad `stripVal` rule below.
9. `addVals(Val,Val) [function]`.
   `addVals(VStr(S1),VStr(S2)) => VStr(S1 +String S2)`. Correct string
   concatenation; other types remain stuck.
10. `multiplyVals(Val,Val) [function]`.
    `multiplyVals(VStr(S),VInt(N)) => VStr(repeatString(S,N))`. Correct
    provided `repeatString` has the equations inventoried below.
11. `countVal(Val,String) [function]`.
    `countVal(VStr(S),Needle) =>
    VInt(countAllOccurrences(S,Needle))`. For every submitted nonempty
    numeral needle this matches Python's non-overlapping `str.count`.
12. `stripVal(Val) [function]`.
    `stripVal(VStr(S)) => VStr(trimTrailingSpace(S))`. This is false as a
    general model of Python `str.strip`: for the accepted alternate program
    `return numbers.strip()` and intended-domain input `"one"`, K proves
    `VStr("on")`, while CPython returns `"one"`. See
    `static-witnesses.k` execution evidence. On the submitted program's actual
    path, the receiver is either empty or a concatenation of one or more
    `"word "` blocks, so it has no leading whitespace and exactly one trailing
    ASCII space; on that restricted set, deleting the final character is
    correct.
13. `repeatString(String,Int) [function]`.
    `repeatString(_,N) => "" requires N <=Int 0
    [concrete(N),simplification]`. Correct for Python string repetition at
    nonpositive counts.
14. `repeatString(S,N) => S +String repeatString(S,N -Int 1)
    requires N >Int 0 [concrete(N),simplification]`. Correct, disjoint from
    the base rule, exhaustive over ground integers, and descending for
    positive `N`. The `[concrete]` attribute deliberately leaves symbolic
    instances summarized.
15. `trimTrailingSpace(String) [function]`.
    `trimTrailingSpace("") => ""`. Correct for the custom last-character
    removal function and for Python strip on the actual empty receiver.
16. `trimTrailingSpace(S) =>
    substrString(S,0,lengthString(S)-Int 1)
    requires lengthString(S)>Int 0 [concrete(S),simplification]`. Correct as
    the stated custom last-character deletion. It is not general strip
    semantics; its use is safe only under the actual receiver-shape argument.
    Its guard is disjoint from the empty rule.
17. Operational rule
    `<k> P:Program ~> invoke(S) => evalProgram(P,S) ...</k>`. It preserves any
    suffix framed by `...`, reads/writes only `<k>`, and introduces no abrupt
    control. On the submitted configuration it transfers the exact program and
    argument to the specialized evaluator.

## `solution-program.k`

All three declarations are constructor abbreviations (`[function]`), not
opaque program summaries.

1. `block(String,String) : Expr` expands exactly to
   `BinOp("*",Str(Printed),
   Call(Attribute(Name("numbers"),"count"),Str(Word)))`.
2. Literal `solutionBody : Expr` expands to the left-associated ten-block
   `+` tree followed by the zero-argument `strip` call. Word/printed pairs are
   `zero` through `nine` in numeric order.
3. Literal `solutionProgram : Program` expands to
   `Module(FuncDef("sort_numbers",Params("numbers"),Return(solutionBody)))`.

The audit-only `pinning-spec.k` reachability check normalized these
abbreviations to the byte-regenerated `solution.mpy` constructor tree and
printed `#Top`. A mutation inside the executed zero block produced the residual
`VStr("WRONG")`, confirming body sensitivity.

## `verification.k`

1. `sortSpec(String) [function]` has one unconditional equation. It returns
   the concatenation, in order zero through nine, of each `"word "` repeated
   `countAllOccurrences(input,word)` times, then removes the one trailing
   space. On the stated valid-token domain no numeral word is a substring of
   another; therefore this is the sorted token sequence with multiplicity.
   This is a definitional mathematical summary, not an operational rewrite of
   the program term.
2. `isNumeral(String) [function,total]` has ten exact true equations and one
   `[owise]` false equation. The `owise` guard excludes every exact case, so
   the equations are complete and non-overlapping.
3. `validNumerals(String) [function]` has four equations:
   - `validNumerals("") => true`;
   - a nonempty/no-space string reduces to `isNumeral(S)`;
   - a string whose first space is not trailing reduces to the conjunction of
     head validity and recursive tail validity;
   - a string whose first space is at `lengthString(S)-1` reduces to `false`.

   The first and fourth equations overlap at `S=""`, because
   `findString(""," ",0) = -1 = lengthString("")-1`. The compiled simplifier
   chooses the fourth rule: the audit claim `validNumerals("") => false`
   prints `#Top`, while `=> true` fails with residual `false`. This contradicts
   the function's own stated inclusion of the empty boundary. The symbol is
   absent from all submitted claims. A separate core definition deleting
   `isNumeral` and `validNumerals` rebuilt and reproved the universal claim
   with `#Top`, establishing non-dependence.

There are no other total declarations, no `[functional]` declarations, no
opaque symbols, no simplification rules, and no explicit priority rules in
`verification.k`.

## `spec.k`

There are five positive reachability claims and no helper/loop claims:

1. For every K `String S`, with no precondition, execution of
   `solutionProgram ~> invoke(S)` must terminate in `VStr(sortSpec(S))`.
2. The prompt example must return `VStr("one three five")`.
3. The duplicate case must return `VStr("zero one two two two")`.
4. The reverse all-numerals case must return the ascending all-numerals string.
5. The empty case must return `VStr("")`.

Every RHS constrains the entire final `<k>` value and consumes the computation.

## Imported `DOMAINS` trust boundary used on the proof path

- Hooked total string primitives: `+String`, `lengthString`, and
  `substrString`.
- Hooked string search `findString`.
- Hooked/defined `countAllOccurrences`, whose two equations split on
  `findString < 0` versus `>= 0` and, for the submitted nonempty needles,
  recursively discard the found prefix and one full occurrence. This matches
  non-overlapping Python `str.count`.
- Integer arithmetic/comparisons and Boolean conjunction/equality used in
  guards.

The intended tokens and all emitted blocks are ASCII, so no Unicode indexing
difference is material. These installed K primitives are low-level trusted
operations rather than task-answer oracles.
