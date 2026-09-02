# Independent adversarial review: 161-solve

The candidate is not a legitimate proof of the full HumanEval/161 contract.
The submitted K claims do reconstruct and close under the supplied theory, and
they execute the submitted constructor body.  However, both the submitted
Python implementation and the theorem materially narrow the unrestricted
Python-string contract to an ASCII-style case model.  The trusted canonical
implementation and the candidate disagree on 1,858 of 16,112 deterministic
tests, including simple Unicode witnesses.  Under the benchmark's explicit
decision rule, this material domain narrowing is `FAIL / NOT_LEGIT`.

There is a second validation defect: the reverse claim needs a result-bearing
slice/reversal simplification, but the candidate supplies no bridge-free
universal connection proof.  The equations appear mathematically true, so I do
not call them unsound without a false witness; I record the narrower missing
connection evidence.

## 1. Input and provenance integrity

The launcher declares:

- problem `161-solve`, condition `semantics`, mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance; and
- the trusted container paths under `/reference`, `/candidate`, and
  `/generation-evidence`.

The infrastructure gate passed.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, and every record required by
  `legacy-selected-stage1` are present and readable.  `usage.json` is present;
  historical `runtime-metrics.json` is not required for this legacy layout.
- The campaign object in `/audit-input.json` equals
  `/audit-campaign-lock.json`, and the lock's actual SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Independent SHA-256 checks matched the recorded canonical, prompt,
  translator, run, task, result, invocation, metrics, usage, generation prompt,
  `codex-last`, and `codex-output` hashes.
- The structured trace contains one valid 245-line JSONL file.  Its SHA-256,
  `534570c8623b6d7bed5584091cefd9960299d0649aae1261474a28ee33cd0b4f`,
  matches the per-file hash in the stage result and invocation record.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- `/reference/reference-semantics` is present, as required in supplied mode.
  A recursive, no-dereference comparison found the candidate and trusted
  semantics trees identical: the same 24 regular files, no missing or extra
  entry, no content difference, and no symlink in either tree.
- The required candidate proof artifacts `solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh` are present.

I read the required legacy launcher records, generation prompt, metrics, usage,
`codex-last`, bounded `codex-output` review, and structured trace only as
untrusted generation history.  They claim prior `#Top` runs but are not used as
proof evidence.

