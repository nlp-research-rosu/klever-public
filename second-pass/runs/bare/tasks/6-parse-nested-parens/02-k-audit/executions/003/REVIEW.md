# Independent adversarial audit: 6-parse-nested-parens

The candidate cleanly proves three concrete executions of the submitted
program, but it does not prove the HumanEval contract over its unrestricted
input domain. `spec.k` contains only three ground examples and no symbolic
input, invariant, or universal claim. The submitted Python also disagrees with
the trusted canonical implementation on empty input and empty fields. Under
the benchmark's explicit decision boundary, this materially narrowed
`SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher declares `record_layout: legacy-selected-stage1`,
`condition: bare`, and `semantics_mode: GENERATED_SEMANTICS` in
`/audit-input.json`.

I inspected all records required for that layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the single structured trace
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-8177-7120-9260-d271199aceaa.jsonl`;
- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`; and
- every candidate entry.

The audit campaign object is exactly equal to
`/audit-campaign-lock.json`, whose SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-declared regular-file hash checked by
[`00_provenance_check.py`](evidence/00_provenance_check.py) matches.
The 248-line trace parses completely as JSONL, starts with `session_meta`, ends
with `task_complete`, and has file SHA-256
`feeb4b9940fffef4d0872d19fd31602a9373aca2ad470dc0a9b78ed8a876af1b`,
matching both the invocation and result records.

An independent pipeline tree digest of `/candidate` is
`85513b4e73fa64d66e210c07a28224739e973856e64a4b4e899e22f998f2ea08`,
matching both `invocation.json:retained_workspace_sha256` and
`generation-result.json:outputs.workspace_sha256`. The corresponding trace
tree digest is
`203c0ed961a1a95e24268cbf443891dd8ecc5bef94abdfda435b7e6c373f2594`,
matching `usage.json:source_trace_sha256`. No candidate, generation-evidence,
or reference entry is symlinked.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist. There is no trusted or hidden
semantics baseline in this review. Full command output and status:
[`00_provenance_check.log`](evidence/00_provenance_check.log), exit 0,
`STAGE1_INTEGRITY=PASS`.

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `prompt.py`, `parse_nested_parens(paren_string: str) -> List[int]`
takes space-separated groups of nested parentheses and returns, in order, the
maximum nesting depth of every group. The prompt states no size bound. Trusted
`canonical.py` splits on `" "` and filters empty fields (`if x`) before
computing the per-group maximum.

The submitted `solution.py` uses the usual depth scan and is correct for
nonempty, well-formed groups separated by exactly one space. Unlike the
canonical, however, it processes every field returned by `split(" ")`,
including empty fields, and appends `0` for each.

### Translation identity

The trusted translator was rerun in scratch:

```text
python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate/solution.py >/tmp/audit-work/candidate/regenerated-solution.mpy
```

It exited 0. The regenerated and submitted files are byte-identical, both with
SHA-256
`4cc43e4ecb2ef1adeb7d7014acb39c8811a7a42a77a48b44ea96974e66ae43e7`.
See [`01_regenerate.sh`](evidence/01_regenerate.sh) and
[`01_regenerate.log`](evidence/01_regenerate.log).

### Differential execution

[`01_differential.py`](evidence/01_differential.py) independently imports the
trusted canonical entry point and submitted entry point. It covers the
documented example, zero/one/multiple loop iterations, both `If` outcomes,
increasing and repeated nesting, empty input, leading/trailing/repeated
separators, and 300 seeded inputs assembled from all 64 Dyck words with one
through five pairs.

The command

```text
python3 /audit-output/evidence/01_differential.py
```

exited 1 because it found seven boundary mismatches; it found zero mismatches
among the 300 generated single-separator cases. Concrete witnesses include:

| Input | Trusted canonical | Submitted |
|---|---:|---:|
| `""` | `[]` | `[0]` |
| `" "` | `[]` | `[0, 0]` |
| `" ()"` | `[1]` | `[0, 1]` |
| `"()  (())"` | `[1, 2]` | `[1, 0, 2]` |

The full bounded result is in
[`01_differential.log`](evidence/01_differential.log). Even if one treated
these whitespace boundaries as outside an informal reading of “groups,” the
finite proof-domain defect in Stage 4 independently determines the verdict.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work`; no candidate compiled
definition or cache was copied or reused. K reports version `v7.1.293`.

