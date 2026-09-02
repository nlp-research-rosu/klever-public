# Independent adversarial audit: 68-pluck

The candidate is **not a legitimate partial-correctness proof** of the
generated program. Fresh reconstruction does produce `#Top`, the Python
implementation is correct, the claim pins the submitted constructor term, and
a false-result mutation is rejected. The decisive defect is that symbolic
execution of the material enumerate/filter/min computation ends at an
unconstrained, result-bearing symbol, `minEvenArray`. The proof closes only
because `verification.k` adds the equation

```k
minEvenArray(ID, OFFSET, LENGTH)
  => specScanArray(ID, OFFSET, LENGTH, 0, 0, 0, 0)
```

which is exactly the missing correctness connection and exactly the
postcondition summary. There is no bridge-free universal theorem connecting
the submitted program's fixed `semantic.k` execution to that value. Removing
this one equation leaves the target claim stuck at the missing equality.

## 1. Input and provenance integrity

Audit infrastructure status: **intact; candidate verdict is permitted**.

`/audit-input.json` declares:

- problem `68-pluck`, condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- complete input provenance;
- the mounted paths under `container_paths`.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and the required legacy-selected-stage1
records:

- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

I also inspected the present `/generation-evidence/usage.json`,
`legacy-metrics.json`, and `legacy-run-input.json`. The absent
`runtime-metrics.json` is not required for this historical layout and is not a
defect.

The campaign block is semantically identical to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`. The campaign ID, prompt hash, image ID, K/pyk
version `7.1.293`, Kit lock/tree identifiers, and toolchain lock all match.

Every required candidate/reference/generation entry is a regular file or
directory; no symlinks were found. The generated-semantics boundary is correct:
neither `/reference/reference-semantics` nor
`/candidate/reference-semantics` exists.

The candidate prompt and translator are byte-identical to their trusted mounts:

| Artifact | Independent SHA-256 | Result |
|---|---|---|
| candidate/trusted prompt | `cd3be7d4325387ffeafdc0c15742e1e5f66dfe1e94b683910809f5c17a9c3a74` | match |
| candidate/trusted translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | match |
| trusted canonical | `17fc39e0b26a436008f9a73891ead78568d5fd2a977e52d5bf402215c699c6de` | matches launcher record |

All independently computed hashes of the run/task/result/invocation/metrics,
prompt, usage, Codex last/output, legacy records, and trace file match their
recorded leaf hashes. Using the pipeline's mounted
`pipeline_contract.sha256_tree`, the candidate digest is
`b653081c2004ca2fbda5514a469d22e434591eb46758f68fef950b2071ce44f6`,
matching both the invocation and generation result workspace hashes. The trace
tree digest is
`610c9d1797d561a54ad442eca54eca34a677c65330a368b28c2efd10395847c0`,
matching `usage.json`; its only JSONL file has the recorded leaf digest
`3770464fe9efb887b24ada55e79de0c13c7952e2009b0d817303937d7f758bef`.
The differently named aggregate fields in `audit-input.json` use a
launcher-specific, undeclared tree canonicalization; I did not compare them
using an unrelated digest algorithm.

The structured trace has 335 nonblank, valid JSON events and no malformed
line. Its sole session UUID,
`019f8961-631d-72a0-bc03-eab6305b691d`, matches the invocation and generation
result. I inspected all event kinds and the command index: the trace contains
one session start/completion, 54 tool calls and outputs, candidate edit events,
many failed construction attempts, final concrete runs, and the claimed final
`#Top`. These are generation claims only and were not reused as proof evidence.

Reproducible evidence:

- `evidence/provenance_check.sh`
- `evidence/provenance_check.log` — command exit 0

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of non-negative integers, return
`[smallest_even_value, first_index_of_that_value]`. Return `[]` if the list is
empty or contains no even value. Equal minimum values are resolved by the
smallest index. The prompt explicitly includes the empty case and states a
maximum list length of 10,000.

The trusted canonical filters even values, takes their minimum, then uses
`arr.index` to select the first occurrence.

### Submitted implementation

`solution.py` constructs `[value,index]` for each even element in enumeration
order and returns Python's lexicographic `min`, with `[]` as the default. Pair
ordering minimizes value first and index second, so it agrees with the
contract. It is a different but valid algorithm.

The trusted translator regenerated `solution.mpy` with exit 0. The regenerated
and submitted files are byte-identical and both hash to
`e34a42c21da1effe94a40dbff2a858b9cddfc8a37602c74ba62efcc157366b26`.

The independent differential test imports the trusted canonical and submitted
Python entry points. It covers all four documented examples; empty,
single-element, all-odd, zero, duplicate-minimum, minimum-at-end, arbitrary
large-integer, and length-10,000 boundaries; every list of length 0 through 6
over values 0 through 7; and 2,000 deterministic broader random cases. Results:

