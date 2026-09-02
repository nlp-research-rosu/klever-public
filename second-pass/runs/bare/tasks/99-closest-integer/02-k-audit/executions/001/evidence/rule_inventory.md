# Exhaustive local declaration and rule inventory

Line references are to the candidate source copied unchanged to
`/tmp/audit-work/99-closest-integer/source/`.

## Syntax, configuration, and attributes

`semantic.k` declares:

| ID | Lines | Declaration / constructor | Role |
|---|---:|---|---|
| D01 | 5 | `Program ::= Module(Stmts)` | Submitted constructor-term root. |
| D02 | 7 | `Stmts ::= List{Stmt,""}` | Ordered statement list; `.Stmts` is empty. |
| D03 | 8 | `Stmt ::= ImportFrom(String,String)` | Exact import form. |
| D04 | 9 | `Stmt ::= FuncDef(String,Params,Stmts)` | Function definition. |
| D05 | 10 | `Stmt ::= Assign(Expr,Expr)` | Assignment. |
| D06 | 11 | `Stmt ::= If(Expr,Stmts,Stmts)` | Conditional. |
| D07 | 12 | `Stmt ::= Return(Expr)` | Return statement. |
| D08 | 14 | `Params ::= Params(String)` | One named parameter. |
| D09 | 16 | `Expr ::= Name(String)` | Variable/builtin name. |
| D10 | 17 | `Expr ::= Int(Int)` | Integer literal. |
| D11 | 18 | `Expr ::= Str(String)` | String literal. |
| D12 | 19 | `Expr ::= Call(Expr,Expr)` | One-argument call. |
| D13 | 20 | `Expr ::= BinOp(String,Expr,Expr)` | Binary operation. |
| D14 | 21 | `Expr ::= Compare(Expr,CmpOp)` | Comparison. |
| D15 | 23 | `CmpOp ::= CmpOp(String,Expr)` | Operator plus right operand. |
| D16 | 37 | `Value ::= pyInt(Int)` | Python integer model. |
| D17 | 38 | `Value ::= pyStr(String)` | Concrete Python string model. |
| D18 | 39 | `Value ::= pyBool(Bool)` | Python Boolean model. |
| D19 | 40 | `Value ::= exactNum(Int,Int)` | Exact rational representation. |
| D20 | 41 | `Value ::= rationalString(Int,Int)` | Abstract symbolic numeric-string input. |
| D21 | 43 | `Result ::= noResult` | No function result yet. |
| D22 | 43 | `Result ::= Value` | Completed result. |
| D23 | 45 | `KItem ::= exec(Stmts)` | Statement-list continuation. |
| D24 | 46 | `KItem ::= assignTo(String)` | Assignment continuation. |
| D25 | 47 | `KItem ::= toDecimal` | `Decimal` conversion continuation. |
| D26 | 48 | `KItem ::= toInt` | `int` conversion continuation. |
| D27 | 49 | `KItem ::= ifControl(Stmts,Stmts)` | Branch continuation. |
| D28 | 50 | `KItem ::= binLeft(String,Expr)` | Evaluate left operand first. |
| D29 | 51 | `KItem ::= binRight(String,Value)` | Evaluate right operand second. |
| D30 | 52 | `KItem ::= compareLeft(String,Expr)` | Compare-left continuation. |
| D31 | 53 | `KItem ::= compareRight(String,Value)` | Compare-right continuation. |
| D32 | 54 | `KItem ::= returnControl` | Return continuation. |
| D33 | 56–62 | `<mpy>` configuration with `<k>`, `<arg>`, `<env>`, `<result>` | Program, immutable configured argument, variable map, and result. No heap, I/O, exception, decimal-context, or call-stack cell exists. |
| D34 | 121 | `exponentPosition(String):Int [function,total]` | Chooses lowercase `e` if present, otherwise uppercase `E` position. This is the only local `[total]` declaration. |
| D35 | 127 | `parseDecimal(String):Value [function]` | Decimal-parser entry. |
| D36 | 128 | `parseExponent(String,Int):Value [function]` | Parses mantissa/exponent at a supplied position. |
| D37 | 129 | `parseMantissa(String):Value [function]` | Parses a non-exponent mantissa. |
| D38 | 130 | `parseMantissaAt(String,Int):Value [function]` | Removes a decimal point at a supplied position. |
| D39 | 131 | `scaleDecimal(Value,Int):Value [function]` | Multiplies/divides an exact rational by a power of ten. |

