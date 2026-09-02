# Reviewer rule inventory

This inventory covers every local declaration and explicit rule in the submitted
`semantic.k`, `verification.k`, and `spec.k`. Imported K builtins are listed in
the trust ledger in the final review rather than reproduced here.

## Local syntax and configuration

| ID | Location | Declaration / generated effect | Audit classification |
|---|---|---|---|
| S1 | `semantic.k:5` | `Program ::= Module(Stmts)` | Source constructor used. |
| S2–S3 | `semantic.k:7-8` | `Stmts ::= Stmt` and `Stmt Stmts` (`StmtSeq`) | Source statement list used. |
| S4–S6 | `semantic.k:10-12` | `FuncDef`, `Assign`, `Return` statements | All occur in the submitted module. |
| S7 | `semantic.k:14` | Two-name `Params` | Used by the submitted function. |
| S8–S14 | `semantic.k:16-22` | `Int`, `Name`, `Attribute`, zero/one-argument `Call`, `Subscript`, `BinOp` expressions | All except no source `Call0`/`Call1` variants beyond `split()` and `int(x)` are needed. |
| E1 | `semantic.k:18` | `Attribute` is strict in operand 1 | Generates the usual heat/cool evaluation context. |
| E2 | `semantic.k:19` | zero-argument `Call` is strict in callee 1 | Generates heat/cool context. |
| E3 | `semantic.k:20` | one-argument `Call` is sequentially strict in callee then argument | Matches Python left-to-right order for the used call. |
| E4 | `semantic.k:21` | `Subscript` is sequentially strict in base then index | Matches the used expression order. |
| E5 | `semantic.k:22` | `BinOp` is sequentially strict in operands 2 then 3 | Matches subtraction order for the used expression. |
| S15–S21 | `semantic.k:32-38` | `VInt`, `VStr`, `VNum`, `VFruits`, fixed-five-element `VWords`, `VSplit`, `VBuiltinInt` values | `VNum` and `VFruits` are invented proof representations with no Python value/type counterpart. |
| S22–S23 | `semantic.k:40-41` | `PyValue < Expr`; `PyValue < KResult` | Defines completed expression values. |
| S24 | `semantic.k:43` | stored `function(P1,P2,BODY)` | Holds the exact submitted body. |
| S25–S29 | `semantic.k:45-49` | `exec`, `setVar`, `finishCall`, `invokeFruit`, `invokeString` K items | `invokeFruit` is the abstract non-string proof driver; `invokeString` is the concrete driver. |
| Cfg | `semantic.k:51-56` | `<py>` with `<k>`, `<functions>`, and `<env>` | Sufficient for this pure, single-call program; no heap, output, or allocation is used. |
| F1–F2 | `semantic.k:94-95` | `spaceAt(String,Int)` and `nextSpace(String,Int)`, both `[function]` | Neither is `[total]`; `spaceAt` intentionally has no negative-index equation. |
| S30 | `verification.k:8-20` | `solutionProgram` macro and expansion rule | Macro expansion is mechanically identical to regenerated `solution.mpy` after initializer expansion. |
| S31–S32 | `verification.k:22-23` | `runFruit` and `runString` K items | Test/entry wrappers. |

There are no local `[total]`, `[functional]`, `[simplification]`, `[priority]`,
`[owise]`, `anywhere`, or opaque declarations. The only local function
declarations are F1–F2; the only macro is S30. No helper K files were submitted.

## Explicit semantic and verification rules