```text
exhaustive_cases=299593
random_cases=2000
total_cases=301608
mismatches=0
case_result_sha256=b5651e9ac2ffb2c0ed6b4709d95d7d5eda433c36330e5efd3cf79e6819ec405e
```

Reproducible evidence:

- `evidence/program_fidelity.sh` and `.log` — exit 0
- `evidence/differential_test.py` and `.log` — exit 0

Stage 2 result: **PASS**. This establishes the Python rewrite bridge only; it
does not establish the K semantic bridge.

## 3. Clean proof reconstruction

All candidate source artifacts needed for execution were copied to
`/tmp/audit-work/68-pluck-audit`. Candidate-built definitions and caches were
not copied or used. Both output-definition paths were confirmed absent before
building.

Concrete definition:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-audit-kompiled
```

Exit: 0. The compiler warned that `[total]` declarations for
`minEvenArray`, `headInt`, `arrayAt`, `tailInts`, and `bindParams` are
non-exhaustive. Those warnings are substantively relevant below.

Fresh `krun` executions all exited 0 and reached `.K` with the Python-expected
result:

| Input | K result |
|---|---|
| `[4,2,3]` | `[2,1]` |
| `[]` | `[]` |
| `[0]` | `[0,0]` |
| `[1]` | `[]` |
| `[4,2,2]` | `[2,1]` |
| `[8,6,4,2]` | `[2,3]` |
| `[1000000000000,3,2]` | `[2,2]` |

Proof definition:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-audit-kompiled
```

Exit: 0. `spec.k` contains exactly one positive target claim. Its independent
proof command was:

```text
kprove spec.k --definition proof-audit-kompiled --spec-module SPEC
```

Actual result:

```text
#Top
kprove exit=0
#Top check exit=0
```

Reproducible evidence:

- `evidence/rebuild_concrete.sh` and `.log`
- `evidence/concrete_execution.sh` and `.log`
- `evidence/rebuild_proof.sh` and `.log`
- `evidence/positive_proof.sh` and `.log`

Stage 3 mechanical result: **PASS**. This is verification under the submitted
theory, not validation of that theory.

## 4. Adequacy and real-program pinning

### Plain-language formal claim

The precondition selects any integer `ID` and any integer `LENGTH >= 0`, starts
with argument `VArray(ID,0,LENGTH)`, empty local environment/function
map/stack, and result `VNone`.

The postcondition requires the computation to reach `.K`, leave the
environment and stack empty, load the exact `pluck` function binding, and put

```text
specScanArray(ID,0,LENGTH,0,0,0,0)
```

in `<result>`. `specScanArray` is a left-to-right scan over the opaque
`arrayAt(ID,index)` observer, retaining the smallest even value and the first
index.

The formal domain is not narrowed by a finite bound: it allows every
nonnegative length and arbitrary integer elements, which is at least as broad
as the prompt's material domain. It does not state non-negativity of elements,
but the scan remains mathematically correct for the broader integer domain.

### Program identity

Trusted regeneration plus a mechanical K constructor claim shows that
`solutionProgram` expands to exactly the submitted `Module(FuncDef(...))`
constructor and exact function body. The pinning claim prints `#Top`; the
backend calls it trivial because the function abbreviations normalize to the
same constructor term during claim simplification. `pluckBody`,
`solutionProgram`, and `solutionFunctions` are truthful definitional
abbreviations.

A body-sensitivity mutation changed the actual term executed by the claim to a
function that always returns `[]`, while retaining the original result
obligation. It built and failed with `WarnStuckClaimState` on
`VList(.Ints) == specScanArray(...)`. A satisfying counterexample is length 1
with element 2. Thus the theorem is genuinely sensitive to the executed body;
changing only `solution.py` was not used as a proxy.

### Satisfying state and ground substitution

`ID=68`, `LENGTH=3` satisfies the entry precondition. Reviewer-authored ground
observer equations

```text
arrayAt(68,0)=4
arrayAt(68,1)=2
arrayAt(68,2)=3
```

represent `[4,2,3]`. Under the proof extension, the K result is `[2,1]`;
trusted canonical Python and submitted Python both produce `[2,1]`. This is a
concrete adequacy witness, not a universal theorem and not part of the
candidate proof.

### Material execution gap

The exact body is present, but its material computation is not executed on the
entry proof representation. Under freshly built `semantic.k` alone:

```text
krun solution.mpy --definition concrete-audit-kompiled \
  -cARGS=VArray(68,0,3)
```

exits 113 and stops visibly at:

```text
minEvenArray ( 68 , 0 , 3 )
```

