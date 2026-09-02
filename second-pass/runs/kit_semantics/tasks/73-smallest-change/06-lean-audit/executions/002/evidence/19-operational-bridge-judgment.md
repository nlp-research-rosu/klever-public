# Independent Stage 5 operational-bridge judgment

The immutable target has 16 parameters. The trusted candidate gate located
exactly one candidate `def` for each, and no shadow declaration. The comparison
below is against the parameter's `kore_symbol`, its bound `source_rule_ids`, the
frozen source rules, `solution.py`, and the supplied MPY semantics.

| Parameters | Candidate meaning | Independent comparison |
|---|---|---|
| `.List`, `.Map`, `ListItem`, `_|->_` | empty list/map and singleton constructors over the generated collection representations | Exact constructor meanings used by the frozen loop configuration and environments. |
| `_-Int_`, `_+Int_`, `_<Int_`, `_<=Int_`, `_andBool_` | Lean integer subtraction/addition/order and Boolean conjunction | Exact matches for the K hooked operations. The source uses all five in loop bounds, mirrored indexing, guards, and accumulator updates. |
| `_Map_` | disjoint map union using the same lookup/disjointness/insertion representation model as the generated semantics | Exact on the defined K domain used by the target: the builtins/global/local maps have distinct keys. The empty result on overlapping keys is only a total completion where K map concatenation is undefined; no proof step exploits that completion. A disjoint singleton merge is proved nonempty in the adversarial audit. |
| `allInts` | structural recursion: true exactly for a sequence containing only `inj_SortInt` values | Equivalent to `isInt(V) andBool allInts(R)` in the frozen rule, including immediate false for a non-integer head. |
| `halfLen` | sequence length followed by the exact normalized remainder and truncated-division expression from the K definition | For the nonnegative `vsLen`, it is `floor(length/2)`, exactly the source loop bound. Edge cases of lengths 0, 1, 2, and 5 were checked. |
| `mismatchCount` | a terminating fuel recursion with fuel `(stop-index).toNat`; each step uses the supplied `applyCmp("!=", left, mirrored)` and adds 1 exactly on `some true` | Implements both guarded K equations: zero when `index >= stop`, otherwise the pair contribution plus the next index. It agrees with the Python source's one comparison per mirrored pair. Concrete non-palindromes reduce to counts 1 and 2, rejecting constant-zero and skipped-index variants. |
| `valSeqAt` | structural zero-based access, descending only for positive indices | Exact for every in-bounds nonnegative index, which is the domain established by the generated guard. Returning integer zero out of bounds is a total completion of the supplied semantics' explicitly underspecified total value and is not used to prove the guarded obligation. |
| `vsLen` | structural sequence length | Exact match to the two MPY-CORE equations. |
| `applyCmp?` | direct delegation to the immutable generated `applyCmp` relation | Preserves the supplied operational dispatch. Integer `2 != 9` reduces to `some true` and `2 != 2` to `some false`; it is neither a constant nor an invented comparator. |

The counterfactual/adversarial file and successful Lean result are recorded in
`14e-bridge-test-source.txt` and `14d-bridge-adversarial-lean.txt`. The tests
also reject identity subtraction, constant sequence recognition, constant or
identity indexing/half-length, and constant-empty disjoint map union.

The candidate definitions are therefore operational bridges, not convenient
definitions chosen merely to make the fixed equation provable.
