# Independent adversarial audit: HumanEval 34 `unique`

This is a completed seven-stage audit of the immutable candidate in
`/candidate`. I treated candidate prose, logs, caches, and generation traces
only as untrusted claims. All executable reconstruction was performed from
source in `/tmp/audit-work/reconstruction`; reviewer-authored artifacts and
bounded command logs are preserved in [`evidence/`](evidence/).

The candidate has a genuine, non-vacuous K proof of a characterization under
the supplied MPY theory, and it pins the submitted body. It is nevertheless not
a legitimate proof of the full Python contract. The formal claim is
unrestricted over `ValSeq`, but the used membership semantics substitutes K
constructor equality for Python equality. The satisfying Python input
`[1, True]` is a concrete counterexample: Python deduplicates it to `[1]`,
whereas the K membership fold treats `1` and `true` as distinct. The proof-side
untyped `sorted` rule then hides the resulting value behind an unguarded opaque
`sortVS`. This is a material real-program/domain gap, not merely thin testing.

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, problem `34-unique`, condition `semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as required for that mode.
There is no mode/mount contradiction.

I read the complete launcher input and campaign lock, then the required
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete structured
trace. The audit streamed all 17,432 transcript lines and all 396 JSONL trace
records. The records are untrusted history and were not used as proof.

The campaign object in `/audit-input.json` exactly equals
`/audit-campaign-lock.json`. All launcher-recorded regular-file SHA-256 values
recomputed exactly. Independent manifest-tree hashes match the stage-one
workspace hash, the supplied-semantics manifest hash, and the trace hash
recorded by `usage.json`. The launcher also records supervisor-side tree
attestations whose implementation is not mounted; those values were read and
recorded, while mount integrity was independently established using two
deterministic tree digests and recursive entry comparison.

The candidate prompt and translator are byte-identical to their trusted
versions. Candidate and trusted `reference-semantics/` have exactly the same
relative directories/files, types, and bytes, with no missing, additional,
changed, or symlinked entries. Evidence:

- [`40-provenance-audit-authoritative.log`](evidence/40-provenance-audit-authoritative.log)
- [`provenance_audit.py`](evidence/provenance_audit.py)
- [`03-mounted-inventory.log`](evidence/03-mounted-inventory.log)
- [`04-generation-records.log`](evidence/04-generation-records.log)
- [`41-optional-records-and-output-hashes.log`](evidence/41-optional-records-and-output-hashes.log)

All required candidate proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`) are present as regular files.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS for the ordinary sortable/hashable domain; one non-decisive
extension is recorded below.

The trusted prompt says: given a list, return its unique elements in sorted
order. The trusted canonical implementation is
`sorted(list(set(l)))`. The candidate constructs a first-occurrence
accumulator using Python `not in` and `append`, then returns
`sorted(result)`. This is a different but equivalent algorithm for ordinary
hashable, mutually sortable values.

Running the trusted translator on the copied `solution.py` produced a
byte-identical `solution.mpy`:

```text
solution.mpy             f127bbe2851b4c49afff06bb7e96bd30c6d76455c05617f66d0d687c73242411
solution.regenerated.mpy f127bbe2851b4c49afff06bb7e96bd30c6d76455c05617f66d0d687c73242411
```

See [`14-translation-fidelity.log`](evidence/14-translation-fidelity.log).

The independent differential test imports `/reference/canonical.py` and
`/candidate/solution.py` separately. It covers the documented example,
empty/singleton cases, all-duplicate and all-distinct cases, alternating
membership branches, very large integers, every integer list of length 0
through 6 over `{-2,-1,0,1,2}`, 1,000 deterministic random integer lists, and
representative bool/int, finite-float, string, and tuple lists. Result: 20,543
primary cases, zero mismatches. See
[`differential_test.py`](evidence/differential_test.py) and
[`15-differential-test.log`](evidence/15-differential-test.log).

For unhashable nested lists, the canonical raises `TypeError` while the
candidate can return a value. This is an observable extension but is not the
decisive proof failure: the canonical itself excludes such inputs
operationally. The decisive witness below uses only hashable, sortable
`int`/`bool` values and both Python implementations terminate normally.

## 3. Clean proof reconstruction

Status: PASS as verification under the supplied theory.