The `VArray` path has syntactically skipped enumerate lookup, iteration,
filter evaluation, pair construction, and `min`, then produced an opaque
result. The proof-local V10 equation supplies the destination scan.

Reproducible evidence:

- `evidence/adequacy_checks.sh` and `.log`
- `evidence/body_sensitivity.sh` and `.log`
- scratch artifacts `pinning-spec.k`, `spec-body-mutation.k`, and `witness.k`

Stage 4 result: constructor identity and non-vacuous result pinning **PASS**,
but real-operation/value pinning **FAILS** because the proof does not connect
the result-bearing abstract execution to the fixed semantics.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.md` is the exhaustive inventory. It enumerates all 27
local syntax declarations, the six-cell configuration, every function/total
declaration, every opaque symbol, all three priority rules, all 70 rules in
`semantic.k`, all 13 rules in `verification.k`, the sole claim, and the mapping
from every constructor used by `solution.mpy` to its rules. It records a
decision for every inventoried rule.

### Rules that are sound on the submitted concrete path

The transparent `minEvenInts`/`chooseEven` recursion is mathematically correct
for concrete finite integer lists:

- it descends structurally;
- odd values are ignored;
- the first even value initializes the result;
- a strictly smaller later value replaces it;
- equality retains the earlier index.

The scan functions V01-V09 in `verification.k` implement the same correct
mathematical scan for a nonnegative length. Their guards are disjoint and
exhaustive on reachable states. Module loading, argument binding, the call
frame, explicit return, result update, and all affected target cells are
consistent on the exact submitted path. The exact body uses no heap,
allocation, exception, I/O, or mutable external state.

Priority overlaps are understood:

- the direct empty-list comparisons preempt the generic comparison rules;
- the specialized `min(...,default=[])` rule preempts the generic named-call
  rule;
- two duplicate value/list argument cases overlap with identical RHSs;
- the two list-empty equality rules overlap at `[] == []` with identical
  results.

There are no local simplification axioms, derived lemmas, helper claims, or
loop circularities to audit.

### Material result-bearing oracle

The executed symbolic path is:

```text
exact ListComp on VArray
  -> VCandidatesArray(ID,OFFSET,LENGTH)          (S47)
  -> minEvenArray(ID,OFFSET,LENGTH)              (S50)
  -> specScanArray(ID,OFFSET,LENGTH,0,0,0,0)     (V10)
```

S47 is an operational bridge over arbitrary continuations and without a
`<funs>` binding guard. S50 introduces the fresh result-bearing abstraction.
V10 both defines that abstraction and makes it exactly the final summary. No
candidate artifact proves, without V10, that fixed execution produces that
value. The same proof-local symbol is on the execution path and at the
postcondition connection, which is circular under the required Kit
result-bearing-abstraction procedure.

The bridge-free removal experiment retained the exact semantics, body,
specification scan functions, and entry claim, removing only V10. Compilation
exited 0, but proof exited 1 with:

```text
minEvenArray(ID,0,LENGTH)
  #Equals
specScanArray(ID,0,LENGTH,0,0,0,0)
```

as the unmet obligation. Therefore every successful positive proof depends on
V10, and V10 is not a derived lemma—it is the missing target theorem asserted
as an equation.

I do not claim that V10's RHS is numerically false; for the intended algorithm
it is the desired answer. The defect is that the candidate theory has not
established that this is the value of the program-derived abstraction. The
required opposite-interpretation witness is concrete: a ground completion
admitted by `semantic.k` assigns
`minEvenArray(69,0,1) = []` and `arrayAt(69,0)=2`. It builds and runs the real
submitted constructor body to `[]`, while trusted and submitted Python both
return `[2,0]`. This witnesses that fixed `semantic.k` leaves the value
unconstrained; choosing the desired completion in V10 is an assumption.

### Complete-context false-behavior witness

S46/S47 also omit the binding of textual `enumerate`. A trusted-translated
witness module defines an `enumerate` function returning `[]` and uses the
same `pluck` expression. On intended input `[2]`, Python returns `[]`; the
fresh K semantics returns `[2,0]` because S46 preempts binding and execution.
This is a concrete false conclusion over the operational bridge's full match
domain. The submitted target happens not to shadow `enumerate`, but rule
priority does not supply the missing context containment theorem.

Other over-broad declarations are catalogued but are not used to inflate the
verdict: for example, the abstract `[1:]` rule maps represented empty length 0
to -1 (symbolic witness `VArray(ID,0,0)`), and index/head/parameter functions
omit off-path bounds or arity behavior. Minimal generated-semantics coverage
for unused constructs would be acceptable; the fatal rules are S47, S50, and
V10 on the actual positive proof path.

Reproducible evidence:

- `evidence/rule_inventory.md`
- `evidence/bridge_audit.sh` and `.log`
- `evidence/operational_context_witness.sh` and `.log`
- scratch `verification-no-bridge.k`, `spec-no-bridge.k`,
  `opposite-interpretation.k`, and `shadow-enumerate.py`

Stage 5 result: **FAIL**. The proof relies on an unjustified
program-derived, result-bearing abstraction and a proof-local answer equation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or trusted. I created a fresh
`SPEC-VACUITY` claim that preserves the exact submitted program and
precondition but requires the final result to be `[]` for every input.
`LENGTH=1` with `arrayAt(ID,0)=2` is a satisfying counterexample: the correct
result is `[2,0]`.

The dry run/build command exited 0:

```text
kprove spec-vacuity.k --definition proof-audit-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

