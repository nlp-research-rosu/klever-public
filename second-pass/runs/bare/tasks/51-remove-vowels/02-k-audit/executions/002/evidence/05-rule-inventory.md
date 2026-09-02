# Local K declaration and rule inventory

Scope: the scratch copies of `semantic.k`, `verification.k`, and `spec.k`.
There are no generated helper K files. Imported K framework modules are treated
as the fixed toolchain boundary, not as candidate-local declarations.

## `semantic.k`: `MPY-SYNTAX`

| ID | Lines | Declaration | Used target construct | Review |
|---|---:|---|---|---|
| D1 | 4 | `Program ::= Module(Stmt)` | translated module | Faithful constructor declaration. |
| D2 | 5 | `Stmt ::= FuncDef(String,Params,Stmt)` | one function definition | Faithful constructor declaration for the submitted arity. |
| D3 | 6 | `Stmt ::= Return(Expr)` | sole function-body statement | Faithful constructor declaration. |
| D4 | 7 | `Params ::= Params(String)` | sole parameter `text` | Faithful constructor declaration for the submitted arity. |
| D5 | 9 | `Expr ::= Name(String)` | `Name("text")` | Faithful constructor declaration. |
| D6 | 10 | `Expr ::= Str(String)` | ten vowel and ten empty literals | Faithful constructor declaration. |
| D7 | 11 | `Expr ::= Attribute(Expr,String)` | each `.replace` lookup | Faithful constructor declaration. |
| D8 | 12 | `Expr ::= Call(Expr,Expr,Expr)` | each two-argument call | Faithful constructor declaration for the submitted calls. |

## `semantic.k`: `MPY`

| ID | Lines | Declaration / rule | Class and complete domain | Review |
|---|---:|---|---|---|
| D9/R1 | 22–24 | `deleteAll(String,String) [function]`; concrete simplification to `replaceAll(S,NEEDLE,"")` | Externally grounded definitional wrapper. Rule applies when both arguments are concrete. | Truthful by the fixed K `STRING.replaceAll` hook. It stays opaque on symbolic arguments; it is deliberately not declared `total`. It influences the returned value and postcondition. There are no competing equations. |
| D10 | 26 | `Value ::= strVal(String)` | Runtime string-value constructor. | Faithful and inert. |
| D11 | 27 | `Value ::= eval(Expr,String,String) [function]` | Partial evaluator: expression, parameter name, input string. | Partiality is explicit; the four rules below cover every target expression. No `total`/`functional` assertion. |
| D12 | 28 | `Value ::= replaceValue(Value,String,String) [function]` | Partial string-method helper. | Its one equation covers every target call after receiver evaluation. No `total`/`functional` assertion. |
| D13 | 29 | `Result ::= noResult` | Initial result marker. | Faithful. |
| D14 | 29 | `Result ::= result(String)` | Final observable string. | Faithful. |
| D15 | 30 | `KItem ::= done` | Terminal computation marker. | Faithful. |
| R2 | 32–33 | `eval(Name(X),P,I) => strVal(I)` if `X ==String P` | Single-parameter lookup. | Guard exactly selects the submitted binding. Reads no other cell and has no overlap with the other `eval` shapes. |
| R3 | 34 | `eval(Str(S),_,_) => strVal(S)` | String literal evaluation. | Faithful and effect-free; disjoint constructor from R2/R4. |
| R4 | 35–36 | `eval(Call(Attribute(E,"replace"),Str(OLD),Str(NEW)),P,I) => replaceValue(eval(E,P,I),OLD,NEW)` | Evaluation of the submitted method-call shape. | Receiver is recursively evaluated; literal arguments are effect-free, so Python's receiver/argument order is preserved for the target. The exact attribute string pins `str.replace`. |
| R5 | 37 | `replaceValue(strVal(S),OLD,"") => strVal(deleteAll(S,OLD))` | String replacement when the replacement is empty. | Every submitted call lies in the domain. Conditional on the fixed `replaceAll` primitive, this is Python `str.replace(OLD,"")` for the nonempty literal needles used by the program. No competing equation. The rule also admits an empty `OLD`; a bounded probe of that unused case timed out while Python returns immediately, so this is an over-broad reuse/coverage gap, not evidence about a reachable target execution. |
| C1 | 39–44 | `<mpy>` with `<k>`, `<input>`, `<result>` | Complete modeled state. | Sufficient: the submitted expression is pure and needs only input and final result. No heap, output, exceptions, allocation, or mutable bindings are exercised. |
| R6 | 46–48 | module/function/return to `eval(E,P,I)` while reading `<input>I</input>` | Direct-entry adapter for a one-function translated module. | For the exact claim term it binds `text` to the supplied K String and executes the exact returned expression. It preserves any framed `<k>` suffix. It ignores the function name only outside the exact submitted term. |
| R7 | 50–51 | sole `strVal(S)` computation to `done`, `noResult` to `result(S)` | Finalization. | Exact `<k>` and result-state match prevent discarding a continuation or overwriting an existing result. |

