# Exhaustive local K inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no other candidate K/helper files.

## Syntax, attributes, and configuration

| ID | Source | Declaration | Role and audit result |
|---|---|---|---|
| S01 | `semantic.k:7` | `Program ::= Module(Stmts)` | Root constructor parsed from `solution.mpy`; used. |
| S02 | `semantic.k:9` | `Stmts ::= List{Stmt, ""}` | Statement-list constructor/unit; used for the singleton function body and singleton return body. |
| S03 | `semantic.k:10` | `Stmt ::= FuncDef(String, Params, Stmts)` | Submitted function binding; used. |
| S04 | `semantic.k:11` | `Stmt ::= Return(Expr)` | Submitted body; used. |
| S05 | `semantic.k:13` | `Ids ::= List{String, ","}` | Parameter-list constructor/unit; used with exactly `"s"`. |
| S06 | `semantic.k:14` | `Params ::= Params(Ids)` | Submitted parameter wrapper; used. |
| S07 | `semantic.k:15` | `Exprs ::= List{Expr, ","}` | Call argument-list constructor/unit; used with two string arguments and with the empty list. |
| S08 | `semantic.k:16` | `Expr ::= Name(String)` | Variable reference; used. |
| S09 | `semantic.k:17` | `Expr ::= Str(String)` | Literal strings; used. |
| S10 | `semantic.k:18` | `Expr ::= Attribute(Expr,String)` | Method selection; used for `replace` and `split`. |
| S11 | `semantic.k:19` | `Expr ::= Call(Expr,Exprs)` | Calls; used twice. |
| S12 | `semantic.k:27` | `Function ::= function(String,Stmts)` | Function-map payload; used. |
| S13 | `semantic.k:28` | `PyVal ::= StrVal(String)` | String runtime value; used. |
| S14 | `semantic.k:28` | `PyVal ::= ListVal(List)` | Return runtime value; used. |
| S15 | `semantic.k:30` | `KItem ::= invoke(String,String)` | Entry invocation; used. |
| S16 | `semantic.k:31` | `KItem ::= execute(Stmts,Map)` | Function-body execution; used. |
| S17 | `semantic.k:33` | `PyVal ::= eval(Expr,Map) [function]` | Partial evaluator. Equations are disjoint; all submitted expression forms are covered. It is not declared total. |
| S18 | `semantic.k:34` | `String ::= asString(PyVal) [function]` | Partial projection. It is used only on `StrVal`; not declared total. |
| C01 | `semantic.k:36-38` | `<k>` plus `<functions>` configuration | The initial state parses a `Program`, appends the concrete `words_string` invocation with arbitrary K `String` input, and starts with an empty function map. Both cells are read or written. |
| S19 | `verification.k:9` | `List ::= splitSpaces(String) [function]` | Defined by R09-R12 below. Equations are disjoint, exhaustive over K strings, and length-decreasing on recursive branches. |
| S20 | `verification.k:26` | `List ::= wordsContract(String) [function,total]` | One unguarded defining equation (R13), hence total assuming its imported K string/list primitives. |

No local declaration has `[functional]`, `[simplification]`, `[concrete]`,
`[macro]`, `[anywhere]`, or a priority attribute. There are no local opaque or
fresh symbols and no local priority rules. The only `[total]` declaration is
`wordsContract`.

## Rule-by-rule review