| ID | Location | Rule effect | Static judgment |
|---|---|---|---|
| R1 | `semantic.k:58` | `Module(SS)` begins `exec(SS)`. | Faithful for the submitted module. |
| R2 | `semantic.k:60` | A multi-statement sequence executes head then tail. | Faithful left-to-right sequencing. |
| R3 | `semantic.k:61` | A singleton `exec` exposes its statement. | Faithful. |
| R4 | `semantic.k:63-64` | `FuncDef` stores parameter names and exact body in `<functions>`. | Faithful for one module-level binding. |
| R5 | `semantic.k:66` | `Assign(Name(X),E)` evaluates `E` then schedules `setVar(X)`. | Faithful for the used assignment target. |
| R6 | `semantic.k:67-68` | A resulting value updates `<env>[X]`. | Faithful. |
| R7 | `semantic.k:70` | `Return(E)` becomes `E`. | Faithful only because the submitted return is the final statement; the language would be incomplete for a return with a trailing continuation. |
| R8 | `semantic.k:72-74` | `invokeFruit(A,O,N)` fetches the real stored body but binds `s` to invented `VFruits(A,O)` and `n` to `VInt(N)`. | Result-bearing abstract entry bridge. It is not a call on any Python string and has no bridge-free connection theorem to `invokeString` or Python execution. |
| R9 | `semantic.k:76-78` | `invokeString(S,N)` fetches the real stored body and binds `s` to `VStr(S)`. | Concrete entry driver; adequate only to the extent the later string rules model Python. |
| R10 | `semantic.k:80-82` | On a returned value, remove `finishCall` and clear function/environment maps. | Adequate for a single pure call whose only observable is its result. |
| R11 | `semantic.k:84-85` | Look up a bound `Name(X)` in `<env>`. | Faithful on submitted reachable states. |
| R12 | `semantic.k:86` | `Name("int")` becomes the builtin integer converter. | Correct on submitted states, but globally overlaps R11 if an environment binds `"int"`; that overlap is unreachable because both invocation rules replace the environment with only parameter bindings and assignment adds only `"words"`. |
| R13 | `semantic.k:87` | Source `Int(I)` becomes `VInt(I)`. | Faithful. |
| R14 | `semantic.k:89` | Any `PyValue.split` attribute becomes `VSplit(value)`. | Over-broad outside reachable `VStr`/`VFruits` inputs, but no false reachable source conclusion was found from this rule alone. |
| R15 | `semantic.k:91-92` | Splitting invented `VFruits(A,O)` fabricates five words with `VNum(A)` and `VNum(O)` at indices 0 and 3. | Task-specific result-bearing abstraction. It truthfully defines the invented pair representation, but no theorem connects it to the actual string operation. The unbounded proof depends on it and still closes with all actual-string split semantics removed. |
| R16 | `semantic.k:96` | `spaceAt(S,0) = findString(S," ",0)`. | Correct for the first literal-space position. |
| R17 | `semantic.k:97-98` | Positive `spaceAt(S,I)` recursively searches after the prior position. | Descends on `I` for the used nonnegative constants. Its correctness depends on R18's interpretation of `findString`. |
| R18 | `semantic.k:100` | `nextSpace(S,START) = START + findString(S," ",START)`. | Inconsistent with K's absolute-index `STRING.find` specification/front-end/LLVM behavior. Witness: for `"5 apples and 6 oranges"` and `START=2`, fixed `findString` is 8 but R18 yields 10. LLVM execution of the documented example aborts with an invalid slice; the Haskell backend happens to evaluate the hook relatively and masks the defect. |
| R19 | `semantic.k:102-108` | Splitting a `VStr` fabricates a fixed five-word value, extracting only positions 0 and 3 via literal spaces. | Not a faithful semantics of Python `str.split()`. Witness on a source input that terminates: Python `fruit_distribution("  5  apples and  6 oranges  ",19)` returns 8, while fresh Haskell K execution reaches `#Bottom`; the tab variant also reaches `#Bottom` while generated Python returns 8. |
| R20–R21 | `semantic.k:110-111` | Fixed-list subscripts 0 and 3 return the corresponding values. | Faithful for the only indices used by the submitted body. |
| R22 | `semantic.k:113` | `int(VInt(I))` returns `VInt(I)`. | Faithful for integer values. |
| R23 | `semantic.k:114` | `int(VNum(I))` returns `VInt(I)`. | Defined only for the invented abstract numeric-word representation; unbounded proof depends on it. |
| R24 | `semantic.k:115` | `int(VStr(S))` uses K's `String2Int`. | Faithful for decimal numeric tokens used by documented examples; partial elsewhere, like Python conversion. |
| R25 | `semantic.k:117` | subtraction of two `VInt` values uses unbounded K integer subtraction. | Faithful to Python integer subtraction. |
| R26 | `verification.k:9-20` | Macro expansion constructs the submitted function body. | Exact constructor identity independently confirmed. |
| R27 | `verification.k:25-26` | `runFruit(P,A,O,N)` sequences `P` then abstract `invokeFruit`. | A wrapper around R8; does not establish string-input correctness. |
| R28 | `verification.k:28-29` | `runString(P,S,N)` sequences `P` then concrete `invokeString`. | Faithful wrapper around R9. |

## Claim inventory

| ID | Location | Start / destination | Formal scope |
|---|---|---|---|
| Q1 | `spec.k:9-18` | Exact `solutionProgram ~> invokeFruit(A,O,N)` from empty maps reaches exactly `VInt(N-A-O)`. | Arbitrary nonnegative `A,O` and `N >= A+O`, but the first argument is invented `VFruits(A,O)`, not a `String`. |
| Q2 | `spec.k:20-25` | Concrete string `"5 apples and 6 oranges"`, 19 reaches `VInt(8)`. | One documented example. |
| Q3 | `spec.k:27-32` | Concrete string `"0 apples and 1 oranges"`, 3 reaches `VInt(2)`. | One documented example. |
| Q4 | `spec.k:34-39` | Concrete string `"2 apples and 3 oranges"`, 100 reaches `VInt(95)`. | One documented example. |
| Q5 | `spec.k:41-46` | Concrete string `"100 apples and 1 oranges"`, 120 reaches `VInt(19)`. | One documented example. |

No loop, invariant, helper claim, implication-only postcondition, RHS-only result
variable, or omitted result cell appears. All five destinations constrain the
returned value exactly.

## Submitted-constructor coverage map

`Module→R1`; `FuncDef/Params→R4`; `StmtSeq→R2/R3`; `Assign→R5/R6`;
`Return→R7`; `Name→R11/R12`; `Attribute(...,"split")→R14`;
zero-argument `Call→R15 or R19`; `Int→R13`; `Subscript(0/3)→R20/R21`;
one-argument `Call(Name("int"),...)→R22/R23/R24`; and subtraction
`BinOp→R25`. Thus every constructor in `solution.mpy` has a rule path, but the
unbounded path deliberately selects the abstract R8/R15/R23 branch rather than
the actual-string R9/R19/R24 branch.
