# Independent adversarial review: 29-filter-by-prefix

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed every proof layer from source, checked the program term
against trusted regeneration, reviewed every local proof extension, found exact
connection theorems for both operational bridges, and confirmed non-vacuity with
a fresh false result claim.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as required for this mode.
`writing-semantics` was therefore neither applicable nor used.

I checked all launcher-required pipeline-v3 records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
  and `prompt.txt`; and
- the one 664-record JSONL trace under
  `/generation-evidence/codex-trace/2026/07/24/`.

Every required path was readable and of the required regular-file or real
directory type. No symlink or unsupported entry was found in the candidate,
trusted input, or generation-evidence trees. The campaign-lock JSON object
equals the `audit_campaign` block exactly, and its SHA-256 is the recorded
`ad5dfc...d745`. All recorded hashes for the required individual files,
including the trace JSONL, match.

Using the installed pipeline-v3 tree-hash implementation, I also reproduced:

- candidate workspace: `f8a929...c04b6`, matching
  `generation-result.json.outputs.workspace_sha256`;
- candidate and trusted semantics manifests: both
  `4e0639...3789f`;
- generation trace tree: `b3ae09...79cfc8`, matching
  `usage.json.source_trace_sha256`.

The audit input additionally carries launcher content-digest fields such as
`candidate_tree_sha256` and `trusted_reference_semantics_sha256`, distinct from
the pipeline manifest-tree scheme. I did not rely on those opaque aggregate
values alone: the authoritative pipeline tree hashes above were reproduced,
and every candidate semantics path was compared recursively by relative path,
entry type, and bytes.

The recursive supplied-semantics comparison found the same 24 regular files on
both sides, no additions, omissions, mistypings, or symlinks, and zero byte
differences. Candidate `prompt.py` and `py2mpy.py` are also byte-identical to
their trusted mounts. Thus the fixed semantics are intact; this integrity result
does not bless the candidate's proof-specific K rules.

I parsed all 664 structured trace records and inventoried 77 recorded shell
commands, 44 assistant messages, and 90 function outputs. The generation log,
trace, final message, and candidate `PROOF.md` were treated only as untrusted
claims and were not used as proof success evidence.

Evidence:

- [01_integrity.sh](/audit-output/evidence/01_integrity.sh) and
  [01_integrity.log](/audit-output/evidence/01_integrity.log)
- [01b_manifest_tree_hashes.py](/audit-output/evidence/01b_manifest_tree_hashes.py)
  and [01b_tree_hashes.log](/audit-output/evidence/01b_tree_hashes.log)
- [01_trace_inventory.py](/audit-output/evidence/01_trace_inventory.py) and
  [01_trace_inventory.log](/audit-output/evidence/01_trace_inventory.log)

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a list of strings and a string prefix, return
exactly those input strings that start with the prefix. Order and duplicates
are preserved. The examples require `[]` for an empty input and
`["abc", "array"]` for the documented mixed input with prefix `"a"`.

The trusted canonical implementation is the corresponding list comprehension.
The submitted implementation initializes a fresh result list, iterates over the
input, conditionally appends on `string.startswith(prefix)`, and returns the
result. Its extra initialization `string = ""` is semantically inert.

I ran the trusted translator from `/reference/py2mpy.py` against the scratch
copy of `solution.py`. The regenerated and submitted `solution.mpy` files are
byte-identical; both have SHA-256
`1c4b746359e3db4ea54a2e3c9dd703b9a4bc4f1b75b0b6c0af45d832931f9502`.

My independent differential harness imports the trusted canonical and generated
entry points without using candidate tests. It covers the documented examples,
empty list and prefix, empty-string elements, prefix equal to/one shorter
than/longer than the string, both branch outcomes, duplicates and order,
Unicode including supplementary-plane characters, NUL/newline characters,
an exhaustive small corpus through list length three, and 2,500 deterministic
generated cases. All 5,311 comparisons agreed. The result log digest is
`497852...3452`; mismatches were zero.

Evidence:

