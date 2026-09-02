# Static soundness review and construct map

The exhaustive, line-addressed source inventory is in
`K_RULE_INVENTORY.md`. It covers all 26 selected K files: the trusted
`semantics.k` assembly, all 23 helper modules, `verification.k`, and `spec.k`.
It contains 229 syntax declarations, 699 rules (461 equational and 238
operational), five contexts, one configuration, and two claims. Attribute
counts are: 148 `function`, 109 `total`, zero `functional`, zero
`simplification`, 45 priority rules, 26 `owise` rules, 36 `concrete` rules,
and 22 opaque `no-evaluators` declarations.

## Rule-by-rule disposition

Every item is present verbatim with its file and starting line in
`K_RULE_INVENTORY.md`. The dispositions used for all 699 inventoried rules
are:

1. `PROOF-LOCAL/ACCEPT`: the four equations in `verification.k` were checked
   individually below. They are exhaustive, pairwise disjoint by the
   `ValSeq` constructor in the recursive argument, and structurally
   descending. Neither rewrites `<k>`.
2. `FIXED/REACHED/ACCEPT`: every fixed-semantics declaration and rule on the
   actual program path is listed below. The sequence preserves evaluation
   order, binding, allocation, heap mutation, loop control, return, and all
   observable cells. Guards and priorities are disjoint or agree on overlap.
3. `FIXED/UNREACHED/ACCEPT-AS-BOUNDARY`: every remaining trusted-semantics
   rule is unreachable from this program and its claim states. The complete
   inventory was checked for rules sharing a reached label or a globally
   active simplifier. There are no simplification rules. Overloaded
   `applyCmp`, `applyBuiltin`, `applyMethod`, and call-interception rules not
   listed below have constructor-, receiver-, method-, builtin-, or
   operation-string patterns disjoint from this program's reached redexes.
   No unused rule encodes `remove_duplicates`, `rdAcc`, or this task's
   answer. This disposition accepts the launcher-selected supplied semantics
   as the language-model boundary; it is not a claim that every unused
   Python feature is fully CPython-faithful.

No rule was classified as unsound. Consequently there is no false-conclusion
witness to report. The fresh false-result and body-sensitivity witnesses are
separate discrimination tests, not unsound-rule allegations.

## Proof-local declarations and equations

- `verification.k:7-9`, `allInts`: total predicate over the two `ValSeq`
  constructors. Empty is true; nonempty is `isInt(head) andBool
  allInts(tail)`. It only restricts preconditions.
- `verification.k:13-19`, `rdAcc`: total three-argument result summary,
  split on empty/nonempty `REST`. The nonempty equation appends exactly when
  `cntOccVS(ALL,V) == 1` and recurses on the strict tail. It does not replace
  execution.
- `spec.k:6-40`, loop claim: exact `#loop` term and body, with the same framed
  continuation. It reads `numbers`, `result`, and `number`; updates only
  `number` and heap location `H`; preserves all other framed cells.
- `spec.k:42-109`, entry claim: exact module load, closure body, call, result
  reference, heap contents, allocation counters, scopes, stack, return,
  exception, and exit-code cells.

There are no proof-local ordinary operational rules, priority rules,
`owise` rules, simplification rules, opaque symbols, trusted primitives, or
unconstrained result-bearing values.

## Constructor-to-semantics map

| Program construct | Declaration | Reached fixed rules and check |
|---|---|---|
| `Module`, `ImportFrom`, `FuncDef`, `Params`, `Stmts` | `syntax.k:41-61` | Initial configuration `core.k:49-60`; load/sequencing `core.k:124-127`; typing import is the non-math no-op `controls.k:35-44`; closure binding `functions.k:14-16`. The import is typing-only and absent from the function body. |
| Function call and local binding | `syntax.k:28`, `core.k:185-188`, `functions.k:8-11` | Name lookup `core.k:130-154`; generic callee and left-to-right arguments `call.k:19-21`, `core.k:189-191`; closure frame allocation `call.k:69-75`; exact positional binding `functions.k:63-66`. |
| `Assign(Name(...), ...)` | `syntax.k:41` | RHS strictness plus local scope write `controls.k:9-11`. |
| `ListExpr()` | `syntax.k:17` | Left-to-right element evaluation and fresh list allocation `list.k:13-15`, `core.k:117-121`, `core.k:217-219`. |
| `Int(0)` and `Int(1)` | `syntax.k:9` | Literal reduction `core.k:193-196`. |
| `For(Name("number"), Name("numbers"), body)` | `syntax.k:45` | Iterable evaluated once; `For` to `#loop` and iteration control `controls.k:62-74`; list iterator `list.k:8-10`; name target binding `tuple.k:30-41`; loop label continuation `controls.k:84-91`. |
| `If(Compare(...), then, empty)` | `syntax.k:49`, `syntax.k:30-32` | Compare operand contexts and dispatch `operators.k:14-17`; integer equality `int.k:22-27`; Boolean truthiness `core.k:198-205`; branch rules `controls.k:50-54`. |
| `numbers.count(number)` | `syntax.k:28-30` | Attribute to bound method `call.k:15-16`; ordinary call and arguments `call.k:19-24`, `core.k:189-191`; exact list-count dispatch and recursive count `methods.k:63-68`. Under `allInts`, `==K` is integer equality. |
| `result.append(number)` | `syntax.k:28-30` | `isMutMethod` keeps the receiver reference `call.k:52-60`; append priority rule mutates the exact heap location and returns `noneV`, `list.k:52-55`; sequence append is total and descending, `list.k:18-20`; expression result is discarded by `controls.k:46-48`. |
| `Return(Name("result"))` | `syntax.k:50` | Strict result evaluation via lookup, abrupt return to `#pop`, restoration of caller environment, frame removal, stack cleanup, and preserved heap allocation in `functions.k:77-90`. |

## Functions, totality, overlaps, and priorities on the reached path

- `allInts`, `rdAcc`, `valSeqConcat`, `cntOccVS`, `appendVal`,
  `vals2valSeq`, `isMutMethod`, `isRefV`, and `builtinsScope` are the only
  source-level functions materially used. Their constructor cases cover
  every reached argument and recurse structurally where recursive.
- `cntOccVS` has empty, equal-head, and unequal-head cases. The latter guards
  are exact Boolean complements. On the intended integer domain its `==K`
  test agrees with Python integer equality.
- `rdAcc` tests `1 ==Int cntOccVS`; the program tests
  `cntOccVS ==Int 1`. Integer equality is symmetric, so these conditions are
  equivalent.
- The reached priority rule is list `append` at `list.k:53-55`; it is the
  exact mutating-method case and correctly preempts receiver dereference.
  Exact math, md5, split, sort, deep-equality, closure-cell, and other
  priority patterns do not match any reached redex.
- The generic `Call` rule is `owise`; no specific call interception matches
  either `remove_duplicates`, `count`, or `append`.

## Opaque-symbol inventory

All 22 opaque declarations are enumerated in `K_RULE_INVENTORY.md`:
`md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`;
and `sortVS`, `sortKeyVS`. None appears in `solution.mpy`,
`verification.k`, `spec.k`, the positive residual path, or the final
postcondition. They influence no branch, value, state, exception, or claim
in this proof.

LLVM reported non-exhaustive-match warnings for unrelated total functions
(`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`) on
constructors outside their intended subdomains. None is reached here. No
false result for an intended `List[int]` input can be obtained from those
warnings, so they are recorded as an unused language-model limitation, not
an unsoundness finding against this theorem.