The independent rebuild script
[`02_rebuild.sh`](evidence/02_rebuild.sh) executed:

```text
kompile semantic.k --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition /tmp/audit-work/runs/rebuild2/semantic-kompiled

kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-VERIFICATION --backend haskell \
  --output-definition /tmp/audit-work/runs/rebuild2/verification-kompiled

kprove spec.k \
  --definition /tmp/audit-work/runs/rebuild2/verification-kompiled \
  --spec-module SPEC
```

Both `kompile` commands exited 0. The combined positive proof exited 0 and
printed `#Top`.

I also copied each target claim verbatim into its own module in
[`02_isolated-specs.k`](evidence/02_isolated-specs.k) and ran:

```text
kprove /tmp/audit-work/candidate/isolated-specs.k \
  --definition /tmp/audit-work/runs/rebuild2/verification-kompiled \
  --spec-module AUDIT-SPEC-EXAMPLE
kprove /tmp/audit-work/candidate/isolated-specs.k \
  --definition /tmp/audit-work/runs/rebuild2/verification-kompiled \
  --spec-module AUDIT-SPEC-INCREASING
kprove /tmp/audit-work/candidate/isolated-specs.k \
  --definition /tmp/audit-work/runs/rebuild2/verification-kompiled \
  --spec-module AUDIT-SPEC-SINGLE
```

All three commands independently exited 0 and printed `#Top`. Exact build,
execution, proof output, and statuses are in
[`02_rebuild.log`](evidence/02_rebuild.log). An earlier isolation attempt put
the copied spec in the wrong directory for its relative
`requires "verification.k"`; it produced a source lookup error and was
corrected before any claim judgment
([`02_rebuild_attempt1.log`](evidence/02_rebuild_attempt1.log)).

### Fresh concrete semantics execution

The LLVM definition executed the actual regenerated `solution.mpy` on normal
and boundary inputs:

| Input | K result | Submitted Python | Canonical Python |
|---|---:|---:|---:|
| documented example | `[2,3,1,3]` | `[2,3,1,3]` | `[2,3,1,3]` |
| `"()()"` | `[1]` | `[1]` | `[1]` |
| `""` | `[0]` | `[0]` | `[]` |
| `"()  (())"` | `[1,0,2]` | `[1,0,2]` | `[1,2]` |

Every `krun` exited 0 with `.K`, empty internal maps, and the listed concrete
result. Thus the generated semantics tracks the submitted program on these
normal and boundary cases, including the submitted program's divergence from
the contract.

## 4. Adequacy and real-program pinning

### Plain-language claims

Every entry precondition is a single fully ground initial configuration:
`<k>` contains `solutionProgram`, `<input>` contains one fixed literal,
`<env>` and `<functions>` are empty, and `<result>` is `noResult`. Every
postcondition requires terminated control, empty internal maps, and one exact
result:

| Claim | Exact input | Required result |
|---|---|---|
| 1 | `"(()()) ((())) () ((())()())"` | `[2,3,1,3]` |
| 2 | `"() (()) ((())) (((())))"` | `[1,2,3,4]` |
| 3 | `"(()(())((())))"` | `[4]` |

Each precondition is manifestly satisfiable by its displayed initial
configuration. Direct execution of both Python implementations on these
inputs yields exactly the required result
([`01_differential.log`](evidence/01_differential.log)).

### Mechanical program identity

Trusted regeneration first established `solution.py -> solution.mpy` byte
identity. [`03_program_pinning.sh`](evidence/03_program_pinning.sh) then:

1. mechanically extracted the RHS of `rule solutionProgram =>` from the
   scratch `verification.k`;
2. normalized only K's internal empty-list spelling (`.Exprs`/`.Stmts`) to the
   equivalent external program syntax;
3. parsed both the submitted program and extracted proof term with `kast`; and
4. compared their JSON KAST.

Both JSON terms have identical SHA-256
`cf651ba5454f0216f0a3b475ff5a55c4e7b6de69b046d31f83e6a6718429274e`;
`cmp` exited 0
([`03_program_pinning.log`](evidence/03_program_pinning.log)). The
`solutionProgram` equation therefore names the actual translated binding and
body; it is not a substituted algorithm or result oracle.

A separate body-sensitivity mutation changed the constructor actually executed
by the claims from `depth += 1` to `depth -= 1`. The mutated proof definition
compiled (exit 0), while the original target spec failed (exit 1,
`WarnStuckClaimState`) with concrete result `[0,0,0,0]` instead of
`[2,3,1,3]`. See
[`03_body_sensitivity.sh`](evidence/03_body_sensitivity.sh) and
[`03_body_sensitivity.log`](evidence/03_body_sensitivity.log).

### Adequacy failure

There is no symbolic input variable in `spec.k`, no domain precondition over
arbitrary parenthesis strings, no loop invariant/circularity, and no theorem
relating a returned list to maximum nesting. The three preconditions admit
exactly three strings. Therefore the proof establishes three examples only.
It says nothing about any fourth valid input, regardless of input size.

The source contract has no three-input or finite-size restriction. This is a
material narrowing of the HumanEval domain, not merely thin test evidence.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`04_rule_inventory.md`](evidence/04_rule_inventory.md). It enumerates:

- all 28 local syntax declarations/groups of productions;
- the five-cell configuration;
- all 18 operational rules;
- all 25 function/equational rules, including `solutionProgram`;
- all 14 `[function]` declarations;
- all three positive claims and the negative probe category; and
- the absence of local `total`, `functional`, simplification, priority,
  `owise`, `anywhere`, macro, opaque, lemma, or auxiliary-claim extensions.

Every constructor in regenerated `solution.mpy` maps to a declaration and
rule: module loading, the typing import, function registration and invocation,
assignments, both loops, both branches, integer updates, explicit-space split,
character iteration, list append, and return.

Material findings:

- Execution order is explicit and faithful for this target. Statement lists
  execute left-to-right; loop iterables are evaluated once; loop values are
  processed in order; guards are evaluated before branch selection; and
  assignment/append updates the environment after pure RHS evaluation.
- The generated model has no general Python call stack, exception semantics,
  heap, or effectful imports. Those are target-specific exclusions, not used
  constructs silently assigned fabricated behavior. The one import is
  typing-only after the trusted translator erases annotations, and the only
  program call is the configured top-level invocation.
- `appendVals`, `chars`, and `splitSpaces` strictly descend. Guarded equation
  pairs are disjoint and cover every use. Other functions are partial rather
  than falsely declared total, so unsupported uses remain stuck.
- The explicit-separator split equations retain empty fields, faithfully
  modeling the submitted `str.split(" ")`. Consequently the boundary
  divergence in Stage 2 is a submitted-program/contract defect, not a
  semantics rule that fabricates a different submitted-program result.
- `solutionProgram` expands to the exact body and then normal operational rules
  execute both loops. No rule encodes maximum-depth answers, replaces a
  property-bearing computation with an oracle, or jumps directly to a result.

Some rules are intentionally broader in syntax than a reusable Python
semantics—most visibly the generic ignored `ImportFrom` and top-level-only
`invoke`/`Return` model. I do not label these rules unsound for this theorem:
on every intended input the imported module and executed body are fixed, and
no concrete or symbolic false conclusion witness exists within that match
domain. Their limited reuse scope is recorded in the inventory.