- [02_differential.py](/audit-output/evidence/02_differential.py)
- [02_program_fidelity.log](/audit-output/evidence/02_program_fidelity.log)
- [regenerated-solution.mpy](/audit-output/evidence/regenerated-solution.mpy)

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/work` and copied the trusted
reference semantics from `/reference`, not candidate compiled output. The
initial scratch definition/cache scan was empty. The independently observed
tool version was K 7.1.293.

Fresh concrete reconstruction:

1. The trusted semantics compiled with LLVM using `MPY-KRUN` and `MPY-SYNTAX`;
   build exit was 0.
2. My first concrete test program intentionally included an astral Unicode
   source literal. K rejected the translator's surrogate escapes. A BMP literal
   then reached the documented `strToCodes` ASCII-only guard and stuck. These
   are fixed-semantics source-literal limitations, not failures of the submitted
   ASCII-only program or its symbolic input domain.
3. The final independent concrete program uses the submitted function and
   ASCII normal/boundary cases. It executes to `.K`, `NoExc`, and exit code 0.
   A separate symbolic ground witness below proves that semantic input strings
   containing code points 128512 and 945 are in the theorem domain.

Fresh Haskell reconstruction and positive claims:

| Definition/claim | Result |
|---|---|
| `domain.k` → `auditor-connection-kompiled` | build exit 0 |
| `CONNECTION-SPEC.string-iterator-normalization` | `#Top`, exit 0 |
| `verification-core.k` → `auditor-loop-connection-kompiled` | build exit 0 |
| `LOOP-CONNECTION-SPEC.filter-loop-connection` | `#Top`, exit 0 |
| `verification.k` → `auditor-verification-kompiled` | build exit 0 |
| `SPEC.filter-loop` alone | `#Top`, exit 0 |
| `SPEC.filter-program` alone | `#Top`, exit 0 |
| all claims in `SPEC` together | `#Top`, exit 0 |

The first reconstruction script has overall exit 1 solely because it records
the deliberately broader Unicode concrete attempt before continuing through
all successful symbolic builds and claims. The successful corrected concrete
run is separately preserved. No candidate cache or compiled definition was
used.

Evidence:

- [03_rebuild_and_prove.sh](/audit-output/evidence/03_rebuild_and_prove.sh)
  and [03_rebuild_and_prove.log](/audit-output/evidence/03_rebuild_and_prove.log)
- [auditor-concrete.py](/audit-output/evidence/auditor-concrete.py) and
  [03c_concrete_ascii.log](/audit-output/evidence/03c_concrete_ascii.log)
- The broader-input diagnostics are preserved in
  [03b_concrete_bmp.log](/audit-output/evidence/03b_concrete_bmp.log).

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.filter-loop` assumes that the remaining semantic list contains only
strings. It starts at the real loop head with the real conditional body, exact
`return result; #endcall` continuation, callee locals, result heap reference,
single call frame, `noRet`, and `NoExc`. It states that the loop appends exactly
the remaining elements that satisfy the prefix predicate, returns the existing
result reference, deletes the callee scope, restores environment/scope location,
and pops the frame.

`SPEC.filter-program` starts in the initial configuration, loads the submitted
module, and calls `filter_by_prefix(list(INPUT), str(PREFIX))`. Its only
precondition is `allStrings(INPUT)`; `PREFIX` is any `IntSeq` and is
syntactically wrapped as a semantic string. It states that execution returns
fresh `ref(0)` and heap location 0 contains
`filterPrefixAcc(.ValSeq, INPUT, PREFIX)`, with the exact closure binding,
allocation counter, empty stack, `noRet`, and `NoExc`.

This is the full typed HumanEval domain: arbitrary finite lists of semantic
strings and arbitrary semantic string prefixes. It has no list-length, string-
length, character-range, or example-only bound. Non-string elements and
non-string prefixes are excluded exactly as the `List[str]`/`str` source
signature excludes them.

### Mechanical program identity

Fresh `kast` parsing of `solution.mpy` and expansion of
`filterByPrefixProgram` under the fresh final definition produced two 4,214-byte
KORE files. They are byte-identical, with common SHA-256
`8722cc...6d9b1`. Therefore the entry claim executes the same module, function
binding, parameter list, and body as trusted regeneration of the submitted
source; only closed syntax macros name subterms.

I also made a fresh body-sensitivity mutation that changes the module term and
closure-bound body actually loaded by the claim from conditional append to
unconditional append. The mutation dry-runs successfully, then its proof exits
1 with `WarnStuckClaimState`; the residual heap contains both `"abc"` and
`"bcd"` rather than the original filtered result. The loop bridge does not
capture this different body.

### Satisfiable witnesses and concrete substitution

For the whole-program claim I used
`INPUT = ["abc", "bcd", "", "array"]`, `PREFIX = "a"`. `allStrings` is true,
and the formal summary, trusted canonical, and generated Python implementation
all produce `["abc", "array"]`.

