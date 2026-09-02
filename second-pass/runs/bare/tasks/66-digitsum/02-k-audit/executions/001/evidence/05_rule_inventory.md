# Exhaustive local rule and declaration inventory

This inventory was reconstructed from the source files, not from any compiled
definition. Line references are to `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`.

## Imports, modules, and configuration

- `semantic.k:1` requires `verification.k`.
- `MPY-SYNTAX` imports `INT-SYNTAX` and `STRING-SYNTAX`.
- `DIGIT-SUM-SEMANTICS` imports `MPY-SYNTAX`, `INT`, `BOOL`, `STRING`,
  `MAP`, and `K-EQUAL`.
- `SEMANTIC` imports both `DIGIT-SUM-SEMANTICS` and
  `DIGIT-SUM-VERIFICATION`.
- `DIGIT-SUM-VERIFICATION` imports `INT`, `BOOL`, `STRING`, and `K-EQUAL`.
- The configuration (`semantic.k:87-93`) has `<k>` initialized from a
  `Program`, immutable `<input>` initialized from a K `String`, mutable
  `<env>` initially `.Map`, and mutable `<result>` initially `noResult`.
  There is no heap, call stack, exception, allocation, or I/O cell.

The submitted program needs none of those absent state components: its only
state is local variables, its only call is the modeled pure `ord`, and it has no
exceptions on its actual executions.

## Syntax declarations

All local productions are listed here, including alternatives.

| ID | Location | Declaration / production | Used by submitted `solution.mpy` |
|---|---|---|---|
| Y1 | `semantic.k:7` | `Program ::= Module(Stmts)` `[symbol(Module)]` | yes |
| Y2 | `semantic.k:10` | `Stmts ::= List{Stmt,""}` | yes: function/body/empty else |
| Y3 | `semantic.k:12` | `Stmt ::= FuncDef(String,Params,Stmts)` `[symbol(FuncDef)]` | yes |
| Y4 | `semantic.k:13` | `Stmt ::= Assign(Expr,Expr)` `[symbol(Assign)]` | yes |
| Y5 | `semantic.k:14` | `Stmt ::= For(Expr,Expr,Stmts)` `[symbol(For)]` | yes |
| Y6 | `semantic.k:15` | `Stmt ::= If(Expr,Stmts,Stmts)` `[symbol(If)]` | yes |
| Y7 | `semantic.k:16` | `Stmt ::= Return(Expr)` `[symbol(Return)]` | yes |
| Y8 | `semantic.k:18` | `Params ::= Params(String)` `[symbol(Params)]` | yes |
| Y9 | `semantic.k:20` | `Expr ::= Name(String)` `[symbol(Name)]` | yes |
| Y10 | `semantic.k:21` | `Expr ::= Int(Int)` `[symbol(IntExpr)]` | yes |
| Y11 | `semantic.k:22` | `Expr ::= Str(String)` `[symbol(Str)]` | yes |
| Y12 | `semantic.k:23` | `Expr ::= BinOp(String,Expr,Expr)` `[symbol(BinOp)]` | yes |
| Y13 | `semantic.k:24` | `Expr ::= Call(Expr,Expr)` `[symbol(Call)]` | yes |
| Y14 | `semantic.k:25` | `Expr ::= Compare(Expr,CmpOps)` `[symbol(Compare)]` | yes |
| Y15 | `semantic.k:27` | `CmpOps ::= List{CmpOp,","}` | yes |
| Y16 | `semantic.k:28` | `CmpOp ::= CmpOp(String,Expr)` `[symbol(CmpOp)]` | yes |
| Y17 | `semantic.k:39` | `Value ::= intVal(Int)` | yes |
| Y18 | `semantic.k:40` | `Value ::= strVal(String)` | yes |
| Y19 | `semantic.k:41` | `Value ::= boolVal(Bool)` | only in the unused generic comparison path |
| Y20 | `semantic.k:42` | `Result ::= noResult` | yes |
| Y21 | `semantic.k:42` | `Result ::= Value` | yes |
| Y22 | `semantic.k:44` | `KItem ::= execute(Stmts)` | yes |
| Y23 | `semantic.k:45` | `KItem ::= execStmt(Stmt)` | yes |
| Y24 | `semantic.k:46` | `KItem ::= loopString(String,String,Stmts)` | yes |
| Y25 | `semantic.k:47` | `KItem ::= addUpper(String)` | yes |
| Y26 | `semantic.k:49` | `Value ::= eval(Expr,Map)` `[function]` | yes |
| Y27 | `semantic.k:50` | `Value ::= addValues(Value,Value)` `[function]` | yes |
| Y28 | `semantic.k:51` | `Value ::= ordValue(Value)` `[function]` | only generic expression path |
| Y29 | `semantic.k:52` | `Value ::= compareLE3(Value,Value,Value)` `[function]` | only generic expression path |
| Y30 | `semantic.k:53` | `String ::= stringOf(Value)` `[function]` | yes |
| Y31 | `semantic.k:54` | `Bool ::= truthOf(Value)` `[function]` | unused |
| Y32 | `semantic.k:55` | `Int ::= pythonUpperOrd(String)` `[function]` | yes |
| Y33 | `verification.k:9` | `Int ::= upperAsciiSum(String)` `[function]` | postconditions |
| Y34 | `verification.k:10` | `Int ::= upperAsciiContribution(String)` `[function]` | postconditions |