`verification.k` adds:

| ID | Lines | Declaration | Role |
|---|---:|---|---|
| D40 | 8 | `solutionProgram:Program [function]` | Inline name for the submitted constructor term. |
| D41 | 24 | `roundNearestAway(Int,Int):Int [function]` | Mathematical exact-rational rounding summary. |

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
macro, anywhere, or opaque-function declarations. There are no proof-local
ordinary operational rules outside the three function equations in
`verification.k`. `rationalString(N,D)` is not an uninterpreted function, but
it is a result-bearing abstract input constructor whose claimed relationship
to real `pyStr` inputs is not established by a connection theorem.

## `semantic.k` rule inventory

| ID | Lines | Rule | Classification and audit judgment |
|---|---:|---|---|
| S01 | 65–70 | Exact `Module(ImportFrom("decimal","Decimal") FuncDef("closest_integer",Params(P),BODY))` starts `exec(BODY)` and binds `P` to `<arg>` | Operational entry bridge. It matches the submitted module exactly, initializes the only supported frame correctly, and changes only `<k>`/`<env>`. Module/import/function-declaration side effects and lookup errors are outside the model. Sound for this exact target invocation, conditional on the external `Decimal` binding. |
| S02 | 72 | `exec(.Stmts) => .K` | Correct empty-sequence completion. |
| S03 | 73 | `exec(S SS) => S ~> exec(SS)` | Correct left-to-right statement sequencing. |
| S04 | 74 | `Assign(Name(X),E) => E ~> assignTo(X)` | Correct target-first/name-fixed assignment evaluation for the used simple-name targets. |
| S05 | 75–76 | Value plus `assignTo(X)` updates `ENV[X]` | Correct assignment state update. |
| S06 | 79 | `Int(I) => pyInt(I)` | Correct arbitrary-precision Python integer literal for the used literal `0`. |
| S07 | 80 | `Str(S) => pyStr(S)` | Correct string literal for `"0.5"`. |
| S08 | 81–82 | `Name(X)` map lookup | Correct lookup when bound; unbound-name exceptions are deliberately unmodeled. |
| S09 | 85 | `Call(Name("Decimal"),E)` evaluates `E` then `toDecimal` | Correct argument-before-call order for the pinned builtin name. Binding/import validation is supplied only by S01’s exact module pattern. |
| S10 | 86 | `pyStr(S) ~> toDecimal => parseDecimal(S)` | Operational bridge for the external `Decimal(str)` primitive. Sound for the implemented finite ordinary/scientific subset; valid forms such as surrounding whitespace/underscores and exceptional Decimal values are not fully modeled. Stuckness is incompleteness, not a witnessed false return. |
| S11 | 87 | `rationalString(N,D) ~> toDecimal => exactNum(N,D)` | Result-bearing abstract-input bridge. For `D>0`, it truthfully states the explicitly named exact-rational contract used by all symbolic target claims. There is no universal connection to concrete `pyStr` parsing, and the rule itself omits `D>0`; target claims impose it. The over-broad off-domain rule is a validation gap, not the source of the intended-domain false witness below. |
| S12 | 88 | `Call(Name("int"),E)` evaluates `E` then `toInt` | Correct evaluation order for the pinned builtin. |
| S13 | 89 | `int(pyInt(I)) => pyInt(I)` | Correct. |
| S14 | 90–91 | `int(exactNum(N,D)) => pyInt(N /Int D)` for `D>0` | Correct truncation toward zero for a finite exact Decimal value, as confirmed on positive and negative tests. |
| S15 | 94 | Begin `BinOp` by evaluating left operand | Correct left-to-right order. |
| S16 | 95 | Store left value and evaluate right operand | Correct left-to-right order. |
| S17 | 96–98 | Add two `exactNum` values by exact cross multiplication | **Materially unsound as Python `Decimal` semantics.** `Decimal` addition is rounded under the ambient context (default precision 28); the K rule is unbounded exact arithmetic and there is no context cell. Witness: input `"9999999999999999999999999999.4"` makes real Python return `10000000000000000000000000000`, while this rule lets K/proof return `9999999999999999999999999999`. See `decimal_context_witness.log` and `unsound_witness_proof.log`. |
| S18 | 99–101 | Subtract two `exactNum` values by exact cross multiplication | **Materially unsound for the same reason.** Witness: input `"-9999999999999999999999999999.4"` makes Python return `-10000000000000000000000000000`, while K/proof returns `-9999999999999999999999999999`. |
| S19 | 103–104 | Begin comparison by evaluating the left operand | Correct. |
| S20 | 105–106 | Store left comparison value and evaluate right | Correct. |
| S21 | 107–109 | `exactNum(N1,D1) >= pyInt(I2)` becomes `N1 >= I2*D1`, `D1>0` | Correct exact comparison; Decimal comparisons are not rounded by context for finite operands. |
| S22 | 112 | Evaluate `If` guard then `ifControl` | Correct. |
| S23 | 113 | True guard executes then-list | Correct. |
| S24 | 114 | False guard executes else-list | Correct. |
| S25 | 115 | Evaluate return expression then `returnControl` | Correct. |
| S26 | 116–117 | Returned value discards the remaining K continuation and sets result from `noResult` | Correct abrupt return for the one-frame language subset used here. It is broad over arbitrary `_REST`, but no modeled user-call stack, cleanup, or exception frame exists; no intended-program counterexample was found. |
| S27 | 122–123 | Lowercase exponent position when lowercase `e` exists | True by definition. |
| S28 | 124–125 | Otherwise return uppercase `E` position | Guard-disjoint with S27 and covers all strings, justifying `[total]`; returns `-1` if neither occurs. |
| S29 | 133–134 | No exponent: parse mantissa | Correct dispatch. |
| S30 | 135–136 | Exponent present: parse at its position | Correct dispatch; guards are disjoint/complete. |
| S31 | 137–140 | Split mantissa/exponent, parse and scale | Correct when `P` is the exponent position supplied by S30. The public helper guard merely says `P>=0`, so direct off-context calls are over-broad; no such call is reachable from the target program. |
| S32 | 142–143 | No dot: `String2Int(S)/1` | Correct for supported integer strings; malformed inputs get stuck. |
| S33 | 144–145 | Dot present: parse at dot position | Correct dispatch; disjoint/complete with S32. |
| S34 | 146–151 | Remove the dot and use denominator `10^(digits-after-dot)` | Correct for supported mantissas when `P` is the actual dot position supplied by S33. Like S31, its direct-call guard is broader than that invariant. |
| S35 | 153–154 | Nonnegative exponent multiplies numerator by `10^E` | Correct exact scaling. |
| S36 | 155–156 | Negative exponent multiplies denominator by `10^(-E)` | Correct exact scaling. Guards with S35 are disjoint and complete. |

