# Reviewer static rule review

This note accompanies the machine-produced, line-addressed inventory in
`05b-exhaustive-k-inventory-corrected.log`. The inventory covers all 26 K
sources used by the proof: 24 files in the trusted supplied-semantics tree,
`verification.k`, and `spec.k`. It enumerates 231 syntax declarations, one
configuration, five contexts, 710 rules, and two claims. There are no
`functional` declarations. There are 111 `total` declarations, 24 opaque
`no-evaluators` symbols, 43 priority-40 rules, three priority-45 rules, one
priority-39 rule, 36 concrete rules, and eight simplification rules.

## Module-by-module disposition

The selected semantics level is the byte/type-identical trusted supplied tree.
The table accounts for all 695 rules in that tree plus all 15 proof-local rules.
“Unused” means no term headed by that module's program construct or helper can
be reached from the submitted AST and entry configuration. The declarations
and every individual rule remain listed with line numbers in the inventory.

| Source | Rules | Relation to this proof | Static disposition |
|---|---:|---|---|
| `semantics.k` | 0 | Assembly/import graph | Exact trusted assembly; proof imports `MPY`, concrete checks use `MPY-KRUN`. |
| `syntax.k` | 0 | AST declarations | Used constructors are mapped below; unused syntax is inert. |
| `core.k` | 46 | Configuration, load, lookup, heap allocation, sequencing, literals, argument evaluation | Used rules preserve left-to-right evaluation, lexical lookup, allocation, and normal cells. Remaining shared helpers are exact trusted semantics and do not introduce task-specific conclusions. |
| `iter.k` | 0 | Iterator protocol declarations | Used by list iteration and the local exact bridge. |
| `range.k` | 6 | Range objects | Unused. |
| `operators.k` | 10 | Comparison routing and reference dereference | Used for each string `not in`; operand order and `in` element/reference treatment agree with the fixed string path. |
| `int.k` | 16 | Integer operators | No submitted body arithmetic; built-in integer predicates in preconditions use K's hooked integer theory. |
| `bool.k` | 13 | Value-returning short-circuit `and`/`or` | The five-way `and` evaluates left to right and stops on the first false comparison, matching the program. Reference-priority variants are unreachable here. |
| `float.k` | 121 | Float subset and 19 opaque float operations | Entirely unused. No float constructor, call, or value is reachable. |
| `str.k` | 28 | ASCII literals, membership, substring helpers | Used literals are ASCII digits; `not in` is `notBool strContains`, and `strContains` is a terminating prefix/scan definition. |
| `set.k` | 12 | String-set operations | Unused. |
| `list.k` | 27 | List literals, list iteration, concatenation, append | Used. List construction allocates; fixed iterator yields the head/rest; append mutates exactly the referenced accumulator and returns `noneV`. The local iterator bridge is checked separately below. |
| `tuple.k` | 21 | Tuples and assignment-target binding | Only `#bindTgt(Name(...), V)` is used by `For`; it updates the current local scope. Tuple-specific paths are unused. |
| `subscript.k` | 40 | Indexing and slicing | Unused. Its compiler-reported non-exhaustive total `valSeqAt` case is therefore an evidence limitation, not a route to the result. |
| `comprehension.k` | 7 | Comprehensions | Unused. |
| `methods.k` | 75 | Pure string/list methods | Unused by the submitted body; list `append` is defined in `list.k`. Its compiler-reported `joinCodes` non-exhaustiveness is off-path. |
| `controls.k` | 34 | Assignment, expression statements, `If`, `For` | Used rules evaluate RHS/guards once, bind each head, execute the exact body, and return to the next loop head. Cell-variable, while, import, and break/continue routes are unreachable. |
| `functions.k` | 15 | Closure creation, parameter binding, return, frame pop | Used plain-closure path binds `x`, executes the embedded body, restores the caller, deletes the local frame, and propagates the returned reference. Annotated-closure paths are unused. |
| `builtins.k` | 137 | Built-in operations | The proof reaches only `str`; symbolic execution is preempted by the audited local bridge. Concrete execution reaches the fixed ground `str` rule. Other built-ins are unused. The runtime warning for total `mapStrVS` is off-path. |
| `call.k` | 21 | Callee and argument evaluation/dispatch | Used. Name lookup selects the closure or built-in first, arguments evaluate left-to-right, and dispatch preserves the selected binding. |
| `sort.k` | 19 | `sorted` and sort summaries | Used unkeyed `sorted` rule allocates a new list containing opaque `sortVS(VS)`. Ground LLVM execution uses the insertion rules. Ascending-permutation meaning is a named trusted primitive, not proved symbolically. Key/reverse and mutating-sort rules are unused. |
| `assert.k` | 3 | Assert | Not in the submitted body; used only by reviewer concrete tests. |
| `dict.k` | 28 | Dictionaries | Unused. |
| `concrete.k` | 16 | LLVM-only keyed sorting/deep equality legs | Imported only by the runtime definition; submitted checks do not use keyed sorting or nested-reference equality. |
| `verification.k` | 15 | Candidate proof extensions | All 15 are individually assessed below. |