The actual proof command exited 1 and reported `WarnStuckClaimState`, with the
expected unmet equality:

```text
VList(.Ints)
  #Equals
specScanArray(ID,0,LENGTH,0,0,0,0)
```

This is a meaningful result-obligation failure, not a parser failure, missing
import, timeout, or unrelated crash.

Reproducible evidence:

- `evidence/non_vacuity.sh` and `.log`
- scratch `spec-vacuity.k`

Stage 6 result: **PASS**. The claim discriminates a false final result. This
does not validate how the accepted result summary was obtained.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the combined `VERIFICATION` theory, and for `LENGTH >= 0`, the exact
submitted constructor term loads and calls `pluck` on the abstract
`VArray(ID,0,LENGTH)` representation. Its specialized symbolic execution
produces `minEvenArray(ID,0,LENGTH)`. Because the theory includes V10, that
term rewrites to `specScanArray(ID,0,LENGTH,0,0,0,0)`, satisfying the
postcondition. The result, function map, environment, stack, and terminal
control are constrained, and a false result does not prove.

That statement is a reachability result under an extended theory. It does not
prove that fixed generated semantics, or Python execution, computes the scan
on arbitrary inputs.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 toolchain and imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, `K-EQUAL` modules | arithmetic, equality, maps/lists, proof execution | Normal low-level trusted base. |
| Trusted `py2mpy.py` | program constructor identity | Acceptable; byte regeneration and constructor comparison succeeded. |
| Trusted canonical Python | source-intent oracle for tests | Acceptable finite evidence only, never a K proof substitute. |
| Mathematical integers instead of bounded machine integers | values, modulo, ordering | Adequate for Python integers on the stated nonnegative domain. |
| `VArray(ID,OFFSET,LENGTH)` plus opaque `arrayAt` | represents all symbolic input elements and affects every result branch | An informal, parametric input-representation bridge. It can be a reasonable abstract observer, but no machine-checked `VList`/Python-list representation theorem is supplied. This would be a concern, not the decisive failure, if execution were connected parametrically. |
| S46 concrete comprehension summary plus S03-S08 | concrete enumerate/filter/min result | Transparent recursive equations are mathematically correct and finite tests support them, but no bridge-free universal connection theorem covers the shortcut's complete binding/context domain. |
| S47/S50 `VArray -> VCandidatesArray -> minEvenArray` | skips all material built-in computation and determines the final result | Program-derived opaque abstraction on the target proof path; unacceptable without a universal connection theorem. |
| V10 `minEvenArray -> specScanArray` | fixes every returned value and is the sole positive-proof closure step | Illegitimate answer equation. It is the desired correctness theorem asserted as a proof rule and has no independent justification. |
| V01-V09 scan equations | mathematical meaning of desired result | Truthful, guarded, descending equations on the entry domain, but they specify the answer; they do not connect that answer to execution without V10. |
| Differential and concrete testing | Python rewrite and finitely many K ground cases | Strong empirical support only. It cannot establish the missing universal operational/value connection. |

Gate accounting:

- Kit Gate A (real-program soundness): **FAIL** — result-bearing abstraction
  and operational bridge lack a bridge-free universal connection; opposite
  interpretation is admitted.
- Kit Gate B (intent adequacy): the postcondition scan matches the source
  contract and does not narrow its material domain, but this cannot rescue
  Gate A.
- Kit Gate C (trust/evidence): evidence is reproducible, but the central
  program-derived assumption is illegitimate rather than merely thin.

### Decision

The successful reconstruction, correct Python implementation, constructor
pinning, body sensitivity, and non-vacuity are all genuine. Nevertheless, the
candidate does not prove that the real material computation has the claimed
value. It assumes that connection through V10. Under the benchmark decision
boundary, a proof that replaces a property-bearing computation with an
unconnected result abstraction and encodes the answer in a proof rule is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