There are **no** local `[total]`, `[functional]`, `[opaque]`, `[priority]`,
`[owise]`, `[anywhere]`, `[macro]`, or `[concrete]` declarations/rules. There
is no local `KResult` declaration. The seven semantic functions and two proof
functions are partial outside their covered subset; no totality assertion
fabricates a value.

## Semantic function/equation inventory

| ID | Location | Rule | Classification and audit decision |
|---|---|---|---|
| F1 | `semantic.k:57` | `eval(Int(I),_) => intVal(I)` | Truthful constructor evaluation. |
| F2 | `semantic.k:58` | `eval(Str(S),_) => strVal(S)` | Truthful constructor evaluation. |
| F3 | `semantic.k:61` | lookup through an update at the same key yields the update value `[simplification]` | True K-map update equation. It overlaps F5 only after map normalization and agrees there. |
| F4 | `semantic.k:62-63` | lookup through an update at a different key removes that update `[simplification]` | True under the disjoint guard `X =/=String Y`; its guard is complementary to F3 for concrete names. |
| F5 | `semantic.k:64-65` | guarded concrete-map lookup | True; the guard ensures the displayed binding is unique in the remaining map. |
| F6 | `semantic.k:66-67` | evaluate `BinOp("+",...)` through `addValues` | Correct for the only modeled integer-addition form; unsupported operands stay visible. |
| F7 | `semantic.k:68-69` | evaluate exact `ord` call through `ordValue` | Correct for the submitted one-character use; unsupported calls stay visible. |
| F8 | `semantic.k:70-72` | evaluate exact two-link `<=` chain through `compareLE3` | Correct on its one-character operands, the only values generated by the submitted loop. |
| F9 | `semantic.k:74` | add two `intVal`s | Ordinary unbounded integer addition. |
| F10 | `semantic.k:75` | `ordValue(strVal(S)) => intVal(ordChar(S))` | Correct when `S` has one code point; K's partial `ordChar` remains stuck otherwise rather than inventing a result. |
| F11 | `semantic.k:76-78` | chained comparison by code point | Correct for one-code-point strings. It remains partial through `ordChar` on other strings. |
| F12 | `semantic.k:79` | unwrap `strVal` | Definitional and true. |
| F13 | `semantic.k:80` | unwrap `boolVal` | Definitional and true; unused. |
| F14 | `semantic.k:81-85` | `pythonUpperOrd(C)` is `ordChar(C)` for code points 65–90, else 0 | A fully defined ASCII contribution on one-code-point strings. It truthfully summarizes the submitted source predicate, but not Python `str.isupper()` or the trusted task contract. It is partial, visibly stuck, for strings outside `ordChar`'s domain. |

F3 and F4 are the only local semantic simplification rules. The other
semantic equations are ordinary function rules. No conflicting right-hand
sides were found on an overlapping, satisfiable guard.

## Operational semantic rule inventory

| ID | Location | Transition / role | State and control audit |
|---|---|---|---|
| O1 | `semantic.k:97-100` | load exact one-argument `digitSum` definition | Binds input to `s`, changes only `<k>` and initially empty `<env>`, and preserves `<input>`/`<result>`. It pins the entry name and parameter. |
| O2 | `semantic.k:102` | `execute(.Stmts) => .K` | Correct empty sequence. |
| O3 | `semantic.k:103` | split a nonempty statement list into `execStmt(S) ~> execute(SS)` | Preserves left-to-right statement order. |
| O4 | `semantic.k:105-106` | assignment updates the named local with `eval(E,ENV)` | Correct simultaneous read-old/write-new behavior for the modeled pure expressions. |
| O5 | `semantic.k:111-123` | atomically execute the exact ASCII-uppercase `if`/assignment | Operational bridge specialized to the translated source. For actual one-character `char` and integer `total`, it preserves the arbitrary continuation and exactly implements the branch's sole state effect. It changes only `total`; the source `if` also changes no other local. No false conclusion witness was found for the submitted operand shape. |
| O6 | `semantic.k:125-127` | turn a `for Name(X) in ITER` into `loopString(X,stringOf(eval(ITER,ENV)),BODY)` | Preserves iterable evaluation before iteration. It delegates iteration binding and body execution to O7/O8. |
| O7 | `semantic.k:129` | empty `loopString` terminates | Correct: an empty Python iteration performs no target binding/body step and preserves the continuation and state. |
| O8 | `semantic.k:130-148` | nonempty exact digit-sum loop takes the head code point, performs `addUpper`, and recurs on the suffix | **UNSOUND operational bridge.** It matches an arbitrary continuation (`...`) but never writes the loop target `char` to `<env>`. Python binds `char` before the body and leaves the last binding observable afterward. The false-conclusion witness is `loop_binding_witness.py` on input `"A"` with pre-loop `char = "B"` and continuation `return ord(char)`: Python returns 65; the K semantics returns 66, and `SPEC-LOOP-BINDING-WITNESS.semantic-result` proves `#Top` for that false Python result. The correct-result claim gets stuck at `intVal(66)`. See `05_operational_bridge_witness.log`. This is a binding/state-footprint and context-containment failure, not an evidence gap. |
| O9 | `semantic.k:150-154` | add one character's ASCII contribution to unique `total` binding | Correct unbounded integer update under the uniqueness guard; preserves frame, control, input, and result. |
| O10 | `semantic.k:156-158` | return evaluates `E` in the old environment, discards the exact remaining continuation, clears locals, and sets result | Correct abrupt return for the submitted single-frame model. The no-ellipsis `<k>` pattern consumes the complete continuation. It only applies while result is `noResult`. |

