# Exhaustive rule-review ledger

`k_rule_inventory.txt` is the line-addressable source inventory. It contains
955 declaration records: 234 syntax declarations, 713 rules, 5 contexts, one
configuration, and two claims. The table below assigns a review disposition to
every numbered entry in that inventory. "Outside executed slice" is not a
soundness exemption: it records that the rule was checked against the supplied
MPY subset, but has no dependency from this theorem and therefore supplies no
false-conclusion witness on this program's intended input domain.

| Inventory entries | Source | Disposition and rationale |
|---|---|---|
| 0001–0003 | `assert.k` | Consistent assertion success/failure and heap dereference; concrete-test only, outside proof slice. |
| 0004–0017 | `bool.k` | Boolean comparison, truth-preserving short circuit, and reference dereference are pairwise guard-disjoint; only ordinary Boolean truth is relevant here. |
| 0018–0192 | `builtins.k` | Registry functions and structural folds decrease on sequences and have disjoint base/step guards. `isIntV` (entries at the file tail) is used and is exact for the `Int` subsort. The evaluator and MD5 primitives are explicit supplied-model abstractions, unused here. |
| 0193–0216 | `call.k` | Callee then left-to-right argument evaluation; the closure rule creates exactly one local scope/frame and preserves heap/exception state. Builtin/method branches are disjoint by callee constructor and unused. |
| 0217–0226 | `comprehension.k` | Syntax expansion follows the supplied eager-comprehension subset; outside executed slice. |
| 0227–0247 | `concrete.k` | Concrete-only deep equality/keyed-sort rules are absent from proof definitions. They are outside the symbolic proof trust path. |
| 0248–0284 | `controls.k` | Assignment, `If`, and list `For` rules used here preserve evaluation order and local writes. Loop-control, import, `While`, and reference paths are guard-separated and unused. |
| 0285–0368 | `core.k` | Value/configuration declarations, module load, sequencing, lookup, literals, argument evaluation, and list helpers are consistent with the supplied MPY subset. Allocation/cell paths are fresh/guarded and unused. |
| 0369–0408 | `dict.k` | Ordered dictionary helpers structurally recurse and guards partition equality/update cases. The supplied model deliberately omits some Python errors; all entries are outside this program. |
| 0409–0563 | `float.k` | Explicit no-evaluator float primitives plus concrete twins form a declared trust boundary; duplicate mixed-arithmetic equations agree on overlaps. No float syntax/value is reachable here. |
| 0564–0582 | `functions.k` | Plain `FuncDef`, bind, `Return`, `#endcall`, and `#pop` exactly implement the used call lifecycle. Annotated-closure rules are outside the slice. |
| 0583–0599 | `int.k` | Integer negation and `<`, `==`, `>` equations are ordinary integer mathematics. Other arithmetic is unused; guarded exponent case and floor operators do not overlap the used cases. |
| 0600 | `iter.k` | Protocol declaration only. |
| 0601–0632 | `list.k` | Empty/cons iterator rules form the exact used list traversal. Literal allocation, list operations, equality and membership are outside the executed slice. |
| 0633–0734 | `methods.k` | Structural ASCII/string/list-method equations have decreasing recursions and partitioned guards under the supplied subset; no method call is reachable here. |
| 0735–0746 | `operators.k` | Strict/context evaluation sends unary and comparisons to the correct dispatch; heap-reference priorities are inapplicable because the proof heap is empty. |
| 0747–0754 | `range.k` | Range length/iterator guard partitions are valid for nonzero step; zero-step error behavior is outside the supplied valid-program subset and this program. |
| 0755–0772 | `set.k` | Structural membership/dedup/subset functions decrease and are outside this program. |
| 0773–0797 | `sort.k` | `sortVS`, `sortKeyVS` are explicit supplied trusted primitives with concrete insertion-sort legs; unused here, so the theorem has no opaque-sort dependency. |
| 0798–0830 | `str.k` | ASCII string iteration, concatenation, membership and lexicographic recursion are structurally sound for the supplied model; unused here. |
| 0831–0887 | `subscript.k` | In-bounds access/slice equations follow the supplied valid-program model. Out-of-bounds/error and zero-step cases are intentionally not modeled and are unreachable here. |
| 0888–0903 | `syntax.k` | Grammar declarations. Strictness attributes enforce the evaluation orders mapped in `used_construct_map.md`; unused syntax does not execute. |
| 0904–0928 | `tuple.k` | Entry 0918's `#bindTgt(Name,Val)` path is used by `For` and writes the current local. Tuple construction/unpacking/index paths are outside the slice. |
| 0929–0936 | `verification.k` macros | Pure exact AST abbreviations. Expansion is byte-correspondent to regenerated `solution.mpy`; no executing body is replaced. |
| 0937–0942 | `asInt`, `nonNegativeInts` | Total, constructor-covering definitions. `asInt` is identity on `Int`; all operationally meaningful uses are guarded or reached from `nonNegativeInts`. |
| 0943–0945 | comparison simplifications | Under both `isIntV` guards they equal the supplied MPY-INT equations. Overlap with those equations has the same Boolean RHS; no state/control effect. |
| 0946–0952 | `sortedScan` | Total structural definition. Empty/less/greater/equal guards are disjoint; equal duplicate counts `<0`, `=0`, and `>=1` partition `Int`; recursive cases consume a strict tail. On the claim domain it is exactly the intended scan summary. |
| 0953 | initialized bridge | Exact substitution instance of `LOOP-SPEC.loop-invariant`; full context/state comparison is in `used_construct_map.md` and `REVIEW.md`. Base proof excludes this rule. The body-sensitivity mutation makes the entry proof fail. |
| 0954 | loop claim | Satisfiable generalized loop-head claim. It executes the exact loop body, trailing return and frame pop under `VERIFICATION-BASE`. |
| 0955 | entry claim | Satisfiable exact-module/call claim. Its RHS is a Boolean function of the input, not a free variable or implication. |

No rule was labeled unsound: the review found no rule capable of enabling a
false conclusion for the real program on a non-negative integer-list input.
The narrower gaps in unused supplied semantics (exceptions, Unicode, full
Python float behavior, and opaque library primitives) have no dependent in
either positive claim.
