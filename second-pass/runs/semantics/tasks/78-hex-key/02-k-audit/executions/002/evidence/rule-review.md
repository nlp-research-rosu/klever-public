# Static declaration and rule review

This review indexes the complete mechanical inventory in `rule-inventory.log`.
That inventory covers the supplied assembled semantics, all 23 helper modules,
`verification.k`, and `spec.k`: 26 files, 944 declarations, including 703
rules, 233 syntax declarations, five contexts, one configuration, and two
claims. There are no `[simplification]` rules and no `[functional]`
declarations. It explicitly tags all 111 `[total]` declarations, all 45
priority rules, all 35 concrete rules, and all 22 `no-evaluators` opaque
declarations.

## Exhaustive disposition scheme

Every inventory entry has exactly one of these dispositions:

- **U (used and validated):** the entry occurs on the submitted program's
  symbolic execution path and is listed below. Its matched domain, evaluation
  order, cells, and result were checked against the submitted source and
  ordinary Python behavior.
- **C (candidate-local):** entries K0929--K0944. These are reviewed
  individually below.
- **O (fixed opaque/partial boundary, unused):** every fixed-semantics entry
  tagged `no-evaluators`, plus the declarations that route float, sort, or MD5
  operations to those symbols, and the explicitly partial cases documented by
  the source (out-of-bounds indexing, zero-step ranges, escaping closures,
  list mutation during iteration, and unsupported imports/exceptions). None
  of their syntax or values is constructible on this program's path.
- **I (fixed, inert for this theorem):** every remaining K0001--K0928 entry not
  in U or O. Each was checked for a left-hand-side or priority overlap with the
  U path. None matches the reachable terms below. Their constructor equations
  are guarded/disjoint or agreeing on overlaps. This disposition does not
  claim the supplied minimal semantics is a complete CPython semantics; it
  states the narrower fact needed here: these entries cannot contribute to
  this theorem or derive a false result for this submitted program.

Thus the four sets cover K0001--K0944 without an unreviewed remainder.

The fixed source contains deliberate minimal-subset behavior outside this
theorem. For example, `cntSub(.IntSeq, _:IntSeq) => 0` does not implement
CPython's special empty-substring count, and several out-of-range/error cases
stay abstract or stuck. Those are genuine language-coverage limitations, but
the real `hex_key` body constructs none of those terms. No such rule can match
or rewrite any configuration in the U dependency graph.

## U: real-program dependency graph

| Source construct or effect | Inventory entries | Review conclusion |
|---|---|---|
| AST sorts, module, statement-list syntax, strict evaluation | K0285--K0297, K0888--K0889, K0894, K0897--K0899, K0902--K0903 | The regenerated term is well-sorted. `Assign`, `AugAssign`, `For`, `If`, and `Return` evaluate the same operand first as Python; `Compare` uses the explicit left-then-right contexts. |
| Module load and sequencing | K0323--K0326 | `#loadAll` exposes the sole `FuncDef`; statement sequencing neither inserts nor skips a body operation. |
| Local name lookup | K0327--K0329 | Every reachable lookup (`hex_key`, `num`, `count`, `digit`) is present in the selected frame, so the direct lookup rule applies and the parent-walk/cell priority cases are inapplicable. |
| Argument evaluation | K0334--K0338 | The single argument is evaluated once and left-to-right before call dispatch. |
| Integer literal and Boolean truth | K0339, K0342--K0343 | Literals preserve their mathematical integer value; the membership Boolean controls the same branch. |
| Function definition, parameter binding, return, frame pop | K0564--K0565, K0577--K0578, K0580, K0582 | The closure captures module scope 0, binds `num` in a fresh frame, executes the actual body, returns `count`, removes the callee frame, and restores all caller/control cells. |
| Call routing and closure dispatch | K0194--K0196, K0212 | Lookup selects the submitted closure; no builtin/method/priority interception overlaps. The saved continuation is restored exactly. |
| Assignment, increment, branch, and loop control | K0248, K0250, K0259--K0262, K0265--K0269, K0274 | `count`/`digit` writes stay in the current frame; `count += 1` uses integer addition; each character binds before the body; the recursive loop continuation is preserved. |
| Integer addition | K0584 | `applyBin("+", Int, Int)` is exactly `+Int`. |
| Compare evaluation and dispatch | K0737--K0739 | The character and literal evaluate in Python order, then membership dispatches by their concrete string sorts. No ref-dereference priority rule applies. |
| String iteration and literal conversion | K0798--K0803 | Empty iteration terminates; nonempty iteration yields exactly the head one-character string and tail. Both literals are ASCII and `strToCodes` produces their exact codes. |
| String membership | K0810, K0812--K0819 | `strPrefix` and `strContains` are exhaustive, disjoint, structurally descending equations. For a one-code pattern they return true exactly for codes 50, 51, 53, 55, 66, or 68. |
| Loop target binding | K0917--K0918 | Each yielded character overwrites local `digit`; the cell-specific priority rule cannot match the exact plain frame. |
| Iterator protocol declaration | K0600 | Only the string cases K0798--K0799 can match the reachable iterable. |