The LLVM build reported non-exhaustive `total` functions `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is reachable from the
submitted AST. No warning involved `sortVS`, `str`, `strContains`, list
iteration/append, the entry path, or a proof-local symbol. Because these are
coverage warnings rather than false equations, and no false conclusion witness
on the intended input domain exists, they are recorded as narrower off-path
evidence gaps rather than unsoundness.

## Used-constructor map

| Submitted constructor | Declaration and operational path |
|---|---|
| `Module`, statement/argument sequences | `syntax.k:56-61`; `core.k:124-127` loads and sequences statements. |
| `FuncDef`, `Params` | `syntax.k:53-60`; `functions.k:14-16` installs the exact `closureVal`. |
| `Call` | `syntax.k:28`; `call.k:20-32,69-75` evaluates the callee, arguments, and plain closure. |
| `Name` | `syntax.k:12`; `core.k:130-154` performs local/global/built-in lookup. |
| `Assign` | `syntax.k:41`; `controls.k:9-18` evaluates RHS then writes the local binding. |
| `ListExpr` | `syntax.k:17`; `list.k:13-15` evaluates elements and allocates a list. |
| `Int`, `Str` | `syntax.k:9,13`; `core.k:193-196` and `str.k:13-17`. |
| `For` | `syntax.k:45`; `controls.k:62-74`, `list.k:9-10`, and `tuple.k:31-41`. |
| `If` | `syntax.k:49`; `controls.k:50-54`. |
| `BoolOp("and", ...)` | `syntax.k:16`; `bool.k:13-25` gives left-to-right short-circuit behavior. |
| `Compare(..., CmpOp("not in", ...))` | `syntax.k:30-32`; `operators.k:14-17`, then `str.k:28-41`. |
| `Attribute(..., "append")`, expression statement | `syntax.k:29,52`; `call.k:15-24`, `list.k:52-55`, and `controls.k:46-48`. |
| `Return` | `syntax.k:50`; `functions.k:77-90` records, pops, and returns the value. |
| built-in `str` | Built-ins scope in `core.k:156-181`; local symbolic bridge in `verification.k:23-26`; ground rule in `builtins.k:147-149`. |
| built-in `sorted` | Built-ins scope in `core.k:172`; `sort.k:34-37` allocates `list(sortVS(VS))`. |

## Every proof-local rule

1. `intProj(I:Int) => I`: an exact projection on the only guarded use. The
   symbol is otherwise opaque/total; no rule assigns a false integer.
2. Ground `decimalCodes(N)`: exactly `strToCodes(Int2String(N))`. Symbolic
   inputs remain named and opaque.
3. `positiveInts(.ValSeq)`: exact base case.
4. `positiveInts(vCons(...))`: conjunction of K subsort membership, exact
   projection, positivity, and the recursive tail; recursion strictly descends.
5. Positive-Int `str` bridge: at the already evaluated
   `#applyK(toCall(typeV("str")), ...)` state it changes only `<k>`. Binding and
   arguments have already been resolved/evaluated. For `I > 0`, its named codes
   equal the fixed ground `str` result; no heap/scope/control effects are skipped.
6. Integer-list iterator bridge: fixed semantics yields `V` and `list(REST)`;
   under `isInt(V)`, `intProj(V) = V`. It changes only `<k>` and preserves the
   exact rest iterator.
7. `filterOdd(.ValSeq)`: exact base case.
8-12. Five reject equations: each removes the head if its positive decimal
   code sequence contains `0`, `2`, `4`, `6`, or `8`. Overlaps have identical
   right sides and strictly descend.
13. Keep equation: its guard is the conjunction of the negations of all five
   reject predicates, so it is disjoint from them and preserves the integer
   head. Together the six recursive cases cover the Boolean predicate space on
   intended positive-Int inputs.
14. `valSeqConcat(A, .ValSeq) => A`: right identity, derivable by induction from
   the fixed recursive definition. It agrees on overlaps with the base rules.
15. Reassociation of nested `valSeqConcat`: associativity, derivable by
   induction; the orientation reduces left nesting and agrees with the identity
   equation on overlaps.

There is no rule that rewrites a whole `unique_digits` call, fabricates a return
reference, skips the function body, or changes any result/state cell to an
unconstrained variable. The only operational bridges are rules 5 and 6; both
have the same state footprint and result as the fixed path on the entry domain.

## Opaque and trust accounting within the rule review

The inventory's 24 opaque symbols comprise 19 float symbols, `md5hexCodes`,
`sortKeyVS`, `sortVS`, `intProj`, and `decimalCodes`. The float, MD5, and keyed
sort symbols are unreachable. `intProj` has an exact Int-injection rule and is
used only under integer guards. `decimalCodes` has an exact ground equation but
is a symbolic empirical bridge for arbitrary positive integers. `sortVS` is the
supplied semantics' explicitly opaque sorted-list primitive, with independently
executable concrete insertion rules. Its ascending-permutation interpretation
is assumed rather than established by the reachability proof.

No rule is labelled unsound: the review found no rule that enables a false
conclusion on a finite list of positive integers. Accordingly there is no false
conclusion witness to report. The symbolic meanings of `decimalCodes` and
`sortVS` are instead explicit evidence/trust limitations, addressed by concrete
and differential tests but not universally proved.