| ID | Source | Complete match/guard | Classification and result |
|---|---|---|---|
| R01 | `semantic.k:41-42` | Front of `<k>` is exactly a one-`FuncDef` `Module`; `<functions>` is exactly `.Map`; arbitrary continuation is preserved. | Operational semantics. Installs the submitted capture-free singleton binding and consumes the module. Exact for the submitted module. |
| R02 | `semantic.k:45-46` | Front is `invoke(F,S)` and the function map contains `F |-> function(P,BODY)`; other map entries and the continuation are preserved. | Operational semantics. Creates the submitted one-argument local environment `P |-> StrVal(S)`. Binding lookup is explicit. Exact on the actual singleton map. |
| R03 | `semantic.k:48` | Front is exactly `execute(Return(E),ENV)`; continuation preserved. | Operational semantics. The submitted body contains only this return, so no statements or return-control effects are skipped. |
| R04 | `semantic.k:50` | `eval(Name(X), X |-> V)` on an exact singleton map. | Definitional evaluator equation. Correct lookup on every reachable environment; deliberately partial on larger maps. |
| R05 | `semantic.k:51` | `eval(Str(S), ENV)` for any environment. | Definitional evaluator equation. String literals are pure and environment-independent. |
| R06 | `semantic.k:54-55` | `eval(Call(Attribute(RECV,"replace"),Str(OLD),Str(NEW)),ENV)` for arbitrary `RECV`, `OLD`, and `NEW`. | Trusted-primitive bridge to K `replaceAll`. On the only reachable submitted instantiation (`OLD=","`, `NEW=" "`), it preserves Python replacement behavior. It is too broad as reusable Python semantics: with receiver `"ab"`, `OLD=""`, and `NEW="x"`, Python produces `"xaxbx"` but this K bridge produces `"xaxb"` before splitting; see `replace-primitive-probes.log`. This false instantiation cannot be reached from the immutable submitted body, so it does not enable a false target conclusion, but it is a non-fatal semantics-reuse concern. |
| R07 | `semantic.k:58-59` | `eval(Call(Attribute(RECV,"split"),.Exprs),ENV)` for arbitrary receiver. | Trusted-primitive bridge to the explicitly defined `splitSpaces`. It is exact for literal U+0020 separators used by the source contract. It is not globally faithful to Python no-argument `str.split`: actual input `"a\\tb"` gives Python `["a","b"]` but K `["a\\tb"]`; see `python-whitespace-boundary.log`. Such non-U+0020 whitespace is outside the stated comma-or-space input language, but the unrestricted formal K-string claim does not record that boundary. |
| R08 | `semantic.k:61` | `asString(StrVal(S))`. | Definitional projection, exact and disjoint. |
| R09 | `verification.k:11` | `splitSpaces("")`. | Mathematical equation: empty input has no words. |
| R10 | `verification.k:12-14` | Nonempty `S` whose first code point is U+0020. | Mathematical equation: delete one leading separator and recur on a strictly shorter string. Disjoint from R09, R11, and R12. |
| R11 | `verification.k:15-17` | Nonempty `S` with no U+0020 occurrence. | Mathematical equation: return the single remaining word. Disjoint from R09, R10, and R12. |
| R12 | `verification.k:18-22` | First U+0020 occurs at an index greater than zero. | Mathematical equation: emit the nonempty prefix and recur after the separator on a strictly shorter suffix. Disjoint from R09-R11. |
| R13 | `verification.k:27` | Every K string `S`. | Definitional contract summary: turn each comma into U+0020 and apply the exhaustive splitter. The equation is unguarded, agrees with the literal source contract, and is the only equation for `wordsContract`. |

R09-R12 cover exactly four mutually exclusive cases: empty; nonempty with first
space at index 0; nonempty with no space; and nonempty with first space at an
index greater than 0. Thus `splitSpaces` has coverage, pairwise consistency,
and structural descent despite lacking a `[total]` attribute.

## Claims

| ID | Source | Entry and destination |
|---|---|---|
| Q01 | `spec.k:7-30` | Arbitrary K string `S`; executes the submitted module followed by `invoke`; requires final `ListVal(wordsContract(S))` and the exact installed function binding. |
| Q02 | `spec.k:33-58` | Prompt input `"Hi, my name is John"`; requires the five stated words and exact installed binding. |
| Q03 | `spec.k:60-85` | Prompt input `"One, two, three, four, five, six"`; requires the six stated words and exact installed binding. |

All claims have logical `requires true` and `ensures true`; their substantive
preconditions and postconditions are the explicit `<k>` and `<functions>` cell
patterns. There are no helper/loop claims.

## Submitted-construct coverage

`solution.mpy` uses S01-S11 in this constructor flow:

`Module -> FuncDef -> Params + Return -> outer Call(split) -> Attribute ->
inner Call(replace) -> Attribute + Name + two Str literals + empty Exprs`.

Execution uses R01, R02, R03, R07, R06, R04/R05, R08, R13, and one or more of
R09-R12. No submitted construct is unmodeled, fabricated on stuck execution, or
replaced by an unconstrained oracle.
