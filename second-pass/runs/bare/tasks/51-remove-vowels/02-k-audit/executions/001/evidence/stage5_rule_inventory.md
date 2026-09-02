# Exhaustive local K inventory and reviewer classification

This inventory is rebuilt from the scratch source copy. Imported K framework
modules (`STRING-SYNTAX` and `STRING`) are listed as trust dependencies, not
expanded as candidate-authored rules. There are no generated helper K files
besides `semantic.k`, `verification.k`, and `spec.k`.

## Local syntax and attributes

| ID | Location | Declaration / alternatives | Attributes and status |
|---|---|---|---|
| D1 | `semantic.k:4` | `Program ::= Module(Stmt)` | Constructor syntax. |
| D2 | `semantic.k:5-6` | `Stmt ::= FuncDef(String, Params, Stmt) \| Return(Expr)` | Constructor syntax. |
| D3 | `semantic.k:7` | `Params ::= Params(String)` | Constructor syntax. |
| D4 | `semantic.k:9-12` | `Expr ::= Name(String) \| Str(String) \| Attribute(Expr,String) \| Call(Expr,Expr,Expr)` | Constructor syntax. |
| D5 | `semantic.k:22` | `String ::= deleteAll(String,String)` | `[function]`; intentionally not `[total]`. It remains opaque for symbolic arguments. |
| D6 | `semantic.k:26` | `Value ::= strVal(String)` | Constructor syntax. |
| D7 | `semantic.k:27` | `Value ::= eval(Expr,String,String)` | Partial `[function]`. |
| D8 | `semantic.k:28` | `Value ::= replaceValue(Value,String,String)` | Partial `[function]`. |
| D9 | `semantic.k:29` | `Result ::= noResult \| result(String)` | Constructor syntax. |
| D10 | `semantic.k:30` | `KItem ::= done` | Constructor syntax. |
| D11 | `verification.k:8` | `String ::= removeLowerVowels(String)` | `[function,total]`; one unconditional, nonrecursive equation. |
| D12 | `verification.k:9` | `String ::= removeUpperVowels(String)` | `[function,total]`; one unconditional, nonrecursive equation. |
| D13 | `verification.k:10` | `String ::= removeVowelsSpec(String)` | `[function,total]`; one unconditional, nonrecursive equation. |

There are no local `[functional]` declarations, priorities, `owise` rules,
macros, aliases, or fresh generators.

## Configuration

`semantic.k:39-44` declares the complete local state:

- `<k>` initially contains `$PGM:K`.
- `<input>` contains `$INPUT:String` and is read but never changed.
- `<result>` starts as `noResult` and is written once to `result(S)`.

There is no heap, environment map, call stack, exception state, output, or
allocation state. That is sufficient for the submitted expression-only,
single-parameter program.

## Semantic and mathematical rules

