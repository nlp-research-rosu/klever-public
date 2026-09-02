# Reviewer static inventory

This inventory covers every local declaration and rule in the submitted
`semantic.k` and `verification.k`.  Line numbers refer to the immutable
candidate files; the scratch copies are byte-identical.

## Configuration, imports, and declarations

| ID | Lines | Declaration | Static decision |
|---|---:|---|---|
| D1 | semantic.k:1 | `requires "domains.md"` | Imports the installed K domains definition; treated as a toolchain primitive. |
| D2 | 3–6 | `MPY-SYNTAX` importing `INT-SYNTAX`, `BOOL-SYNTAX`, `STRING-SYNTAX` | Appropriate lexical bases. |
| D3 | 8 | `FloatLiteral` regex token | Declared but unused by `solution.mpy`; notably there is no `eval(Float(...))` rule. Missing behavior is not material for this submitted body. |
| D4 | 10 | `Pgm ::= Module(Stmts)` | Used by the submitted module. |
| D5 | 12 | `Stmts ::= List{Stmt, ""}` | Used for all function-body statement sequences and empty branches. |
| D6 | 13 | `Names ::= List{String, ","}` | Used by `Params("a","b")`. |
| D7 | 14 | `Params ::= Params(Names)` | Used by the function definition. |
| D8 | 15 | `Exprs ::= List{Expr, ","}` | Used by calls. |
| D9 | 16 | `CmpOps ::= List{CmpOp, ","}` | Used by comparisons. |
| D10 | 18–21 | `Stmt` alternatives: `FuncDef`, `Assign`, `If`, `Return` | Exactly the statement forms used by the program. |
| D11 | 23–30 | `Expr` alternatives: `Name`, `Int`, `Float`, `Str`, `NoneVal`, `Call`, `Attribute`, `Compare` | All program expression forms are declared; `Int` and `Float` literals are not used in this body. |
| D12 | 32 | `CmpOp(OP, Expr)` | Used for `==` and `>`. |
| D13 | 34–39 | `PyVal`: integer, rational-float, string, bool, type, None | Supplies the modeled input/result universe. `pyFloat(N,D)` has no constructor invariant enforcing nonzero/positive `D` or binary64 representability. |
| D14 | 42–48 | `MPY-SEMANTIC` imports syntax, Bool, Int, String, Map, K equality | Appropriate built-in domains; their hooks are in the trusted toolchain boundary. |
| D15 | 50–56 | `<mpy>` configuration: `<k>`, `<functions>`, `<env>`, `<result>` | Minimal state for the submitted single function. No exception, call-stack, or output cells exist. |
| D16 | 58 | `Function ::= function(Params,Stmts)` | Stored function representation. |
| D17 | 59–60 | `KItem ::= execute(Stmts) \| invoke(PyVal,PyVal)` | Internal control forms. |
| D18 | 87 | `eval(Expr,Map) [function]` | Partial meta-level expression evaluator. This avoids operational evaluation contexts; valid only while the modeled expressions are pure and the equations accurately implement their operations. |
| D19 | 88 | `typeOf(PyVal) [function,total]` | Six constructor equations cover the six normal `PyVal` constructors. `[total]` is not itself a proof. |
| D20 | 89 | `pyFloatOf(PyVal) [function]` | Partial conversion function; materially disagrees with Python binary64 conversion. |
| D21 | 90 | `pyReplace(...) [function]` | Partial, but all reachable submitted uses pass three strings. |
| D22 | 91 | `pyCompare(...) [function]` | Partial, but submitted reachable calls use supported type equality and rational equality/greater-than. |
| D23 | 127–129 | `parseDecimal`, `parseUnsignedDecimal`, `decimalDigits` `[function]` | Exact-decimal parser, not Python's `float` parser. It omits scientific notation and binary64 rounding. |
| D24 | 155–157 | `MPY` imports `MPY-SEMANTIC` | Concrete main module. |
| D25 | verification.k:1–4 | `VERIFICATION` imports the submitted semantics | No separate proof-local helper theory. |
| D26 | verification.k:8 | `Pgm ::= theSolution [macro]` | Semantically inert syntax macro if its expansion is the submitted constructor term; fresh KORE comparison establishes exact identity. |