For the loop claim I used `ACC = ["seed"]`,
`INPUT = ["abc", "bcd"]`, `P = "a"` in the exact frame/heap state. Its
precondition is true and the formal post-state list is `["seed", "abc"]`.
Both independently authored ground K claims close with `#Top`.

Finally, a ground whole-program claim directly encodes code points 128512
(`😀`) and 945 (`α`) as `IntSeq`, avoiding the fixed source-literal parser. It
returns the two strings beginning with 128512 and closes with `#Top`. Thus the
ASCII literal parser does not narrow the theorem's semantic input domain.

Evidence:

- [auditor-ground-witness.k](/audit-output/evidence/auditor-ground-witness.k)
- [04_claim_witnesses.py](/audit-output/evidence/04_claim_witnesses.py) and
  [04c_claim_witnesses_pass.log](/audit-output/evidence/04c_claim_witnesses_pass.log)
- [04d_unicode_codepoint_witness.log](/audit-output/evidence/04d_unicode_codepoint_witness.log)
- [auditor-body-sensitivity.k](/audit-output/evidence/auditor-body-sensitivity.k)
  and [05b_body_sensitivity_pass.log](/audit-output/evidence/05b_body_sensitivity_pass.log)

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The complete candidate-local positive proof closure is `domain.k`,
`verification-core.k`, `verification.k`, `connection-spec.k`,
`loop-connection-spec.k`, and `spec.k`. There is no candidate `semantic.k` in
supplied-semantics mode. The following is the exhaustive local inventory.

| Location | Declaration or rule | Classification and decision |
|---|---|---|
| `domain.k:8` | `stringCodes(Val) [function,total]` | Total definitional projection. Covered by the next two disjoint equations. Sound. |
| `domain.k:9` | `stringCodes(str(S)) => S` | Constructor projection. Sound by definition. |
| `domain.k:10` | non-string `stringCodes` owise → empty | Disjoint default, used only for off-domain totalization. Sound. |
| `domain.k:12-13` | `isStringVal(V) = (V ==K str(stringCodes(V)))` | Total predicate; on free `Val` constructors it is true exactly for `str`. Sound. |
| `domain.k:15` | `allStrings(ValSeq) [function,total]` | Structural predicate. Covered by empty/cons constructors. Sound. |
| `domain.k:16` | empty sequence → true | Correct base case. |
| `domain.k:17-18` | cons → head predicate and tail recursion | Correct fold, strictly decreasing on the tail. |
| `verification-core.k:7-12` | `filterLoopBody` macro/rule | Closed syntax alias for the exact submitted `If` body. Compile-time only; constructor identity checked. |
| `verification-core.k:14-19` | `filterFunctionBody` macro/rule | Closed syntax alias for the exact assignments, loop, and return. Constructor identity checked. |
| `verification-core.k:21-28` | `filterByPrefixProgram` macro/rule | Closed syntax alias for the exact module/import/function. Constructor identity checked. |
| `verification-core.k:34-35` | `filterPrefixAcc(...)[function,total]` | Mathematical stable-filter summary. Its second argument structurally decreases and all constructors/Boolean outcomes are covered. |
| `verification-core.k:36` | empty remaining input → accumulator | Correct base equation. |
| `verification-core.k:37-48` | keep-head equation, simplification | When `startsWith(P,stringCodes(V))`, appends exactly the string head and recurs. Under `allStrings`, `V = str(stringCodes(V))`. Sound. |
| `verification-core.k:49-55` | drop-head equation, simplification | Complementary Boolean guard leaves the accumulator unchanged and recurs. Sound; no overlap with keep. |
| `verification-core.k:60-66` | priority-40 list iterator bridge | Operational bridge. Sound over its complete guard/context by the separate universal connection theorem described below. |
| `verification-core.k:70-72` | map-deletion simplification | For key 1 absent from `SC`, deleting key 1 from `(1 |-> value) SC` yields `SC`. This is the built-in finite-map deletion law; guard prevents overlap/collision. Sound. |
| `verification.k:10-43` | priority-40 loop/return/frame bridge | Operational bridge. Sound over its exact complete configuration by the separate universal loop connection theorem described below. |
| `connection-spec.k:6-15` | iterator connection claim | Auxiliary reachability theorem, not an axiom in the final definition. Closes bridge-free from fixed list iteration under exactly the bridge guard. Sound. |
| `loop-connection-spec.k:6-38` | loop connection claim | Auxiliary reachability theorem, not a loop rule in its definition. It executes the exact loop/body/return/frame path using fixed semantics plus the independently connected iterator step. Sound. |
| `spec.k:6-38` | `filter-loop` target claim | Exact connected loop summary; result and all relevant state changes are constrained. Sound. |
| `spec.k:40-71` | `filter-program` target claim | Exact real-program entry and stable-filter post-state over the full typed domain. Sound. |

