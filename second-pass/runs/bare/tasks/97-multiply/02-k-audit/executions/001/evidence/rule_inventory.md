# Exhaustive local rule and declaration inventory

Source hashes and the mechanical declaration census are in
`10_static_source_census.log`. There are no candidate helper K sources beyond
`semantic.k`, `verification.k`, and `spec.k`.

## Configuration and value domains

`semantic.k:53-59` defines one `<task>` configuration with:

- `<k>` initially containing the parsed `Program` followed by the fixed
  `#invoke("multiply", A, B)` harness;
- `<env>` for integer local-variable bindings;
- `<functions>` for loaded function definitions; and
- `<result>` initially `noResult`, later an `Int`.

This is sufficient for the submitted top-level, two-argument, integer-only
program. There is deliberately no heap, I/O, exception state, or call stack.
Those omissions would be inadequate for a larger Python subset, but none is
exercised by `solution.mpy`.

## Local syntax and attributes

| Source | Declaration | Attribute / generated behavior | Audit decision |
|---|---|---|---|
| `semantic.k:10` | `Program ::= Module(Stmts)` | `symbol(Module)` | AST constructor used and executed by S1. |
| `semantic.k:11` | `Stmts ::= List{Stmt,""}` | list unit `.Stmts` and juxtaposition | Exact statement-list representation emitted by the translator. |
| `semantic.k:13` | `Params ::= Params(String,String)` | `symbol(Params)` | Exact two-parameter form used by the submitted function. |
| `semantic.k:15-19` | `Stmt ::= FuncDef | If | Assign | Return` | named `symbol` attributes | Exactly the four statement nodes present in `solution.mpy`; no unused behavior is needed. |
| `semantic.k:21-25` | `Expr ::= Int | Name | UnaryOp | BinOp | Compare` | named `symbol` attributes | Exactly the five expression nodes present in `solution.mpy`. |
| `semantic.k:27` | `CmpOp ::= CmpOp(String,Expr)` | `symbol(CmpOp)` | Carries the used `<` operator and right operand. |
| `semantic.k:36-37` | `Function ::= function(String,String,Stmts)` | `symbol(function)` | Opaque data constructor stored in `<functions>`; it does not compute a result. |
| `semantic.k:38` | `Result ::= noResult | Int` | `symbol(noResult)` | `noResult` is an opaque initialization sentinel; it cannot determine the final integer. |
| `semantic.k:40-48` | `KItem ::= #invoke | #if | #assign | #return | #lessThan` | `strict(1)` on `#if`; `strict(2)` on `#assign`; `strict(1)` on `#return`; `strict` on both `#lessThan` operands | Internal computations. Strictness generates standard heat/cool rules. Both less-than operands are pure in this program, so unspecified order cannot change state or result. |
| `semantic.k:50` | `KResult ::= Int | Bool` | result classification | Correct values for all used expressions. |
| `semantic.k:51` | `Expr ::= Int | Bool` | injection of evaluated values | Lets strict computations receive results. |
| `semantic.k:81-82` | `KItem ::= #unaryMinus(Expr)` | `strict(1)` | Evaluates the pure operand before S9. |
| `semantic.k:87-90` | `KItem ::= #modulo | #multiply` | `strict` on both operands | Both operands are pure name/literal expressions in this program; the lack of left-to-right `seqstrict` has no observable effect here. |
| `verification.k:9` | `Stmts ::= multiplyBody` | `symbol(multiplyBody)` | Closed abbreviation, completely expanded by V1. |
| `verification.k:19` | `Program ::= multiplyProgram` | `symbol(multiplyProgram)` | Closed abbreviation, completely expanded by V2. |
| `verification.k:24-25` | `Int ::= unitDigit(Int)` | `function`, `total`, `symbol(unitDigit)` | Only proof-local function. V3 is unguarded, terminating, and covers every integer. |

