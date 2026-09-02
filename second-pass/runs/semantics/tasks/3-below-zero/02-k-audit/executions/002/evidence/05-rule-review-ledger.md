# Static rule-review ledger

This ledger covers every declaration recorded in
`05-rule-inventory.tsv`.  The inventory is lexical and contains the complete
normalized text, source file, line, module, and attributes for 1,120
declarations: 695 supplied-semantics rules, 8 proof-local rules, 2 claims, 233
syntax declarations, 5 contexts, 1 configuration, 91 imports, 25 file
requirements, and module delimiters.  There are no local `simplification` or
`functional` declarations.  There are 146 function declarations, 108 marked
`total`, 36 concrete-only declarations/rules, 46 priority rules, and 26
`owise` rules.

## Per-module disposition

| Source/module | Rules | Relevance and disposition |
|---|---:|---|
| `semantics.k` / `MPY`, `MPY-KRUN` | 0 | Assembly only. The proof imports `MPY`; `MPY-CONCRETE` is reachable only from `MPY-KRUN`, not either proof definition. |
| `syntax.k` / `MPY-SYNTAX` | 0 | Constructor grammar. `Module`, `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`, `For`, `If`, `Return`, `Call`, `Name`, `Int`, `Bool`, `Compare`, and `CmpOp` are used. Strictness is left-to-right and matches the source evaluation order. |
| `core.k` / `MPY-CORE` | 46 | Used path: configuration; `#loadAll`; statement sequencing; current-scope lookup; builtins scope; left-to-right argument evaluation; Int/Bool literals; Bool truthiness; and list helper equations. These preserve all cells they do not update, have disjoint guards/constructors, and match the submitted program. Remaining allocation, cell, keyword, and sequence-helper rules are not reached. No false conclusion witness was found. |
| `iter.k` / `MPY-ITER` | 0 | Declares the iterator protocol only. |
| `range.k` / `MPY-RANGE` | 6 | Unused. Structural range predicates/length/iteration; guards split positive and negative steps. No overlap that yields different right sides was found. |
| `operators.k` / `MPY-OPERATORS` | 10 | Used path: the two Compare evaluation contexts and generic `applyCmp` dispatch. Ref-dereference priorities are unreachable for the unboxed integer list representation. Evaluation is left-to-right and the used dispatch preserves state. |
| `int.k` / `MPY-INT` | 16 | Used path is exactly unbounded integer `+` and `<`; these coincide with Python integer behavior. Other arithmetic/comparison equations are irrelevant to the theorem. |
| `bool.k` / `MPY-BOOL` | 13 | Imported but its Boolean operators are unused. Structural short-circuit rules and heap-ref priorities are disjoint by truthiness and sequence shape. |
| `float.k` / `MPY-FLOAT` | 121 | Entirely unused by the theorem. Twenty-two symbolic float primitives are intentionally opaque in Haskell proofs and have concrete LLVM equations. They are trust boundaries for float-using programs, not for this integer-only program. |
| `str.k` / `MPY-STR` | 28 | Unused. Structural code-sequence functions. The unused-variable warnings in `strLt` do not alter its lexicographic cases. |
| `set.k` / `MPY-SET` | 12 | Unused. Structural membership/deduplication/subset equations with constructor descent. |
| `list.k` / `MPY-LIST` | 27 | The fixed `.ValSeq`/`vCons` iteration cases do not match `asValSeq`; they serve as the constructor-level model copied by the proof-local iterator equations. Other literal/allocation, concatenation, equality, mutation, and membership rules are unused. |
| `tuple.k` / `MPY-TUPLE` | 21 | Unused. Structural tuple iteration/equality/binding. |
| `subscript.k` / `MPY-SUBSCRIPT` | 40 | Unused. Contains intentionally underspecified total out-of-bounds/opaque access; it cannot influence this claim. |
| `comprehension.k` / `MPY-COMPREHENSION` | 7 | Unused macro expansion and list-building execution. |
| `methods.k` / `MPY-METHODS` | 75 | Unused string/list method equations. Constructor recursion and `owise` fallbacks were checked for guard agreement. |
| `controls.k` / `MPY-CONTROLS` | 34 | Used path: plain local Assign, plain integer AugAssign, the non-math ImportFrom no-op, If/branch, and For/loop/loop-step. The update and control cells coincide with the submitted function. Ref/cell, while, break, and continue rules do not match. The broad import no-op abstracts a typing-only import here and has no result/control effect. |
| `functions.k` / `MPY-FUNCTIONS` | 15 | Used path: plain `FuncDef`, exact parameter bind, `Return`, and `#pop`. Return discards the current function continuation as Python return does; `#pop` restores env, frame, scope location, and return state exactly. Closure-cell variants are unused. |
| `builtins.k` / `MPY-BUILTINS` | 137 | No builtin is called. The module contains one opaque MD5 primitive and many structural builtin equations. None can be introduced by a rule on the used path. |
| `call.k` / `MPY-CALL` | 21 | Used path: callee lookup, left-to-right argument collection, and plain closure invocation. The exact empty-stack continuation becomes `frame(.K,0,1)`, which is exactly the auxiliary/summary context. Builtin, method, ref, and closure-cell cases do not match. |
| `sort.k` / `MPY-SORT` | 19 | Unused. `sortVS` and `sortKeyVS` are explicitly opaque proof primitives with concrete sorting equations in the runtime-only module. |
| `assert.k` / `MPY-ASSERT` | 3 | Unused by the positive proof; used only in the fresh LLVM smoke program. The true/false guards are disjoint. |
| `dict.k` / `MPY-DICT` | 28 | Unused structural dictionary equations. |
| `concrete.k` / `MPY-CONCRETE` | 16 | Excluded from both proof main modules; included only in the LLVM runtime definition. It cannot contribute to either `#Top`. |
| `verification.k` / `BELOW-ZERO-COMMON` | 7 | Reviewed individually below. |
| `verification.k` / `MPY-VERIFICATION-LEMMA` | 1 | Reviewed individually below. |

