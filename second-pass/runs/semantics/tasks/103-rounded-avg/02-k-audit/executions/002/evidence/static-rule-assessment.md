# Rule-by-rule assessment index

The companion `static-rule-inventory.md` contains the complete source block and
line number of every declaration and rule. This file assigns an assessment to
every inventoried block by file/family. No candidate-built definition was used.

Global source totals are 697 rules, 229 syntax declarations, five contexts, one
configuration, four claims, 147 function-bearing declarations, 109
total-bearing declarations, 25 symbol-bearing declarations, 22
`no-evaluators` declarations, 35 concrete-only rules, 41 priority rules, 26
`owise` rules, four macro declarations, and no `functional`,
`simplification`, `simplify`, `anywhere`, or alias declarations.

## Fixed supplied semantics

| File | Rules | Assessment applying to every inventoried rule in the file |
|---|---:|---|
| `semantics.k` | 0 | Assembly only. `MPY` imports the proof semantics; `MPY-KRUN` additionally imports concrete-only rules. |
| `assert.k` | 3 | Restricted but coherent assertion/abort behavior. Unused by the target proof. The concrete audit assertions finished with `exit-code` 0. |
| `bool.k` | 13 | Truth-preserving boolean comparison and short-circuit rules; ref priorities preserve identity of returned operands. Unused except indirectly through K Boolean guards. |
| `builtins.k` | 137 | Algebraic folds and restricted builtin cases. Target-used lines 108–121 implement `bin` by a descending base-2 fold; guards partition negative/nonnegative integers and the recurrence is mathematically exact. `md5hexCodes` is an unused opaque boundary. Other cases do not overlap the one-argument `bin` dispatch. |
| `call.k` | 21 | Target-used lines 20–21 evaluate callee before arguments; line 31 dispatches the resolved `bin`; lines 69–74 create the actual closure frame. Other receiver/ref/annotated-closure routes are sort/shape-disjoint from this target. |
| `comprehension.k` | 7 | Macro expansion into accumulator/loop syntax. No target term contains these constructors. |
| `concrete.k` | 16 | Imported only by LLVM `MPY-KRUN`, not by the Haskell proof definition. Concrete deep-equality/key-sort rules are irrelevant to the target; none matches its integer/string path. |
| `controls.k` | 34 | Target-used lines 9–11 perform local assignment; lines 52–54 select the branch from truthiness. Loop/import/ref rules are constructor- or guard-disjoint from the target. |
| `core.k` | 46 | Configuration, sequence, lexical lookup, literal, argument-order, and helper equations. Target-used lines 126–127, 131–134, 152–154, 158–181, 189–195, 202, and 214–215 preserve the expected cells and left-to-right evaluation. Heap/cell rules cannot match the empty-heap plain closure path. |
| `dict.k` | 28 | Restricted insertion-ordered dict operations. No dict constructor occurs in the target. |
| `float.k` | 121 | Fixed opaque/concrete float boundary. All float sorts and math interception shapes are disjoint from the integer-only target. Duplicate mixed arithmetic equations have identical right-hand sides. |
| `functions.k` | 15 | Target-used lines 63–66 bind the two parameters; lines 78–90 implement abrupt return, restore caller state, delete the callee frame, and restore `scopeLoc`. The saved continuation is restored by `#pop`; no target closure escapes. |
| `int.k` | 16 | Target-used unary minus, addition, `%`, `//`, `>`, and `==` rules are ordinary integer equations. `pyMod` and floor division are correct for divisor 2; the target never divides by zero. |
| `iter.k` | 0 | Iterator syntax only; unused. |
| `list.k` | 27 | Algebraic list operations/iteration and guarded heap mutations. No list constructor or ref is on the target path. |
| `methods.k` | 75 | ASCII string/list method subset. No method call is on the target path. |
| `operators.k` | 10 | Target-used unary/binary dispatch and the two comparison contexts enforce operand evaluation before `apply*`. Ref priorities are inapplicable to integer operands. |
| `range.k` | 6 | Guarded range length/iteration equations. Unused. |
| `set.k` | 12 | Algebraic code-set operations. Unused. |
| `sort.k` | 19 | `sortVS`/`sortKeyVS` are fixed opaque sorting boundaries. No `sorted` or `.sort` term occurs in the target. |
| `str.k` | 28 | String representation and ordinary sequence equations. The target result is constructed directly by `bin`; no string operator is used. |
| `subscript.k` | 40 | Restricted indexing/slicing equations. No subscript occurs in the target. |
| `syntax.k` | 0 | The target uses `Int`, `Name`, `UnaryOp`, `BinOp`, `Call`, `Compare`, `CmpOp`, `Assign`, `If`, `Return`, `Stmts`, `Params`, and `ParamNames`. `strict`/`seqstrict` attributes generate value-before-dispatch evaluation. |
| `tuple.k` | 21 | Tuple iteration/binding/unpacking subset. Unused. |

For the unused fixed-semantics families, this assessment is not a claim that
the supplied language is a full CPython semantics. It is a check that their
left-hand sides, sorts, priorities, and guards cannot overlap or rewrite the
submitted target path. The benchmark supplies this semantics as the fixed
language boundary. No false-conclusion witness was found for any fixed rule on
the target's positive-integer domain, so none is labeled unsound.

## Candidate proof-local theory

`verification.k` has exactly two syntax declarations and two unconditional
equations:

1. `roundedAvgBody : Stmts` expands to the translated function body. It is a
   definitional summary, not an operational oracle. Fresh `kast` parsing gives
   the same constructor-tree SHA-256 for this RHS and the body extracted from
   the trusted regeneration of `solution.mpy`.
2. `roundedAvgCall(N,M)` expands to a `Call` of
   `closureVal(("n","m"), roundedAvgBody, 0)` with the two arguments. Fixed call
   semantics then evaluates the actual body. The initial scope 0 in every
   claim is exactly the definition location and has builtins scope -1 as its
   parent.

Both equations cover their declared nullary/binary domains, have no overlapping
equations, and terminate in one expansion. They do not introduce an opaque
value, priority, simplifier, oracle, abrupt control, framed wildcard, or
proof-local arithmetic lemma.

`spec.k` adds four reachability claims and no rules. Their guards are disjoint
and exhaustive for positive integers: inverted interval; valid/even sum;
valid/odd sum with even lower neighbor; valid/odd sum with odd lower neighbor.