K 7.1.293 was available independently (`kup` was absent but the installed
toolchain ran). I copied only source artifacts and the trusted supplied
semantics into scratch. I did not copy or reuse any candidate kompiled
definition or cache.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. The independently authored six-case MPY assertion program then reached
`.K` with `NoExc` and exit code 0. Evidence:
[`18-kompile-llvm.log`](evidence/18-kompile-llvm.log),
[`concrete_reconstruction.py`](evidence/concrete_reconstruction.py), and
[`19-krun-concrete.log`](evidence/19-krun-concrete.log).

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module UNIQUE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit 0. The complete positive target command:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module UNIQUE-SPEC
```

printed `#Top` and exited 0. The membership claim also closed alone, and the
loop claim closed with its membership dependency selected. The entry claim
closed in the complete dependency set. Evidence:
[`20-kompile-proof.log`](evidence/20-kompile-proof.log),
[`22-kprove-all.log`](evidence/22-kprove-all.log),
[`23-kprove-member-summary.log`](evidence/23-kprove-member-summary.log), and
[`24-kprove-member-and-loop.log`](evidence/24-kprove-member-and-loop.log).

Thus the candidate's historical `#Top` was reproducible, but this establishes
closure only under the supplied and proof-local theory.

## 4. Adequacy and real-program pinning

Status: program pinning PASS; full-contract adequacy FAIL.

The claims mean:

1. `member-summary`: from
   `#memberAcc(V, list(VS)) ~> CONT`, fixed execution reaches
   `memberVS(V, VS) ~> CONT`. It preserves the arbitrary continuation.
2. `unique-loop`: from a loop head over `INPUT`, with local `result` pointing
   to accumulator `ACC` and `item` initially `OLD`, execution returns to
   `CONT`; the accumulator becomes `uniqueAcc(INPUT, ACC)` and `item` becomes
   `lastItem(INPUT, OLD)`. All omitted configuration cells are framed.
3. `unique-correct`: from the fresh module configuration, load the `unique`
   definition and call it on an arbitrary `list(INPUT)`. At normal completion,
   heap location 0 is the first-occurrence accumulator
   `uniqueAcc(INPUT,.ValSeq)`, heap location 1 is
   `sortVS(uniqueAcc(INPUT,.ValSeq))`, and `answer` points to location 1.

All preconditions are satisfiable. Examples are:

- membership: `V=1`, `VS=vCons(1,.ValSeq)`, `CONT=.K`;
- loop: `INPUT=.ValSeq`, `ACC=.ValSeq`, `OLD=0`, with a matching local scope,
  heap reference, and `CONT=.K`;
- entry: `INPUT=[2,1,2,3,1]` in the exact initial configuration.

The last witness was machine-checked with an explicit expected accumulator
`[2,1,3]` and answer `[1,2,3]`; both trusted canonical and candidate Python
returned `[1,2,3]`. See
[`ground-witness-spec.k`](evidence/ground-witness-spec.k) and
[`27-ground-witness.log`](evidence/27-ground-witness.log).

The entry claim does execute the actual submitted program body. A mechanical
KAST comparison extracted the translated `FuncDef` body, expanded
`uniqueBody` and `uniqueLoopBody` from their defining rules, normalized only
the surface spellings of empty associative lists, and found constructor
identity. It also confirmed that the claim installs the `unique` binding and
calls it on the symbolic list. See
[`pinning_check.py`](evidence/pinning_check.py) and
[`26-pinning-check-final.log`](evidence/26-pinning-check-final.log).

Body sensitivity is positive. A separate definition changed the body actually
installed by the claim from `Return(sorted(result))` to `Return(result)`.
The unchanged ground result claim then failed with `WarnStuckClaimState`; its
residual visibly contains the mutated closure, `answer -> ref(0)`, only one
allocation, and the unsorted `[2,1,3]` accumulator. See
[`verification-body-mutation.k`](evidence/verification-body-mutation.k),
[`ground-body-mutation-spec.k`](evidence/ground-body-mutation-spec.k), and
[`30-body-mutation-kprove.log`](evidence/30-body-mutation-kprove.log).

The adequacy failure is domain/material semantics, not substituted code. The
prompt's annotation is the unparameterized `list`, and the formal claim adds no
element restriction. Python's equality makes `1 == True`, so both Python
implementations return `[1]` for `[1, True]`. The K theorem instead
characterizes membership using constructor equality, which regards `1` and
`true` as distinct. This witness lies inside the claim's precondition and uses
values for which real Python terminates normally.

## 5. Rule-by-rule static soundness review

Status: FAIL for real-Python soundness.