The unused supplied-semantics rules remain part of the selected fixed language
model, but no unused rule can synthesize a symbol on this theorem's execution
path.  The observed non-exhaustive-total warnings concern `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none is reachable from
this program.  They are coverage gaps rather than witnessed false equations.

## Proof-local declarations and rules

1. `belowZeroLoopBody` syntax plus macro rule (`verification.k:7-12`) is a
   definitional macro. Its expansion is exactly the loop-body constructor term
   in trusted-regenerated `solution.mpy`.
2. `belowZeroFunctionBody` syntax plus macro rule (`verification.k:14-19`) is
   a definitional macro. It includes both assignments, the real `For`, and the
   final false return.
3. `solutionProgram` syntax plus macro rule (`verification.k:21-25`) is a
   definitional macro. Macro-expanded KORE is byte-identical to the submitted
   module term.
4. `.IntVals | intCons(Int,IntVals)` (`verification.k:30`) is a free
   inductive representation of every finite integer list; it neither bounds
   length nor integer magnitude.
5. `asValSeq(IntVals)` (`verification.k:31`) embeds that proof datatype into a
   read-only semantic list value.
6. The empty iterator rule (`verification.k:32`) yields `#iterDone`, exactly
   corresponding to fixed `list(.ValSeq)` iteration.
7. The cons iterator rule (`verification.k:33-34`) yields the integer head and
   the structurally smaller tail, exactly corresponding to fixed
   `list(vCons(...))` iteration. The two rules are exhaustive and disjoint.
8. `prefixBelow` (`verification.k:37-43`) is a total structural function. The
   empty and cons equations are exhaustive/disjoint; the recursive call
   descends on `IS`; and the right side says precisely that the newly updated
   balance is negative or a later prefix is negative.
9. The high-priority loop summary (`verification.k:55-80`) is an operational
   bridge, not an oracle. Its match contains the exact loop body, final false
   return, `#endcall`, environment, all scope changes, frame, return/exception,
   heap, allocation counters, and exit code. `AUX-SPEC` proves the same
   universally quantified configuration transition against
   `MPY-VERIFICATION`, which does not import the summary. Thus the bridge match
   domain equals—not merely overlaps—the bridge-free theorem domain. Priority
   only selects the already-proved transition.

There are no proof-local opaque symbols, simplification rules, unguarded
answer axioms, or task-result oracles. The same `prefixBelow` symbol appears in
the bridge and postcondition, but this is not circular here because the
bridge-free `AUX-SPEC` independently executes the exact loop and proves that
value before the bridge is admitted.

## Operational and value sensitivity

The summary has no `<k> ... </k>` frame ellipsis, so an extra continuation
does not match. Its auxiliary claim has the same complete context. A reviewer
mutation changed the actually executed comparison from `< 0` to `> 0`.
The bridge-free auxiliary theorem then failed on the expected symbolic
condition, while the admitted summary alone still made the mutant main claim
close. This confirms both that the auxiliary theorem is body-sensitive and
that both submitted positive targets—not the main `#Top` alone—are necessary.
See `07-body-sensitivity.log`.

## Opaque and total-function ledger

The complete opaque-symbol set in the supplied tree is:

- float: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
  `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  `sqrtF`;
- sorting: `sortVS`, `sortKeyVS`;
- digest: `md5hexCodes`.

All 25 are unreachable and have no dependents among `AUX-SPEC` or
`MAIN-SPEC`. The proof-local `prefixBelow` is not opaque: its equations are
truthful, exhaustive, disjoint, and structurally descending.

## Static conclusion

No rule contributing to either positive claim has a concrete or symbolic
false-conclusion witness. The only operational bridge is independently proved
over its complete domain, including value and control state. Unused broad or
partial supplied-language behaviors are excluded from the theorem and do not
make a false conclusion about any `List[int]` input to the submitted program
provable.