## `verification.k` rule inventory

| ID | Lines | Rule | Classification and audit judgment |
|---|---:|---|---|
| V01 | 9–20 | `solutionProgram` expands to an inline constructor term | Definitional program name. The right-hand side is parse-identical to trusted-translator-regenerated `solution.mpy`; `pinning-spec.k` closes (the frontend reports it as trivial after function simplification). It does not itself read the file at proof time, so identity remains an audited source-to-term bridge. |
| V02 | 25–27 | Nonnegative `roundNearestAway(N,D)` | Truthful exact-rational formula for `N>=0,D>0`; integer division truncates after adding one half. |
| V03 | 28–30 | Negative `roundNearestAway(N,D)` | Truthful exact-rational formula for `N<0,D>0`; integer division truncates toward zero after subtracting one half. Guards are disjoint and cover every target use because all claims require `D>0`. |

## Construct coverage and state/control map

Every constructor in `solution.mpy` is covered:

- `Module`, `ImportFrom`, `FuncDef`, and `Params` are consumed by S01.
- Statement-list concatenation/emptiness, both assignments, the `If`, and both
  `Return` sites use S02–S05 and S22–S26.
- `Name`, `Int`, and `Str` use S06–S08.
- `Call(Name("Decimal"),...)` and `Call(Name("int"),...)` use S09–S14.
- `BinOp("+",...)` and `BinOp("-",...)` use S15–S18.
- `Compare(...,CmpOp(">=",Int(0)))` uses S19–S21.

Evaluation is explicitly left-to-right. The environment records `value`,
`number`, and `half`; assignment updates it and return updates only `<result>`.
No allocation, heap, I/O, or user-defined nested calls occur in the submitted
program. The absent decimal-context cell is material because S17/S18 depend on
that state. Exceptions and several accepted `Decimal` string spellings are also
unmodeled, but those omissions yield stuck paths rather than the concrete false
normal return witnessed for S17/S18.
