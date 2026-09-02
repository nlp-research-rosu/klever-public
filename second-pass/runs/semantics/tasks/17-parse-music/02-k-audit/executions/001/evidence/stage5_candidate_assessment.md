# Candidate-local declaration and rule assessment

This table assesses all 29 candidate-local inventory entries. The exhaustive
source inventory, including all 928 supplied-semantics entries, is
`stage5_rule_inventory.tsv`.

| Source | Entry | Classification | Assessment |
|---|---|---|---|
| `verification.k:7` | `Music` constructors | Proof data syntax | Sound finite valid-note sequence abstraction. |
| `verification.k:15` | `musicCodes(Music)` | Opaque result-bearing constructor | Rejected as a real-input bridge: there are no equations relating it to concrete `IntSeq` codes. |
| `verification.k:19` | `musicIter(Music)` | Proof iterator syntax | Sound as abstract syntax if connected to fixed split execution. |
| `verification.k:20` | empty iterator rule | Iterator semantic rule | Correct for an empty sequence. |
| `verification.k:21` | whole iterator rule | Iterator semantic rule | Correctly yields code 111 (`"o"`). |
| `verification.k:23` | half iterator rule | Iterator semantic rule | Correctly yields codes 111,124 (`"o|"`). |
| `verification.k:25` | quarter iterator rule | Iterator semantic rule | Correctly yields codes 46,124 (`".|"`). |
| `verification.k:28` | proof-only `split` rewrite | Operational bridge, priority 35 | Unsound over its complete state footprint. It preempts fixed split, fabricates `musicIter(M)`, omits the fixed `#alloc`, changes the final heap and `heapLoc`, and has no bridge-free connection theorem. Ground witness: valid input `"o"` ends with `heapLoc=2` under fixed semantics but the claim proves `heapLoc=1`. |
| `verification.k:33` | `musicAcc` declaration | Total definitional summary | Constructor-complete and descending over `Music`. |
| `verification.k:34` | `musicAcc` empty | Equation | Correct identity base case. |
| `verification.k:35` | `musicAcc` whole | Equation | Correctly appends 4 and descends. |
| `verification.k:37` | `musicAcc` half | Equation | Correctly appends 2 and descends. |
| `verification.k:39` | `musicAcc` quarter | Equation | Correctly appends 1 and descends. |
| `verification.k:43` | `musicLast` declaration | Total definitional summary | Constructor-complete and descending over `Music`. |
| `verification.k:44` | `musicLast` empty | Equation | Correctly preserves the prior note. |
| `verification.k:45` | `musicLast` whole | Equation | Correctly updates to `"o"` and descends. |
| `verification.k:47` | `musicLast` half | Equation | Correctly updates to `"o|"` and descends. |
| `verification.k:49` | `musicLast` quarter | Equation | Correctly updates to `".|"` and descends. |
| `verification.k:54` | `parseMusicLoopBody` declaration | Macro syntax | Acceptable exact fragment name. |
| `verification.k:55` | loop-body macro expansion | Macro equation | Matches `solution.mpy:7-11` exactly. |
| `verification.k:62` | `parseMusicBody` declaration | Macro syntax | Acceptable exact fragment name. |
| `verification.k:63` | body macro expansion | Macro equation | Matches `solution.mpy:4-12` exactly. |
| `verification.k:71` | `parseMusicClosure` declaration | Macro syntax | Acceptable exact fragment name. |
| `verification.k:72` | closure macro expansion | Macro equation | Correct parameter, body, and defining scope for the module function. |
| `verification.k:75` | `parseMusicProgram` declaration | Macro syntax | Acceptable exact fragment name. |
| `verification.k:76` | program macro expansion | Macro equation | Matches all of submitted `solution.mpy`, including the ignored typing import. |
| `verification.k:89` | loop summary rewrite | Derived operational summary, priority 35 | Its exact loop claim independently closes against the base definition. The rewrite accepts an arbitrary continuation whereas the proved claim's `<k>` cell is exact; no universal context theorem is supplied. No false continuation witness was found for this normal, abrupt-control-free body, so this is recorded as a narrower context-justification gap, not independently called unsound. |
| `spec.k:9` | loop reachability claim | Positive auxiliary claim | Satisfiable, result/state-constraining, and freshly closes with `#Top`. |
| `spec.k:32` | entry reachability claim | Positive entry claim | Satisfiable as a K term and freshly closes with `#Top`, but depends on the rejected split bridge and concludes the bridge's false exact heap/allocator state. |

There are no candidate-local simplification rules or `[functional]`
declarations. The only candidate priority rules are the split bridge and loop
summary. The only candidate opaque result-bearing symbol is `musicCodes`.

## Supplied-semantics review disposition

The supplied `semantics.k` contains assembly imports and module declarations but
no local operational rules. Its 23 helper files contribute the other 928
inventory entries: one configuration, all language syntax, 157 function
declarations (117 marked total), 624 ordinary rules, 32 concrete rules, 26
`owise` rules, 31 priority rules, five contexts, eight macros, and 25
`symbol`/`no-evaluators` opaque function declarations. There are no
simplification or `[functional]` declarations.

Every supplied entry is byte-for-byte the trusted mounted baseline. The used
path was reviewed directly:

- `syntax.k` declares every submitted constructor and gives left-to-right
  strictness for assignment, `For`, `If`, and `Return`.
- `core.k:49-60,117-127,130-154,183-219` supplies the complete configuration,
  allocation, load/statement sequencing, lookup, argument evaluation, literals,
  and algebraic sequence helpers.
- `functions.k:14-16,63-66,77-90` and `call.k:15-24,52-74` supply closure
  creation, binding, calls, return, stack restoration, and scope deallocation.
- `controls.k:9-18,33-54,62-74,85-108` supplies assignment, the harmless
  non-math import no-op used for `typing`, expression statements, branches, the
  iterator loop, and list-iterator dereference.
- `tuple.k:30-41` supplies the `Name("note")` loop-target rebinding operation.
- `str.k:13-26`, `methods.k:70-86`, `operators.k:14-17`, and
  `list.k:12-20,52-55` supply ASCII literals, equality, concrete whitespace
  split, compare dispatch, list allocation/concatenation, and in-place append.
- `iter.k` declares the protocol used by both fixed semantics and the proof
  extension.

These used fixed rules preserve evaluation order, bindings, call/return control,
heap writes, and allocations for this program. The remaining supplied entries
model constructs absent from `solution.mpy`; their opaque float, keyed-sort,
MD5, and related symbols cannot influence either proof claim. Fresh compilation
reported non-exhaustive-total warnings for `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`; none is reachable from this program or
from the candidate-local equations. No supplied rule was changed by the
candidate and no used-path false conclusion witness was found.
