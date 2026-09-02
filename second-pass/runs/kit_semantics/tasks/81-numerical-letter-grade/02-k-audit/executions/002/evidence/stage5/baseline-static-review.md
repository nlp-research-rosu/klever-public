# Supplied baseline static review

The authoritative inventory contains 928 items from the byte-identical trusted
supplied semantics: 314 are conservatively marked potentially relevant and 614
are marked unused by the submitted constructor vocabulary. Every baseline row
has an explicit `ACCEPT_FIXED_BASELINE_USED` or
`ACCEPT_FIXED_BASELINE_UNUSED` disposition in `rule-inventory.tsv`.

The baseline is the launcher-selected MPY model, not a candidate proof
extension. It contains no task name, submitted function/binding name, grading
string table, `gradeValue`, `gradeAcc`, or proof macro (see
`task-answer-scan.log`). `MPY-CONCRETE` is imported by `MPY-KRUN` only and is
absent from the proof module `MPY`.

The potentially relevant rules were checked by subsystem:

- `syntax.k` declares exactly the constructor categories appearing in
  `solution.mpy`, with strictness on assignment RHS, loop iterable, branch
  guard, return expression, expression statements, and attributes.
- `core.k` declares the complete configuration, value injections, fresh heap
  allocation, module sequencing, lexical lookup, left-to-right argument
  evaluation, and the `applyCmp` dispatch symbol. Its freshness and lookup
  guards are satisfiable in the entry state and preserve unrelated map entries.
- `operators.k` evaluates comparison operands left-to-right and dispatches
  only once both are values. Its reference-dereference priorities do not match
  numeric inputs.
- `controls.k` implements assignment, branch selection, and one
  `#iterNext`/`#loopStep` cycle. `list.k` provides the disjoint empty/cons
  iterator cases, fresh list construction, structural concatenation, and the
  exact in-place `append` heap update.
- `functions.k` and `call.k` perform closure binding, callee-then-arguments
  evaluation, parameter binding, frame creation, return, and restoration. The
  target has exact arity, returns no closure, and exercises no unsupported
  exceptional call behavior.
- `float.k` supplies the exact Int/Float comparison dispatch equations used by
  the target. `intToF`, `eqF`, and `gtF` are declared total opaque symbols for
  symbolic proof and have concrete LLVM equations. This is the material
  low-level trust boundary, not an answer-specific rule.
- `str.k` converts all grade literals (ASCII) to exact code sequences.
  `methods.k` supplies method dispatch generally; the target's mutating
  `append` case is deliberately implemented operationally in `list.k`.
- The remaining supplied modules define constructors or redex patterns absent
  from the submitted program. Their symbols and guards do not overlap the
  target redexes. They remain part of the trusted limited-MPY baseline rather
  than being silently promoted to claims about full CPython.

The 45 priority-bearing baseline rules were checked for target overlap. On the
target path, the relevant ones are list `append` and ordinary reference/method
routing; their more-specific patterns preempt generic dispatch without
changing argument order or unrelated cells. The 22 baseline
`no-evaluators` functions are enumerated in the inventory. Only `intToF`,
`eqF`, and `gtF` influence this theorem; all three are accounted for in the
trust ledger. The baseline has no `[simplification]` rule. No baseline rule
encodes the task answer, bypasses the function or loop, or fabricates the
returned list.

No rule is labeled materially unsound on the intended numeric-GPA domain.
Accordingly, no unsound-rule false-conclusion witness is claimed.
