# Used-construct and extension assessment

This map supplements `RULE_INVENTORY.md`, whose 950 source-addressed rows cover
all 26 K files in the proof build: 231 `syntax` declarations, one
configuration, five contexts, 703 rules, and ten target claims. There are no
`functional` declarations and no simplification rules. The 22
`[no-evaluators]` declarations are supplied float/hash/sort abstractions; none
occurs in `solution.mpy`, `verification.k`'s entry wrapper, or a postcondition.

## Constructor-to-semantics map

| Submitted constructor/control | Declaration | Operational path used by the claims | Assessment |
|---|---|---|---|
| `Module`, `Stmts` | `semantics/syntax.k:56,61` | `core.k:124-127` loads and sequences both exact function bodies | Fixed semantics executes, rather than summarizes, the module. |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` binds closures in module scope | Exact names, parameters, bodies, and defining environment are retained. |
| `Name` | `syntax.k:12` | `core.k:130-154` walks local, module, then builtin scopes | The called `_evaluate`, recursive binding, operands, locals, and `len` use normal lookup. |
| `Call` | `syntax.k:28` | `call.k:19-21,69-75`, `core.k:183-191`, `functions.k:62-90` | Callee first, then arguments left-to-right; a real frame is allocated, parameters bind, return unwinds, and caller state is restored. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` | Return expression evaluates before abrupt return; the current function suffix is discarded and the saved caller continuation resumes. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:51-54` | The condition evaluates before the selected branch; no answer-bearing bridge is present. |
| `While` | `syntax.k:46` | `controls.k:76-85` | Each condition is reevaluated and the body returns to an explicit loop label. The submitted scans therefore execute. |
| `Assign` | `syntax.k:41 [strict(2)]` | `controls.k:9-18` | RHS first, then current-frame update. The cell priority branch is inapplicable to these plain frames. |
| `AugAssign` | `syntax.k:44 [strict(3)]` | `controls.k:20-31`, `int.k:9,13` | `i += 1` and `i -= 1` use the current integer binding and write the computed integer back. |
| `Int` | `syntax.k:9` | `core.k:193-196` | K mathematical integers represent the contract's non-negative Python integers and intermediate negative results. |
| `Str` | `syntax.k:13` | `str.k:13-17,25-26` | The five ASCII operator literals become exact code sequences and equality compares those sequences. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:14-20`, `int.k:22-27`, `str.k:25-26` | Contexts evaluate left then right; integer order/equality and string equality are the relevant cases. |
| `BinOp` | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12`, `int.k:9-20` | Operands evaluate left-to-right; `+`, `-`, `*`, Python floor `//`, and non-negative `**` reduce to the corresponding integer operations. |
| `Subscript` | `syntax.k:22,38` | `subscript.k:11-41` plus `core.k:223-225` | Object then index evaluate; bare list values use normalized in-bounds positional access. Every submitted-claim access is in bounds. |
| `len` | builtin scope at `core.k:156-181` | `call.k:31-32`, `builtins.k:17-26`, `core.k:223-225` | Normal lookup selects the fixed builtin and computes the full operator-list length. |
| Bare `list(OPS)` / `list(NDS)` values in the wrapper | `core.k:17-34` | Passed directly through call argument evaluation | These are read-only claim inputs; no construction or allocation shortcut replaces program behavior. |

The configuration cells used by the path are `k`, `env`, `scopes`, `scopeLoc`,
`heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`
(`core.k:49-60`). Calls modify and restore scope/stack/return state. The
submitted program does not construct or mutate heap objects, so the claims'
unchanged empty heap and zero `heapLoc` are consistent. Final scopes are
deliberately existential because loading the exact module installs its two
closures.

## Candidate-local extension inventory

| Extension | Class and complete role | Guard/domain and state footprint | Review decision |
|---|---|---|---|
| `solutionProgram` and its rule (`verification.k:7-82`) | Definitional macro containing the program term | No guard; constructor term only; no cells | Accepted. Independent macro expansion is byte-identical at KORE level to trusted-regenerated `solution.mpy`. |
| `plusV`, `minusV`, `timesV`, `floorDivV`, `powerV` and five rules (`verification.k:85-94`) | Definitional token macros | No guard; values only | Accepted. Code points are exactly ASCII `+`, `-`, `*`, `//`, `**`; guards do not overlap because the symbols are distinct. |
| `floorQuot` declaration/rule (`verification.k:97-98`) | Definitional mathematical summary used only in postconditions | Equation has no guard; no cells | On every actual use, `B > 0`; there it is exactly the supplied `//` equation `(A - pyMod(A,B))/B`. The `[total]` declaration is over-broad at `B=0`, where Python quotient/modulo are undefined. No target claim reaches that case and no concrete false equality witness follows from the stuck division-by-zero term, so this is recorded as a narrow totality/evidence gap, not labeled an unsound rule. |
| `runDoAlgebra` and its rule (`verification.k:100-104`) | Execution-entry wrapper, not a result summary | Any `OPS,NDS`; rewrites only the active `k` item and preserves its continuation/cells | Accepted. It expands to `#loadAll(solutionProgram) ~> Call(Name("do_algebra"), list(OPS), list(NDS))`; it neither supplies a result nor skips lookup, argument evaluation, calls, loops, or returns. |

There are no candidate-local opaque result symbols, axioms, trusted claims,
priority rules, simplification rules, or proof lemmas. The supplied proof
definition imports `MPY`, not concrete-only `MPY-CONCRETE`. The fixed
semantics' 22 opaque float/hash/sort symbols are therefore both unrelated to
this integer/list program and absent from all ten proof paths.

## Rule-by-rule disposition

- Every fixed-semantics row in `RULE_INVENTORY.md` is byte-identical to the
  launcher-supplied selected semantics. Rules on the mapped execution path
  above were checked for binding, evaluation order, calls/returns, loop
  control, arithmetic, indexing, and all affected cells; they implement the
  submitted program's operations directly.
- Fixed rules outside that map are unreachable because the exact program has
  no floats, dicts, sets, tuples, comprehensions, slicing, iteration, methods,
  imports, assertion, sorting, hashing, or corresponding builtins. Their
  declarations—including every opaque symbol and priority rule—cannot affect
  a branch, result, state cell, exception, or postcondition in these claims.
- The eight candidate-local rules are individually disposed of in the table
  above. None encodes the task answer, replaces `_evaluate` by an oracle, or
  fabricates a result.

Static Gate A therefore passes for the submitted claims. This does not cure
Gate B: the claims enumerate only fixed operator-list shapes and do not state a
theorem for arbitrary contract-valid lists.