There are no local declarations bearing `functional`, `simplification`,
`concrete`, `priority`, `owise`, or `anywhere`. There are no local priority
rules, simplification rules, lemmas, auxiliary claims, fresh variables, or
unconstrained result-bearing opaque symbols.

## Ordinary semantic rules

| ID | Source and rule | Complete role / state footprint | Decision |
|---|---|---|---|
| S1 | `semantic.k:62` `Module(SS) => SS` | Removes the module wrapper; no state cells touched. | Faithful module-body scheduling for the one submitted definition. |
| S2 | `semantic.k:63` `(S SS) => S ~> SS` in `<k>` | Selects the first statement and leaves the tail as continuation. | Enforces source statement order. |
| S3 | `semantic.k:64` `.Stmts => .K` | Consumes an empty statement list. | Faithful empty-branch/list behavior. |
| S4 | `semantic.k:67-68` load `FuncDef` | Reads its exact name, two parameters, and untranslated body; updates only `<functions>[F]`; consumes the definition. | Faithful for the single module-level definition. |
| S5 | `semantic.k:71-73` `#invoke` | Looks up exact `F` in `<functions>`, schedules that stored `BODY`, and resets `<env>` to the two actual/formal bindings. `<functions>` and `<result>` are preserved. | Faithful for the fixed top-level entry harness. It is not a general nested-call semantics, but `Call` is absent from the submitted AST. |
| S6 | `semantic.k:76` `Int(I) => I` | Evaluates an integer AST literal. | Exact mathematical-integer literal meaning. |
| S7 | `semantic.k:77-78` `Name(X) => I` | Reads the exact integer binding from `<env>`; no writes. | Faithful for all submitted variable reads. |
| S8 | `semantic.k:80` unary `"-"` dispatch | Replaces the used AST node by `#unaryMinus(E)`. | Exact operator dispatch; no oracle. |
| S9 | `semantic.k:83` unary-minus computation | Computes `0 -Int I`. | Ordinary integer negation; truthful for every integer. |
| S10 | `semantic.k:85` modulo dispatch | Replaces `BinOp("%",...)` by `#modulo`. | Exact used-operator dispatch. |
| S11 | `semantic.k:86` multiplication dispatch | Replaces `BinOp("*",...)` by `#multiply`. | Exact used-operator dispatch. |
| S12 | `semantic.k:91-92` modulo computation | Computes `I1 %Int I2` when `I2 != 0`; no state. | All actual divisors are literal `10`, and operands have already been made nonnegative. Thus K remainder and Python `%` agree on every reached use. Missing zero-division behavior is unused, not fabricated. |
| S13 | `semantic.k:93` multiplication computation | Computes `I1 *Int I2`. | Truthful mathematical integer multiplication. |
| S14 | `semantic.k:95` less-than dispatch | Replaces the exact used comparison with `#lessThan`. | Exact used-operator dispatch. |
| S15 | `semantic.k:96` less-than computation | Computes `I1 <Int I2`. | Truthful integer comparison. |
| S16 | `semantic.k:99` `If` dispatch | Places the condition in strict `#if`. | The condition is evaluated before branch selection. |
| S17 | `semantic.k:100` true branch | Selects `THEN`; discards `ELSE`. | Faithful conditional behavior. |
| S18 | `semantic.k:101` false branch | Selects `ELSE`; discards `THEN`. | Faithful conditional behavior, including `.Stmts`. |
| S19 | `semantic.k:103` assignment dispatch | Accepts the actually used `Name(X)` target and schedules expression evaluation. | Correct target binding; no generalized store oracle. |
| S20 | `semantic.k:104-105` assignment effect | Updates only `<env>[X]` to evaluated integer and consumes the statement. | Faithful local reassignment. |
| S21 | `semantic.k:109-110` return effect | Sets `<result>` to the evaluated integer and discards `_REST` in `<k>`. | Correct for return from the only entry invocation and for unreachable following statements; no caller frame exists in this scoped language. |
| S22 | `semantic.k:111` return dispatch | Schedules strict evaluation through `#return(E)`. | Faithful result evaluation before control transfer. |