All heap, heap-location, exception, return-state, exit-code, and unrelated scope
cells are framed through the loop lemma. The program allocates no heap object
and has no exceptional or abrupt loop control.

## Priority, overlap, and opaque review

All 45 priority rules are enumerated in `rule-inventory.log`. They cover
heap references, closure cells, special calls, concrete sort/deep-equality
legs, and mutating methods. Reachable values here are integers, plain strings,
and one ordinary closure; the exact scope has no `$cells` marker and the heap
is empty. Therefore no priority rule preempts a U rule. The generic
`Call`/`Compare` `[owise]` rules are selected only after all disjoint
interceptions fail.

The 22 `no-evaluators` symbols (float operations, `sortVS`, `sortKeyVS`, and
`md5hexCodes`) are all O. None appears in the submitted AST, candidate helper
equations, either claim, or any reachable cell. They cannot influence control
or the result. Compiler warnings about non-exhaustive total functions likewise
name unused constructors (`mapStrVS`, `joinCodes`, `floorFI`, `toF`, `ceilF`,
and `valSeqAt`); none is in the dependency graph.

## C: candidate-local declarations and claims

- **K0929--K0932 (`hexKeyLoopBody`, `hexKeyBody`):** syntax macros only. They
  introduce no operational rewrite and skip no execution. Macro-expanded
  `kast` JSON for `Module(FuncDef("hex_key", Params("num"), hexKeyBody))` is
  byte-identical to the trusted-regenerated `solution.mpy` AST
  (`program-term-pinning.log`).
- **K0933--K0934 (`isPrimeHexCode`):** one unguarded equation covers every
  integer and tests a one-code sequence against exactly
  `[50, 51, 53, 55, 66, 68]`. It is total and truthful.
- **K0935--K0936 (`primeHexBit`):** one unguarded equation maps that Boolean to
  exactly 1 or 0. It is total and truthful.
- **K0937--K0939 (`hexCount`):** two disjoint constructor equations cover all
  `IntSeq` values and descend on the tail. The result is exactly the sum of
  `primeHexBit` for every code.
- **K0940--K0942 (`finalDigit`):** two disjoint constructor equations cover
  all `IntSeq` values and descend on the tail. They preserve the old value for
  empty input and otherwise return the final one-code string, exactly matching
  the loop-variable side effect.
- **K0943 (loop lemma):** its initial map forces `ACC` to be an integer and
  contains exactly plain `count`, `digit`, and `num` bindings. One fixed
  semantics step is required before circularity. Empty input leaves the
  bindings unchanged; the step case adds one precisely when K0934 is true,
  updates `digit`, executes no abrupt control, and returns to the same loop
  head over the strict tail. Arbitrary `CONT` is sound because the body cannot
  inspect or discard it.
- **K0944 (entry point):** begins at the complete translated module load,
  performs lookup/call/body execution, and constrains the returned K value to
  `hexCount(CS)`. Every non-result cell is fixed to its actual initial/final
  value. There is no right-only free result variable, implication-only
  postcondition, simplification axiom, operational bridge, or candidate
  opaque symbol.

The body-sensitivity experiment changed the macro-expanded operation itself
from `Int(1)` to `Int(2)`. The mutated definition compiled, and the proof
failed with the explicit false obligation
`ACC +Int 2 +Int hexCountMutated(R) == ACC +Int (hexCountMutated(R) +Int 1)`
(`kompile-body-mutation.log`, `kprove-body-mutation.log`). This confirms the
claim depends on the executed body, not merely on an external source file.