There are no local `[simplification]`, `[functional]`, `[concrete]`, priority,
`owise`, or opaque-symbol declarations.  The only local `[total]` declaration
is `typeOf`; the only local `[macro]` declaration is `theSolution`.

## Rule-by-rule inventory

| ID | Lines | Rule role | Static decision |
|---|---:|---|---|
| R1 | semantic.k:62 | `Module(SS) => execute(SS)` | Faithful module-sequence entry for the submitted subset. |
| R2 | 63 | `execute(.Stmts) => .K` | Faithful empty-sequence completion. |
| R3 | 64 | `execute(S REST) => S ~> execute(REST)` | Faithful left-to-right statement sequencing. |
| R4 | 66–67 | `FuncDef` stores `function(PS,BODY)` | Faithful for a definition-only module; no decorators/defaults are in the source. |
| R5 | 69–71 | `invoke(A,B)` looks up exact `compare_one`, installs `a,b`, executes body | Pins the binding and two arguments used by this task. It is intentionally not reusable Python call semantics (no argument evaluation, outer environment, call stack, defaults, or exceptions), but those features are absent from this entry execution. |
| R6 | 73–74 | assignment writes `eval(E,ENV)` | Correct for pure supported expressions, conditional on `eval` equations. It erases Python exception behavior. |
| R7 | 76–78 | true `If` branch | Correct conditional branch when `eval` yields true. |
| R8 | 79–81 | false `If` branch | Correct conditional branch when `eval` yields false. The two guards are disjoint for `pyBool`. |
| R9 | 83–85 | `Return(E) ~> _ => .K`, set result | Correctly discards the remaining function-body continuation in this execution. Its declared match accepts any complete continuation and has no call-frame delimiter, so it is over-broad as reusable language semantics; no submitted reachable witness places observable computation after the function return. |
| R10 | 93 | environment name lookup | Correct when the key exists. |
| R11 | 94 | `Name("str") => pyType("str")` | Correct for the unshadowed builtin in this program. It overlaps R10 if an environment contains `"str"`; that state is not reached by this body, but the reusable binding model is not globally deterministic there. |
| R12 | 95 | integer literal to `pyInt` | Correct but unused by the submitted body. |
| R13 | 96 | string literal to `pyStr` | Correct and used for comma/dot replacement literals. |
| R14 | 97 | `NoneVal => pyNone` | Correct. |
| R15 | 99 | modeled `type(E)` | Correct for built-in values in the source domain, conditional on R19–R24. |
| R16 | 100 | modeled `float(E)` via `pyFloatOf` | This operation executes, but its value semantics is materially false for Python because R25–R27 use exact rationals. |
| R17 | 101–102 | modeled string `.replace(old,new)` | Correct for the program's string-only, all-occurrences replacement. Argument evaluation is represented as a pure equation; no side effects occur here. |
| R18 | 103–104 | comparison dispatch | Correct dispatcher for the program's one comparison operator and operand. |
| R19 | 106 | `typeOf(pyInt) => "int"` | Correct for modeled base integers. |
| R20 | 107 | `typeOf(pyFloat) => "float"` | Correct under the representation contract. |
| R21 | 108 | `typeOf(pyStr) => "str"` | Correct and controls replacement branches. |
| R22 | 109 | `typeOf(pyBool) => "bool"` | Correct but source-domain inputs exclude booleans. |
| R23 | 110 | `typeOf(pyNone) => "NoneType"` | Correct but source-domain inputs exclude None. |
| R24 | 111 | `typeOf(pyType) => "type"` | Correct, used for comparing the result of `type` to builtin `str`. |
| R25 | 113 | `pyFloatOf(pyInt(I)) => pyFloat(I,1)` | **Materially invalid bridge to Python.** Witness on the intended integer domain: `I=9007199254740993`, `J=9007199254740992`. Python converts both to the same binary64 number and returns `None`; R25 preserves distinct exact integers, after which R30/R31 make K return `I`. |
| R26 | 114 | `pyFloatOf(pyFloat(N,D))` is identity | Conditional representation assumption, not Python conversion semantics. A normalized exact binary rational could represent a finite Python float, but the syntax/spec quantify arbitrary positive-denominator rationals, including values not representable as Python floats. |
| R27 | 115 | `pyFloatOf(pyStr(S)) => parseDecimal(S)` | **Materially invalid bridge to Python.** The intended numeric string `"9007199254740993"` rounds in Python to `9007199254740992`; the exact parser preserves the larger integer and K returns the string instead of `None`. |
| R28 | 117–118 | `pyReplace` via `replaceAll` | Correct for K's string hook and Python's all-occurrences replacement on the program literals. |
| R29 | 120–121 | type equality | Correct string equality. |
| R30 | 122–123 | rational equality by cross multiplication | Correct when both denominators are nonzero; the submitted float claims require positive denominators and parser outputs positive denominators. The rule itself has no denominator guard. |
| R31 | 124–125 | rational greater-than by cross multiplication | Correct only when `D1*D2 > 0`; submitted symbolic claims require both positive. The declared unguarded rule is false on other syntactic states—for example it reports `pyFloat(1,-1) > pyFloat(0,1)` because `1*1 > 0*(-1)`, although `-1 > 0` is false. Negative-denominator states are not a demonstrated Python-input encoding, so this is an over-broad reusable-rule defect rather than the intended-domain counterexample used for the verdict. |
| R32 | 131–134 | strip a leading minus and parse with sign -1 | Correct exact-decimal sign handling for the accepted grammar. |
| R33 | 135–137 | otherwise parse with sign +1 | Guards are disjoint from R32 and cover empty/non-leading-minus strings. |
| R34 | 139–141 | no-dot decimal to exact integer rational | Correct only for a digit string accepted by `String2Int`; it does not apply binary64 rounding and therefore contributes to R27's false witness. |
| R35 | 142–149 | one-dot decimal to exact base-10 rational | Correct exact-decimal arithmetic for digit-only prefix/suffix, but not Python binary64 conversion. Multiple dots or exponent suffixes reach invalid `String2Int`. |
| R36 | 151 | empty digit segment to zero | Useful for `.5`/`5.` segments. At top level it also makes `parseDecimal("")` return zero even though Python `float("")` raises, but the source contract excludes an empty string as not representing a real number. |
| R37 | 152 | nonempty segment via trusted `String2Int` hook | Correct for plain decimal digits. It is not a Python numeric-string parser: the valid intended string `"1e2"` makes the LLVM backend throw `invalid_argument`/time out rather than return `"1e2"` for comparison against `99`. |
| V1 | verification.k:9–32 | macro expansion for `theSolution` | Constructor-for-constructor identical to trusted regeneration of `solution.py` (identical expanded KORE hash). It is not an oracle or execution bridge; all body statements subsequently execute under R1–R37. |