The internal dispatch symbols are not opaque: S8/S9, S10/S12, S11/S13,
S14/S15, S16-S18, S19/S20, and S22/S21 each fully connect the AST node to a
builtin operation or state transition.

## Verification rules and claim

| ID | Source and rule | Classification | Decision |
|---|---|---|---|
| V1 | `verification.k:10-17` `multiplyBody =>` the three submitted statements | Definitional closed-program expansion | The RHS is the exact body in `solution.mpy`. It does not return a summary value or skip execution. The reviewer literal-program claim removes this abbreviation entirely and still proves `#Top` (`08_literal_program_kprove.log`). |
| V2 | `verification.k:20-21` `multiplyProgram => Module(FuncDef(...multiplyBody))` | Definitional closed-program expansion | Exact module/function wrapper and binding. The literal-program proof removes it entirely. |
| V3 | `verification.k:26` `unitDigit(I) => absInt(I) %Int 10` | Definitional mathematical summary | Unguarded, total over `Int`, nonrecursive, and unique. It truthfully defines the postcondition's unit digit of the absolute input. It does not replace execution. |
| C1 | `spec.k:9-20` sole reachability claim | Positive entry claim | No `requires`: all mathematical integer `A,B`. It starts with empty environment/functions, `noResult`, the exact program abbreviation, and the fixed invocation. It requires complete computation, final parameter bindings `absInt(A/B)`, the exact loaded body, and result `unitDigit(A)*unitDigit(B)`. |

V1 and V2 are ordinary rules, not macros or simplifications. Their match
domains are closed constants, so they cannot accept a broader continuation,
binding, or value interpretation than their literal right-hand sides. V3 is
the only `[function,total]` declaration; its one equation has complete
coverage, no overlap, and no descent obligation.

## Used-construct coverage map

| `solution.mpy` construct | Syntax | Rules |
|---|---|---|
| `Module` | `Program` at `semantic.k:10` | S1 |
| statement juxtaposition / empty branch | `Stmts` at `semantic.k:11` | S2, S3 |
| `FuncDef`, `Params` | `semantic.k:13,15-16` | S4 |
| fixed entry call | internal `#invoke` at `semantic.k:40-41` | S5 |
| `If` | `semantic.k:17` | S16-S18 plus strict heat/cool |
| `Compare`, `CmpOp("<",...)` | `semantic.k:25,27` | S14, S15 plus strict heat/cool |
| `Name` | `semantic.k:22` | S7 |
| `Int` | `semantic.k:21` | S6 |
| `Assign(Name(...),...)` | `semantic.k:18` | S19, S20 plus strict heat/cool |
| `UnaryOp("-",...)` | `semantic.k:23` | S8, S9 plus strict heat/cool |
| `Return` | `semantic.k:19` | S22, S21 plus strict heat/cool |
| `BinOp("%",...)` | `semantic.k:24` | S10, S12 plus strict heat/cool |
| `BinOp("*",...)` | `semantic.k:24` | S11, S13 plus strict heat/cool |

Every constructor appearing in the regenerated byte-identical
`solution.mpy` is mapped. No used construct falls through to a fabricated
result.

## Static soundness conclusion

No local semantic or proof rule is labeled unsound. In particular, there is no
answer-encoding execution rule, result-bearing oracle, free result variable,
proof-only bypass, or false algebraic simplification. The deliberately narrow
function/call/return model is sound for the submitted entry-only program but is
not a reusable Python semantics for nested calls or exceptions. Because those
constructs are not used, this is a scope limitation rather than a false-rule
witness on the intended submitted-program configurations.

The material false conclusion instead comes from implementation-to-contract
fidelity, not from a K rule: for satisfying input `A=-1, B=1`, the K theorem and
candidate Python both yield `1`, while the trusted canonical program yields
`9` (`09_claim_ground_witness.log`). The differential evidence records 338
such mismatches.
