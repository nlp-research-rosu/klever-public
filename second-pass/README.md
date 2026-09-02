# Second pass — the six-stage, three-arm HumanEval verification campaign

This directory is the complete archive of the second pass: every one of
the 164 HumanEval problems run through a six-stage verification pipeline
(Codex K proof → independent K audit → trust-boundary classification →
deterministic K-to-Lean export → Lean proof → independent adversarial
Lean audit) in three experimental arms.

## Final results (campaign complete, 2026-08-01)

| Arm | Primary verdict stage | LEGIT | PASS | CONCERNS | FAIL |
| --- | --- | --- | --- | --- | --- |
| `bare` | stage 2 (K audit) | 64/164 | 23 | 41 | 100 |
| `semantics` | stage 2 (K audit) | 73/164 | 37 | 36 | 91 |
| `kit_semantics` | stage 6 (Lean audit) | **164/164** | 162 | 2 | 0 |

Every verdict was produced by an independent audit session, gated by
mechanical checks; LEGIT = PASS + CONCERNS.

## What is where

- `runs/{bare,semantics,kit_semantics}/` — the final run tree per arm,
  complete six-stage per-task records; see `runs/README.md` for
  provenance and the copy-time verification.
- `prompts/` — the exact per-stage prompts (proof, audits, lemma
  discovery, Lean, resume variants).
- `tools/`, `docker/` — stage runners, contracts, mechanical gates, and
  the container definitions for all six stages.
- `data/` — pinned inputs: the 164 questions, skill bundles, reference
  semantics (current + `semantic-archive/` history), `kit-archive/`,
  `stage4-producer-sources/`, and every lock file.
- `audits/` — the earlier kit-fix / regression audit campaigns.
- `submission/` — the AAAI-27 supplementary package exactly as shipped
  (self-contained; its own README walks a reviewer end to end).
- `tests/` — the pipeline's own test suite.

The remainder of this file is the benchmark's design and operations
documentation as written during the campaign (paths in it refer to the
original working repository, where run directories carry full run ids
such as `codex-gpt-5.6-sol-xhigh-kit-semantics-frozen-20260724` —
archived here as `runs/kit_semantics`).

---

## Campaign documentation: docstring-only HumanEval K benchmark

This repository prepares isolated, one-shot HumanEval
implementation-and-proof tasks for Codex, Claude Code, and OpenCode. The
generation runner gives an agent the exact HumanEval prompt, asks it to write
the missing Python implementation itself, and then asks it to construct and
run a K proof. The generation agent never receives `canonical.py`, hidden
tests, an oracle, a prior candidate, or audit feedback. Correctness and proof
legitimacy are adjudicated independently after generation by a separate
verifier.

## Condition-visible inputs

Every fresh task starts with exactly `prompt.py`, `py2mpy.py`, and
`run-input.json` under the writable `/work` mount. `prompt.py` is the exact
original HumanEval prompt, including intentionally supplied helpers or setup,
but no completed target implementation. `run-input.json` records hashes of the
problem prompt, instruction prompt, translator, and any condition-specific
inputs.

The launcher passes one instruction prompt to the agent and adds only the
condition-specific inputs shown here:

| Condition | Instruction prompt | Initial `/work` seed | Kit input |
| --- | --- | --- | --- |
| `bare` | `prompts/bare.md` | `prompt.py`, `py2mpy.py`, `run-input.json` | none |
| `semantics` | `prompts/with-semantics.md` | the common seed plus `reference-semantics/` | none |
| `kit` | `prompts/kit-bare.md` | the common seed | read-only `/kit-skills` |
| `kit-semantics` | `prompts/kit-semantics.md` | the common seed plus `reference-semantics/` | read-only `/kit-skills` |

Codex and Claude support all four conditions. OpenCode supports only `bare` and
`semantics`; its launcher rejects Kit-looking configurations. In Codex and
Claude, the base Compose file has no Kit mount. Only
`docker-compose.kit.yml` adds `/kit-skills`, and only a Kit condition selects
that override.

Active generation tasks and instructions must never expose `canonical.py`, an
answer fragment, official tests, or an oracle. The population validator checks
the exact seed bytes and recursively rejects the forbidden answer filename.
Do not copy verifier inputs into `runs/` and do not mount them in a generation
container.

`runs/archive/` is immutable historical evidence from the earlier setup. Never
modify, repopulate, resume, or treat it as an active configuration. Fresh
configurations are direct children of `runs/` outside `archive`.

