# Exhaustive local rule and declaration inventory

Audited sources: scratch copies of `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. There are no generated
helper K source files in the candidate. K's generated heating/cooling contexts
from `strict` attributes are inventoried separately below.

## Configuration and state

`semantic.k:53-59` declares one `<task>` configuration with:

- `<k>`: submitted `Program` followed by the entry harness
  `#invoke("multiply", $A:Int, $B:Int)`;
- `<env>`: local `Map`, initially empty;
- `<functions>`: function-definition `Map`, initially empty;
- `<result>`: `noResult`, later an `Int`.

No heap, caller stack, exceptions, allocation, I/O, globals, or mutable
aggregate state are declared. None are exercised by the submitted program.

## Local syntax declarations

| ID | Location | Declaration / attributes | Role and assessment |
|---|---|---|---|
| D01 | `semantic.k:10` | `Program ::= Module(Stmts)` `[symbol]` | Translator `Module`; sound constructor. |
| D02 | `semantic.k:11` | `Stmts ::= List{Stmt,""}` | Ordered statement list; empty list is `.Stmts`. |
| D03 | `semantic.k:13` | `Params(String,String)` `[symbol]` | Two-parameter fragment used by the target. |
| D04 | `semantic.k:15-16` | `Stmt ::= FuncDef(...)` `[symbol]` | Target function definition. |
| D05 | `semantic.k:17` | `Stmt ::= If(...)` `[symbol]` | Target conditional. |
| D06 | `semantic.k:18` | `Stmt ::= Assign(...)` `[symbol]` | Target local assignment. |
| D07 | `semantic.k:19` | `Stmt ::= Return(...)` `[symbol]` | Target return. |
| D08 | `semantic.k:21` | `Expr ::= Int(Int)` `[symbol(IntLiteral)]` | Translator integer literal. |
| D09 | `semantic.k:22` | `Expr ::= Name(String)` `[symbol]` | Local-name read. |
| D10 | `semantic.k:23` | `Expr ::= UnaryOp(String,Expr)` `[symbol]` | Only `"-"` receives a semantic rule. |
| D11 | `semantic.k:24` | `Expr ::= BinOp(String,Expr,Expr)` `[symbol]` | Only `"%"` and `"*"` receive rules. |
| D12 | `semantic.k:25` | `Expr ::= Compare(Expr,CmpOp)` `[symbol]` | One-comparison fragment. |
| D13 | `semantic.k:27` | `CmpOp(String,Expr)` `[symbol]` | Only `"<"` receives a rule. |
| D14 | `semantic.k:36-37` | `Function ::= function(String,String,Stmts)` `[symbol]` | Stored closure-free entry definition. |
| D15 | `semantic.k:38` | `Result ::= noResult` `[symbol]` or `Int` | Result cell domain. |
| D16 | `semantic.k:40-41` | `#invoke(String,Int,Int)` `[symbol]` | Internal entry harness; arguments are already values. |
| D17 | `semantic.k:42-43` | `#if(Expr,Stmts,Stmts)` `[symbol,strict(1)]` | Evaluates guard before branch selection. |
| D18 | `semantic.k:44-45` | `#assign(String,Expr)` `[symbol,strict(2)]` | Evaluates RHS before map update. |
| D19 | `semantic.k:46` | `#return(Expr)` `[symbol,strict(1)]` | Evaluates returned expression. |
| D20 | `semantic.k:47-48` | `#lessThan(Expr,Expr)` `[symbol,strict]` | Pure integer comparison helper. |
| D21 | `semantic.k:50` | `KResult ::= Int \| Bool` | Values recognized by generated strict contexts. |
| D22 | `semantic.k:51` | `Expr ::= Int \| Bool` | Embeds evaluated values in expression positions. |
| D23 | `semantic.k:81-82` | `#unaryMinus(Expr)` `[symbol,strict(1)]` | Pure unary helper. |
| D24 | `semantic.k:87-90` | `#modulo`, `#multiply` `[symbol,strict]` | Pure binary integer helpers. |
| D25 | `verification.k:9` | `Stmts ::= multiplyBody` `[symbol]` | Closed abbreviation, reduced by V01. |
| D26 | `verification.k:19` | `Program ::= multiplyProgram` `[symbol]` | Closed abbreviation, reduced by V02. |
| D27 | `verification.k:24-25` | `Int ::= unitDigit(Int)` `[function,total,symbol]` | Definitional postcondition summary, reduced by V03. Its one unconditional equation covers every `Int`. |

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
associativity, opaque-result, or fresh-symbol declarations. Data constructors
such as `noResult` and `function` are not result-bearing oracles. The only
local `[function,total]` declaration is `unitDigit`.

