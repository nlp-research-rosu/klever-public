# Actual-program construct and rule map

The submitted AST is the byte-identical output of the trusted translator. Its
expanded `solutionProgram` macro is byte-identical at the parsed KORE level
(`04_adequacy.log`).

| Submitted construct | Declaration | Execution rules on the universal proof path | Review |
|---|---|---|---|
| `Module(...)` | `semantics/syntax.k:61` | `core.k:124-127` loads and sequences its statements | Faithfully loads the real translated statement sequence. |
| `ImportFrom("typing","List")` | `syntax.k:43` | `controls.k:35-44`; the `owise` rule at line 36 makes non-`math` imports no-ops | Adequate for an erased Python type-only import; it affects neither value nor control. |
| `FuncDef("below_zero", Params("operations"), BODY)` | `syntax.k:53,57,60` | `functions.k:14-16` stores the exact body in `closureVal` in module scope | No body replacement occurs during definition loading. |
| `Call(Name("below_zero"), list(...))` | `syntax.k:28` | `core.k:131-154` resolves the exact module binding; `call.k:20-21,69-75` evaluates callee/argument, allocates a local frame, binds the body, and installs `#endcall` | Binding, argument order, frame allocation, and return continuation are pinned. |
| `Assign(Name("balance"), Int(0))` and `Assign(Name("operation"), Int(0))` | `syntax.k:9,12,41` | `core.k:194`; `controls.k:9-18` | RHS is evaluated first by strictness; ordinary local-map writes are exact. |
| `For(Name("operation"), Name("operations"), BODY)` | `syntax.k:12,45` | name lookup `core.k:131-154`; loop protocol `controls.k:69-74`; target binding `tuple.k:31-41`; typed iteration `verification.k:30-34` | Iterable is evaluated once. Each `Int` head is bound before the exact body; empty and cons iterator equations are disjoint and exhaustive. |
| `AugAssign(Name("balance"), "+", Name("operation"))` | `syntax.k:44` | RHS lookup `core.k:131-154`; local update `controls.k:20-23`; integer addition `int.k:9` | For the claimed frame both operands are `Int`; the local balance becomes exactly `B +Int I`. |
| `Compare(Name("balance"), CmpOp("<", Int(0)))` | `syntax.k:30,32`; comparison contexts `operators.k:15-17` | name/literal evaluation in `core.k`; integer comparison `int.k:22` | Left-to-right evaluation produces exactly `B +Int I <Int 0`. |
| `If(C, Return(true), .Stmts)` | `syntax.k:49-50` | `controls.k:51-54`; Boolean literal `core.k:195`; return rules `functions.k:78-90` | The negative branch records `true`, discards the loop/false-return suffix, and pops the exact frame; the nonnegative branch resumes the loop. |
| final `Return(Bool(false))` | `syntax.k:50` | `core.k:195`; `functions.k:78-90` | On exhausted iteration it returns `false` and restores all caller cells represented in the claim. |

## Proof-local extension decisions

| Extension | Class and value/control influence | Complete domain and justification |
|---|---|---|
| `belowZeroLoopBody`, `belowZeroFunctionBody`, `solutionProgram` macros (`verification.k:7-27`) | Definitional aliases only. They select program body, binding, control, and final result but do not rewrite at runtime after macro expansion. | Parsed expanded KORE exactly equals submitted `solution.mpy`; see `04_adequacy.log`. |
| `IntVals`, `intCons`, `.IntVals`, `asValSeq` (`verification.k:30-31`) | Typed inductive representation of every finite integer list. No opaque value. | Constructor sorts restrict every head to K `Int`; empty/cons exhaust the sort. |
| typed `#iterNext` rules (`verification.k:32-34`) | Proof-local operational representation. They expose the next integer head and remaining structural list. | Empty and cons LHSs are disjoint and exhaustive; each is identical to the selected semantics' native `.ValSeq`/`vCons` iterator rule modulo the typed representation. No cells are read or changed. |
| `prefixBelow` and two equations (`verification.k:37-43`) | Result-bearing definitional summary. It affects the final Boolean postcondition. | Empty/cons equations are disjoint and exhaustive; the recursive call strictly descends `IS`; the cons equation is exactly one balance update followed by the `< 0` test. |
| loop-summary rule (`verification.k:55-80`, priority 40) | Operational bridge. It summarizes all remaining loop execution, early returns, the final `false` return, `#endcall`, frame pop, and caller restoration. | `AUX-SPEC` imports only bridge-free `MPY-VERIFICATION` and proves an exactly matching 611-character normalized reachability claim. The rule accepts the same `<k>` suffix, `env`, complete scopes, allocation counters, heap, stack frame, return/exception/exit states, and variable sorts. See `03_reconstruct.log`, `04_adequacy.log`, and `05_operational_sensitivity.log`. |

No proof-local symbol is opaque, `[no-evaluators]`, `[concrete]`, or
`[simplification]`. The only proof-local `[total]` symbol is `prefixBelow`, whose
two constructor equations are exhaustive.

## Supplied but unreachable declarations

The exact supplied baseline contains opaque/no-evaluator operations for floats,
sorting, and MD5, along with total functions and priority rules for many unused
language features. The complete list and every attribute are in
`05_rule_inventory.md`. None can be reached from this program's AST or from the
proof-local `IntVals`/`prefixBelow` terms. LLVM reported non-exhaustiveness
warnings for `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`; none occurs in either K claim or any execution path of the submitted
program. These warnings are an evidence limitation about the broad supplied
language, not a false-conclusion witness on the intended `List[int]` domain.
