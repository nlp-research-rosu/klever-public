# Independent adversarial audit: 33-sort-third

Overall decision: **CONCERNS / LEGIT**. The fresh reconstruction proves a
result-constraining reachability claim for the exact translated program, and
the candidate adds no execution-bypassing or mathematically false rule. The
qualification is that the supplied semantics intentionally leaves `sortVS`
opaque to symbolic proof. Thus the universal K result is conditional on the
external contract that `sortVS` is Python's ascending, length-preserving sort.
Concrete K execution and 100,208 differential cases support that bridge for
integer lists, but finite testing is not a universal connection theorem.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is a real directory.
The recursive reviewer manifest found 25 entries in each semantics tree, with
identical entry names, kinds, sizes, and SHA-256 hashes. There were no missing,
additional, changed, mistyped, or symlinked entries under the candidate's
`reference-semantics/`. The candidate `prompt.py` and `py2mpy.py` are byte
identical to their trusted versions:

- `prompt.py`:
  `41c45573886f68a38b5dc46f74ab70ef4cb79656e72bc97a04b861810158fa8c`
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The required executable proof sources `solution.py`, `solution.mpy`, `spec.k`,
and `verification.k` are ordinary files. The candidate contains no supplied
compiled definition. Its `__pycache__`, `prove.sh`, `concrete_tests.py`, and
`concrete-tests.mpy` were treated as untrusted, non-required extras and were not
used for reconstruction.

Four requested provenance records are missing:
`run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`.
No structured trace (`*trace*`, JSONL, or NDJSON) is present. Therefore there
was nothing in those categories to read as an untrusted claim. This is an
auditability gap, but not a contradictory mount or an infrastructure breach.

Evidence:

- `evidence/integrity_check.py`
- `evidence/stage1-integrity.log` (exit 0)
- `evidence/stage3-source-provenance.log` (all copied sources still match their
  mounted origins, exit 0)

All execution sources were copied to
`/tmp/audit-work/audit-33-sort-third`. Candidate caches and compiled artifacts
were neither copied nor reused.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation specify this contract: return
a fresh list of the same length; preserve every value at indices not divisible
by three; take the values originally at indices `0, 3, 6, ...`, sort that
subsequence in ascending order, and place it back at those same indices. The
input is not mutated. The prompt does not state an element type, so the natural
Python domain is a finite list whose every-third subsequence is mutually
sortable. All prompt examples are integer lists.

`solution.py` follows a different but equivalent algorithm. It computes
`sorted(l[::3])`, scans the original input once, takes `thirds[i // 3]` exactly
when `i % 3 == 0`, otherwise takes the scanned value, and appends into a new
list. The branch and index arithmetic are correct at lengths in every residue
class modulo three.

The trusted translator was run afresh:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0, and `cmp --verbose solution.mpy regenerated-solution.mpy` exited
0. The submitted MPY is therefore exactly the trusted translation of the
submitted Python.

The independent differential script imports
`/tmp/audit-work/audit-33-sort-third/canonical.py` and
`solution.py`, and also compares both to an independently coded index-assignment
oracle. It exercised:

- both documented examples and eight additional explicit cases;
- 42 ascending, descending, and patterned length-boundary cases for lengths
  0 through 13;
- all 97,656 integer lists of lengths 0 through 7 over
  `{-2,-1,0,1,2}`;
- 2,500 deterministic random integer lists of lengths 0 through 100.

All 100,208 cases agreed, and neither implementation mutated its input. The
input stream digest was
`0b9038782537d07da1f9c5ca44f8bf65536181cbb482cee561ec7291e5a44054`.

Evidence:

- `evidence/differential_test.py`
- `evidence/differential-input-plan.json`
- `evidence/stage2-translate.log`
- `evidence/stage2-mpy-byte-identity.log`
- `evidence/stage2-differential.log`

## 3. Clean proof reconstruction

The live toolchain was K `v7.1.337` and Python `3.10.12`
(`evidence/toolchain.log`). Both definitions were built from source in the
fresh scratch tree.

Concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0. A reviewer-authored concrete program contains an AST-identical
copy of the submitted function plus empty, length-1, length-2, modulo-boundary,
documented, and negative-value assertions. Its trusted translation and
`krun concrete-audit.mpy --definition runtime-kompiled` both exited 0; the
final configuration has `.K`, `NoExc`, and exit code 0.

Proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0. The claims were reconstructed as follows:

- `kprove ... --claims SPEC.sort-third-loop` exited 0 and printed `#Top`.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC`
  exited 0 and printed `#Top`, discharging the auxiliary loop claim and entry
  claim together.

An entry-only diagnostic was also run. Filtering the specification to
`SPEC.sort-third-correct` removes the auxiliary circularity, so that diagnostic
exited 1 at the real `#iterNext`/`#loopStep` state. Adding `--trusted` did not
reinclude a claim removed by `--claims`. This is expected claim dependency,
not closure of a false target: the actual positive target set includes and
simultaneously proves the loop claim, and that complete set closes with
`#Top`.

Evidence:

- `evidence/stage3-kompile-concrete.log`
- `evidence/k_concrete_tests.py`
- `evidence/stage3-concrete-function-identity.log`
- `evidence/stage3-translate-concrete-test.log`
- `evidence/stage3-krun-concrete.log`
- `evidence/stage3-kompile-proof.log`
- `evidence/stage3-kprove-loop.log`
- `evidence/stage3-kprove-all.log`
- `evidence/stage3-kprove-entry.log` and
  `evidence/stage3-kprove-entry-with-aux.log` (dependency diagnostics)

## 4. Adequacy and real-program pinning

### Loop claim

`sort-third-loop` assumes `I >= 0` and a real fixed-semantics loop head:
`#loop(list(INPUT), Name("value"), sortThirdBody) ~> CONT`. In the current
scope, `i` is `I`, `l` is an arbitrary preserved value, `value` is `OLD`,
`result` points to heap location `HR`, and `thirds` points to `HT`. The two heap
objects contain the prebuilt prefix `ACC` and sorted sequence `SORTED`;
unrelated scope and heap mappings are framed.

The post-state reaches the same arbitrary `CONT`, increments `i` by
`vsLen(INPUT)`, makes `value` the last iterated element (or preserves `OLD` for
empty input), and changes the result list to
`sortThirdAcc(INPUT,SORTED,I,ACC)`. This exactly matches the supplied
`#loop`/`#iterNext`/`#loopStep` control path and the real submitted loop body.
It neither introduces return nor discards a continuation.

### Entry claim

`sort-third-correct` has no `requires` clause. Its precondition is the exact
initial MPY configuration: module environment 0, builtins at scope -1, empty
module map and heap, allocation counters 1 and 0, empty stack, `noRet`,
`NoExc`, and exit code 0. `INPUT` is any K `ValSeq`. The `<k>` cell loads
`sortThirdModule` and then calls `sort_third` on `list(INPUT)`.

The postcondition is not a free result or implication. It requires returned
reference `ref(2)`, a loaded closure, heap location 0 containing the every-third
slice, location 1 containing its `sortVS`, and location 2 containing exactly
`list(sortThird(INPUT))`. It also fixes `heapLoc` to 3, restores the module
scope counter and caller environment, empties the stack, and retains `NoExc`
and exit code 0.

The named module is genuinely the submitted program:

1. trusted retranslation is byte-identical to `solution.mpy`;
2. reviewer claim `pinning.k` checks that `sortThirdModule` reduces to that
   exact AST and closes with `#Top`;
3. changing only the branch divisor from 3 to 2 in `pinning-mutated.k` produces
   a genuine stuck claim whose residual displays the original divisor 3.

For a satisfiable ground substitution,
`INPUT = [5,6,3,4,8,9,2]`, the claimed location-2 result is
`[2,6,3,4,8,9,5]` under the `sortVS` contract. The trusted canonical function,
submitted function, independent oracle, and concrete K execution all produce
that list.

Evidence:

- `evidence/pinning.k`
- `evidence/stage4-kprove-pinning.log`
- `evidence/pinning-mutated.k`
- `evidence/stage5-pinning-mutation.log`
- `evidence/ground_witness.py`
- `evidence/stage4-ground-witness.log`

## 5. Rule-by-rule static soundness review

The complete source-ordered inventory is
`evidence/rule-inventory.json`, generated by
`evidence/build_rule_inventory.py`. It covers the top-level supplied
`semantics.k`, all 23 supplied helper K files, `verification.k`, and `spec.k`.
It contains 1,116 records:

