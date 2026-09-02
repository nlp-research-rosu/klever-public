# Exhaustive local K inventory

This inventory covers the candidate source copies at
`/tmp/audit-work/135-can-arrange/source/{semantic.k,verification.k,spec.k}`.
Imported standard K modules are part of the trust boundary, not local rules.
The reviewer-added `pin-spec.k` and mutation specs are evidence, not candidate
extensions.

## Declarations, attributes, and configuration

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`.
- `Stmts`: separator-free list of `Stmt`.
- `Params`: `Params(Strings)`.
- `Strings`, `Exps`, and `CmpOps`: comma-separated lists.
- `Stmt`: `FuncDef`, `Return`, `Assign`, and `If`.
- `Exp`: `Int`, `Name`, `Call`, `Compare`, `Subscript`, `Slice`, `BinOp`, and
  `UnaryOp`.
- `Bound`: an `Exp` or `NoBound`.
- `CmpOp`: `CmpOp(String, Exp)`.
- `Ints`: comma-separated `Int` list.
- `Arr`: `seq(Ints)`.
- `Val`: `intVal`, `boolVal`, and `arrayVal(Arr, Int, Int)`.
- `Function`: `function(Params, Stmts)`.

`MPY` declares 20 control `KItem`s: `invokeEntry`, `load`, `install`, `invoke`,
`exec`, `eval`, `value`, `assignTo`, `branch`, `callValue`, `applyLen`,
`sliceFromOne`, `indexAt`, `unaryMinus`, `binLeft`, `binRight`, `cmpLeft`,
`cmpRight`, `doReturn`, and `noReturn`.

The configuration is `<mpy>` containing:

- `<k> $PGM:Pgm ~> invokeEntry($ARGS:Val) </k>`;
- `<env> .Map </env>`;
- `<defs> .Map </defs>`;
- `<stack> .List </stack>`.

Local `[function, total]` declarations are `appendStmts`, `get`, `arrSize`,
`intsSize`, `answer`, and `answerStep`. `appendStmts`, `arrSize`, `intsSize`,
`answer`, and `answerStep` have disjoint, covering equations and structural
descent where recursive. `get` does not: there is no equation for
`get(seq(.Ints), N)` or negative `N`. Fresh LLVM compilation reports exactly
this non-exhaustive total match. The target claim's bounds invariant keeps all
actual `get` uses in range, but the global `[total]` declaration is inaccurate.
The empty-index probe reaches the unsupported residual and exits 113 rather
than fabricating a fixed integer; this is recorded as a coverage/totality gap,
not as an alleged false numeric equation.

The only `[macro]` declarations are `canArrangeFunction` and
`solutionProgram`. There are no local `[functional]`, `[simplification]`,
`[concrete]`, priority, `owise`, or explicit opaque declarations. There are no
candidate helper K files. The only candidate reachability claim is the entry
claim in `spec.k`.

## Construct coverage for `solution.mpy`

| Submitted construct | Declaration | Operational coverage |
|---|---|---|
| `Module` and `FuncDef` | `Pgm`, `Stmt` | S03-S07 |
| statement lists and `Params("arr")` | list and `Params` syntax | S01-S02, S04-S06, S08-S16 |
| `If` | `Stmt` | S12-S14 |
| `Assign(Name("result"), ...)` | `Stmt`, `Exp` | S10-S11, S18 |
| `Return` | `Stmt` | S15-S16 |
| `Int`, `Name` | `Exp` | S17-S18 |
| unary `-` | `UnaryOp` | S19-S20 |
| `len(arr)` | `Call` | S21-S22 |
| recursive `can_arrange(...)` | `Call` | S23-S24 and S08 |
| `arr[1:]` | `Subscript`, `Slice`, `Bound` | S25-S26 |
| `arr[0]`, `arr[1]` | `Subscript` | S27-S28, S40-S41 |
| integer `+` | `BinOp` | S29-S31 |
| one-link `<=`, `!=`, `<` comparisons | `Compare`, `CmpOp`, `CmpOps` | S32-S36 |
| integer arrays and view length | `Arr`, `Ints`, `Val` | S22, S26, S28, S37-S41 |

Every constructor in the submitted term has a declaration and a rule path.
Generic syntax admits forms not needed here; these deliberately stop when no
rule covers them.

## `semantic.k` rules (41)

| ID | Lines | Rule | Decision |
|---|---:|---|---|
| S01 | 78 | `appendStmts(.Stmts, MORE) => MORE` | Sound empty-list concatenation. |
| S02 | 79 | `appendStmts(S REST, MORE) => S appendStmts(REST, MORE)` | Sound structural concatenation; first argument decreases. |
| S03 | 91 | `Module(SS) => load(SS)` | Sound target-module loading step. |
| S04 | 92 | `load(.Stmts) => .K` | Sound completion of module loading. |
| S05 | 93-94 | expose a `FuncDef` as `install ~> load(REST)` | Sound left-to-right definition installation. |
| S06 | 95-96 | install `F` as `function(PS,BODY)` in `<defs>` | Sound for the scoped function-only module; later definitions overwrite earlier ones. |
| S07 | 97 | `invokeEntry(V) => invoke("can_arrange",V)` | Sound target harness, not a general Python module rule. |
| S08 | 102-105 | invoke a one-parameter function; save caller env on stack | Sound for the submitted single-parameter function. Exact lookup, local binding, caller map, and continuation are preserved. |
| S09 | 107 | `exec(.Stmts) => .K` | Sound statement-list completion. Falling off a function then leaves `noReturn` unsupported, but every submitted branch returns. |
| S10 | 108-109 | evaluate assignment RHS, then assign, then execute rest | Sound Python order for the target assignment. |
| S11 | 110-111 | update local environment after obtaining a value | Sound local assignment. |
| S12 | 113-114 | evaluate `If` condition before branching | Sound control/evaluation order. |
| S13 | 115-116 | true branch plus following statements | Sound; `appendStmts` preserves the enclosing continuation. |
| S14 | 117-118 | false branch plus following statements | Sound; guards are disjoint from S13. |
| S15 | 120 | evaluate a return expression and discard following statements | Sound abrupt-return behavior. |
| S16 | 121-123 | consume the current call's `noReturn`, restore caller env, pop one frame | Sound for normal return; the exact sentinel prevents unwinding the wrong frame. |
| S17 | 126 | integer literal to `intVal` | Sound. |
| S18 | 127-128 | local name lookup | Sound for local `arr` and `result`. Calls treat callable names separately. |
| S19 | 130 | evaluate unary-minus operand first | Sound. |
| S20 | 131 | unary integer minus as `0 -Int I` | Sound for arbitrary-precision integers. |
| S21 | 133 | evaluate the sole `len` argument | Sound under the closed-module/builtin-`len` assumption. |
| S22 | 134 | array-view length is `N` | Sound for well-formed views (`N >= 0`); the claim enforces this invariant. |
| S23 | 136-137 | evaluate sole argument of a non-`len` named call | Sound for the recursive call; guard is disjoint from S21. It abstracts global-name lookup under a closed-module assumption. |
| S24 | 138 | call the named definition after argument evaluation | Sound for the pinned definition map. |
| S25 | 140-141 | evaluate the receiver of exactly `[1:]` | Sound evaluation order for this side-effect-free fixed slice. |
| S26 | 142-143 | `[1:]` maps `(A,O,N)` to `(A,O+1,N-1)` | **False on its complete match domain.** For `N=0`, Python `[][1:]` has length 0, while this rule produces length -1. The executable witness `slice_boundary_probe.py` returns Python `0` but fresh K `-1`. The submitted function reaches this rule only after establishing `N>1`, so the target proof does not exercise the false case; nevertheless this is an over-broad false semantic rule. |
| S27 | 145 | evaluate receiver of a literal integer subscript | Sound for the target's indices 0 and 1. |
| S28 | 146-147 | select `get(A,O+I)` | Sound on in-bounds target accesses. It omits Python negative-index and exception behavior outside that range; the unused `N` and lack of a bounds guard expose the incomplete boundary. |
| S29 | 149-150 | evaluate binary left operand first | Sound. |
| S30 | 151-152 | evaluate binary right operand second, retaining left value | Sound. |
| S31 | 153-154 | integer `+` | Sound; operand placement yields left `I` plus right `J`. |
| S32 | 156-157 | evaluate left side of a one-link comparison | Sound for all submitted comparisons. |
| S33 | 158-159 | evaluate right side, retaining left value | Sound. |
| S34 | 160-161 | integer `<=` | Sound; computes retained left `I <= J` where `J` is the evaluated right. |
| S35 | 162-163 | integer `!=` | Sound. |
| S36 | 164-165 | integer `<` | Sound. |
| S37 | 172 | `arrSize(seq(IS)) => intsSize(IS)` | Sound and covering because `seq` is the only `Arr` constructor. |
| S38 | 173 | empty integer-list size is 0 | Sound. |
| S39 | 174 | nonempty size is one plus tail size | Sound structural recursion. |
| S40 | 175 | `get` index 0 from nonempty sequence is the head | Sound. |
| S41 | 176-177 | positive index selects from tail at `N-1` | Sound structural equation on its guard. Together with S40 it intentionally lacks out-of-range/negative cases despite `[total]`. |

No S-rule is an operational proof bridge: these rules are the generated
language definition itself. The only demonstrated false equation is S26, with
the concrete false-conclusion witness cited above. S28/S40/S41 and `[total]`
`get` are instead reported as an incomplete unsupported boundary because the
probe stops/errors and does not establish a false fixed integer result.

## `verification.k` rules (7)

| ID | Lines | Rule | Class and decision |
|---|---:|---|---|
| V01 | 12-13 | `answer(A,O,N) => -1` when `N <= 1` | Definitional summary; sound base case. Guard is disjoint from V02. |
| V02 | 14-19 | recurse on suffix and call `answerStep` when `N > 1` | Definitional summary; sound. `N` decreases, and the entry bounds imply both selected positions are valid. |
| V03 | 21-22 | non-`-1` tail result shifts by one | Sound: every tail drop has a larger original index than the head pair. |
| V04 | 23-24 | no tail drop plus `Y < X` gives index 1 | Sound. |
| V05 | 25-26 | no tail drop plus `Y >= X` gives `-1` | Sound and complementary to V04 over integers. V03-V05 cover all integer arguments without overlap disagreement. |
| V06 | 31-45 | `canArrangeFunction` macro | Exact program data, not an operational bridge. The full-program pin proof can unify the loaded submitted body with this macro. |
| V07 | 47-61 | `solutionProgram` macro | Exact full program data. Expanded KORE is byte-identical to the freshly translated submitted `solution.mpy`. |

`answer` is result-bearing but not opaque and does not replace execution. Its
equations exhaustively define the mathematical result. The entry reachability
claim executes the real body until recursive invocations, where the same
guarded reachability claim is used as the inductive/circular hypothesis. No
rule rewrites `invoke`, `exec`, or another program term directly to `answer`.

## Candidate claim

The single claim in `spec.k` has no free result oracle. It requires a
well-formed in-bounds array view, fixes the definition map to the exact submitted
function body, preserves arbitrary caller environment, stack, and continuation,
and requires the returned integer to equal the fully defined `answer(A,O,N)`.
The empty-array false-result mutation reaches `value(intVal(-1))`, cannot unify
with required `value(intVal(0))`, emits `WarnStuckClaimState`, and exits 1.