## Compact legacy-run migration

The migration targets only `codex-gpt-5.6-sol-xhigh-bare` and
`codex-gpt-5.6-sol-xhigh-semantics`. From the repository root, first create
and review a no-change plan:

```bash
python3 tools/migrate_legacy_runs.py --dry-run \
  --report /tmp/legacy-migration-plan.json
```

After reviewing that report, apply the transaction and preserve its result
report:

```bash
python3 tools/migrate_legacy_runs.py --apply \
  --report /tmp/legacy-migration-result.json
```

Neither command launches a model, an audit, or Klean. After a successful
apply, inspect both migrated runs:

```bash
python3 tools/run_pipeline.py status codex-gpt-5.6-sol-xhigh-bare
python3 tools/run_pipeline.py status codex-gpt-5.6-sol-xhigh-semantics
```

Use `python3 tools/run_pipeline.py dry-run <run-id>` to obtain the exact next
command for each eligible task. Do not launch a task reported as blocked or
terminal. The four migrated semantics tasks reported as `K_PROOF_TIMEOUT` are
the exception to normal orchestration: after explicit launch authorization,
resume each original session with:

```bash
docker/codex/run_task.sh \
  codex-gpt-5.6-sol-xhigh-semantics <problem>
```

For each successful semantics task reported as `PENDING_K_AUDIT`, start its
fresh independent audit with:

```bash
docker/audit/run_task.sh \
  codex-gpt-5.6-sol-xhigh-semantics <problem>
```

For each bare task, or subsequently audited semantics task, reported as
`PENDING_LEMMA_DISCOVERY`, resume the original generating session for lemma
classification with:

```bash
docker/codex/resume_lemma_discovery_task.sh <run-id> <problem>
```

Only Stage 2 `PASS` and `CONCERNS` selections are `LEGIT` and eligible for
Stage 3. Stage 2 `FAIL` and incomplete-input tasks remain blocked. Re-run
`status` or `dry-run` after every explicit task operation rather than
assuming that a later stage is eligible.

Each invocation or audit execution's `usage.json` is authoritative for tokens
extracted from its immutable trace. The run-level `usage-summary.json` is
reproducible derived data aggregated from those records; resumed-session
records use invocation deltas so cumulative session totals are not counted
twice. Historical monetary cost is unavailable because the traces contain
neither an authoritative charge nor a historical pricing snapshot. Any later
cost calculation must use a separately pinned rate card and be labeled as an
estimate.

## One candidate, resumable sessions

Each task has one self-written solution. A fresh stochastic solution attempt
requires a fresh run ID. The pipeline may continue the same exact Codex
session after a wrapper-owned timeout, but it never rerolls the candidate or
reveals audit feedback. The persistent session UUID and `CODEX_HOME` prove
that a continuation belongs to the original attempt.

Kit conditions add proof-engineering and validation instructions, not solution
content. If the agent finds that Gate A fails, it must preserve its
self-written `solution.py`, remove the unsound extension, expose the genuine
proof obligation, and continue inside the same invocation/session. Difficult
proof work is not itself a hard blocker.

## Locked Kit treatment

The approved Kit bundle is pinned to:

- commit `46af96a89de7b297e9dd4e9cfc2bf248e6d4698f`;
- skills tree `ac515c9de2c87ac2366c9ea3d55c78cad172897b`;
- `data/kit-skills.lock.json` schema version 2.

Check the vendored topology, modes, and hashes against the lock:

```bash
python3 tools/check_kit_bundle.py
```

When the approved source checkout is present, also verify its clean commit,
tree, plugin version, and bytes:

```bash
python3 tools/check_kit_bundle.py --source /home/yuqing/Documents/Code/kit
```

Do not regenerate the lock from a dirty or different Kit checkout.

## Split auditor Kit and per-task Kit provenance

The generation Kit evolves through the recorded iterative loop
(Klever-derived Kit development), so two bundles exist:

- `data/skills` + `data/kit-skills.lock.json`: the **moving generation
  bundle**, advanced by each Kit revision. `tools/check_kit_bundle.py`
  pins the current revision.
- `data/audit-skills` + `data/audit-kit-skills.lock.json`: the
  **campaign-frozen auditor bundle** (commit
  `b9135325caf193f3db60f4ae425dc862a4cd5d5d`), mounted by
  `docker/audit/run_task.sh` and pinned by
  `data/audit-campaign.lock.json`. It never moves during the campaign, so
  every Stage 2 audit is judged by one identical instrument.