- 706 rules, 235 syntax declarations, 5 evaluation contexts, 1 configuration,
  and 2 claims;
- 153 function-bearing declarations, 115 `total` entries, 25 explicit
  `symbol(...)` declarations, and 22 `no-evaluators` opaque declarations;
- 45 priority-bearing entries, 35 concrete-only entries, and 26 `owise`
  entries;
- zero `functional` declarations and zero simplification rules.

Counts overlap when one declaration or rule has multiple attributes. Every
record includes source location, normalized source, attributes, origin, and an
assessment. All 1,087 supplied-semantics records are accepted at the selected
fixed semantics level because the tree is a trusted input and the candidate
copy is recursively identical. They are not candidate proof extensions. The
actual path through that fixed semantics was separately traced construct by
construct in `evidence/used-construct-map.md`.

The used-path review checked the complete configuration and cells, strictness
and explicit evaluation contexts, left-to-right call arguments, allocation,
scope lookup and parameter binding, list-slice allocation, sort allocation,
empty-result allocation, list iteration, conditional dispatch, append heap
writes, integer `%` and `//` with positive divisor 3, return, frame pop, and
preservation of the returned heap object. The entry's locations 0, 1, and 2
match that allocation order.

The candidate contributes eight total function declarations and eleven rules:

- `sortThirdBody`, `sortThirdFunctionBody`, `sortThirdClosure`, and
  `sortThirdModule` are exact, terminating AST/value aliases. They expose the
  submitted body to fixed semantics; none intercepts a call or replaces
  execution with a summary.
- The two `thirdValue` equations have complementary guards
  `pyMod(I,3) == 0` and `=/= 0`. They are disjoint and exhaustive. At the first
  guard the selected index is `I/3`; at the second the original value is
  preserved.
- `sortThirdAcc` has disjoint empty/cons equations, consumes one input
  constructor per recursive step, advances `I` by one, and appends exactly one
  value.
- `lastLoopValue` has disjoint empty/cons equations and structurally descends.
- `sortThird` simply composes the fixed every-third slice, `sortVS`, and the
  truthful fold.

These rules have no priorities, `owise`, `concrete`, opaque symbols, or
simplification attributes. Their `total` annotations are supported by complete
constructor/guard coverage, with no disagreeing overlap. No task answer is
installed as an operational rewrite: `sortThird` appears only as a
postcondition summary, and the loop circularity connects the fixed-semantics
execution to it.

The one result-bearing opacity is in the supplied baseline:

```text
sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

The Haskell proof does not establish ordering, permutation, or length
preservation of this symbol. Indeed, the symbolic theorem is
interpretation-parametric enough that an identity interpretation of `sortVS`
would preserve proof closure while not express the natural-language sort on an
unsorted every-third slice. This is an adequacy/trust limitation, not a false
candidate rule: `sorted` is a fixed supplied builtin outside the
program-defined body, and the K postcondition honestly retains `sortVS` rather
than asserting an unproved ordering formula. The fixed LLVM leg implements
insertion sort for integer and string sequences, and the independent integer
tests found no mismatch. No universal bridge-free connection theorem was
provided, so those tests are finite evidence only.

`valSeqAt` is likewise total on an opaque sequence. Its uses are in bounds if
the external `sortVS` contract includes length preservation. That dependence is
recorded rather than silently inferred.

The other explicit supplied symbols are
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`,
`sortKeyVS`, `floorFI`, `toF`, and `ceilF`. All are unreachable from this
submitted integer-list program and neither influence control nor its
postcondition.

No candidate rule was judged unsound, so there is no unsoundness allegation
requiring a false-conclusion witness. The narrower evidence gaps are the
explicit `sortVS` contract and the prompt's unstated element-type boundary.

Evidence:

- `evidence/rule-inventory.json`
- `evidence/build_rule_inventory.py`
- `evidence/stage5-rule-inventory-build.log`
- `evidence/used-construct-map.md`

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. The reviewer-created
`evidence/spec-vacuity.k` preserves the real auxiliary loop claim but changes
the entry's result-bearing obligation to require

```text
valSeqConcat(sortThird(INPUT), vCons(0, .ValSeq))
```

