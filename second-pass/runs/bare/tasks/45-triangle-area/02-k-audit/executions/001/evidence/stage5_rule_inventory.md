# Stage 5 exhaustive local rule/declaration inventory

Scope: the only candidate K sources are `semantic.k`, `verification.k`, and
`spec.k`; this was established by `stage5_source_inventory.log`. Imported K
built-ins are accounted for as trust boundaries, not copied into this local
inventory.

## Local syntax declarations

| ID | Source | Declaration | Role and judgment |
|---|---|---|---|
| S1 | `semantic.k:10` | `PyVal ::= PyNum(Int, Int)` | Internal numerator/denominator value. It does not require a nonzero denominator or canonical form. The submitted execution reaches only denominators 1 and 2, so malformed pairs are not reached there. |
| S2 | `semantic.k:11` | `KResult ::= PyVal` | Marks every `PyVal` evaluated. Sound for the reached values. |
| S3 | `semantic.k:13` | `Exp ::= PyVal` | Embeds evaluated values as expressions. |
| S4 | `semantic.k:14` | `Exp ::= Int(Int)` | Translator constructor for the literal `2`. |
| S5 | `semantic.k:15` | `Exp ::= Name(String)` | Translator constructor for `a` and `h`. |
| S6 | `semantic.k:16` | `Exp ::= BinOp(String, Exp, Exp) [strict(2,3)]` | Binary operator constructor. Strictness generates heating/cooling behavior for both operands; it does not impose Python's left-to-right `seqstrict` order. The submitted operands are pure, so no false conclusion witness arises from that order gap here. |
| S7 | `semantic.k:18` | `Params ::= Params(String, String)` | Exactly two formal parameters; sufficient for this program. |
| S8 | `semantic.k:19` | `Stmt ::= Return(Exp) [strict]` | Return constructor; strictness generates evaluation of its expression. |
| S9 | `semantic.k:20` | `Stmt ::= FuncDef(String, Params, Stmt)` | One-body-statement, two-parameter function subset. |
| S10 | `semantic.k:21` | `Stmt ::= Module(Stmt)` | One-statement module subset. |
| S11 | `semantic.k:23` | `Args ::= Args(Int, Int)` | Entry harness accepts unbounded mathematical integers only. It excludes float inputs without saying so in the prompt. |
| S12 | `semantic.k:24` | `Result ::= noResult` | Initial result marker. |
| S13 | `semantic.k:24` | `Result ::= PyVal` | Completed-result injection. |
| S14 | `verification.k:8` | `Stmt ::= triangleProgram` | Proof-local abbreviation for the submitted constructor tree. `stage4_pinning.log` shows exact normalized tree identity. |