A run manifest records the Kit its run was created under. A task promoted
from a later-revision staging run records its own `kit` override in
`task.json`; resolution of historical artifacts accepts recorded
historical Kits, while launching new model work requires the effective Kit
to equal the current lock (`require_current_kit` in
`tools/pipeline_contract.py`).

Because `humaneval-codex-runner:latest` may drift past the frozen audit
campaign image, the audit launcher accepts `HUMANEVAL_AUDIT_IMAGE`; the
campaign lock verifies whatever image is resolved.

Operational scripts for the loop (batch auditing, staging promotion,
usage/auth management, the current v2 hold ledger) are under `ops/`; the
running state, protocol, and takeover instructions are in `TAKEOVER.md`
and the `HANDOVER.md` addendum.

## Canonical resumable six-stage K/Klean/Lean pipeline

New Codex experiments use one unique run ID and the following stages:

| Stage | Purpose | Session |
| --- | --- | --- |
| `01-k-proof` | Agent writes the Python solution and K proof | New generating session; one same-session timeout continuation |
| `02-k-audit` | Independently audit the K proof | Fresh auditor |
| `03-lemma-discovery` | Classify the frozen K simplification rules and select domain lemmas | Resume the exact generating session from Stage 1 |
| `04-klean-generation` | Deterministically generate and sanity-check the fixed Lean theorem | No model |
| `05-lean-proof` | Prove the immutable generated theorem, when one exists | Resume the exact generating session from Stages 1 and 3 |
| `06-lean-audit` | Independently reclassify the rules and, when present, audit the Lean proof | Fresh auditor |

`PASS` and `CONCERNS` from Stage 2 are both `LEGIT` and may enter Stage 3;
`FAIL` is terminal. The Stage 3 agent gets the frozen Stage 1 workspace and
rule inventory, but does not receive Stage 2 audit feedback. It has a
20-minute default allocation with no timeout continuation. Stage 5 likewise
does not receive Stage 2 audit feedback, failed Stage 4 diagnostics, or any
auditor output.

Stages 1, 3, and 5 are cryptographically and structurally bound to the same
Codex session UUID and persistent `CODEX_HOME`. Stage 3 and Stage 5 use
`codex exec resume` against that exact session rather than starting a new
agent or rerolling the solution. Stage 5 has a one-hour initial budget and a
two-hour default cumulative budget; only a wrapper-owned timeout can allocate
the second hour. OOM and ordinary failures do not receive a continuation.

Stage 3 classifies every source `[simplification]` rule as a summary definition
or a domain lemma and publishes the protected manifest. Stage 4 consumes only
the frozen Stage 1 workspace and that protected Stage 3 manifest. It
deterministically maps every selected domain lemma bijectively by source ID,
span, and hash to one hashed Lean conjunct. The generated Base project defines
an immutable, parameterized `targetStatement`; it never contains a proof of
that target and never substitutes `True`. The exact generator image ID is
bound into the generation manifests, and every target parameter records its
KORE symbol, source-rule IDs, and binding hash.

`KLEAN_PREFLIGHT_ERROR` is a tooling failure, not an agent verdict. Repair the
exporter, adapter, or pinned toolchain without changing the Stage 1 candidate
or Stage 3 classification, then explicitly rerun Stage 4. The repair creates a
new numbered generation and leaves the failed generation immutable. Never
show Stage 4 diagnostics to the benchmark agent or edit generated Lean output
by hand.

For a nonempty domain set, Stage 5 receives the generated Base project, its
Lake files, the protected Stage 3 manifest, and original K workspace
read-only. Its writable `Proof.lean` contains the sole initial `sorry` plus
the permitted operational bridge definitions. Successful output may contain
no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`.

For an empty domain set, Stage 4 records `KLEAN_NO_OBLIGATIONS`, emits no
target, and does not start Stage 5.
KLEAN_NO_OBLIGATIONS still proceeds to Stage 6; it is not a completed
pipeline verdict. Stage 6 runs in
classification-only mode to independently confirm that the domain set is
genuinely empty. With a successful Stage 5 proof, Stage 6 instead runs in
classification-plus-proof mode.

Stage 6 treats every prior artifact as untrusted evidence. Its fresh auditor
reconstructs and reclassifies the inventory, checks the fixed generation, and
in proof mode validates each operational bridge against the frozen K
semantics.
In both modes, a separate no-network mechanical container reruns deterministic preflight
against the frozen Stage 1 input, protected Stage 3 manifest, and selected
Stage 4 generation.
Classification-only confirms the no-obligation generation and has no proof
candidate.
Proof mode additionally clean-builds and type-checks the candidate, verifies
`Proof.final`, and reconciles `#print axioms` with the trust inventory. A
failed mechanical gate forces `FAIL`/`NOT_LEGIT`; mechanical infrastructure
failure is `AUDIT_ERROR`.