Evidence:
[mount inventory](evidence/stage1_initial_mounts.log),
[launcher records](evidence/stage1_launcher_records.log),
[record inventory](evidence/stage1_record_inventory.log),
[generation metadata](evidence/stage1_generation_metadata.log),
[hash checks](evidence/stage1_campaign_and_declared_hashes.log),
[recursive semantics comparison](evidence/stage1_integrity_checks.log),
[per-file semantics hashes](evidence/stage1_semantics_independent_hashes.log),
[trace structure](evidence/stage1_trace_structure.log),
[trace actions](evidence/stage1_trace_actions.log), and
[generation-output review](evidence/stage1_output_log_review.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Real contract

For a Python string `s`, process each character independently.  If a character
is a letter according to Python `str.isalpha()`, replace that character by its
`str.swapcase()` result; otherwise preserve it.  If the entire string contains
no letters, reverse the string.  Return the resulting string.  The source does
not restrict strings to ASCII.

The trusted canonical code implements this literally: it iterates over
characters, uses `i.isalpha()`, applies `i.swapcase()` per character, and uses a
flag to decide whether to reverse.

The candidate instead computes whole-string `s.swapcase()` and takes equality
with the original string as the test for “contains no letters”:

```python
result = s.swapcase()
if result == s:
    return s[::-1]
return result
```

That equivalence is valid for the candidate's intended ASCII subset, but not
for Python strings generally.

### Translation fidelity

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced a byte-identical `solution.mpy`.  All three relevant
hashes and `cmp` status 0 are in
[stage2_translation_identity.log](evidence/stage2_translation_identity.log).

### Independent differential

The reviewer-authored [differential_test.py](evidence/differential_test.py)
loads the trusted canonical and candidate by independent file paths.  It checks
the three documented examples, empty input, single-character and branch
boundaries, ASCII letter boundaries, mixed strings, explicit Unicode cases,
and all strings of lengths 0 through 4 over an 11-character alphabet.

Command:

```text
python3 /audit-output/evidence/differential_test.py
```

Result: exit 0, 16,112 cases, both canonical branches exercised, and 1,858
mismatches.  Exit 0 means the differential completed; mismatches remain visible
in its output.

Two independent failure modes are material:

- `s = "1中"`: `中`.isalpha() is true but does not change case.  Canonical
  returns `"1中"`; the candidate incorrectly decides “no letters” and returns
  `"中1"`.
- `s = "aΣ"`: the canonical applies swapcase per character and returns `"Aσ"`;
  whole-string Python swapcase is context-sensitive here and the candidate
  returns `"Aς"`.

Thus `solution.py` itself does not implement the full source contract.
Evidence: [stage2_differential.log](evidence/stage2_differential.log).

## 3. Clean proof reconstruction

All candidate artifacts were copied to `/tmp/audit-work/161-solve`; the copied
Python cache was removed, and no candidate-built K definition was reused.  The
installed tools are K v7.1.293, matching the campaign.

Fresh proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0.  Evidence:
[stage3_clean_kompile.log](evidence/stage3_clean_kompile.log).

Every positive target claim was then run both together and independently:

| Target | Result |
|---|---|
| all `SPEC` claims | exit 0, `#Top` |
| `SPEC.swaps-when-a-letter-exists` | exit 0, `#Top` |
| `SPEC.reverses-when-no-letter-exists` | exit 0, `#Top` |

Evidence:
[all claims](evidence/stage3_all_positive_claims.log),
[swap claim](evidence/stage3_claim_swap.log), and
[reverse claim](evidence/stage3_claim_reverse.log).

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0.  The reviewer-authored ASCII suite translated with the trusted
translator and ran to `.K`, `NoExc`, exit code 0.  It covers both branches,
empty input, documented examples, and ASCII case boundaries.
Evidence:
[LLVM build](evidence/stage3_clean_llvm_kompile.log),
[test source](evidence/audit_concrete_tests.py),
[translated test](evidence/audit_concrete_tests.mpy), and
[krun output](evidence/stage3_concrete_ascii_krun.log).

A concrete Unicode literal test failed with process status 113 at
`strToCodes("\xe4\xb8\xad")`, before program execution.  This is not an audit
infrastructure failure: the same fresh definition executes the ASCII suite.
It is direct evidence of the supplied semantics' explicit ASCII literal
boundary.  See
[stage3_concrete_krun.log](evidence/stage3_concrete_krun.log) and
[audit_concrete_unicode.py](evidence/audit_concrete_unicode.py).

Conclusion for this stage: the submitted K claims genuinely reconstruct and
close under the supplied theory.  That fact does not cure the source-contract
failure or validate the proof-local theory.

## 4. Adequacy and real-program pinning

### Plain-language claims

Both claims start with environment 0; an empty module scope whose parent is the
builtins scope at -1; empty heap and stack; fresh counters; `noRet`, `NoExc`,
and exit code 0.  The scope rewrite in each claim requires execution to leave
the exact `solve` closure installed in module scope 0.

1. `swaps-when-a-letter-exists`: for any `IntSeq CS` satisfying
   `CS != mapSwap(CS)`, load and call `solve(str(CS))`; require the final result
   `str(mapSwap(CS))`.
2. `reverses-when-no-letter-exists`: for any `IntSeq CS` satisfying
   `CS == mapSwap(CS)`, load and call `solve(str(CS))`; require the final result
   `str(revIS(CS))`.

These claims are result-constraining and their two K preconditions partition
the supplied sequence model.

### Satisfiable preconditions and ground substitution

Concrete states exist:

- `CS = [97,49]` (`"a1"`) satisfies the first precondition and all three
  evaluators return `"A1"`.
- `CS = [49,50]` (`"12"`) satisfies the second and all three return `"21"`.
- `CS = []` satisfies the second and returns `""`.

But the same substitution exposes inadequacy:

- `CS = [49,20013]` (`"1中"`) satisfies the K “no letter” precondition and the
  claim result is `"中1"`; trusted canonical Python returns `"1中"`.
- `"aΣ"` produces K claim result `"AΣ"`, trusted canonical `"Aσ"`, and
  candidate Python `"Aς"`.

Evidence:
[adequacy_witnesses.py](evidence/adequacy_witnesses.py) and
[stage4_ground_witnesses.log](evidence/stage4_ground_witnesses.log).

### Mechanical real-program pinning

The pinning checks pass.

- Trusted regeneration is byte-identical to `solution.mpy`.
- `kast` parsed the regenerated module into the normalized constructor term.
- A reachability comparison between `solutionModule()` and that normalized
  regenerated term closed with `#Top`.  The backend reports the claim as
  trivial after frontend function normalization, which is the expected exact
  constructor equality.
- `#runSolve(CS)` expands only to
  `#loadAll(solutionModule()) ~> Call(Name("solve"), ...)`.  Fixed semantics
  loads the exact `FuncDef`, binds it, evaluates the call, and restores the
  frame.  It does not replace the function body with a result oracle.
- A body-sensitivity mutant changed the executed method from `swapcase` to
  `lower` while preserving the target.  The mutant definition built, but its
  proof exited 1 with a genuine result residual
  `str(mapLower(CS))` versus `str(mapSwap(CS))`.

Evidence:
[KAST normalization](evidence/stage4_kast_translated_module.log),
[constructor comparison spec](evidence/constructor-compare-spec.k),
[constructor result](evidence/stage4_constructor_compare_cell.log),
[body mutant](evidence/verification-body-mutant.k),
[mutant build](evidence/stage4_body_mutant_kompile.log), and
[mutant rejection](evidence/stage4_body_mutant_proof.log).

There are no helper or loop claims.  The only auxiliary result-bearing proof
steps are the slice/reversal simplifications reviewed in Stage 5.

Adequacy result: **fail**.  The theorem pins the submitted body but not the full
Python meaning of that body, and both are materially narrower than the source
contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [inventory_k.py](evidence/inventory_k.py) inventories the
assembled semantics, all 23 helper K files, `verification.k`, and `spec.k`.
The final [rule_inventory.tsv](evidence/rule_inventory.tsv) contains every
line-addressed module/import/require, configuration, context, syntax
declaration, ordinary rule, priority rule, concrete rule, simplification rule,
and claim:

- 1,114 total inventory rows;
- 233 syntax declarations;
- 703 rules: 621 ordinary, 45 priority, 35 concrete, and 2 simplification;
- 112 declarations marked `total`;
- 22 `no-evaluators` opaque declarations; and
- 2 reachability claims.

Every inventory row has an explicit disposition and rationale in
[rule_assessment.tsv](evidence/rule_assessment.tsv), generated by
[assess_inventory.py](evidence/assess_inventory.py).  The dispositions are:

| Disposition | Rows | Decision |
|---|---:|---|
| accepted fixed supplied entries | 1,050 | Coherent on the declared subset or unreachable from this program |
| accepted inert opaque primitives | 22 | Float/sort/MD5-style symbols cannot influence this program |
| accepted exact pinning/plumbing | 19 | Exact constructors, runner, modules, and imports |
| fixed string-model limitations | 15 | ASCII rules do not model Python Unicode |
| domain-narrowing unused helpers | 4 | `containsLetter`/`solveSpec`; false as Unicode intent, but unused |
| true-looking unvalidated bridges | 2 | Slice/reversal simplifications; no false witness, missing connection theorem |
| closes but inadequate claims | 2 | Valid under the extended ASCII theory, not the source domain |

This grouping is a decision for every inventoried row, not a sample.  The TSV
preserves the exact source, line, attributes, complete normalized declaration,
disposition, and rationale.

### Used-construct mapping and control/state review

| Submitted construct | Declaration and material rules | Finding |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `syntax.k:53,57,61`; `core.k:124-127`; `functions.k:14-16` | Exact body is loaded and bound in scope 0 |
| `Assign(Name(...), Call(...))` | strict `Assign` at `syntax.k:41`; `controls.k:9-18`; call machinery below | RHS evaluates before scope write |
| `Name` | `syntax.k:12`; `core.k:130-154` | Lookup selects the loaded local binding, then builtins by parent traversal |
| `Call`, `Attribute`, empty args | `syntax.k:28-29`; `core.k:185-191`; `call.k:15-24,69-75` | Callee then arguments evaluate left-to-right; closure frames, calls, and returns are real |
| `.swapcase()` | `methods.k:21,149-164` | Real execution in the supplied model; value is ASCII per-code `mapSwap`, not Python Unicode |
| `Compare(... == ...)` | `syntax.k:30,32`; contexts and dispatch in `operators.k:14-20`; string equality `str.k:25` | Branch condition is the computed string equality |
| `If` | strict syntax at `syntax.k:49`; `controls.k:51-54`; `core.k:199-205` | Exactly one branch executes based on Boolean truth |
| `Return` and call pop | strict syntax at `syntax.k:50`; `functions.k:77-90` | Return value, continuation, environment, scope, stack, and `ret` are restored consistently |
| `s[::-1]` | `Subscript`, `Slice`, `NoBound`, unary integer at `syntax.k:14,22,38-39`; `operators.k:10`; `int.k:7`; `subscript.k:25-121` | Bounds evaluate in order and fixed semantics reaches `buildIS(CS,len-1,-1,-1)` |

The initial/final configuration and all observable cells are constrained.
There is no allocation in the submitted body, no exception path in the modeled
subset, and the call frame restores the empty heap, counters, stack, `ret`,
exception, and exit code.  The loaded module binding is explicitly constrained
in the post-state.

The used `swapC` guards are disjoint (`A-Z` versus `a-z`), the `owise` case is
the identity, and `mapSwap` recurses structurally.  Slice step `-1`, default
start `len-1`, default stop `-1`, and the build condition agree with reversal
for finite algebraic `IntSeq`s.  I found no overlapping used equation that
admits two different right-hand sides.

### Proof-local extension inventory

| Extension | Class and context | Value/control/state influence | Static decision |
|---|---|---|---|
| `solveBody()` | Definitional summary, no guard | Exact statements used by module and closure | Accepted; trusted regeneration comparison passes |
| `solutionModule()` | Definitional summary | Exact `FuncDef` loaded into scope 0 | Accepted |
| `solutionClosure()` | Definitional summary | Exact expected post-state binding | Accepted; same `solveBody` |
| `containsLetter(CS)` | Definitional summary | None; unused by both claims | Its name overstates the ASCII predicate; `CS=[20013]` is a Python-letter counterexample |
| `solveSpec(CS)` | Definitional summary | None; unused by both claims | Same unused domain narrowing |
| `doSlice(str(CS),noB,noB,someB(-1)) => str(revIS(CS))` | Result-bearing pure operational bridge/simplification over an exact term; no cells or continuation effect | Can close the reverse result | Algebraically true-looking, exact context, but no candidate connection theorem |
| `buildIS(CS,isLen(CS)-1,-1,-1) => revIS(CS)` | Result-bearing derived simplification | Can close the same reverse result | Algebraically true-looking; no candidate connection theorem |
| `#runSolve(CS)` | Fresh runner expansion | Adds exact load and call in the existing continuation; touches no cell itself | Accepted; does not bypass execution |

The simplifications do not introduce abrupt control, discard a continuation,
or abstract state.  Their complete domains are pure function terms.  Therefore
there is no concrete false conclusion witness with which to call either rule
unsound.  Nevertheless, the required Kit connection evidence is absent:

- Removing both simplifications still lets the swap claim close, but the
  reverse claim exits 1 at the exact residual
  `buildIS(CS,isLen(CS)-1,-1,-1) = revIS(CS)`.
- In a definition importing only fixed semantics, separate universal
  `doSlice` and `buildIS` connection claims both exit 1 with that same residual.

These failures do not prove the equations false; they prove that neither the
candidate nor the direct bridge-free reconstruction machine-checks the
connection demanded for a result-bearing proof bridge.

Evidence:
[no-bridge definition](evidence/verification-no-bridges.k),
[swap without bridges](evidence/stage5_swap_without_bridges.log),
[reverse without bridges](evidence/stage5_reverse_without_bridges.log),
[connection claims](evidence/bridge-connection-spec.k),
[doSlice connection result](evidence/stage5_doslice_connection_without_bridge.log),
and
[buildIS connection result](evidence/stage5_buildis_connection_without_bridge.log).

### Concrete false-conclusion witnesses for the material model gap

I do not label the fixed ASCII equations internally inconsistent.  The false
conclusion is at the source-contract bridge:

- For `CS=[49,20013]`, the reverse claim proves `[20013,49]`, while the trusted
  Python contract requires `[49,20013]`.
- For `"aΣ"`, supplied `mapSwap` gives `"AΣ"`, candidate Python gives `"Aς"`,
  and canonical Python gives `"Aσ"`.

These witnesses make the inadequacy concrete and prevent treating the gap as a
mere undocumented assumption.

## 6. Fresh non-vacuity test

The fresh [spec-vacuity.k](evidence/spec-vacuity.k) changes the first claim's
postcondition from `str(mapSwap(CS))` to the false unchanged result `str(CS)`.
`CS = [97]` (`"a"`) satisfies the entry precondition; real submitted execution
in the supplied model returns `"A"`, while the mutant demands `"a"`.

Frontend/build check:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Result: exit 0 and a valid `kore-exec` invocation.  Evidence:
[stage6_vacuity_dry_run.log](evidence/stage6_vacuity_dry_run.log).

Proof:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY
```

Result: exit 1 with `WarnStuckClaimState`.  The reachable final `<k>` cell is
`str(mapSwap(CS))`; the path retains `CS != mapSwap(CS)`, so it cannot imply
the false `str(CS)` target.  This is the intended unmet result obligation, not
a parser error, timeout, unrelated crash, or unreachable mutation.
Evidence: [stage6_vacuity_proof.log](evidence/stage6_vacuity_proof.log).

Non-vacuity result: pass.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied K definition and the two proof-local reversal
simplifications, the exact submitted constructor body has this partial-
correctness behavior over finite `IntSeq` values:

- if per-code ASCII `mapSwap(CS)` differs from `CS`, termination returns
  `mapSwap(CS)`;
- otherwise termination returns `revIS(CS)`;
- the modeled environment, module binding, heap, allocation counters, stack,
  return marker, exception marker, and exit code meet the claim's final
  constraints.

It does **not** establish HumanEval/161 for unrestricted Python strings, and it
does not establish that supplied K string behavior equals candidate CPython
behavior outside the ASCII subset.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 frontend, Haskell prover, LLVM runtime, K builtins | All build and proof results | Ordinary machine-checking trust; versions and fresh builds recorded |
| Trusted translator `/reference/py2mpy.py` | Python-to-constructor identity | Acceptable; byte identity plus KAST/constructor comparison |
| Supplied fixed semantics | All execution claims | Immutable and integrity-checked, but explicitly a subset; its ASCII string boundary is fatal to source adequacy |
| `doSlice` reversal simplification | Reverse claim | True-looking exact pure equation, but no bridge-free universal machine proof |
| `buildIS` reversal simplification | Reverse claim | Same; redundant/alternative result bridge, no universal machine proof |
| 22 imported opaque float/sort/MD5 symbols | None | Inert: no submitted term can reach them |
| `containsLetter` and `solveSpec` | None | Unused; cannot help claim closure, but expose the candidate's ASCII intent |
| Differential testing | Only implementation/source and model/source bridges on tested cases | Finite evidence, not a substitute for K proof; it disproves the claimed full-domain bridge |
| Informal finite-sequence algebra for reversal | Static assessment of the two simplifications | Supports “no false witness found”; does not replace the missing Kit connection theorem |

`PROOF.md`, generation traces, candidate concrete tests, and the prior `#Top`
were not accepted as substitutes for reconstruction.

### Gate and verdict accounting

- Kit Gate A, real-program soundness: **fail as validated proof evidence**.
  Exact-body execution, body sensitivity, result constraint, and non-vacuity
  pass, but the reverse result depends on an unconnected proof-local bridge.
  No claim of bridge unsoundness is made.
- Kit Gate B, intent adequacy: **fail materially**.  The Python implementation,
  supplied string model, precondition partition, and postconditions do not
  cover the HumanEval Python-string domain.  Concrete source-contract
  counterexamples are recorded.
- Kit Gate C, trust/evidence: **fail for the reversal bridge**.  Evidence is
  reproducible, but the required universal connection theorem is absent.

Even if the reversal equations were accepted on ordinary mathematical review,
the result would be Kit `SOUND-BUT-LIMITED` because of the Unicode/domain gap.
The benchmark instruction explicitly maps that material HumanEval contract
narrowing to `FAIL / NOT_LEGIT`, not to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