There are no local priority rules, `owise` rules, strictness declarations,
fresh symbols, allocation rules, exception rules, or `functional`
declarations.

## `verification.k`

| ID | Lines | Declaration / rule | Class and complete domain | Review |
|---|---:|---|---|---|
| D16/V1 | 8, 12–21 | `removeLowerVowels(String) [function,total]` and its unguarded equation | Definitional summary for every K String. | One-step, nonrecursive, complete, and nonoverlapping. It names five sequential `deleteAll` operations. |
| D17/V2 | 9, 23–32 | `removeUpperVowels(String) [function,total]` and its unguarded equation | Definitional summary for every K String. | One-step, nonrecursive, complete, and nonoverlapping. It names five sequential `deleteAll` operations. |
| D18/V3 | 10, 34 | `removeVowelsSpec(String) [function,total]` and its unguarded equation | Contract summary for every K String. | One-step, complete, and nonoverlapping. Expands to lower- then uppercase deletion. |

The three `total` functions each have exactly one unguarded equation over their
entire declared sort. There are no proof-local operational rules, priority
rules, simplification rules, claims, opaque fresh values, or overlaps in
`verification.k`.

## `spec.k`

| ID | Lines | Declaration | Review |
|---|---:|---|---|
| Q1 | 8–59 | One unlabeled reachability claim | Precondition: the ordinary sort constraints only; `INPUT` ranges over all K Strings, `<k>` is the exact submitted constructor tree, `<result>` starts `noResult`. Postcondition: computation is `done`, input is preserved, and result is exactly `removeVowelsSpec(INPUT)`. No free RHS value, implication-only result, omitted observable cell, helper/loop claim, or finite bound. |

## Construct coverage

`Module`/`FuncDef`/`Params`/`Return` are consumed by R6; `Name` by R2;
`Str` by R3; each `Call(Attribute(...,"replace"),Str(...),Str(""))` by
R4 then R5; ten nested calls repeatedly exercise those rules; D9/R1 grounds
each deletion for concrete execution; and R7 produces the observable result.
Every constructor in regenerated `solution.mpy` is therefore declared and has
applicable behavior.

## Trust and limitation identified by the inventory

The value-bearing boundary is the fixed K `String` domain together with
`STRING.replaceAll`. It is an external primitive, not program-defined code.
The symbolic proof intentionally leaves `deleteAll` opaque and is
interpretation-parametric in that primitive; the ground equation connects it
to K's documented total hook. The theorem does not itself prove that K's
Unicode-string hook is extensionally identical to CPython for all Python
`str` values, nor does it formalize the equivalence between the canonical
`lower()` filter and deletion of the ten ASCII vowels. Those are adequacy
bridges supported by the trusted canonical source, toolchain documentation,
exhaustive Python singleton differential testing, and finite K/Python
concrete comparisons. They are not reachability-proof conclusions.

The empty-needle case admitted by R5 is outside the submitted constructor tree:
all ten needles are fixed nonempty one-character strings. The bounded timeout
does not establish a false rewrite conclusion, and there is no satisfying
target input that can change those literals, so it is recorded as the narrower
evidence/semantics-reuse gap required by the audit instructions rather than
called an unsound target rule.