Stage 1's second invocation also exists only after a wrapper-owned timeout and
resumes the explicit same session UUID. The runner preflights Codex's bundled
bubblewrap sandbox before starting the model. Stage 1 accepts exit zero only
with one exact `RESULT: KPROVE_PASSED — ...` marker.
If a finalized timeout continuation has protected bubblewrap
namespace-denial evidence and identical input/output workspace hashes, an
operator may run `tools/stage1_runner.py --infrastructure-retry` once. That
creates immutable `003-infrastructure-retry` evidence and resumes the same
session; it never edits the two earlier invocations. If `003` fails before the
model starts with a zero-duration, evidence-empty harness error, one `004` may
record the corrected preflight attempt. No fifth invocation is permitted.
The two independent audits may be repeated only after `AUDIT_ERROR`; `FAIL`
must not be retried to seek a different verdict.

### Layout

```text
runs/<run-id>/
├── run.json
├── task-list.txt
└── tasks/<problem>/
    ├── task.json
    ├── 01-k-proof/
    │   ├── workspace/
    │   ├── invocations/{001-initial,002-timeout-resume,003/004-infrastructure-retry}/
    │   └── result.json
    ├── 02-k-audit/
    │   ├── executions/{001,002}/
    │   └── selected.json
    ├── 03-lemma-discovery/
    │   ├── workspace/
    │   ├── invocations/001-initial/
    │   └── result.json
    ├── 04-klean-generation/
    │   ├── generations/{001,002}/
    │   └── selected.json
    ├── 05-lean-proof/
    │   ├── workspace/
    │   ├── invocations/{001-initial,002-timeout-resume}/
    │   └── result.json
    └── 06-lean-audit/
        ├── executions/{001,002}/
        └── selected.json
```

Conditional `002` directories appear only for a timeout continuation,
auditor-infrastructure retry, or manually repaired Stage 4 generation.
Stage 1's conditional `003` is the evidence-gated runner-infrastructure retry;
`004` exists only when `003` stopped before invoking the model, as described
above. `selected.json` is a hashed manifest, not a mutable symlink. Numbered
Stage 2/4/6 directories are immutable evidence attempts. Stage 4 builds into
an isolated temporary output and atomically publishes only the new numbered
generation; prior generations are never mounted writable.

Persistent session control lives separately:

```text
runner-state/<run-id>/<problem>/
├── codex-home/
├── session.json
└── stage-ledger.jsonl
```

The complete `runs/<run-id>/` tree is archiveable evidence.
`runner-state/` contains credentials and resumable agent state and must not be
archived, committed, or mounted into either auditor.
`run.json` also records the exact Codex, K, pyk/Klean, and Lean versions plus
the frozen toolchain-lock hash used to create the run.

### Create, inspect, and run

Create a run without launching a model:

```bash
python3 tools/create_run.py experiment-2026-07-23 \
  --config codex-gpt-5.6-sol-xhigh-kit-semantics \
  --all-selected
```

Inspect all tasks or show the exact next commands without launching:

```bash
python3 tools/run_pipeline.py status experiment-2026-07-23
python3 tools/run_pipeline.py dry-run experiment-2026-07-23
```

After explicit launch authorization, run eligible tasks with bounded
parallelism:

```bash
python3 tools/run_pipeline.py run experiment-2026-07-23 --jobs 4
```

The public per-stage entrypoints remain independently callable:

```bash
docker/codex/run_task.sh <run-id> <problem>
docker/audit/run_task.sh <run-id> <problem>
docker/codex/resume_lemma_discovery_task.sh <run-id> <problem>
docker/klean/generate_task.sh <run-id> <problem>
docker/klean/check_task.sh <run-id> <problem>
docker/codex/resume_lean_task.sh <run-id> <problem>
docker/klean-audit/run_task.sh <run-id> <problem>
```