## Ordinary semantic rules

| ID | Location | Rule | Static judgment |
|---|---|---|---|
| S01 | `semantic.k:62` | `Module(SS) => SS` | Exposes the submitted ordered statement list; sound. |
| S02 | `semantic.k:63` | list head `S SS => S ~> SS` in `<k>` | Preserves source statement order; sound. |
| S03 | `semantic.k:64` | `.Stmts => .K` | Empty-list identity; sound. |
| S04 | `semantic.k:67-68` | `FuncDef` updates `<functions>` | Stores exact formals/body and consumes only the definition; sound for target. |
| S05 | `semantic.k:71-73` | `#invoke` selects stored body and resets `<env>` to parameter bindings | Exact for the initial, closure-free entry invocation. It is intentionally not a general Python call-stack model; current program reaches it with empty environment and no caller. |
| S06 | `semantic.k:76` | `Int(I) => I` | Literal evaluation; sound. |
| S07 | `semantic.k:77-78` | `Name(X) => I` when `<env>` maps `X` to `I` | Sound local lookup; stuck on unbound names. |
| S08 | `semantic.k:80` | unary `"-"` to `#unaryMinus` | Exact operator dispatch for the used constructor. |
| S09 | `semantic.k:83` | `#unaryMinus(I) => 0 -Int I` | True integer negation. |
| S10 | `semantic.k:85` | `BinOp("%",...) => #modulo(...)` | Exact dispatch for used `%`. |
| S11 | `semantic.k:86` | `BinOp("*",...) => #multiply(...)` | Exact dispatch for used `*`. |
| S12 | `semantic.k:91-92` | `#modulo(I1,I2) => I1 %Int I2` if `I2 != 0` | K `%Int` is truncating remainder. The submitted execution reaches this only after converting both inputs to nonnegative values and with divisor `10`, where it agrees with Python `%`. |
| S13 | `semantic.k:93` | `#multiply(I1,I2) => I1 *Int I2` | True mathematical/Python-big-integer multiplication. |
| S14 | `semantic.k:95` | `Compare(...,"<",...) => #lessThan(...)` | Exact dispatch for used comparison. |
| S15 | `semantic.k:96` | integer less-than | True comparison. |
| S16 | `semantic.k:99` | `If` to strict `#if` | Preserves branches while scheduling guard. |
| S17 | `semantic.k:100` | true guard selects `THEN` | Sound. |
| S18 | `semantic.k:101` | false guard selects `ELSE` | Sound. |
| S19 | `semantic.k:103` | `Assign(Name(X),E) => #assign(X,E)` | Exact used assignment target. Unsupported targets remain visible/stuck. |
| S20 | `semantic.k:104-105` | evaluated assignment updates `<env>` | Correct local rebinding. |
| S21 | `semantic.k:109-110` | evaluated `#return` discards remaining computation and writes `<result>` | Correct for the single entry invocation and every integer input: its only reachable suffix is the rest of that function body and there is no caller/top-level continuation after `#invoke`. The rule is not evidence for a reusable multi-call Python semantics. |
| S22 | `semantic.k:111` | `Return(E) => #return(E)` | Exact scheduling of return expression. |

