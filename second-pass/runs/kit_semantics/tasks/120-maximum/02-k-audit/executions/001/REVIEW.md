# Independent adversarial audit: HumanEval 120 `maximum`

## Executive finding

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I independently rebuilt the semantics
and proof from source, proved the sole positive target claim with a fresh
definition, mechanically pinned the claim's loaded constructor tree to the
trusted translation, and rejected both a loaded-body mutation and a false-result
mutation.

The finding is not an unconditional PASS because the supplied semantics makes
`sortVS` opaque during symbolic proof. The reachability theorem is sound and
result-constraining for any interpretation of that fixed primitive, but the
source-level conclusion that the value is the ascending list of the greatest
`k` integers depends on the unproved external contract that `sortVS` is an
ascending permutation. The fixed concrete rules and finite tests support that
contract; they do not constitute a universal K connection theorem. This is a
material but non-fatal trust-boundary limitation, not a substituted-program,
vacuity, or domain-narrowing defect.

## 1. Input and provenance integrity

The launcher record declares:

- `record_layout = pipeline-v3`
- `problem_id = 120-maximum`
- `condition = kit-semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `mount_reference_semantics = true`

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` exists and is a real directory. There is no
infrastructure breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required
`/generation-evidence` scalar records, `codex-last.txt`, the complete
`codex-output.log`, `prompt.txt`, and all 356 JSONL records in the structured
trace. Generation reports and the candidate's `PROOF.md` were treated only as
untrusted claims.

Independent checks in
`evidence/provenance_check.py` and
`evidence/provenance_check.log` established:

- The campaign block is structurally identical to
  `/audit-campaign-lock.json`, whose SHA-256 is the recorded
  `ad5dfc...d745`.
- Every required pipeline-v3 record is a real regular file, every required
  directory is a real directory, and the required mounts are readable.
- All recorded scalar-file hashes match.
- The independently reproduced pipeline tree digest of `/candidate` is
  `6bf4de...d8a8`, matching the stage result.
- The trace file hash is `01e63e...b27`; its independent pipeline tree digest
  is `c67c67...e495`, matching `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- The candidate and trusted supplied-semantics trees each contain exactly 25
  entries. Entry names, types, and file bytes are identical; there are no
  candidate symlinks, missing entries, additions, or type mismatches. Their
  pipeline tree digest is the recorded `4e0639...789f`.
- `solution.py`, `solution.mpy`, `verification.k`, and `spec.k` are real
  candidate proof files. Candidate-provided kompiled directories were not
  copied or used.

The bounded rendering of the complete structured trace is preserved in
`evidence/generation-trace-summary.log`; its renderer is
`evidence/summarize_generation_trace.py`.

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `prompt.py` and `canonical.py`, `maximum(arr, k)` must return an
ascending list containing the greatest `k` members of `arr`, with multiplicity.
The intended domain is:

- `arr` is a list of integers;
- `1 <= len(arr) <= 1000`;
- every element is between `-1000` and `1000`;
- `0 <= k <= len(arr)`.

The prose calls `k` positive, but the explicit numbered constraint includes
zero. I therefore included `k = 0`.

The trusted canonical implementation returns `[]` when `k == 0`; otherwise it
sorts the argument in place and returns `arr[-k:]`. The candidate is:

```python
def maximum(arr, k):
    return sorted(arr)[len(arr) - k:]
```

For every valid `k`, this expression has the same return value: for `k = 0`,
the lower bound is `len(arr)`; for positive `k`, it selects the final `k`
members of the ascending copy.

### Trusted regeneration

The command recorded in `evidence/translation_identity.log` was:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-source/solution.py > /tmp/audit-work/candidate-source/solution.regenerated.mpy
cmp -s /tmp/audit-work/candidate-source/solution.regenerated.mpy /tmp/audit-work/candidate-source/solution.mpy
```

Both commands exited `0`. The submitted and regenerated MPY files are
byte-identical with SHA-256
`9940ac33863a39ff689beea3a0e5b38b93312bac216254cb9a2dbd667385b021`.

### Independent differential

`evidence/differential_test.py` imports the trusted canonical and generated
entry points independently. Its third oracle selects with `heapq.nlargest` and
then sorts the selection, rather than importing candidate equations. The full
deterministic inputs are in `evidence/differential_inputs.json`.