Use `python3 tools/run_pipeline.py stage <run-id> <problem> 4` only after a
manual exporter/toolchain repair of a selected `KLEAN_PREFLIGHT_ERROR`.
Completed stages are never overwritten.

### Migrate schema-v2 evidence

Schema-v2 runs must be moved into the canonical six-stage layout before they
can use the current orchestrator. First generate and review a read-only,
hash-bound plan:

```bash
python3 tools/migrate_six_stage_layout.py --dry-run \
  <run-id> [<run-id> ...] \
  --report /tmp/six-stage-migration-plan.json
```

Only after reviewing every source/tree hash and blocker, apply the exact run
set:

```bash
python3 tools/migrate_six_stage_layout.py --apply \
  <run-id> [<run-id> ...] \
  --report /tmp/six-stage-migration-result.json
```

Active runs must not be migrated. Dry-run reports matching Codex, audit,
Klean, and pipeline processes; apply checks again and fails closed. Wait until
the schedulers and their subprocesses have finished, then rerun dry-run
immediately before apply. Migration preserves legacy Stages 3–5 below
`legacy-v2/`, creates empty canonical Stages 3–6, and does not launch a model
or a downstream stage.

## Populate fresh task folders

`data/selection.json` currently selects 24 tasks, balanced 8/8/8 across its
easy, medium, and hard tiers. Population creates 24 task folders per
configuration; it does not launch Docker, an agent, or a model.

Use suffixes to select the condition. For example, the supported routes can be
populated with:

```bash
python3 tools/populate_runs.py \
  codex-gpt-5.6-sol-xhigh-bare \
  codex-gpt-5.6-sol-xhigh-semantics \
  codex-gpt-5.6-sol-xhigh-kit \
  codex-gpt-5.6-sol-xhigh-kit-semantics \
  claude-code-opus-xhigh-4-8-bare \
  claude-code-opus-xhigh-4-8-semantics \
  claude-code-opus-xhigh-4-8-kit \
  claude-code-opus-xhigh-4-8-kit-semantics \
  opencode-kimi-k3-bare \
  opencode-kimi-k3-semantics
```

Existing task folders are validated, not silently refreshed. The same
pre-launch check is available explicitly as:

```bash
python3 tools/populate_runs.py --validate-task \
  codex-gpt-5.6-sol-xhigh-kit-semantics 8-sum-product \
  runs/codex-gpt-5.6-sol-xhigh-kit-semantics/8-sum-product
```

## Inspect routing without launching

`--print-config` is the only supported launcher inspection mechanism. It
resolves a real direct-child task path, runs the `--validate-task` seed check,
prints the model, condition, prompt, Kit flag, and Compose files, then exits
before Docker:

```bash
docker/codex/run_task.sh --print-config \
  codex-gpt-5.6-sol-xhigh-kit-semantics 8-sum-product

docker/claude-code/run_task.sh --print-config \
  claude-code-opus-xhigh-4-8-kit-semantics 8-sum-product

docker/opencode/run_task.sh --print-config \
  opencode-kimi-k3-semantics 8-sum-product
```

Do not inspect routing by invoking a one-task launcher without
`--print-config`, by overriding an entrypoint, or by calling Compose directly.
`run_matrix.sh --dry-run` may list queued folders, but it is not a substitute
for the validated one-task route inspection above.

## No-model verification

The fast setup checks are local/static except for Compose configuration
resolution performed by the test suite:

```bash
python3 -m unittest discover -s tests -v
bash -n docker/codex/*.sh docker/claude-code/*.sh docker/opencode/*.sh tools/*.sh
python3 -m json.tool data/humaneval-prompts.lock.json >/dev/null
python3 -m json.tool data/kit-skills.lock.json >/dev/null
git diff --check
```

The unit suite also audits every active direct child of `runs/` against the
24-task selection and the complete seed contract. It checks `archive` only as
a direct entry and never traverses `runs/archive/`.

The offline runner-image smoke requires these prebuilt local images:

- `humaneval-codex-runner:latest`;
- `humaneval-claude-runner:latest`;
- `humaneval-opencode-runner:latest`.

Run the no-model image inspection with:

```bash
bash tests/smoke-containers.sh
```

