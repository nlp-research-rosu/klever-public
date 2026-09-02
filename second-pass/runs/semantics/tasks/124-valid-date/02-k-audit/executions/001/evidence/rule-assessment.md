# Rule inventory assessment

This assessment is keyed to `stage5-rule-inventory-with-guards.log`. That log
contains the complete normalized text and source location of all 944 top-level
K entries: 234 syntax declarations, 702 rules, five contexts, one
configuration, and two claims.

## Exhaustive range disposition

Every inventory entry is covered by exactly one row below. `FIXED` means the
entry is byte-identical to the trusted supplied-semantics tree and therefore
defines the selected semantics level. It is not a candidate proof extension.
For fixed files, the task-reachable subset was additionally checked against
the program's control flow as described in the next section. Rules in unused,
sort-disjoint modules cannot create a rewrite on this program.

| Inventory entries | Source | Disposition |
|---|---|---|
| 0001-0003 | `assert.k` | FIXED; unused by symbolic claims (used only in the independent concrete driver) |
| 0004-0017 | `bool.k` | FIXED; task-relevant short-circuit and Boolean comparison rules checked |
| 0018-0192 | `builtins.k` | FIXED; task-relevant `len` and `ord` rules checked, remainder disjoint |
| 0193-0216 | `call.k` | FIXED; task-relevant call route, builtin dispatch, and plain closure call checked |
| 0217-0226 | `comprehension.k` | FIXED; unused |
| 0227-0247 | `concrete.k` | FIXED; runtime-only module, not imported by proof module `MPY` |
| 0248-0284 | `controls.k` | FIXED; task-relevant assignment and `If` rules checked, loops unused |
| 0285-0368 | `core.k` | FIXED; task-relevant configuration, load, lookup, sequencing, values, argument order, and length checked |
| 0369-0408 | `dict.k` | FIXED; unused |
| 0409-0563 | `float.k` | FIXED; unused and sort-disjoint |
| 0564-0582 | `functions.k` | FIXED; task-relevant function definition, parameter binding, return, and frame pop checked |
| 0583-0599 | `int.k` | FIXED; task-relevant integer arithmetic/comparisons checked |
| 0600 | `iter.k` | FIXED; unused |
| 0601-0632 | `list.k` | FIXED; unused |
| 0633-0734 | `methods.k` | FIXED; unused |
| 0735-0746 | `operators.k` | FIXED; task-relevant binary and comparison dispatch checked |
| 0747-0754 | `range.k` | FIXED; unused |
| 0755-0772 | `set.k` | FIXED; unused |
| 0773-0797 | `sort.k` | FIXED; unused |
| 0798-0830 | `str.k` | FIXED; no string operation from this module is used (inputs are already `str(IntSeq)`) |
| 0831-0887 | `subscript.k` | FIXED; task-relevant string index path and normalization checked, slices unused |
| 0888-0903 | `syntax.k` | FIXED; declarations checked against every constructor in `solution.mpy` |
| 0904-0928 | `tuple.k` | FIXED; unused |
| 0929-0942 | `verification.k` | PROOF-LOCAL; all seven declarations and seven equations checked individually below |
| 0943-0944 | `spec.k` | CLAIM; both entry claims checked for satisfiability, coverage, state footprint, and result constraint |

## Task-reachable fixed-semantics mapping

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `If`, `Compare`, `CmpOp`,
`Call`, `Name`, `Subscript`, `Int`, `Bool`, `BoolOp`, `Return`, `Assign`, and
`BinOp`, plus the `Stmts`/`Exprs` lists. All are declared in `syntax.k:9-61`.

The exact execution path is:

1. `core.k:49-60,124-127` supplies the cells, loads the module, and sequences
   statements.
2. `functions.k:14-16` installs the actual function closure.
   `core.k:130-181` performs local/builtin lookup, including the `len` and
   `ord` bindings.
3. `call.k:19-21,31,69-74`, `core.k:185-191`, and
   `functions.k:63-66,78-90` evaluate callee/arguments left-to-right, create
   the callee scope, bind `date`, return, restore the caller, and remove the
   callee frame. The claims constrain the resulting scope, heap, stack,
   return state, exception state, and exit code.
4. `builtins.k:20-26,143` maps `len(str(IS))` to `isLen(IS)` and
   `ord(str(iCons(C,.IntSeq)))` to `C`.
5. `subscript.k:16-23,27-41` evaluates every fixed nonnegative string index.
   The length-ten claim makes indices 0,1,2,3,4,5,6,7,8,9 in bounds; the
   non-ten claim returns before any index. Thus the partial `intSeqAt` has no
   unmodeled reachable case.
6. `controls.k:9-18,50-54`, `bool.k:10-25`,
   `operators.k:12-17`, and `int.k:9-27` implement assignment, branch
   selection, short-circuit `or`, arithmetic, and comparisons. The short
   circuiting preserves the source order and prevents indexing on the
   non-ten branch.

No loop, allocation, mutable heap object, exception, method, collection,
float, sort, import, comprehension, or opaque operation is reachable.
Relevant priority rules either concern heap references/cell closures, which
are absent here, or are sort-disjoint. The proof-local module adds no priority,
ordinary operational bridge, simplification, or `owise` rule.

## Proof-local declarations and equations

| Entry | Classification and decision |
|---|---|
| 0929-0930 `validDateBody` | Definitional nullary function. Its sole equation is the complete translated statement body; it does not rewrite a `Call` or bypass fixed execution. It is structurally the same program term as the freshly regenerated `solution.mpy`, with explicit `.Stmts` spelling for empty branches. |
| 0931-0932 `validDateClosure` | Definitional name for `closureVal("date", validDateBody, 0)`, exactly the closure installed by loading the module at environment 0. |
| 0933-0934 `validDateModule` | Definitional name for the one-function module; fixed `#loadAll` and `FuncDef` rules still execute it. |
| 0935-0936 `digitCode` | Total mathematical predicate `48 <= C <= 57`; one catch-all equation, no overlap. |
| 0937-0938 `dateNumber` | Total decimal conversion `(T-48)*10+(O-48)`; one catch-all equation, no overlap. |
| 0939-0940 `dateLimit` | Total, exhaustive conditional: 29 for month 2, 30 for 4/6/9/11, otherwise 31; one catch-all equation, no overlap. |
| 0941-0942 `validDate10` | Total conjunction for separators, all eight ASCII digits, month 1-12, day at least 1, and day at most `dateLimit`; one catch-all equation. It names the destination value but does not participate in program execution. |

All seven proof-local functions have a catch-all equation and terminate
without recursion. Their `[total]` declarations do not introduce an
underspecified value. There are no proof-local opaque symbols, operational
rewrites, priority rules, simplification rules, or auxiliary claims.

## Opaque and special declarations

The supplied tree has no `[functional]` or `[simplification]` declarations.
Its 25 explicit opaque `symbol(...)` functions are:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`.

None occurs in `solution.mpy`, either claim, any proof-local equation, or the
final result. They are therefore inert for this theorem and cannot act as a
result-bearing oracle. The fixed `valSeqAt` is also total-but-underspecified
out of bounds, but the program uses `intSeqAt` on strings, not `valSeqAt`, and
all reached string indices are proved in bounds.

## Static conclusion

No inventoried proof-local rule encodes a program result, intercepts a real
call, fabricates state, or replaces property-bearing execution. No rule was
classified unsound, so no false-conclusion witness is asserted. The narrower
limitations are the intentionally partial supplied language semantics for
unused constructs and the opaque fixed-semantics functions above; neither is
in the dependency cone of the claims.