The 185 cases comprise the three examples, `[1,2], k=1`, the requested empty
case (explicitly marked outside the length contract), singleton and duplicate
cases, `k` boundaries `0`, `1`, `len-1`, and `len`, both element limits,
four length-1000 boundary cases, and generated arrays at lengths
`1,2,3,4,7,16,50,127` with seed `1202026`. The run exited `0` with zero
canonical/generated/oracle result mismatches; see
`evidence/differential_test.log`.

The canonical code performs `arr.sort()` for every `k > 0`; observable argument
content changed in 130 recorded cases. The generated implementation never
mutated its argument. The HumanEval contract constrains the returned list and
does not require the canonical implementation's incidental mutation, so this
is an implementation difference, not a contract failure.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/candidate-source` and
trusted inputs into `/tmp/audit-work/trusted`. No candidate-built definition,
binary, cache, or `__pycache__` was copied.

Tool versions are recorded in `evidence/toolchain.log`: K `v7.1.293` and Python
`3.10.12`.

The fresh commands were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled

kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
```

Both `kompile` commands exited `0`; logs are
`evidence/kompile-runtime.log` and
`evidence/kompile-verification.log`. The candidate has exactly one positive
target claim, `SPEC.maximum-correct`. Its independent proof exited `0` and
printed exactly one line `#Top`; see `evidence/kprove-target.log`.

As a concrete source check, I translated
`evidence/concrete_harness.py` with the trusted translator and ran it using the
fresh LLVM definition. It contains all three prompt examples, `k = 0`,
singleton behavior, and a length-1000 comprehension whose top three members
are checked. `krun` exited `0`; see `evidence/concrete_execution.log`.

The compiler reported non-exhaustive functions in unrelated or deliberately
total/opaque portions of the supplied semantics (`mapStrVS`, several float
helpers, `joinCodes`, and out-of-bounds `valSeqAt`). None caused a build or
proof failure. The relevant `valSeqAt` limitation is included in the trust
accounting below.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry precondition quantifies `VS:ValSeq` and `K:Int` with:

```text
1 <= vsLen(VS) <= 1000
0 <= K <= vsLen(VS)
```

Starting with module scope `0`, the fixed builtins scope `-1`, empty heap and
stack, `noRet`, `NoExc`, and exit code `0`, the `<k>` cell first loads a module
containing `maximum` and then calls that binding with `list(VS), K`.

At the destination:

- `<k>` is `ref(1)`;
- scope `0` contains a closure with the exact submitted body;
- heap location `0` contains `list(sortVS(VS))`;
- heap location `1` contains `maximumResult(VS,K)`;
- `heapLoc` is `2`;
- the call frame is gone, the stack is empty, return state is reset, no
  exception is present, and exit code remains zero.

`maximumResult` is fully defined by the sole candidate rule:

```k
maximumResult(VS, K)
  => doSlice(
       list(sortVS(VS)),
       someB(vsLen(VS) -Int K),
       noB,
       noB)
```

Thus the returned pointee is a fixed function of the input, not a free value,
tautological destination, existential oracle, or one-way implication.

### Mechanical identity

`evidence/pinning_check.py` lexes constructors and strings, extracts the
balanced argument of `#loadAll`, and compares constructor tokens with the
trusted regeneration. Both sides contain 63 constructor tokens and have token
digest `56eab5...8f9b`; they are identical. The check also confirms one claim
and one `#loadAll`; see `evidence/pinning_check.log`.

This establishes the allowed source-to-proof bridge mechanically. There is no
omitted material operation: function loading and binding, lookup of `maximum`,
`sorted`, and `len`, argument evaluation, allocation of the sorted copy,
subtraction, default-step slicing, slice allocation, return, and frame pop all
execute under the fixed semantics.

### Satisfiable substitution

`VS = vCons(1,vCons(2,.ValSeq))` and `K = 1` satisfy every entry condition.
Substitution gives the intended result `[2]`. Both Python implementations and
the `heapq` oracle return `[2]` in `evidence/differential_test.log`.

The full fresh K execution in `evidence/ground_execution.log` terminates with
`.K`, `NoExc`, exit code `0`, and:

```text
0 |-> list([1,2])
1 |-> list([1,2])
2 |-> list([2])
```

where the extra location `0` is the program-level list literal used by this
concrete harness.

### Body sensitivity

`evidence/audit-body-mutation.k` changes the constructor term actually loaded
and bound from `len(arr)-k` to `len(arr)-k-1`, while retaining the original
result obligation. Its dry run exited `0`, proving the mutation parsed and
built. The proof then exited `1` with one reachable
`WarnStuckClaimState`; the residual closure contains the mutated body and its
heap result is `[1,2]`, not `[2]`. See
`evidence/body-mutation-dry-run.log` and
`evidence/body-mutation-proof.log`.