at heap location 2. This is demonstrably false for the satisfying input
`[5,6,3,4,8,9,2]`: the real result has length 7, whereas the mutation demands
the same sequence plus an eighth trailing zero.

The dry run parsed and compiled the mutated specification and exited 0. The
actual proof then exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet condition:

```text
sortThirdAcc(...) #Equals
valSeqConcat(sortThirdAcc(...), vCons(0, .ValSeq))
```

The reached configuration otherwise contains `ref(2)`, the exact final heap,
empty stack, `NoExc`, and exit code 0. This is a reached false obligation, not a
parser error, missing import, timeout, unrelated crash, or unreachable
mutation.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6-vacuity-dry-run.log` (exit 0)
- `evidence/stage6-vacuity-proof.log` (expected exit 1)

## 7. Proven versus assumed accounting

### Machine-checked result

Under the fixed supplied MPY semantics, the exact translated
`sort_third` program, started in the entry claim's concrete initial
configuration on any finite K `ValSeq INPUT`, returns `ref(2)` with no
exception; location 2 contains `sortThird(INPUT)`. The proof also establishes
the exact loop fold, final loop index/value, allocation order, restored caller
state, empty stack, and unchanged exit code. The result list preserves
non-third elements and takes third-position elements from
`sortVS(buildVS(INPUT,0,vsLen(INPUT),3))`.

This is a partial-correctness result under the supplied language model. It is
not, by itself, a K theorem that `sortVS` is an ascending permutation.

### Trust ledger

1. **Supplied MPY semantics.** All 706 semantic rules, K's integer/Boolean/map/
   list hooks, heating/cooling machinery, and the K backend are the selected
   fixed-semantics trust base. Integrity is exact and the reachable route was
   statically inspected and concretely exercised. This is an acceptable
   low-level boundary for this task.
2. **`sortVS` contract.** This fixed external builtin affects the sorted slice,
   every replaced element, and the final postcondition. The symbolic proof is
   conditional on it being ascending and length-preserving. The LLVM concrete
   equations and differential evidence support integer cases, but no universal
   bridge-free K theorem establishes the Python `sorted` contract. This is the
   principal concern.
3. **Total `valSeqAt` on opaque sequences.** In-bounds safety depends on
   `sortVS` preserving the slice length. It is acceptable under that named
   contract and concerning without it.
4. **Trusted translator and source bridge.** `/reference/py2mpy.py` is a
   trusted input. Byte identity, the exact-AST K claim, its rejected body
   mutation, concrete K execution, and Python differential tests support the
   bridge. The general correctness of the translator is not proved by this K
   claim.
5. **Natural-language domain.** The prompt does not spell out element types.
   The proof's `ValSeq` is broader than Python's normal-success domain:
   heterogeneous incomparable values can produce a symbolic `sortVS` result in
   K while Python raises `TypeError`. The theorem is adequate for the
   demonstrated integer-list domain, and conditionally for other mutually
   sortable values; it should not be read as a normal-return theorem for every
   heterogeneous Python list.
6. **Other opaque/symbolic primitives.** The 24 other explicit supplied symbols
   listed in Stage 5 are imported but unreachable and have no dependent claim
   in this proof.
7. **Empirical evidence.** The 100,208 Python cases and bounded K concrete
   assertions support program/canonical agreement and the integer sorting
   bridge only on their recorded inputs. They do not replace the reachability
   proof or universally define `sortVS`.
8. **Missing generation records.** The four absent provenance files prevent an
   audit of the original generation process. Fresh source reconstruction,
   exact mount comparison, body sensitivity, and non-vacuity still make the
   submitted proof artifacts independently auditable.

Gate A (real-program soundness) passes: exact body execution is pinned, all
candidate equations are valid on their full guards, the result is constrained,
and the false mutation is rejected. Gate B (intent adequacy) passes for finite
integer lists and is conditional on the named `sortVS` contract for the
prompt's broader sortable-value reading. Gate C (trust/evidence auditability)
passes for the reconstructed artifacts, with the documented provenance and
universal-sort-bridge limitations. Those limitations warrant `CONCERNS`, but
they do not make a false result provable on the intended integer-list domain or
turn the candidate's real-program proof into an oracle shortcut.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