There are no local `[function]`, `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, `[owise]`, macro, alias, priority, opaque, hook, or symbol
declarations. There are no candidate helper K files.

## Configuration

`semantic.k:32-38` declares one `<triangle>` configuration with:

- `<k>`: current `Stmt`;
- `<args>`: the two harness integers, read but never changed;
- `<env>`: initially empty map, populated with parameter bindings and then
  preserved;
- `<result>`: initially `noResult`, written once by `Return`.

No heap, call stack, exception, Python object/type, float, output, or allocation
cell is modeled. Those omissions are harmless for small ordinary executions of
this pure body, but float rounding and `OverflowError` are observable and
material on the symbolic claim's unbounded integer domain.

## Ordinary and attribute-generated rules

| ID | Source | Complete local behavior | Footprint / overlap / soundness judgment |
|---|---|---|---|
| R1 | `semantic.k:42-44` | `Module(FuncDef(_F, Params(X,Y), BODY))` becomes `BODY`; `Args(A,H)` is preserved; empty environment becomes bindings `X -> PyNum(A,1)` and `Y -> PyNum(H,1)`. | Entry-harness operational bridge. It reads `<k>`, `<args>`, `<env>`; writes `<k>`, `<env>`; frames `<result>`. It skips Python module definition and a separate function-call mechanism, but for the exact one-function submitted term it binds the correct distinct names and executes the exact body. `_F` is broader than necessary, but no false witness exists on this submitted term. |
| R2 | `semantic.k:46` | `Int(I)` becomes `PyNum(I,1)`. | Reads/writes only the front of `<k>`. Correct for the used integer literal `2`; no overlap with R3-R6. |
| R3 | `semantic.k:47-48` | `Name(X)` becomes the map-bound `V`. | Reads `<env>`, writes only `<k>`. Correct for the reached `a`/`h` bindings. Missing-name behavior is stuck rather than `NameError`, but every used name is bound. |
| R4 | `semantic.k:50-51` | Multiplies two pairs componentwise. | Writes only `<k>`. For reached denominator-1 integer operands, the numerator equals Python's arbitrary-precision integer product. Noncanonical/zero-denominator pairs are over-broad but unreachable from an entry state. |
| R5 | `semantic.k:52-54` | Divides pairs as `(AN*BD)/(AD*BN)` when `BN != 0`. | Writes only `<k>`. Mathematically correct rational arithmetic, but materially false as semantics of Python `/`, whose observable result is a binary float or `OverflowError`. Witness 1: entry `A=9007199254740993,H=1` reaches `PyNum(9007199254740993,2)`, while both Python implementations return `4503599627370496.0`; see `stage5_rounding_witness.log`. Witness 2: `A=10**309,H=1` reaches a normal `PyNum(...,2)`, while Python raises `OverflowError`; see `stage5_overflow_witness.log`. Both entries satisfy the symbolic claim, so this is an unsound real-program bridge, not an unused-language gap. |
| R6 | `semantic.k:56-57` | Evaluated `Return(V)` consumes `<k>` and changes `noResult` to `V`. | Reads/writes `<k>` and `<result>`, frames `<args>`/`<env>`. Correct for the top-level harness body. General Python return/call-stack behavior is unmodeled, but no stack or trailing continuation exists on this submitted path. |
| R7 | `verification.k:9-11` | `triangleProgram` expands to the exact `Module(FuncDef(...))` constructor tree. | Pure syntactic expansion in `<k>` or any `Stmt` context; no cells are read or written directly. It carries no answer and does not bypass R1-R6. Tree identity is independently checked in `stage4_pinning.log`, and the direct-tree claim closes in `stage4_prove_direct.log`. |
| G1 | generated from S6 | Heat/cool operand 2 and operand 3 of `BinOp` until each is a `KResult`. | Potentially permits either pure operand first; both orders reach the same values and state in this program. |
| G2 | generated from S8 | Heat/cool the expression inside `Return` until it is a `KResult`. | Ensures R6 cannot fire before body-expression evaluation. |

R2-R6 have distinct front constructors or operator strings, so no local
ordinary-rule overlaps or priority conflicts exist. R5's nonzero guard is true
on the only source divisor, `Int(2)`. No local recursive function, totalization,
or simplification termination/coverage obligation exists.

## Submitted constructor-to-rule coverage

| Submitted construct | Declaration | Execution rule(s) |
|---|---|---|
| `Module` | S10 | R1 |
| `FuncDef` | S9 | consumed within R1 |
| `Params("a","h")` | S7 | consumed within R1 |
| `Return` | S8 | G2 then R6 |
| `BinOp("/",...)` | S6 | G1 then R5 |
| `BinOp("*",...)` | S6 | G1 then R4 |
| `Name("a")`, `Name("h")` | S5 | R3 |
| `Int(2)` | S4 | R2 |
| proof entry `triangleProgram` | S14 | R7 |

## Reachability claims

- C1 (`spec.k:8-12`): from any unbounded K integers `A,H`, empty environment,
  `noResult`, and `triangleProgram`, execution terminates with empty `<k>`,
  exact bindings, and the strongly constrained pair `PyNum(A*H,2)`.
- C2 (`spec.k:15-19`): the same exact transition at `A=5,H=3`, result
  `PyNum(15,2)`.
- C3 (`spec.k:21-25`): the same exact transition at `A=0,H=99`, result
  `PyNum(0,2)`.

All are positive target claims and all close independently under this generated
theory. C2 and C3 agree with real Python; C1 is false as a universal
real-program characterization because it depends on R5 over all K integers.
