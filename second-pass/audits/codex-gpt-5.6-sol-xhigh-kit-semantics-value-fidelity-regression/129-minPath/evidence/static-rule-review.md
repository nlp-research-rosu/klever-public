# Static rule review and construct map

This is the reviewer-authored companion to `k-rule-inventory.tsv`. The TSV
contains every declaration, context, rule, and claim from the supplied
semantics, `verification.k`, and `spec.k`, with file and line locations. Its
final totals are 1 configuration, 5 contexts, 166 function declarations, 93
other syntax declarations, 748 ordinary rules, 15 simplification rules, and 6
claims.

## Supplied-semantics decision

The 928 records outside `verification.k` and `spec.k` are the fixed,
trusted supplied-semantics baseline, not candidate-authored proof extensions.
The candidate tree recursively matches `/reference/reference-semantics`
byte-for-byte. Each such record is therefore classified
`ACCEPTED_FIXED_SUPPLIED_SEMANTICS` for this audit. This classification means
the rule defines the selected execution model; it does not claim the model is
full CPython.

The global inventory finds two genuinely opaque fixed-semantics functions:
`md5hexCodes` in `semantics/builtins.k:285` and `sortKeyVS` in
`semantics/sort.k:49`. Neither symbol, its call route, nor any dependent
construct occurs in `solution.mpy`, `verification.k`, or `spec.k`, so neither
affects any target claim. The proof definition imports `MPY`, not
`MPY-CONCRETE`; the concrete LLVM definition imports `MPY-KRUN`, as required.

## Used-construct coverage

Every syntax node in `solution.mpy` is declared and has a fixed rule path:

| Submitted construct | Fixed declaration / execution |
|---|---|
| `Module`, statement sequencing | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, params, closure creation | `syntax.k:53,57`; `functions.k:14-16` |
| `Name`, `Int` | `syntax.k:9,12`; `core.k:129-154,193-196` |
| `Assign(Name, ...)` | `syntax.k:41`; `controls.k:8-18` |
| tuple expression and tuple-target assignment | `syntax.k:21`; `tuple.k:13-16,30-57` |
| `If` | `syntax.k:49`; `controls.k:50-54` |
| `For` over list and range | `syntax.k:45`; `controls.k:62-74,104-108`; `list.k:8-10`; `range.k:9-24` |
| `Return`, calls, frames, parameter binding | `syntax.k:28,50`; `call.k:18-32,69-75`; `functions.k:62-90` |
| `UnaryOp`, `BinOp`, `Compare` | `syntax.k:14-15,30-32`; `operators.k:10-20`; `int.k:7-27` |
| `len`, `abs`, `min`, `range` | `core.k:156-181`; `call.k:26-32`; `builtins.k:19-26,43-45,96-105,176-180` |
| list literal/allocation and `append` | `syntax.k:17,29`; `core.k:117-121`; `list.k:12-20,52-55`; `call.k:15-24,52-67` |
| expression statement | `syntax.k:52`; `controls.k:46-48` |

Evaluation is left-to-right for binary operands and argument sequences
(`syntax.k:15`, `core.k:183-191`, `call.k:18-21`). List inputs and returned
lists are heap values; the entry claim explicitly constrains heap allocation
location 0 and `heapLoc` from 0 to 1. Calls normally allocate and pop a local
scope, restore the caller environment and return continuation, and preserve
escaped heap allocations (`call.k:69-75`, `functions.k:77-90`).

The fresh LLVM execution in `logs/16-fresh-concrete-krun.log` exercises all
constructs used by the entry implementation and terminates with `.K`, empty
call stack, `noRet`, and the expected result lists.

## `VERIFICATION-SYNTAX` records

The eleven macro declarations and eleven expansion rules at
`verification.k:6-142` are exact constructor aliases for:

- each of the four loop bodies;
- all five function bodies; and
- the complete `minPath` body.

Manual constructor comparison against regenerated `solution.mpy` found no
changed statement, reordered expression, omitted branch, or substituted
literal. Decision for every one of these 22 records:
`VALID_EXACT_SYNTAX_ALIAS`.

## Pure verification functions and equations

The following declarations and all their equations are total structural
definitions. Base/recursive cases cover `.ValSeq` versus `vCons`; guarded
integer/non-integer or true/false branches are disjoint; each recursion
consumes a sequence or increases the index while consuming one:

