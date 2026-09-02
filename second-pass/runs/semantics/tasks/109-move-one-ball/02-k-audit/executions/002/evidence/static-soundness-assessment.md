# Static soundness assessment

This assessment accompanies the mechanical 6,407-line inventory in
`rule-inventory.md`. The supplied-semantics tree is byte/type identical to the
trusted mount. The Haskell proof imports `MPY`; it does not import
`MPY-CONCRETE`.

## Construct-to-rule map for `solution.mpy`

| Submitted construct/runtime form | Declaration and material rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, `Params`, closure | `syntax.k:53-60`; `functions.k:14-20`; proof starts from the prebound closure |
| `Call(Name("move_one_ball"), ...)` | `call.k:18-21,69-74`; `core.k:130-154,183-191`; `functions.k:63-66,78-90` |
| `Call(Name("len"), Name("arr"))` | fixed route `call.k:18-32`, `builtins.k:17-26`, `core.k:223-225`; candidate preemption `verification.k:49-56` |
| `Int`, `Bool`, `Name` | `syntax.k:9-13`; `core.k:130-154,193-196` |
| `Compare(..., "=="/"<", ...)` | `syntax.k:30-32`; `operators.k:14-17`; `int.k:22-27` |
| `If` | `syntax.k:49`; `controls.k:50-54`; strictness evaluates its guard first |
| `Assign(Name, ...)` | `syntax.k:41`; `controls.k:8-18` |
| `Subscript(Name("arr"), Int(0))` | `syntax.k:22,38`; `subscript.k:25-41`; candidate preemption `verification.k:60-62` |
| `For(Name("current"), Name("arr"), ...)` | `syntax.k:45`; `controls.k:62-74`; iterator declaration `iter.k:8`; fixed list cases `list.k:9-10`; candidate cases `verification.k:43-47` |
| loop target binding | `tuple.k:30-41` |
| `AugAssign(..., "+", Int(1))` | `syntax.k:44`; `controls.k:20-31`; integer addition `int.k:9` |
| `Return` and call-frame restoration | `syntax.k:50`; `functions.k:77-90` |

The execution order is: callee lookup, argument evaluation, call-frame
allocation/binding, body statements in sequence, strict guard/operand
evaluation, one iterator step at a time, and abrupt `Return`/frame pop. The
material rules preserve `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`,
`ret`, `exc`, and `exit-code` as required. The target performs no allocation,
output, mutation of its input, or exception on the formal integer-list domain.

## Supplied modules, rule-by-rule disposition

Every declaration, context, configuration, and rule is reproduced with its
guards and attributes in `rule-inventory.md`. The following table records the
disposition of every file-level group; rules marked inactive have no top symbol
or value sort reachable from this submitted program or its claims.

| File/module | Disposition |
|---|---|
| `semantics.k` / `MPY`, `MPY-KRUN` | Assembly only. Proof imports `MPY`; concrete-only rules are excluded. |
| `syntax.k` | Pure syntax and evaluation attributes. All used constructors are mapped above; strict/seqstrict order matches Python for the target. |
| `core.k` | Used configuration, sequencing, name lookup, argument evaluation, literals, and integer/list helpers are operationally faithful. Allocation/cell/keyword paths are inactive. |
| `iter.k` | Declarations only. |
| `list.k` | Fixed `.ValSeq`/`vCons` iteration rules are exact. Literal allocation, list ops, equality, mutation, and membership paths are inactive in the proof. |
| `tuple.k` | The `#bindTgt(Name, Val)` rule is used and exactly updates the current local frame. Tuple construction/unpacking/index paths are inactive. |
| `subscript.k` | Contexts enforce object-before-index evaluation. The fixed `applyIndex`/`valSeqAt` path is correct for ordinary in-bounds index zero; the candidate bridge preempts it only for `intVals`. Slice rules are inactive. |
| `operators.k` | Used integer comparison dispatch and evaluation contexts are exact; ref and identity/membership paths are inactive. |
| `int.k` | Used `+`, `<`, and `==` equations are ordinary unbounded-integer mathematics, with disjoint operand/operator guards. Other integer operators are inactive. |
| `controls.k` | Used assignment, augmented assignment, branch, `For`, loop-step, and loop-label rules match the target’s control/state effects. Import, while, and break/continue paths are inactive. |
| `functions.k` | Used plain parameter binding, return, and frame pop match the exact call configuration. Annotated closures/cells/lambdas are inactive. |
| `call.k` | Used plain closure and builtin routes preserve evaluation/binding/control. Method, type, ref, and annotated-closure routes are inactive. |
| `builtins.k` | The fixed `len` definition is exact on ordinary `vCons` lists. All other builtin folds/functions and the opaque `md5hexCodes` primitive are inactive. |
| `range.k` | Inactive. |
| `bool.k` | Inactive except that K `Bool` values are results; no `BoolOp` or boolean comparison appears. |
| `float.k` | All 22 inventory-marked opaque symbols and all float operational rules are inactive. |
| `str.k` | Inactive. |
| `set.k` | Inactive. |
| `dict.k` | Inactive. |
| `comprehension.k` | Inactive macros. |
| `methods.k` | Inactive. |
| `sort.k` | Both opaque sorting primitives and all sorting rules are inactive. |
| `assert.k` | Inactive in the proof; used only by the separately rebuilt concrete smoke harness. |
| `concrete.k` | Not imported into the Haskell proof. |

