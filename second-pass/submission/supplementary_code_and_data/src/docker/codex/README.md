# Codex benchmark runner

This runner supports the legacy flat benchmark route and the new stage-oriented
pipeline. New pipeline runs use an 8 GiB container with K, pinned Klean, Lean,
Lake, and Codex. The task workspace, immutable invocation evidence, and
persistent `CODEX_HOME` are separate mounts.

The image and every stage entrypoint fail closed unless the runtime is exactly
Codex `0.144.6`, K and pyk/Klean `7.1.293`, and Lean `4.22.0`, with the source
commits recorded in `data/klean-toolchain.lock.json`.

Each populated task begins with `prompt.py`, `py2mpy.py`, and
`run-input.json`. A semantics condition also has `reference-semantics/`. The
launcher calls `tools/populate_runs.py --validate-task` before printing a
configuration or invoking Docker, so missing, stale, linked, or forbidden seed
inputs fail closed.

## Conditions and isolation

| Suffix | Prompt | Reference semantics | Kit |
| --- | --- | ---: | ---: |
| `bare` | `prompts/bare.md` | no | no |
| `semantics` | `prompts/with-semantics.md` | yes | no |
| `kit` | `prompts/kit-bare.md` | no | yes |
| `kit-semantics` | `prompts/kit-semantics.md` | yes | yes |

The base `docker-compose.yml` has no Kit mount and uses `KIT=0`.
`docker-compose.kit.yml` is a Kit-only override that adds exactly one
read-only `/kit-skills` mount and uses `KIT=1`. The entrypoint copies those
skills into the ephemeral profile only for a Kit condition.

Config names use `codex-<model>-xhigh-<condition>`, for example
`codex-gpt-5.6-sol-xhigh-kit-semantics`.

## Setup and population

```bash
docker build -f docker/codex/Dockerfile \
  -t humaneval-codex-runner:latest .
mkdir -p secrets/codex
cp ~/.codex/auth.json secrets/codex/auth.json
```

Credentials under `secrets/` are ignored and must never be committed.

From the repository root, populate any or all supported conditions. This only
creates/validates task folders; it does not start Codex:

```bash
python3 tools/populate_runs.py \
  codex-gpt-5.6-sol-xhigh-bare \
  codex-gpt-5.6-sol-xhigh-semantics \
  codex-gpt-5.6-sol-xhigh-kit \
  codex-gpt-5.6-sol-xhigh-kit-semantics
```

## Safe route inspection

Use `--print-config` to inspect a populated task. It runs the same
`--validate-task` check used immediately before a real launch and exits before
Docker or Codex is invoked:

```bash
docker/codex/run_task.sh --print-config \
  codex-gpt-5.6-sol-xhigh-kit-semantics 8-sum-product
```

Do not call `run_task.sh` without `--print-config` until the sample launch has
been explicitly briefed. `run_matrix.sh --dry-run` lists pending tasks only;
actual matrix execution launches models.

After launch authorization, the same wrapper without `--print-config` runs one
task, while `run_matrix.sh --jobs N` delegates every pending `codex-*` task to
that wrapper. A folder containing `metrics.json` is treated as completed.

## Outputs and status

The entrypoint writes `codex-output.log`, `codex-last.txt`, a structured
`codex-trace/`, and `metrics.json` into the task directory. The shared
A shared status helper reads the result line and ignores archived/hidden
directories.

The required runner marker is
`RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED>`. `KPROVE_PASSED` reports that every
required positive target-proof command printed `#Top` and exited zero; it does
not by itself claim a validated or sound proof.

## Canonical six-stage pipeline route

Create runs with `python3 tools/create_run.py`; the run ID is distinct from
the reusable configuration name. The model-bearing stages are
`01-k-proof`, `03-lemma-discovery`, and optional `05-lean-proof`. All three
are bound to the exact same Codex session UUID and persistent `CODEX_HOME`;
the resume launchers never start a replacement session or reroll the
candidate.

Stage 1 is:

```bash
docker/codex/run_task.sh <run-id> <problem>
```

It writes candidate files only to
`runs/<run-id>/tasks/<problem>/01-k-proof/workspace/`. Invocation logs and
traces go to numbered `invocations/`. The exact same Codex session lives under
`runner-state/<run-id>/<problem>/codex-home/`; it is resumed once only after a
wrapper-owned timeout. The initial allocation is 3,600 seconds and the single
continuation adds at most another 3,600 seconds.

The Compose runner relaxes Docker's seccomp filter without adding capabilities
so Codex's bundled bubblewrap can create its unprivileged namespace. The
entrypoint preflights that exact sandbox before invoking the model. An
unchanged Stage 1 timeout continuation with protected namespace-denial evidence
may be resumed once with:

```bash
python3 tools/stage1_runner.py --infrastructure-retry <run-id> <problem>
```

This creates `003-infrastructure-retry`, uses the same session and workspace,
and preserves `001` and `002`. A zero-duration, evidence-empty harness failure
in `003` permits one corrected `004`; no later retry is allowed.

After a selected Stage 2 `LEGIT` K audit, Stage 3 is invoked separately:

```bash
docker/codex/resume_lemma_discovery_task.sh <run-id> <problem>
```

Stage 3 resumes the same Codex session from Stage 1 for one 20-minute
(1,200-second) default allocation. It mounts the frozen Stage 1 K workspace
and deterministic rule inventory read-only and writes only below
`03-lemma-discovery/`. The agent does not receive Stage 2 audit feedback.
There is no Stage 3 timeout continuation and no later retry of a non-error
classification.

Stage 4 is model-free. After its selected result is `PASS`, Stage 5 is:

```bash
docker/codex/resume_lean_task.sh <run-id> <problem>
```

Stage 5 resumes the same session from Stages 1 and 3, mounts the original K
workspace, protected Stage 3 manifest, and selected Stage 4 generated project
read-only, and makes only `05-lean-proof/workspace/` writable. It does not
receive Stage 2 audit feedback or failed Stage 4 diagnostics. Stage 5 has a
one-hour initial budget and a two-hour default cumulative budget
(3,600 + 3,600 seconds); only its wrapper-owned timeout can allocate the
second hour.

If Stage 4 records `KLEAN_NO_OBLIGATIONS`, Stage 5 remains absent and the task
still proceeds to Stage 6 classification-only audit. Proof-bearing tasks
proceed to Stage 6 classification-plus-proof audit after successful Stage 5.

The complete `runs/<run-id>/` task tree is immutable result evidence after
completion. `runner-state/` contains credentials and full session state and
must not be archived or committed.

Use these no-model commands before launching:

```bash
python3 tools/run_pipeline.py status <run-id>
python3 tools/run_pipeline.py dry-run <run-id>
```

The remaining deterministic-stage and fresh-auditor entrypoints are:

```bash
docker/audit/run_task.sh <run-id> <problem>
docker/klean/generate_task.sh <run-id> <problem>
docker/klean/check_task.sh <run-id> <problem>
docker/klean-audit/run_task.sh <run-id> <problem>
```

No live model call is part of the unit or container smoke tests.
