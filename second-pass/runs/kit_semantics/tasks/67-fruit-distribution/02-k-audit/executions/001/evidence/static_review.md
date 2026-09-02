# Static semantics and proof-rule review

`rule_inventory.tsv` gives one hashed row and an explicit disposition for every
local configuration, syntax statement, context, rule, and claim. Its complete
inventory is 929 rows: 1 configuration, 227 syntax statements, 5 contexts, 695
rules, and 1 claim. It found 145 function declarations, 107 total declarations,
25 symbol declarations, 22 `no-evaluators` declarations, 35 concrete
sentences, 45 priority sentences, 26 `owise` sentences, and no `functional`,
`simplification`, or explicitly `opaque` attributes.

## Per-module decision

| Source module | Inventory | Decision |
|---|---:|---|
| `semantics.k` | assembly only | `MPY` imports all fixed proof semantics. `MPY-KRUN` additionally imports `MPY-CONCRETE`; the Haskell proof does not. |
| `MPY-SYNTAX` | 16 syntax | Constructor arities and strictness/sequence-strictness correctly cover the submitted term. Unused Python subset constructors are inert. |
| `MPY-CORE` | 1 config, 37 syntax, 46 rules | Configuration, allocation, scope-chain lookup, left-to-right argument evaluation, literals, and sequence helpers preserve the cells used here. |
| `MPY-ITER` | 1 syntax | Declaration only; unreachable from this program. |
| `MPY-RANGE` | 2 syntax, 6 rules | Guard-disjoint arithmetic/iterator equations; unreachable. |
| `MPY-OPERATORS` | 2 contexts, 10 rules | Generic cooled dispatch plus priority dereference rules. Only plain integer subtraction is reached, so no priority overlap changes this run. |
| `MPY-INT` | 1 syntax, 16 rules | Integer subtraction is ordinary unbounded integer subtraction. Other arithmetic/comparison rules are guard/sort separated and unused. |
| `MPY-BOOL` | 1 context, 13 rules | Short-circuit and heap-reference cases are priority separated; unreachable. |
| `MPY-FLOAT` | 34 syntax, 121 rules | Fixed but mostly opaque proof-domain float boundary; every `no-evaluators` symbol is unreachable. Repeated mixed Int/Float equations have identical right sides, so their overlaps agree. |
| `MPY-STR` | 5 syntax, 28 rules | Recursive concatenation/comparison functions descend structurally. `strToCodes` is ASCII-only; all target labels and ground witnesses are ASCII. |
| `MPY-SET` | 6 syntax, 12 rules | Structurally descending character-set equations; unreachable. |
| `MPY-LIST` | 5 syntax, 27 rules | `valSeqConcat` is used by split token construction and descends on its first sequence. Other list semantics are unreachable. |
| `MPY-TUPLE` | 4 syntax, 21 rules | Tuple and target-binding semantics are unreachable except the built-in parameter-name list syntax; priority cell-binding cases are guarded. |
| `MPY-SUBSCRIPT` | 2 contexts, 15 syntax, 40 rules | Evaluation order and list dereference are correct. `valSeqAt` is intentionally total and underspecified out of bounds, but exact five-token shape proves indices 0 and 3 in bounds. |
| `MPY-COMPREHENSION` | 3 syntax, 7 macro rules | Macro expansion only; unreachable. |
| `MPY-METHODS` | 27 syntax, 75 rules | The used no-arg split recursively consumes one code at a time, flushes only nonempty tokens, and allocates. Its whitespace set is space/tab/LF/CR, narrower than full CPython Unicode whitespace, and this is recorded as a domain limitation rather than an unsound rule on the stated phrase domain. |
| `MPY-CONTROLS` | 3 syntax, 34 rules | Assign/import/branch/loop/control rules are unreachable. Priority rules preserve heap dereference at control consumers. |
| `MPY-FUNCTIONS` | 4 syntax, 15 rules | Exact `FuncDef` binding, parameter binding, return, and frame-pop behavior. The return rule deliberately discards only the current callee suffix and recovers the caller continuation from the saved frame. |
| `MPY-BUILTINS` | 38 syntax, 137 rules | Used `int(str)` equations compute decimal values. The length-at-least-two rule lacks its own digit guard: e.g. fixed MPY would map `"AA"` to 187 instead of raising `ValueError`; the entry's nonempty `allDigit` guards make that false behavior unreachable. The opaque MD5 symbol and all other folds are unused. |
| `MPY-CALL` | 3 syntax, 21 rules | Callee evaluation, argument ordering, method/type/closure dispatch, dereference priorities, and frame creation match the actual control path. No candidate interception preempts these rules. |
| `MPY-SORT` | 6 syntax, 19 rules | `sortVS` and `sortKeyVS` are fixed opaque trusted primitives, but no sort term is reachable. Concrete insertion equations are inactive in the Haskell proof. |
| `MPY-ASSERT` | 3 rules | Ordinary success/failure assertion behavior; assertions occur only in the independent LLVM smoke program, not the proof target. |
| `MPY-DICT` | 12 syntax, 28 rules | Ordered dictionary subset semantics; unreachable. |
| `MPY-CONCRETE` | 5 syntax, 16 rules | Imported only by `MPY-KRUN`, not by `VERIFICATION`. Concrete list equality/key-sort rules therefore cannot close the symbolic target. |
| `VERIFICATION` | no declarations | Pure import wrapper; there are no proof-local extensions, bridges, summaries, or lemmas. |
| `SPEC` | 1 claim | Exact closure body, satisfiable guarded phrase domain, and result `N-APPLES-ORANGES`; independently rebuilt and mutation-tested. |

## Overlap, totality, and control conclusions

- The used priority rules distinguish heap references and concrete call forms;
  they do not overlap the plain string/integer path with a different result.
- The used recursive functions (`splitWS`, `flushTok`, `valSeqConcat`,
  `allDigit`, `isLen`, `intDigAcc`, and in-bounds `valSeqAt`) descend on a
  constructor sequence. Guards for digit parsing and in-bounds indexing are
  supplied by the entry claim.
- `Return` and closure application save and restore the continuation, caller
  environment, stack, return state, scope location, and exception/exit state.
  Only temporary heap allocations are existentially framed in the post-state.
- No local rule encodes the fruit answer, replaces the function with an oracle,
  or introduces an unconstrained value affecting the result.
- The globally over-broad invalid-token conversion has the concrete excluded
  witness above, but there is no false-conclusion witness satisfying this
  entry's guards. Accordingly it is a language-domain limitation, not a
  candidate soundness failure.
