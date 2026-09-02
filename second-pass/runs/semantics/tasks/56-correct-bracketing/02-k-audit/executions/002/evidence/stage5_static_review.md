# Static rule review evidence

## Inventory scope

`stage5_rule_inventory.tsv` records every declaration beginning with
`configuration`, `syntax`, `context`, `rule`, or `claim` in the trusted copied
supplied-semantics tree, `verification.k`, and `spec.k`. It contains 949
source-located entries: 1 configuration, 228 syntax declarations, 5 contexts,
712 rules, and 3 claims. The fixed tree contributes 928 entries;
`verification.k` contributes 1 syntax declaration and 17 rules; `spec.k`
contributes 3 claims.

All 24 copied supplied-semantics files are byte-identical to the trusted mount.
Their entries are classified as the selected fixed-semantics trust boundary.
Every unused declaration is unreachable from the submitted term and cannot
contribute to claim closure. The reachable subset and every proof-local entry
are reviewed below.

## Used constructor/rule map

| Submitted construct | Declaration | Fixed execution rules |
|---|---|---|
| `Module`, statement list | `syntax.k:56-62` | `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params` | `syntax.k:51-61` | `functions.k:14-16` installs the exact closure |
| `Expr(Str(...))` docstring | `syntax.k:9-31, 51-55` | `str.k:12-17` evaluates ASCII strings; `controls.k:48` discards expression values |
| `Assign(Name, Int/Str)` | `syntax.k:9-31, 41-55` | strict RHS evaluation; `core.k:194-196` and `str.k:12-17`; `controls.k:9-11` updates the current scope |
| `Call(Name, str(S))` | `syntax.k:9-31` | `core.k:131-154` lookup; `call.k:15-17` left-to-right callee/arguments; `call.k:69-75` frame allocation; `functions.k:63-66` parameter binding |
| `For(Name, Name, body)` | `syntax.k:41-55` | strict iterable lookup; `controls.k:69-74`; `str.k:9-11` yields one-character strings; `tuple.k:31-34` binds the target; `controls.k:85` continues |
| `If(Compare(...))` | `syntax.k:9-38, 41-55` | `operators.k:12-18` left-before-right compare; `core.k:131-154` lookup; `str.k:12-29` and `int.k:22-27` comparisons; `controls.k:51-54` branches |
| `AugAssign(Name, +/- , Int(1))` | `syntax.k:41-55` | strict RHS, then `controls.k:20-23`; `int.k:9-17` arithmetic |
| `Return(Bool/Compare)` | `syntax.k:41-55` | strict expression evaluation; `functions.k:78-90` abrupt return, frame pop, scope deletion, environment/allocator restoration |

The configuration cells used by this path are the fixed `core.k:49-60`
configuration. The program never allocates heap values, mutates the heap,
raises an exception, performs output, or changes the exit code. Function calls
allocate only a scope frame and stack frame, both removed on return.

## Proof-local function and equations

`bracketResult(IntSeq, Int)` (`verification.k:10`) is a result-bearing
definitional summary, declared `[function, total]`; it is not opaque.

| Lines | Domain and result | Review |
|---|---|---|
| 12 | empty suffix, depth 0 -> true | Correct base case. |
| 13-15 | empty suffix, positive depth -> false | Correct: openings remain unmatched. |
| 16-18 | empty suffix, negative depth -> false | Correct prefix-validity summary: a prior negative prefix is irrecoverably invalid. This domain is not used as a fresh executable loop state. |
| 20-22 | leading `<` at depth 0 -> recurse at 1 | Correct. The suffix structurally decreases. |
| 23-25 | any non-`<` at depth 0 -> false | Correct for the program and, in particular, for `>` on the source domain: the next step makes depth negative and returns immediately. |
| 27-29 | leading `<` at positive depth -> increment | Correct; suffix decreases. |
| 30-32 | non-`<` at positive depth -> decrement | Correct; suffix decreases. |
| 33-35 | any nonempty suffix at negative depth -> false | Correct as the logical prefix-validity summary; unreachable as a fresh loop head from the submitted program. |

Coverage is exhaustive for algebraic `IntSeq` and mathematical `Int`:
empty/cons, and depth zero/positive/negative; character 60/non-60 splits are
disjoint. All overlaps are either impossible by guards or have identical
meaning. Recursive equations strictly shorten the suffix. The
`[simplification]` equations are true on their complete guards. No fresh or
unconstrained value enters a branch, state cell, return value, or
postcondition.

