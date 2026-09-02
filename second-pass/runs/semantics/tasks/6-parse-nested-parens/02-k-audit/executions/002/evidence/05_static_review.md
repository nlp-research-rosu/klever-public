# Static rule and used-path review

The exhaustive machine-generated inventory is
`05_rule_inventory.tsv`. It contains 958 source entries: 237 syntax
declarations, 713 rules, 5 contexts, 1 configuration, and 2 claims. Of these,
928 belong to the byte-identical launcher-supplied fixed semantics, 28 are
proof-local entries in `verification.k` (10 syntax declarations and 18 rules),
and 2 are claims in `spec.k`. There are no proof-local priority,
simplification, `functional`, opaque, or `no-evaluators` declarations.

## Fixed supplied semantics

Every fixed-semantics source entry is inventoried individually as
`ACCEPTED_FIXED_SUPPLIED_SEMANTICS`. The candidate copy was recursively equal
to the trusted mount, including entry types, and contained no symlink. Under
the benchmark's `SUPPLIED_SEMANTICS` boundary this is the selected fixed
language model, not a candidate proof extension.

The used execution path was nevertheless checked directly:

| Submitted construct/effect | Fixed declaration/rules | Review |
|---|---|---|
| Direct closure call and argument evaluation | `syntax.k` `Call`; `call.k:20-21,69-76`; `core.k:186-191` | Callee first, then the one argument, then exact closure application; frame created at scope 1 and stack frame records the caller. |
| The omitted module `ImportFrom("typing","List")` and `FuncDef` | `controls.k:35-36`; `functions.k:14-16` | Typing import is a no-op. Loading the submitted `FuncDef` would bind the exact parameter/body closure at definition environment 0. Mechanical KAST comparison proves the claim constructs that same closure directly. |
| Local lookup and writes | `core.k:130-153`; `controls.k:9-24`; `tuple.k:32-41` | Ordinary non-cell local scope. Lookup, assignment, augmented assignment, and loop-target binding preserve all other cells. |
| Empty list and heap allocation | `list.k:14-15`; `core.k:117-121` | Allocates `list(.ValSeq)` at fresh heap location 0 and increments `heapLoc` once. |
| String literals/input iteration | `str.k:8-17` | ASCII literals become code sequences; each input code yields one one-character semantic string in order. |
| `for` control | `controls.k:65-74` | Iterable evaluated once; each yield binds `char`, executes the exact loop body, and resumes on the residual string. |
| Comparisons and branches | `operators.k:15-17`; `str.k:25`; `int.k:24`; `controls.k:51-54`; `core.k:199-205` | Operands evaluate left-to-right; string equality and integer greater-than produce Bool; the selected branch alone executes. |
| Integer depth updates | `int.k:9,13`; `controls.k:20-24` | Unbounded K integers implement `+1` and `-1`; no overflow abstraction. |
| `result.append(maximum)` | `call.k:16,20-24`; `list.k:53-55`; `controls.k:48` | Receiver binding is the heap ref in local `result`; append mutates that exact list in place and the expression statement discards `noneV`. |
| Return and frame cleanup | `functions.k:78-90` | Return fixes `retV(ref(0))`, pops the callee, restores environment 0 and `scopeLoc` 1, deletes scope 1, and preserves the escaping heap list. |
| Result-list concatenation in the mathematical summary | `list.k:18-20` | Structural, total append with descent on the first `ValSeq`. It is not an operational shortcut. |

No fixed opaque symbol is reachable on this path. The 22 inventoried
`no-evaluators` symbols are `md5hexCodes`; the float-family
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`; and `sortVS` and
`sortKeyVS`. The submitted term cannot call any of them.

## Proof-local declarations and all 18 rules

| Lines | Entries | Class and decision |
|---|---|---|
| `verification.k:7-20` | `parseLoopBody` declaration and rule | Definitional program-term alias. It does not match a fixed operational redex. Its parsed constructor tree is identical to the `For` body in freshly regenerated `solution.mpy`. |
| `verification.k:23-31` | `parseFunctionBody` declaration and rule | Definitional program-term alias. Expanding `parseLoopBody` produces the constructor-identical submitted function body. |
| `verification.k:33-35` | `parseNestedParensClosure` declaration and rule | Definitional binding alias. It has the submitted sole parameter, identical body, and module definition environment 0. |
| `verification.k:41-42` | `ScanState`, `scanDone`, `scanParens` declaration | Mathematical summary datatype/function only; it never rewrites `<k>` or any cell. |
| `verification.k:44-46` | `parenMax` declaration and two equations | Truthful maximum: guards `A > B` and `A <= B` are disjoint and exhaustive over Int. Totality is justified. |
| `verification.k:48-58` | Five `scanParens` equations | Empty input returns the accumulated state. Codes 40, 41, and 32 respectively update depth/maximum, decrement depth, or append/reset. The `owise` case ignores every other code, matching the program's final `elif` fall-through. Constructor cases are disjoint and each recursive rule consumes one code. |
| `verification.k:60-65` | Three projection declarations and three equations | Project the three fields of `scanDone`. Every ground `scanParens` structurally normalizes to `scanDone`; no conflicting equation exists. |
| `verification.k:67-70` | `finalChar` declaration and two equations | Empty suffix preserves the old loop variable; nonempty suffix consumes one code and recursively leaves its last one-character string. Complete and descending. |
| `verification.k:72-76` | `parsedParens` declaration and equation | Spec-side result definition: completed group maxima followed by the final current maximum, exactly mirroring the submitted final append. It neither bypasses nor rewrites execution. |
| `verification.k:78-82` | `parenInput` declaration and two equations | Complete structural predicate accepting exactly code points 40, 41, and 32. It does not require balance, nonempty groups, or normalized separators. |

The equations have no overlap with inconsistent right-hand sides, and every
recursive definition descends structurally. The only `owise` proof-local rule
is the truthful fall-through case of `scanParens`. The `[total]` declarations
are `parenMax`, the three projections, `finalChar`, and `parenInput`; their
coverage is as stated above. There is no proof-local oracle, abrupt-control
bridge, priority rule, operational rewrite, or assumed lemma.

## Claims and state footprints

`parse-loop` is a circularity over the fixed `#loop`. It updates exactly the
loop-touched locals (`depth`, `maximum`, `char`) and heap object 0 while
preserving the arbitrary continuation, input binding, scope locations, caller
stack, return/exception/exit cells, and other fixed frame structure. The
result summary is derived by real fixed-semantics loop execution.

`parse-nested-parens` begins from an explicit initial configuration, evaluates
the mechanically pinned closure, and fixes the returned reference, entire
result heap value, allocation counters, scopes, stack, return state,
exception state, and exit code. The output is not a free variable or
implication-only condition.

The fresh body mutation changed an expression inside the actually executed
`parseLoopBody` term; the definition rebuilt, and the unchanged proof became
stuck. This confirms body sensitivity independently of source-file linkage.