The complete lexical inventory is
[`35-rule-inventory-final.tsv`](evidence/35-rule-inventory-final.tsv), generated
by [`k_inventory.py`](evidence/k_inventory.py). It enumerates 948 outer
sentences with stable source/line IDs, attributes, theorem-slice classification,
assessment, and normalized text:

```text
233 syntax declarations
  1 configuration
  5 contexts
706 rules
  3 claims
```

It includes all supplied `semantics.k` helper files, `verification.k`, and
`spec.k`; there are no other generated helper K files. The inventory includes
all 151 function declarations, 113 `total` declarations, 22
`no-evaluators` declarations, 29 priority rules, 32 concrete rules, 26
`owise` rules, and both simplification rules. Counts by file and the inventory
digest are in
[`36-rule-inventory-final-summary.log`](evidence/36-rule-inventory-final-summary.log).

### Material fixed-semantics path

Every constructor used by `solution.mpy` is declared in `semantics/syntax.k`.
The executed rule path is:

```text
Module/#loadAll and statement sequencing
  -> FuncDef and closure binding
  -> Assign/ListExpr/#alloc
  -> For/#loop/list #iterNext
  -> target binding
  -> If/truthy
  -> Compare "not in"/#memberAcc
  -> bound append/in-place heap update
  -> Return/frame pop
  -> Name("sorted") lookup/call
  -> fresh allocation containing sortVS
  -> answer assignment
```

The relevant declarations and rules in `syntax.k`, `core.k`, `functions.k`,
`controls.k`, `call.k`, `iter.k`, `list.k`, `operators.k`, `bool.k`,
`builtins.k`, and `sort.k` were checked for evaluation order, binding, frame
control, allocation, heap writes, and continuation behavior. Strictness and the
explicit argument loop give left-to-right evaluation. `append` mutates the
correct referenced heap object. Return records the value, pops exactly one
frame, restores the caller environment, and preserves escaped list heap
objects. The `sorted` call allocates a distinct result object. Rules outside
this head-symbol/control slice were checked for import/head interference and
are marked individually in the inventory as not influencing this theorem.

### Proof-local inventory

`verification.k` adds six functions and eleven equations:

| Extension | Equations | Assessment |
|---|---:|---|
| `memberVS` | 3 | Empty/head-equal/head-distinct cases are exhaustive; guards are disjoint under K equality; tail recursion descends. |
| `addUnique` | 2 | Complementary membership guards; append uses the fixed `valSeqConcat`. |
| `uniqueAcc` | 2 | Empty/cons cases; recursion strictly descends on the input. |
| `lastItem` | 2 | Empty/cons cases; recursion strictly descends. |
| `uniqueLoopBody` | 1 | Definitional alias for the exact translated loop body. |
| `uniqueBody` | 1 | Definitional alias for the exact translated function body. |

The two `[simplification]` equations are truthful on their complete K guards.
There are no proof-local operational bridge rules, opaque values, priority
rules, or unguarded answer axioms. The three reachability claims are target or
auxiliary theorems, not silently added semantic rewrites. The loop auxiliary
preserves its arbitrary continuation and frames all unmentioned cells.

### Concrete false-conclusion witness

The material unsoundness relative to real Python is in
`semantics/list.k:63-66`. These rules decide membership by `E ==K V`.
For `E=1` and `V=true`, K constructor equality is false, so the fold reaches
the conclusion that `True` is not in `[1]`. Python's conclusion is the
opposite because `True == 1`.

The reviewer-authored witness contains:

```python
assert True in [1]
assert not (1 not in [True])
```

Python exits 0. The freshly compiled K execution follows the challenged rules,
sets `AssertionError`, and exits 1. This is the required false-conclusion
witness, not an inference from differential tests. See
[`mixed-equality-witness.py`](evidence/mixed-equality-witness.py) and
[`34-mixed-equality-witness.log`](evidence/34-mixed-equality-witness.log).

It affects the target directly. The real candidate and canonical both return
`[1]` for `unique([1, True])`, but freshly compiled concrete K cannot complete
the same translated program and stops at
`sortVS(vCons(true,.ValSeq))` after the membership mismatch. See
[`mixed-unique-witness.py`](evidence/mixed-unique-witness.py) and
[`39-mixed-unique-witness.log`](evidence/39-mixed-unique-witness.log).

### Opaque and priority review

