# Used-construct and fixed-rule dependency map

The complete 957-record source inventory is
`16-k-rule-inventory.log`: 928 records from the exact trusted supplied
semantics, 27 from candidate `verification.k`, and two reachability claims.
There are no local `[simplification]` declarations or `functional`
declarations.

## Submitted program construct coverage

| Submitted constructor/operation | Declaration | Material fixed-semantics rules |
|---|---|---|
| `Module`, statement sequence, `#loadAll` | `syntax.k:61`, `core.k:124-127` | module body is loaded and sequenced left-to-right |
| `ImportFrom("typing","List")` | `syntax.k:43` | `controls.k:35-44`; non-math import is an operational no-op |
| `FuncDef`, `Params`, closure binding | `syntax.k:53,57`; `core.k:31` | `functions.k:14-16` binds the exact body in the module frame |
| function `Call`, callee and argument evaluation | `syntax.k:28`; `core.k:185-191` | `call.k:20-24,69-75`; callee then arguments, new scope/frame, return continuation |
| parameter binding and return/pop | `functions.k:8-11` | `functions.k:63-66,78-90` |
| `Assign(Name(...), ...)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18`; RHS evaluates before binding |
| empty `ListExpr()` and allocation | `syntax.k:17`; `list.k:13` | `list.k:14-15`, `core.k:117-121`; fresh heap reference and `heapLoc` increment |
| string and integer literals | `syntax.k:9,13` | `core.k:194`, `str.k:13-17`; valid task literals are ASCII |
| `For` and loop protocol | `syntax.k:45` (`strict(2)`); `iter.k:8` | `controls.k:69-74`; iterable evaluated once, target bound, body sequenced, next iteration |
| no-argument `str.split()` | `syntax.k:28-29` | `call.k:16,20-24`; `methods.k:72-86`; returns a freshly allocated list and recognizes ASCII space/tab/LF/CR |
| target-name binding | `tuple.k:31-35` | `#bindTgt(Name(...),V)` updates current scope |
| `If` and truth | `syntax.k:49` (`strict(1)`) | `controls.k:51-54`; selected branch only |
| `Compare(...,"==",...)` | `syntax.k:30,32`; `operators.k:15-17` | `str.k:25`; structural code-sequence equality |
| `Attribute(...,"append")` and call | `syntax.k:29`; `call.k:16,20-24,52-60` | mutator receiver remains a reference |
| list `append` | `list.k:53-55` | in-place heap update using `valSeqConcat`; returns `noneV`, allocates nothing |
| expression statement | `syntax.k:52` | `controls.k:48`; evaluates for effect and discards returned value |
| `Return(Name("beats"))` | `syntax.k:50` (`strict`) | `functions.k:78-90`; result is returned and frame popped |
| duration accumulation helper dependency | `list.k:18-20` | `valSeqConcat` is disjoint, exhaustive, and structurally decreasing |

The source configuration in `core.k:49-60` accounts for every cell constrained
by the entry claim: `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.

## Exhaustive decision policy for the 928 supplied records

Every supplied record is enumerated with source line and normalized text in the
inventory. Because this is `SUPPLIED_SEMANTICS`, each is part of the selected
fixed semantics and is byte/type-identical to the trusted tree. The records in
the dependency table above were manually checked for evaluation order,
binding, frame/return control, allocation, mutation, and overlaps. The
remaining fixed records begin with constructors/functions absent from the
submitted program and from this dependency closure (floats, dictionaries,
sets, comprehensions, ranges, sorting, indexing, arithmetic, and unrelated
builtins/methods); they cannot match a target state and are classified
`FIXED_SUPPLIED_BASELINE / OUTSIDE TARGET DEPENDENCY CONE`, not as proof
extensions.

LLVM compilation reported non-exhaustive `[total]` warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. The missing cases
involve `cellsMark` or empty indexing and none of those functions is reached by
the submitted program or proof summaries. No fixed-semantics warning justifies
or repairs a candidate-local rule.

## Candidate-local rules

The 27 local records are K0929-K0955 in the complete inventory.

- `Music`, `musicIter`, and four `#iterNext` equations are a disjoint,
  exhaustive ghost algebra. They define a note-token iterator, but have no
  connection to ordinary concrete strings.
- `musicCodes(Music)` is a fresh result-bearing `IntSeq` constructor with no
  encoding equations. It is not constructor-identical to any concrete
  `iCons`/`.IntSeq` string.
- The `split` bridge at `verification.k:28-30` preempts fixed split execution,
  returns `musicIter(M)` instead of a fresh `ref`, and omits the fixed
  `<heap>/<heapLoc>` allocation. It has no bridge-free connection theorem.
- `musicAcc` and `musicLast` each have disjoint, exhaustive base/constructor
  cases and structurally decrease on `Music`. Their `[total]` attributes are
  supported by those equations.
- The four program/body/closure macros are non-overlapping. Macro-expanded JSON
  is byte-identical to the trusted-regenerated `solution.mpy` parse.
- The loop summary rule changes only the loop target binding and the referenced
  list. Its exact isolated loop claim closes without the rule, and a body
  mutation from 4 to 5 is rejected. The submitted auxiliary claim has an empty
  continuation whereas the installed rule frames an arbitrary continuation;
  no universal context theorem is supplied. No false continuation witness was
  found for this straight-line loop body, so this is recorded as an evidence
  gap rather than labeled an independent false rule.