O5 and O8 are proof-sensitive, source-specialized operational bridges. O5 has
the same state footprint as its exact statement on the actual operand domain.
O8 does not. There is no priority annotation, but O8 is the only rule capable
of advancing the matched nonempty loop, so the bad transition is unavoidable
whenever its pattern matches.

## Proof-local declaration and rule inventory

| ID | Location | Rule | Classification and audit decision |
|---|---|---|---|
| V1 | `verification.k:12` | `upperAsciiSum("") => 0` `[simplification]` | True base equation. |
| V2 | `verification.k:13-16` | nonempty recursive `upperAsciiSum` over first code point and strict suffix `[simplification]` | True definition of ASCII contribution sum; its guard is disjoint from V1 and the suffix strictly decreases. |
| V3 | `verification.k:18-22` | `upperAsciiContribution(C)` uses code-point range 65–90 `[simplification]` | True on every one-code-point string supplied by V2; partial through `ordChar` otherwise and not declared total. |
| V4 | `verification.k:25` | `(I +Int J) +Int K => I +Int (J +Int K)` `[simplification]` | Integer associativity. Orientation decreases left nesting and is mathematically true for unbounded K integers. |

V1–V3 define the **ASCII** summary already computed by the candidate. They do
not prove that ASCII uppercase is equivalent to Python `str.isupper()`;
`"É"` is a concrete counterexample. V4 is an ordinary valid lemma. No opaque
or unconstrained result-bearing symbol occurs: every local summary reaching the
postcondition has equations fixing its value on every actual use.

## Reachability claims

| ID | Location | Plain-language role |
|---|---|---|
| C1 | `spec.k:10-26` | For any K string in an empty initial environment, exact submitted constructor program terminates with empty environment and result `upperAsciiSum(S)`. |
| C2 | `spec.k:30-51` | From the exact specialized loop plus exact `return total` continuation, accumulator `A`, suffix `S`, and a frame without another `total`, execution returns `A + upperAsciiSum(S)` and clears the environment. |

C2's exact continuation does not observe the omitted final `char` binding, so
the candidate theorem happens not to expose O8's wrong binding. That does not
repair O8: the rule itself admits arbitrary continuations and therefore exceeds
the only context in which the omission is observationally irrelevant.

## Construct-to-rule coverage for `solution.mpy`

| Submitted construct | Declaration | Executing rules |
|---|---|---|
| `Module(FuncDef(...))`, `Params` | Y1, Y3, Y8 | O1 |
| statement lists | Y2 | O2, O3 |
| `Assign(total,Int(0))` | Y4, Y10 | O4, F1 |
| `For(char,Name(s),BODY)` | Y5, Y9 | O6, F3/F4/F5, F12, then O7/O8/O9 |
| exact `If(Compare(...),Assign(...),empty)` | Y6, Y11–Y16 | recognized by O8 and computed by O9/F14; it is **not** executed through O5/F6–F11 on the real loop path |
| `Return(Name(total))` | Y7, Y9 | O10 and F3/F4/F5 |
| `BinOp("+",...)`, `Call(ord,...)`, chained `Compare` | Y12–Y16 | their general F6–F11 rules exist, but O8 bypasses those program expression nodes and directly uses F14 |

Thus every used syntax form parses and the concrete program reaches a final
configuration, but the property-bearing loop body is implemented by a
task-specific operational bridge rather than ordinary body execution. Its
ASCII value computation is fixed, not an oracle; its missing loop-target
binding is the demonstrated unsound part.