The only result-bearing opaque symbol reached by this program is
`sortVS` (`sort.k:18`). The rule at `sort.k:36-37` maps the external Python
`sorted` builtin to a fresh list containing `sortVS(VS)`. This is reasonably
classifiable as an external trusted primitive, not program-defined code, but
its contract is not proved in K and its rule is unguarded over all `ValSeq`.
Concrete equations cover homogeneous integers and strings only. The theorem
uses the same opaque term in its postcondition, so it is conditional on
`sortVS` being the real stable ascending sort over the relevant Python domain.
Finite differential evidence supports, but cannot universally establish, that
bridge.

The other explicit `no-evaluators` symbols are unused by this program:
`sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. They cannot affect this claim's control, state, or result.

All priority rules were inventoried. On the material path they select
heap-reference dereference, mutating-method dispatch, or allocation before
generic dispatch; the selected footprints match the displaced fixed behavior.
No proof-local priority rule exists. The opaque sort limitation alone would be
a named trust-boundary concern on a properly guarded homogeneous domain. In
combination with the demonstrated unrestricted equality mismatch, it does not
rescue the present theorem.

## 6. Fresh non-vacuity test

Status: PASS.

I created a fresh spec that retains the two supporting claims but changes the
entry result at heap location 1 from
`sortVS(uniqueAcc(INPUT,.ValSeq))` to
`vCons(999,sortVS(uniqueAcc(INPUT,.ValSeq)))`. This is false for the
satisfying input `INPUT=.ValSeq`: the real returned list is empty.

`kprove --dry-run` parsed and built the mutation successfully with exit 0.
The actual proof then exited 1 with `WarnStuckClaimState`. Its residual shows
the genuine completed empty-input configuration, empty lists at heap locations
0 and 1, and the path condition `INPUT #Equals .ValSeq`; it fails solely
because that configuration cannot match the injected `[999]` result. Evidence:
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k),
[`37-vacuity-dry-run.log`](evidence/37-vacuity-dry-run.log), and
[`38-vacuity-kprove.log`](evidence/38-vacuity-kprove.log).

This establishes that the successful positive proof constrains the returned
heap value. It does not cure the real-semantics/domain mismatch.

## 7. Proven versus assumed accounting

Under the supplied K theory, the successful reachability proof establishes:

> For every finite K `ValSeq INPUT`, the exact submitted `unique` body,
> started in the claim's fresh configuration and executed to the modeled normal
> return, creates a first-occurrence accumulator according to K constructor
> membership and returns a new list denoted by
> `sortVS(uniqueAcc(INPUT,.ValSeq))`, with the stated scope, heap, stack,
> return, exception, and exit-code cells.

What is formally proved:

- the fixed K execution steps around list construction, iteration, branching,
  append mutation, call/return, and allocation;
- the `member-summary` and `unique-loop` reachability claims;
- the entry heap/control characterization in terms of `uniqueAcc` and
  `sortVS`;
- result sensitivity, demonstrated by the rejected false postcondition;
- exact body sensitivity, demonstrated by the rejected body mutation.

What is assumed or empirical:

- **Trusted translator.** The mounted translator is launcher-trusted; byte
  regeneration and KAST comparison establish source/artifact pinning, not a
  universal proof of translator correctness.
- **Supplied MPY/Python bridge.** This is an informal language-model bridge.
  It is acceptable only where its used rules match Python. The bool/int witness
  disproves it on a satisfying part of the formal and prompt domain.
- **`sortVS` contract.** This result-bearing external primitive is assumed to
  mean Python's ascending `sorted`; no bridge-free universal K theorem fixes
  its value. Its concrete equations cover homogeneous integer/string lists.
- **Unused opaque primitives.** The 21 other `no-evaluators` symbols listed in
  stage 5 are present in the supplied theory but have no dependency path to
  these claims.
- **Differential bridge.** Zero mismatches over 20,543 Python cases support
  candidate-versus-canonical equivalence on the tested scope only. They do not
  validate K membership or universally define `sortVS`.
- **Concrete K evidence.** Six integer assertion cases support the used
  concrete semantics. The mixed bool/int K witnesses explicitly refute
  generalization to unrestricted `ValSeq`.

Gate A passes for proof-local soundness and non-vacuity but fails the required
real-program semantics connection on `[1, True]`. Gate B therefore fails:
restricting the result to homogeneous integer-style K equality would materially
narrow the prompt's unparameterized list domain, and the candidate claim does
not even state that restriction. Under the benchmark's decision boundary, this
cannot be downgraded to `CONCERNS / LEGIT`. Gate C evidence is reproducible,
but later evidence cannot repair the failed real-program gate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