No supplied opaque primitive affects a target branch, state cell, returned
value, helper equation, or postcondition.

## Candidate extension inventory and decisions

| Extension | Class, domain, footprint, influence, and decision |
|---|---|
| `MOVE-ONE-BALL-LOOP-BODY` | Nullary definitional function naming the exact translated loop-body `Stmts`. No state rewrite. Constructor-level comparison and body sensitivity validate it. Sound. |
| `MOVE-ONE-BALL-BODY` | Nullary definitional function naming the exact translated function body. No state rewrite. Sound and body-sensitive. |
| `MOVE-ONE-BALL-CLOSURE` | Nullary definitional function yielding `closureVal("arr", body, 0)`. Binding/body/definition scope match the submitted module. Sound. |
| `intVals(IntSeq)` | Fresh `ValSeq` representation claimed to encode every finite integer list. It has no bridge-free conversion/equivalence theorem to `.ValSeq`/`vCons`. This is the central representation gap. |
| empty/nonempty `#iterNext(list(intVals(...)))` | Operational bridges, arbitrary continuation and all omitted cells framed. Under the intended constructor mapping, they yield exactly the first integer and typed tail, preserving every cell. Their equations are locally faithful, but no bridge-free universal connection theorem establishes the mapping. |
| empty `len(intVals)` | Operational bridge returning `0`; locally agrees with the corresponding empty standard list. No connection theorem. |
| nonempty `len(intVals)` | Operational bridge returning `1` for *every* nonempty length and accepting an arbitrary continuation. Globally false as exact Python/K semantics. For the intended two-element list `[7,8]`, fixed semantics returns `2` while this rule returns `1`; both conclusions close in `bridge-witness.k`. A continuation observing `== 2`, storing the length, or returning it distinguishes the executions. **Unsound.** |
| `Subscript(list(intVals(iCons(I,...))), 0)` | Operational bridge. Index is exactly zero and result/head are exact under the intended mapping; cells and continuation are preserved. No bridge-free connection theorem. |
| `addDrop` | Total definitional integer equation; ordinary mathematics; sound. |
| four `scanDrops` equations | Structurally descending and pairwise constructor-disjoint. Truthful for integer `vCons` and `intVals` sequences. The `[total]` declaration is over-broad because a `vCons` with a non-`Int` head has no equation; this is a totality coverage gap, not a demonstrated wrong value on the formal integer domain. |
| four `scanLast` equations | Same disposition as `scanDrops`: truthful and descending on integer sequences, over-broad `[total]` declaration on all `ValSeq`. |
| `circularDrops` | Definitional equation for internal descents plus last-to-first descent. Sound where the scans are defined. |
| four `moveOneBallSpec` equations | Pairwise constructor-disjoint and truthful for empty/nonempty integer sequences. The `[total]` declaration again lacks non-integer `vCons` coverage. The formal target uses only `intVals(IntSeq)`. |
| loop-induction claim | Exact local-store transformer for a nonempty remaining typed sequence, arbitrary continuation, and framed omitted cells. It follows only in the bridge-extended theory. |
| loop-entry claim | Exact first-target-binding case feeding the induction claim. It follows only in the bridge-extended theory. |
| functional claim | Executes the pinned closure and constrains the returned `Bool` to `moveOneBallSpec`; it is neither a tautology nor a free-result claim. It follows only in the bridge-extended theory. |

There are no candidate simplification rules, `functional` declarations, or
opaque `symbol`/`no-evaluators` declarations. Candidate priority rules are the
five operational bridges at priority 40. The helper equations have disjoint
constructor/operator domains; no conflicting right-hand sides were found.

## False-conclusion witness and Gate A result

`bridge-witness.k` proves under the rebuilt definition:

- fixed supplied representation `list(vCons(7,vCons(8,.ValSeq)))` has length 2;
- candidate representation `list(intVals(iCons(7,iCons(8,.IntSeq))))` has
  length 1.

The candidate itself describes the latter as a typed encoding of the same
finite Python integer list. If that mapping is accepted, the priority bridge
is a false semantic equation. If it is not accepted, the functional claim
quantifies over an alien `ValSeq` constructor rather than real Python lists.
Either interpretation fails real-program Gate A. The fact that the submitted
body currently observes only `len(arr) == 0` does not narrow the rule’s match
context and cannot make a globally false exact rewrite sound.