## Construct coverage and evaluation/control summary

`solution.mpy` uses `Module`, `FuncDef`, `Params`, statement lists, `If`,
`Assign`, `Return`, `Name`, `Str`, `NoneVal`, `Call`, `Attribute`, `Compare`,
`CmpOp`, and expression/operator lists.  D4–D12 declare all of them; R1–R18
execute all material occurrences.  The body has no loop, recursion, mutation
outside the local environment, allocation, I/O, or user-defined nested call.

Evaluation is encoded by the pure `eval` function instead of strictness
contexts.  That preserves value/order for this body only so far as `type`,
`float`, `replace`, lookup, and comparisons are accurately modeled and do not
raise.  The exact-rational `float` rules violate that condition on ordinary
unrestricted integers and numeric strings.  Exceptions and a call stack are
absent.

The four cells have clear footprints: R4 updates `<functions>`; R5 reads it and
replaces `<env>`; R6 updates `<env>`; R7–R8 read `<env>`; R9 reads `<env>`,
clears `<k>`, and writes `<result>`.  Other rules are equations without state.

## Proof-extension classification

There are no proof-local summaries, lemmas, operational shortcuts, fresh
oracles, simplification rules, or auxiliary claims.  `theSolution` is a
definitional syntax macro and was mechanically connected to the submitted
constructor term.  Therefore the proof failure is not a hidden
`verification.k` shortcut: it is the generated language definition's false
numeric bridge plus the materially restricted claim set.