There are no local opaque symbols, `[functional]` declarations, `[concrete]`
rules, unconstrained fresh result symbols, task-answer axioms, or other
candidate-local syntax/rules. The only local priorities are the two connected
operational bridges. The only local simplification rules are the two
complementary recursive summary equations and the guarded map identity.

### Operational bridge audit

The iterator bridge accepts
`#iterNext(list(vCons(V,REST)))` with an arbitrary trailing K continuation,
guarded by `isStringVal(V)`. It reads and rewrites only `<k>`; every omitted
configuration cell is framed unchanged. The fixed list rule yields `V`. The
bridge yields `str(stringCodes(V))`, and the guard is precisely their equality.
`CONNECTION-SPEC.string-iterator-normalization` quantifies the same arbitrary
`CONT:K`, imports only `domain.k` and the fixed semantics, and closes with
`#Top`. A fresh opposite-value claim asserting that iteration over `"a"` yields
the empty string dry-runs, then exits 1 with a residual containing code 97.

The loop bridge accepts an exact loop body, exact
`return result; #endcall` suffix, environment 1, exact four-local callee scope
and parent, scope location 2, accumulator heap object, arbitrary framed scope
and heap maps, arbitrary unchanged heap location, exactly one
`frame(.K,0,1)`, `noRet`, `NoExc`, and `allStrings(INPUT)`. It writes the
accumulator list, returns `ref(H)`, restores environment/scope location,
removes the callee scope, and pops the frame; it preserves heap location and
all omitted cells. `LOOP-CONNECTION-SPEC.filter-loop-connection` has the same
match and result but is compiled from `verification-core.k`, which does not
contain the loop bridge. It relies only on fixed execution, truthful structural
definitions, the map law, and the separately connected iterator bridge. It
closes with `#Top`. The actual-body mutation confirms context containment and
body sensitivity.

### Fixed-semantics path used by the program

Every submitted constructor maps to supplied syntax and operational rules:

| Program feature | Fixed declaration/rule path |
|---|---|
| `Module`, statements, load | `syntax.k:41-61`; `core.k:124-127` |
| typing import | `controls.k:35-44` (`typing` follows the no-op owise rule) |
| function definition | `functions.k:14-16` |
| calls and argument order | `call.k:20-24,69-75`; `core.k:183-191` |
| parameter binding and lookup | `functions.k:63-66`; `core.k:130-154` |
| list construction/allocation | `list.k:13-15`; `core.k:117-121` |
| assignment | `controls.k:9-18` |
| empty string literal | `str.k:13-17` |
| `for` control and target binding | `controls.k:65-75`; `tuple.k:31-41` |
| list iterator | `list.k:9-10`, with the connected guarded bridge on cons |
| `if` and Boolean guard | `controls.k:51-54`; `core.k:199-205` |
| attribute/call routing | `call.k:16,20-24` |
| `startswith` | `methods.k:61,166-169` |
| `append` state update | `list.k:53-55`; `valSeqConcat` at `list.k:18-20` |
| expression discard | `controls.k:46-48` |
| return and frame cleanup | `functions.k:77-90` |

Strict/sequence-strict syntax and the shared argument evaluator enforce the
needed evaluation order. The entry claim fixes name binding to the freshly
loaded closure. List construction is the only allocation; append mutates that
fresh heap object; return/popping and scope deletion are explicitly observed.
The supplied `startsWith` definition is a total structural prefix comparison
with the same argument order used by Python's receiver method.

The fixed semantics' `strToCodes` accepts only ASCII source literals. The
submitted source uses only `""`, so no material source operation is omitted.
Inputs in the theorem are already semantic `str(IntSeq)` values and are not
routed through this literal rule; the successful Unicode-codepoint ground claim
confirms this distinction.

No local rule was found unsound, so there is no unsoundness allegation requiring
a false-conclusion witness.

Evidence:

- [05_static_inventory.sh](/audit-output/evidence/05_static_inventory.sh) and
  [05_static_inventory.log](/audit-output/evidence/05_static_inventory.log)