- `intsOnly`, `rowContents`, `isIntList`, `intRows`;
- `lastValOr`, `scanOneCol`, `gridDistance`, `scanNeighbor`, `foundCol`;
- `locateRow`, `locateCol`, `lastFoundCol`, `scanGridNeighbor`;
- `flattenRows`, `squareRows`, `cellsInRange`, `valMember`, `distinctVals`,
  and `validGrid`;
- `alternatingValue` and `alternatingSeq`.

Decision for their declarations and equations at
`verification.k:149-176,337-498`: `VALID_DEFINITIONAL_SUMMARY`.
`rowContents` deliberately maps non-lists to empty, but every result-bearing
use in a target claim is guarded by `isIntList`/`intRows`; `validGrid` rejects
non-list rows. No false conclusion is enabled on the formal domain.

The guarded `applyCmp` projection at lines 154-155 agrees with the fixed
integer equality rule on its complete `isInt(V)` guard. The guarded `minVals`
projection at lines 157-160 agrees with the fixed two-argument integer `min`
fold. `intsOnly(rowContents(V))` at lines 170-172 follows directly from
`isIntList(V)`. Integer reassociation at lines 356-357 and `valSeqConcat`
associativity at lines 499-501 are ordinary mathematical associativity.
Decision: `VALID_DERIVED_EQUATION`.

The `For` normalization at lines 178-181 rewrites `V` to
`list(rowContents(V))` only when `isIntList(V)`. That guard implies
`V = list(VS)` and `rowContents(V) = VS`, so the rewrite preserves the exact
iterable and all cells. Decision: `VALID_IDENTITY_OPERATIONAL_BRIDGE`.

There are no proof-local opaque symbols.

## Program-defined call rules

The five priority-35 rules at `verification.k:183-335` intercept:

1. `find_one(row)` and return `foundCol(ROW)`;
2. `scan_row(...)` and return `scanNeighbor(...)`;
3. `locate_one(grid)` and return the pair of `locateRow`/`locateCol`;
4. `find_neighbor(...)` and return `scanGridNeighbor(...)`; and
5. `build_path(...)` and allocate `alternatingSeq(...)`.

They pin the expected textual call, caller locals, module binding, and macro
body, but they run before the fixed generic call route. They therefore skip
callee lookup/argument evaluation, scope allocation, parameter binding, the
actual helper body, return, frame pop, and—in the fifth case—the actual loop.
Their `<k> ... </k>` matches an arbitrary continuation, and their omitted
stack, return, exception, scope-location, and most heap cells are framed.

The summarized values influence branches, coordinates, the selected neighbor,
the final allocation, and the entry postcondition. No auxiliary reachability
claim proves an exact helper invocation from call through restored caller
state to any of these values. The loop claims start at `#loop`; they do not
establish the straight-line initialization, call frame, or return connection.
Using the same summary functions in these bridges and in the postcondition is
circular, not a connection theorem.

Decision for all five rules:
`ILLEGITIMATE_UNPROVED_RESULT_BEARING_OPERATIONAL_BRIDGE`.

This decision is not an assertion that the summaries happen to be numerically
wrong for the submitted source. For the current source they agree with finite
testing and manual reasoning. The narrower defect is that correctness of the
program-defined computations is installed as proof rules rather than derived
from the fixed semantics.

The required sensitivity witness is preserved as
`verification-body-witness.k`, `body_witness.py`, and logs 27-31. It changes
the exact `find_neighbor` body to `return 999` while leaving its bridge summary
unchanged. The valid input `grid=[[1,2],[3,4]], k=3` produces `[1,999,1]` in
Python and under the fixed LLVM semantics, but the entry claim still prints
`#Top` and retains the old formal result `[1,2,1]`. Thus the proof architecture
can enable a concrete false conclusion on an intended-domain state when the
displaced computation changes, establishing failure of the required
body-to-summary connection.

## Claim records

All six claims are inventoried in `spec.k`. Their equations and guards are
result-constraining, and the independent false-result mutation fails. The
claims are not themselves false axioms; their closure is conditional on the
five illegitimate call rules above. The three inner loop claims (`find_one`,
`scan_row`, `build_path`) execute real loop bodies. The two outer loop claims
depend on intercepted helper calls, and the entry claim depends directly or
transitively on every intercepted helper.