The formal precondition does not state that each `VS` member is an integer in
`[-1000,1000]`; it is broader, not narrower, than the source domain. MPY's
opaque sort also permits symbolic mixed `ValSeq` inputs for which CPython
sorting could raise `TypeError`. Such inputs are outside the source contract;
no intended-domain false conclusion follows.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` generated
`evidence/rule-inventory.txt` directly from all 24 supplied-semantics source
files plus `verification.k`. It contains every declaration block with source
line and full guards/attributes:

- 1,093 declaration blocks;
- 696 rules: 458 equational/concrete/owise and 238
  operational/priority/owise;
- 228 syntax declarations;
- 108 total-function declarations;
- 147 function-bearing declarations;
- 25 symbol declarations, including 22 with `no-evaluators`;
- 45 priority rules;
- 36 concrete-bearing blocks;
- 26 owise rules;
- 5 contexts and 1 configuration;
- zero `functional` declarations and zero simplification rules.

`evidence/rule_assessment.py` produced
`evidence/rule-assessment.tsv`, one disposition for every one of the 1,093
inventoried declarations. Its counts are:

- 2 accepted candidate-definition declarations;
- 132 accepted reachable fixed-semantics declarations/rules;
- 1 reachable accepted-with-trust-boundary declaration (`sortVS`);
- 24 concrete-runtime-only declarations;
- 774 reviewed declarations outside the submitted program's reachable
  constructor path;
- 160 structural module/import declarations.

For imported constructs that cannot be produced by this exact straight-line
body on integer-list inputs, I found no false conclusion witness on the
intended domain. I therefore record the narrower reachability/evidence
limitation rather than label such rules unsound.

### Used-construct map and execution audit

| Submitted construct/operation | Fixed declaration and behavior checked |
| --- | --- |
| `Module`, `FuncDef`, `Params`, `Return` | `syntax.k`; `core.k` load/sequencing; `functions.k` closure creation, parameter binding, return, pop |
| `Call`, `Name` | `call.k` callee-first and left-to-right argument evaluation; `core.k` lexical/builtin lookup |
| `sorted(arr)` | fixed builtin binding and `sort.k` exact `#applyK` allocation of `list(sortVS(VS))` |
| `len(arr)` | `builtins.k` `applyBuiltin("len",...)`, `seqLen(list)`, and `core.k` `vsLen` |
| `BinOp("-")` | `syntax.k` sequential strictness, `operators.k` dispatch, `int.k` subtraction |
| `Subscript` and `Slice(...,NoBound,NoBound)` | object-first contexts, ref dereference, lower/high/step order, `noB`, default step `1`, bounds helpers, `doSlice`, `buildVS`, and fresh allocation in `subscript.k` |
| cells/state | exact environment and scope binding; monotone heap allocation; saved continuation/frame; restored scope/stack/return/exception cells |

The generic call rule is owise and does not preempt special builtin
application. The specific sorted application preempts the generic builtin
owise dispatcher. Priority 40 dereference rules and priority 45 slice
allocation preserve the object and two fresh allocations. Guards on the
integer insertion rules (`<=` versus `>`) and default-step slice rules are
disjoint over the intended domain.

### Candidate extension

`verification.k` adds no k-cell rewrite, operational bridge, lemma, auxiliary
claim, priority, simplification, or fresh opaque symbol. It adds only:

1. `maximumResult(ValSeq,Int) [function,total]`; and
2. its one unconditional defining equation.

The equation covers the entire declared domain, terminates in one step, has no
overlap, and exactly names the term built by fixed execution. It neither
preempts execution nor encodes a different answer.

### Supplied-semantics trust boundary

The reachable declaration:

```k
syntax ValSeq ::= sortVS(ValSeq)
  [function, total, symbol(sortVS), no-evaluators]
```

is supplied, not candidate-added. In the proof backend it is a fixed,
result-bearing opaque primitive. The program genuinely calls the fixed
`sorted` builtin; the candidate does not bypass a program-defined body.
Execution and the formal postcondition are interpretation-parametric in this
primitive.