The script first runs a no-model contract fixture for both complete Stage 6
routes: a fake proof-bearing task with one domain lemma and a
summary-definition-only `KLEAN_NO_OBLIGATIONS` task. It then
production-populates canonical-free seed fixtures under a guarded `/tmp`
directory and starts exactly five inspection containers: three base checks
and two Kit-treatment checks. Each container gets a unique temporary name,
fails closed on a name collision, and uses raw `docker run` with an overridden
Bash entrypoint, `--network none`, a read-only root, and read-only task inputs.
This raw-Docker path is a controlled exception for prebuilt image inspection;
it is not a launcher or Compose-route inspection mechanism. `--pull=never`
forbids network pulls, so a missing local image is an intentional, actionable
failure. The smoke mounts no credentials and only locates agent, K, Lean,
Lake, and Klean executables/modules. For the Codex image it also requires the
exact frozen toolchain versions; it never executes a model.

The contract fixture proves the six-stage state/provenance path using
deterministic fake command runners; it does not claim real Klean/Lean
execution or semantic soundness. The containers prove each image's declared
user, home, and working directory; seed visibility; required executable
presence; absence of a `/kit-skills` path or mount in base images; and
readability of the approved read-only Kit mount in treatment containers. The
smoke does not prove launcher or Compose routing, normal entrypoint behavior,
authentication, model availability, real K execution, proof closure,
soundness, or HumanEval correctness.

The deterministic generator is a separate image and is verified separately:

```bash
docker build -f docker/klean/Dockerfile \
  -t humaneval-klean-runner:locked .
docker run --rm --pull=never --network none \
  --entrypoint /usr/local/bin/assert-frozen-toolchain \
  humaneval-klean-runner:locked klean
```

The canonical runtime is one indivisible frozen stack:

- Codex CLI `0.144.6`;
- K `7.1.293`, source commit
  `ff15baac9e66426612ec45ff912af7f14965b64a`, and Jammy base-image digest
  `sha256:f3f64ab72bd7b560082d50e4c6c23e107025cf217ca62ab73700104fc45de09a`;
- pyk/Klean `7.1.293` from that exact K commit; and
- Lean `4.22.0`, commit
  `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

Both pipeline Dockerfiles pin these identities, downloaded archive checksums,
and the Codex CLI package. Every model, audit, Klean-generation, and Lean-proof
entrypoint runs the same fail-fast check before doing stage work; a mixed
runtime exits as a harness error. Runtime launchers use `--pull=never` and do
not download dependencies.

## Evaluation and launch gate

The generation runner's final marker is
`RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED>`. `KPROVE_PASSED` means every required
positive target-proof command printed `#Top` and exited zero; it is an
execution result, not an automatic soundness or intent-validation judgment.

After generation, transfer only the candidate `solution.py` and necessary
generated proof artifacts to a separate verifier whose hidden tests and oracle
are never visible to the generation agent. Keep that verifier outside the
mounted task and outside this repository's generation workflow.

## Independent proof audit

The audit runner starts a fresh `gpt-5.6-sol`/`xhigh` Codex session in a
separate 8 GiB, one-hour container. It mounts the complete generated task,
`canonical.py`, the trusted prompt and translator, and Kit read-only. Only the
external `audits/` output is persistent and writable; proof reconstruction and
mutations use `/tmp/audit-work`.

Inspect the route without starting a model:

```bash
docker/audit/run_task.sh --print-config \
  codex-gpt-5.6-sol-xhigh-kit-semantics-fix-kit 104-unique-digits
```

Start one independent audit:

```bash
docker/audit/run_task.sh \
  codex-gpt-5.6-sol-xhigh-kit-semantics-fix-kit 104-unique-digits
```

For `semantics` and `kit-semantics`, the auditor also receives the trusted
reference semantics for an integrity comparison. For `bare` and `kit`, it does
not receive that reference: it must validate the candidate's individual
`semantic.k` from its rules and concrete behavior.

Each completed output preserves `REVIEW.md`, the exact audit prompt, logs,
structured trace, metrics, input hashes, evidence, and `verdict.json`.
`PASS` and `CONCERNS` mean `LEGIT`; `FAIL` means `NOT_LEGIT`. A timeout,
container failure, or malformed review is `AUDIT_ERROR`, never a proof verdict.

Stop before any sample launch. Complete population, lock checks, static tests,
no-model smoke, and `--print-config` inspection, then wait until the user
briefs the exact sample launch. Only that later briefing authorizes invoking a
launcher without `--print-config`.

No live model call is part of the automated test suite. Container builds and
offline executable checks are safe verification steps; a stage launcher
without inspection/dry-run mode is not.