No S-rule encodes the target product or introduces an unconstrained value.
No overlaps have different right-hand sides: S10/S11 have disjoint operator
strings; S17/S18 have disjoint Boolean values; all other apparent helpers have
disjoint outer constructors. S12's nonzero guard covers every actual divisor
and correctly leaves division-by-zero stuck rather than fabricating a value.

## Generated strict contexts

The `strict` attributes generate heating/cooling rules for:

1. D17 guard argument;
2. D18 RHS argument;
3. D19 result argument;
4. D20 both comparison arguments;
5. D23 unary argument;
6. D24 both modulo arguments;
7. D24 both multiplication arguments.

The binary helpers use `strict`, not `seqstrict`, so either unfinished operand
may be selected. Every expression form in this submitted fragment is pure:
literal, name read, unary minus, comparison, modulo, and multiplication.
Consequently the possible order does not alter result, cells, control, or
exceptions on the submitted program. Python's left-to-right order would matter
for effectful expressions, but none are declared or used.

## Verification extensions

| ID | Location | Class | Complete domain, influence, and judgment |
|---|---|---|---|
| V01 | `verification.k:10-17` | Definitional closed-term expansion | `multiplyBody` unconditionally expands to the exact translated body. It affects all subsequent execution but introduces no result; mechanical expansion matches trusted-regenerated `solution.mpy` (`04-term-pinning.log`). |
| V02 | `verification.k:20-21` | Definitional closed-term expansion | `multiplyProgram` unconditionally expands to the exact `Module(FuncDef(...))` wrapper. V01+V02 pin the real generated program. |
| V03 | `verification.k:26` | Definitional mathematical summary | `unitDigit(I) => absInt(I) %Int 10` for every integer. The equation is terminating, non-overlapping, and total. It is used only in the postcondition, never to replace program execution. It truthfully defines the candidate's nonnegative-decimal-digit summary, although that summary is not the trusted canonical function on general negative inputs. |

There are no operational bridges, proof-local semantic shortcuts, auxiliary
claims, priorities, simplification rules, fresh variables, or opaque
result-bearing symbols in `verification.k`.

## Target claim

`spec.k:9-19` contains one unlabeled reachability claim and no `requires` or
`ensures` clause. Its sorted domain is all mathematical `A:Int, B:Int`. It
executes V02/V01 and S01-S22 from an empty environment/function map and
`noResult`, then requires:

- empty `<k>`;
- final environment `a = absInt(A), b = absInt(B)`;
- the exact stored function binding/body;
- result `unitDigit(A) *Int unitDigit(B)`.

The claim is satisfiable and result-constraining (`04-claim-witnesses.log`);
changing the executed body to `Return(Int(0))` causes a built proof to fail on
the unmet equality (`04-body-mutation-kprove.log`).

## Used-constructor coverage map

| Submitted constructor/operator | Declarations | Behavior |
|---|---|---|
| `Module` | D01 | S01 |
| statement sequence / empty branch | D02 | S02-S03 |
| `FuncDef`, `Params` | D03-D04 | S04 |
| entry call | D14, D16 | S05 |
| `If` | D05, D17 | S16-S18 + strict guard context |
| `Compare`, `CmpOp("<",...)` | D12-D13, D20 | S14-S15 + strict contexts |
| `Assign(Name(...),...)` | D06, D09, D18 | S19-S20 + strict RHS |
| `Return` | D07, D19 | S21-S22 + strict result |
| `Int` | D08, D22 | S06 |
| `Name` | D09 | S07 |
| `UnaryOp("-")` | D10, D23 | S08-S09 + strict context |
| `BinOp("%")` | D11, D24 | S10, S12 + strict contexts |
| `BinOp("*")` | D11, D24 | S11, S13 + strict contexts |

Every constructor in the trusted-regenerated `solution.mpy` is declared and
mapped to an operational rule. Unused translator constructs are deliberately
absent, which is acceptable for generated minimal semantics.