Concrete supplied rules implement insertion sort for integer sequences. Their
base/step cases descend structurally, and the insertion guards `X <= Y` and
`X > Y` are disjoint and exhaustive. Nevertheless, no bridge-free universal K
theorem in the submitted proof establishes that symbolic `sortVS(VS)` is an
ascending permutation of `VS`. Similarly, total `valSeqAt` intentionally stays
abstract for an opaque sequence or out-of-bounds access. For valid concrete
default-step slices its constructor equations are correct; symbolically, the
top-k meaning remains part of the same informal sort/slice interpretation
bridge.

This boundary cannot prove a false fixed value because the reachability claim
does not equate `sortVS` to an independently chosen answer; it constrains the
program result to the same fixed operation it executed. It does limit what can
be claimed unconditionally at the HumanEval contract level.

No candidate rule was found that encodes the requested answer, replaces a
property-bearing program computation with a fresh oracle, fabricates a used
result, or introduces inconsistent equations. No intended-domain unsound rule
witness was found.

Stage 5 result: PASS for real-program soundness, with the documented supplied
trust-boundary concern.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
`evidence/audit-false-result.k`:

- loads and executes the original submitted body;
- uses the satisfiable ground input `[1,2], k=1`;
- keeps binding, control, heap locations, and all other destination cells
  meaningful;
- changes only heap location `1` from the real `[2]` result to an demanded
  empty list.

The exact dry-run command, in
`evidence/false-result-dry-run.log`, exited `0`, so this is not parser,
import, or build failure:

```text
kprove /audit-output/evidence/audit-false-result.k \
  -I /tmp/audit-work/candidate-source \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
```

The same command without `--dry-run` exited `1` and emitted exactly one
`WarnStuckClaimState`. The reachable residual has completed execution
(`ref(1) ~> .K`, empty stack, `NoExc`, exit code `0`) and heap location `1`
contains `list(vCons(2,.ValSeq))`. The unmet condition is precisely the
mutation's demand for `list(.ValSeq)`, not an unrelated failure. Full bounded
output is in `evidence/false-result-proof.log`.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly compiled supplied MPY theory, for all `VS:ValSeq` and
`K:Int` satisfying `1 <= vsLen(VS) <= 1000` and
`0 <= K <= vsLen(VS)`, if execution terminates from the claim's exact initial
configuration, loading and calling the exact submitted module:

- binds and executes the submitted `maximum` body;
- returns `ref(1)`;
- stores the fixed sorted-copy value at heap location `0`;
- stores
  `doSlice(list(sortVS(VS)),someB(vsLen(VS)-K),noB,noB)` at location `1`;
- restores call control state;
- raises no modeled exception and leaves exit code zero.

This is partial correctness. The reachability proof does not itself prove
termination.

### Trusted or informal boundaries

| Boundary | Dependents | Assessment |
| --- | --- | --- |
| K `v7.1.293`, its Haskell prover, LLVM runtime, and hooked integer/map/list theories | compilation, symbolic closure, concrete runs | Normal low-level proof-tool trust; version recorded |
| Trusted supplied MPY semantics | every operational step and state cell | Integrity independently established; it is an intentionally partial Python model |
| `sortVS` means ascending permutation for integer lists | inference from the formal returned term to “greatest `k` integers, ascending” | Material external contract; acceptable for legitimacy because fixed and outside program-defined code, but the principal reason for CONCERNS |
| Total/abstract `valSeqAt` on opaque or invalid sequences | symbolic slice normalization | Valid intended slices are supported by concrete equations; invalid/mixed cases remain outside the source domain |
| Trusted translator | Python-to-constructor identity | Byte identity proved for this source; translator correctness itself is trusted |
| Trusted canonical and `heapq` oracle | finite program-fidelity evidence | 185 finite cases, not a universal theorem |
| Concrete K harness and ground run | finite semantics/Python bridge evidence | Examples, `k=0`, singleton, length 1000, and ground `[1,2]`; supportive, not universal |
| Ordinary mathematical argument that the suffix of an ascending permutation contains the greatest `k` values | HumanEval intent bridge | Straightforward but informal in this artifact |

The candidate's `PROOF.md`, prior `#Top`, traces, and candidate tests were not
used as proof of any item above.

### Decision

The proof closes independently, is non-vacuous, is sensitive to the actual
loaded body, constrains the result, covers the full material source-contract
domain, and pins the trusted regeneration of the real generated program. The
opaque supplied sort contract prevents an unconditional claim that K itself
proved the mathematical top-k interpretation. Under the benchmark decision
boundary, that is a legitimate proof with a documented non-fatal trust
limitation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