Gate A (real-program soundness) passes for the theorem actually stated: the
ground claims execute the pinned body, constrain the exact result, and contain
no unsound proof extension. Gate B fails because that theorem is materially
smaller than the requested contract.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/mutation-spec.k`.
[`05_false_postcondition.k`](evidence/05_false_postcondition.k) is a fresh
mutation of the third positive result: for input `"(()(())((())))"`, it
requires `[5]` instead of `[4]`.

The independent witness script shows both Python implementations return `[4]`.
Then:

```text
kprove /tmp/audit-work/candidate/audit-false-postcondition.k \
  --definition /tmp/audit-work/runs/verification-kompiled \
  --spec-module AUDIT-FALSE-POSTCONDITION --dry-run
```

exited 0, establishing that the mutation parsed and built. The same command
without `--dry-run` exited 1 with `WarnStuckClaimState`; its residual final
configuration contains `result(pyList(pyInt(4) :: .PyVals))`, which cannot
unify with required `[5]`. The wrapper therefore reports
`FRESH_NONVACUITY=PASS`. See
[`05_nonvacuity.sh`](evidence/05_nonvacuity.sh) and
[`05_nonvacuity.log`](evidence/05_nonvacuity.log).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, crash, or unreachable mutation.

## 7. Proven versus assumed accounting

### What is machine-checked

Relative to the freshly compiled generated K definition, the exact submitted
constructor program reaches the exact final list for the three literal inputs
in `spec.k`. All three claims independently close with `#Top`. The proof is
result-constraining and non-vacuous on those configurations.

It does **not** establish:

- correctness for arbitrary valid parenthesis-group strings;
- any inductive relationship between scanning prefixes, current depth, and
  maximum depth;
- equivalence with the canonical function on the source-contract domain;
- behavior for empty/leading/trailing/repeated separators; or
- a universal Python-to-K semantics equivalence theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 Haskell/LLVM backends and reachability implementation | All build, execution, and proof results | Standard unavoidable checker trust boundary; version and fresh commands recorded. |
| Imported K `INT`, `STRING`, `BOOL`, and `MAP` hooks | Arithmetic, comparison, splitting, character extraction, environments | Standard low-level primitives. Inputs material to the contract are ASCII parentheses/spaces; concrete boundaries were rerun. |
| Trusted `py2mpy.py` as the source-to-constructor bridge | Identity of `solution.py` and `solution.mpy` | Byte regeneration plus KAST identity establishes the exact artifact chain; this is not itself a universal compiler-correctness theorem. |
| Candidate-generated `semantic.k` as a model of the used Python subset | Meaning of all reachability claims | Audited rule-by-rule and concretely compared on normal/boundary cases. No opaque result or operational shortcut exists. General unused Python behavior is excluded. |
| Erasure of annotations and typing-only import effects | Source/program identity | Informal but direct for this source: the imported `List` is used only in annotations, which the trusted constructor translator omits; function value/control is unaffected. |
| Trusted canonical implementation as intent oracle | Differential adequacy evidence | Authoritative task input, but differential results are finite evidence. They support the displayed boundary witnesses and do not replace a K theorem. |

There are no local opaque symbols, external result oracles, trusted
proof-local lemmas, loop summaries, operational bridges, or empirical
abstractions on which claim closure depends. Gate C passes for the limited
three-input theorem because its trust and evidence are reproducible.

### Decision

The reconstructed `#Top` results are genuine but only for three examples.
According to the Kit terminology this is `SOUND-BUT-LIMITED`: Gate A passes,
Gate B fails, and Gate C passes for the limited theorem. The benchmark prompt
explicitly maps a `SOUND-BUT-LIMITED` result caused by materially narrowing the
HumanEval source-contract domain to `FAIL / NOT_LEGIT`. The independent
canonical mismatch on empty fields is an additional program-fidelity defect;
the finite ground spec is independently sufficient for the same verdict.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