| ID | Location | Rule and complete domain | Class / matched context / footprint | Reviewer decision |
|---|---|---|---|---|
| R1 | `semantic.k:23-24` | `deleteAll(S,NEEDLE) => replaceAll(S,NEEDLE,"")` when both arguments are concrete; `[simplification, concrete(S,NEEDLE)]`. | Trusted external string primitive. No cells. It fixes the value of the opaque symbolic operation on ground calls. | Correct for every nonempty literal needle used by the submitted body; all ten needles are one-character ASCII vowels. Ground normal/boundary K runs agree with Python. An out-of-scope empty-needle probe times out, although Python terminates; therefore the declaration is broader than its validated/generated-program scope. It enables no witnessed false result for the submitted program. |
| R2 | `semantic.k:32-33` | `eval(Name(X),P,I) => strVal(I)` when `X ==String P`. | Ordinary evaluator equation. No cells. It models lookup of the sole parameter. | Correct for the actual `Name("text")`, `Params("text")`; disjoint from R3/R4 by constructor. |
| R3 | `semantic.k:34` | `eval(Str(S),_,_) => strVal(S)`. | Ordinary evaluator equation. No cells. | Correct literal evaluation; constructor-disjoint from R2/R4. |
| R4 | `semantic.k:35-36` | Evaluate `Call(Attribute(E,"replace"),Str(OLD),Str(NEW))` as `replaceValue(eval(E,P,I),OLD,NEW)`. | Ordinary evaluator equation. No cells. Receiver evaluation is nested before `replaceValue`; literal arguments have no side effects. | Correct for every submitted call. Calls with other shapes visibly remain unmodeled. |
| R5 | `semantic.k:37` | `replaceValue(strVal(S),OLD,"") => strVal(deleteAll(S,OLD))`. | Operational external-primitive bridge from an evaluated string receiver; no cells. | Correct for the submitted calls, whose replacement is always empty. It does not fabricate a value: R1 supplies ground behavior and symbolic execution stays parametric in `deleteAll`. |
| R6 | `semantic.k:46-48` | At the front of `<k>`, turn `Module(FuncDef(_,Params(P),Return(E)))` into `eval(E,P,I)` while reading `<input>I`; arbitrary continuation is framed. | Entry semantics. Reads `<input>`, rewrites `<k>`, preserves `<result>` and continuation. | Correct for the exact one-function submitted module. It intentionally treats the sole function declaration as the configured entry call. No abrupt control effect is introduced. |
| R7 | `semantic.k:50-51` | When `<k>` is exactly `strVal(S)`, rewrite it to `done` and `noResult` to `result(S)`. | Return/finalization rule. Reads/writes `<k>` and `<result>`; `<input>` is preserved. Exact `<k>` content means it does not discard a continuation. | Correct and control-contained. It applies once because the result cell must be `noResult`. |
| R8 | `verification.k:12-21` | Expand `removeLowerVowels(S)` to five nested `deleteAll` calls for `"a","e","i","o","u"`. | Definitional summary; no cells. | Unconditional, terminating, and total over K `String`; no overlap. |
| R9 | `verification.k:23-32` | Expand `removeUpperVowels(S)` to five nested `deleteAll` calls for `"A","E","I","O","U"`. | Definitional summary; no cells. | Unconditional, terminating, and total over K `String`; no overlap. |
| R10 | `verification.k:34` | `removeVowelsSpec(S) => removeUpperVowels(removeLowerVowels(S))`. | Definitional summary; no cells. | Unconditional, terminating, and total; no overlap. |

No local rule has a priority. R1 is the only local simplification rule. R8-R10
are ordinary function equations in the proof definition, not operational
bridges that replace program execution.

## Claim inventory

| ID | Location | Claim |
|---|---|---|
| C1 | `spec.k:8-59` | With no `requires`, from the exact submitted `Module(FuncDef(...))`, arbitrary `INPUT:String`, and `noResult`, execution reaches `done`, preserves `INPUT`, and changes the result to `result(removeVowelsSpec(INPUT))`. |

There are no helper/loop claims, lemmas, or circularities. C1 is the only
positive target and is unlabeled, so the recorded unfiltered `kprove` command
runs every claim.

## Submitted-constructor coverage

| Submitted constructor | Declarations and rules |
|---|---|
| `Module` | D1, R6 |
| `FuncDef`, `Return` | D2, R6 |
| `Params` | D3, R6 |
| `Name` | D4, R2 |
| `Str` | D4, R3 |
| `Attribute`, `Call` | D4, R4 |
| ten calls to `str.replace(vowel,"")` | R4, R5, R1 |
| returned string/result finalization | D6, D9, D10, R7 |

Every submitted constructor is covered. Normal and boundary concrete runs
exercise all seven semantic rules. Missing behavior for non-submitted call
shapes is visible as a stuck term and is outside the generated-semantics scope.

## Opaque and trusted-value trace

For symbolic `INPUT`, each `deleteAll` remains opaque. It influences the nested
program result, all three verification summaries, and C1's postcondition. Its
origin is the external built-in `str.replace` operation, not program-defined
code. The proof is interpretation-parametric: R2-R7 establish that the actual
body applies this same operation in the same ten-call order as R8-R10. R1 fixes
ground nonempty-needle behavior through K's imported `replaceAll` hook.

This supports the theorem about the submitted program. It does not itself prove
a separate character-level theorem that the nested operation preserves every
nonvowel in order and removes every vowel. That intent bridge is supported by
the imported primitive's contract, concrete K/Python comparisons, and the
independent differential test; those finite tests are evidence, not a universal
connection theorem.