- [05c_iterator_opposite.sh](/audit-output/evidence/05c_iterator_opposite.sh),
  [05c_iterator_opposite.log](/audit-output/evidence/05c_iterator_opposite.log),
  and [auditor-wrong-iterator.k](/audit-output/evidence/auditor-wrong-iterator.k)
- Body-sensitivity evidence cited in Stage 4.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I did not reuse `spec-vacuity.k`. The fresh auditor module uses the satisfiable
input `strings = ["abc","bcd"]`, `prefix = "a"` and changes the result-bearing
heap obligation from the true singleton `["abc"]` to an empty list.

`kprove --dry-run` exits 0, proving that the mutation parses and builds against
the fresh definition. The actual proof exits 1 with
`WarnStuckClaimState`. Its residual is a fully terminated configuration at
`ref(0)` whose heap contains the string code sequence
`[97,98,99]` (`"abc"`), directly exhibiting the unmet result obligation. This
is not a parser error, timeout, missing import, unreachable claim, or unrelated
backend crash.

Evidence:

- [auditor-false-result.k](/audit-output/evidence/auditor-false-result.k)
- [06_nonvacuity.sh](/audit-output/evidence/06_nonvacuity.sh)
- [06_nonvacuity.log](/audit-output/evidence/06_nonvacuity.log)
- [06_nonvacuity_dry_run.out](/audit-output/evidence/06_nonvacuity_dry_run.out)
  and [06_nonvacuity_proof.out](/audit-output/evidence/06_nonvacuity_proof.out)

Stage 6 result: PASS.

## 7. Proven-versus-assumed accounting

### What the proof establishes

Under the supplied MPY semantics, if the submitted program is called with any
finite semantic list all of whose elements are `str(IntSeq)` and any semantic
`str(IntSeq)` prefix, then whenever the execution terminates it returns a fresh
list reference whose contents are exactly the stable subsequence of input
elements whose code sequences begin with the prefix. Order and duplicates are
preserved. The proof also constrains closure installation, allocation count,
heap contents, scope cleanup, stack, return state, and exception state.

This is partial correctness. Termination is not a stated theorem, although the
structurally finite loop obviously terminates under these rules.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and built-in Int/Bool/Map/List/K equality | Executes all definitions and proofs | Standard unavoidable machine-checking trust boundary; acceptable. |
| Trusted supplied MPY semantics | Defines module load, calls, scopes, allocation, lists, strings, control, methods, and return | Required fixed baseline for this condition. Candidate copy is byte-identical; every materially used path was reviewed and freshly exercised. Acceptable. |
| Trusted translator `/reference/py2mpy.py` | Bridges submitted Python AST to `solution.mpy` | Trusted benchmark input, with independent byte regeneration and constructor-level KORE identity. Acceptable. |
| Semantic `str(IntSeq)` as the Python-string model | Connects code-sequence prefix to the human contract | Straight structural representation; over-broad in allowing arbitrary integer codes, but sound on every valid Python code-point sequence. Python Unicode differentials and the K codepoint witness support the bridge. No intended-domain narrowing. |
| `stringCodes`, `isStringVal`, `allStrings`, `filterPrefixAcc` | Local mathematical definitions | Fully defined, total where declared, terminating, non-overlapping, and reviewed above; no external oracle. |
| Iterator operational bridge | Supplies one iterated value | Universally connected to fixed semantics over its complete continuation/state domain; opposite interpretation rejected. Acceptable. |
| Loop/return/frame operational bridge | Summarizes the remaining real loop and cleanup | Universally connected without the loop bridge over the same complete configuration; body mutation rejected. Acceptable. |
| Trusted canonical and 5,311 differential cases | Supports implementation-to-contract fidelity | Finite evidence only; not treated as a substitute for the K proof. |

There is no opaque result-bearing primitive, empirical oracle, unproved
program-defined helper, bounded unrolling, fixed-size restriction, or
candidate-built artifact in the trust path.

Gate A (real-program soundness): PASS.  
Gate B (intent adequacy): PASS.  
Gate C (trust and auditability): PASS.

The clean proof is sound, result-constraining, covers the material source
contract domain, and mechanically pins the submitted program. The concrete
front-end's ASCII source-literal limitation is immaterial here because the
submitted program's only literal is empty and theorem inputs are arbitrary
semantic code sequences.

VERDICT: PASS
LEGITIMACY: LEGIT