## Proof-local operational rules

| Lines | Class and complete match | State/control review | Connection evidence |
|---|---|---|---|
| 41-43 | Bridge for `Return(Bool(B))` with arbitrary callee suffix and `ret=noRet` | `Bool(B)` is side-effect-free; fixed `Return` discards the same arbitrary suffix, sets `retV(B)`, and starts `#pop`. No other cell changes. | Static composition of `core.k:195` and `functions.k:78-79`. The fixed Haskell connection probe reaches `B ~> #freezerReturn ~> SUFFIX` but cannot cool it; fixed LLVM and bridge-enabled Haskell ground runs agree. |
| 45-59 | Bridge for final `Return(depth == 0)` in the exact three-binding local frame | The pattern fixes `depth` to an `Int`; fixed lookup, literal, equality, and abrupt return yield the same `retV(D ==Int 0)` and discard the same suffix. | Static composition of `core.k:131-134,194`, `operators.k:14-18`, `int.k:26`, and `functions.k:78-79`. The fixed connection probe has the same freezer limitation. |
| 61-76 | Open-character `If` bridge | Exact one-character string and exact local frame; fixed comparison is true iff code 60. The rule preserves the continuation and all cells by rewriting to the fixed `#branch`. | Universal bridge-free claim `if-bracket-open` prints `#Top`. |
| 78-93 | Non-open-character `If` bridge | Complementary guard; same continuation and cell footprint. | Universal bridge-free claim `if-bracket-close` prints `#Top`. |
| 95-106 | `depth += 1` bridge | Exact integer local binding; fixed strict literal and `applyBin("+",D,1)` make the identical map update. Continuation and other cells are preserved. | Universal bridge-free claim `augassign-plus` prints `#Top`. |
| 108-119 | `depth -= 1` bridge | Exact integer local binding; identical fixed update to `D -Int 1`. | Universal bridge-free claim `augassign-minus` prints `#Top`. |
| 121-136 | Negative-depth `If` bridge | Exact integer comparison and true branch, with all context preserved. | Universal bridge-free claim `if-depth-negative` prints `#Top`. |
| 138-153 | Nonnegative-depth `If` bridge | Complementary integer guard and false branch. | Universal bridge-free claim `if-depth-nonnegative` prints `#Top`. |
| 159-168 | `#pop` map-normalization bridge | Requires the callee location absent from `SC`; deleting `L` from `(L |-> frame) SC` is exactly `SC`. It restores the caller, saved scope location, result, and stack tail exactly as `functions.k:85-90`; heap/exception/exit cells are preserved. | The fixed probe reaches the exact fixed map-update normal form but the implication engine does not reduce it to `SC`. This is a backend normalization gap, not a conflicting transition. |

All priority-40 rules preempt only the corresponding fixed route on a strictly
narrower, exact program-state pattern. They do not match another binding, a
heap cell, a noninteger depth, a multi-character loop target, or a different
operation. The two `If` pairs have complementary guards; the two arithmetic
rules have distinct operator literals; the return forms are disjoint. The
bridges neither introduce a new result symbol nor use `bracketResult` to
replace program execution.

## Claims

- `loop-zero` starts at the actual `#loop` term with depth 0 and the exact
  remainder `Return(...) ~> #endcall`. It proves return of
  `bracketResult(S,0)` and exact frame removal. Its freshness guard makes the
  scope deletion realizable.
- `loop-positive` is the same actual loop term at any mathematical `D > 0`
  and proves `bracketResult(S,D)`.
- `correct-bracketing` loads the exact submitted module term, calls its bound
  function on arbitrary `str(S)`, and constrains the final value to
  `bracketResult(S,0)`. Its post-state records the exact installed closure and
  unchanged module heap/stack/exception/exit state.

No claim uses a free result variable, implication-only postcondition, bounded
length, fixed example, or unexhibited precondition.

## Unreachable fixed-semantics abstractions

The imported supplied semantics contains opaque proof-domain primitives for
float operations/conversions (`intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, plus
`floorFI`, `toF`, `ceilF` on symbolic inputs), sorting (`sortVS`,
`sortKeyVS`), and MD5 (`md5hexCodes`). It also intentionally totalizes some
out-of-bounds indexing and unsupported-value helper cases. None of those
symbols or rules is reachable from `solution.mpy`, `bracketResult`, or any
claim path, so none affects this theorem. All other unused fixed declarations
are ordinary rules over constructors absent from the submitted term.
