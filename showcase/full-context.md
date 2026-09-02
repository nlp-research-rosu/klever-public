# Second-pass campaign: full experimental context

Reference card for the second-pass HumanEval campaign (164 problems, six
stages, three arms). Every element of the controlled environment — model,
reasoning level, system prompt, user prompt, visible inputs, tools — is
recorded on disk; this page says exactly where.

## Model and reasoning level

| Item | Value | Recorded in |
| --- | --- | --- |
| Model | `gpt-5.6-sol` (provider `openai`) | per-invocation Codex rollout trace, e.g. [3-below-zero stage-1 trace](../second-pass/runs/kit_semantics/tasks/3-below-zero/01-k-proof/invocations/001-initial/codex-trace/2026/07/31/rollout-2026-07-31T09-48-22-019fb8a5-d12d-7dd1-b954-b4a7bacc6d44.jsonl) (`"model":"gpt-5.6-sol"`) |
| Reasoning effort | `xhigh` | same trace (`"reasoning_effort":"xhigh"`) |
| Harness | OpenAI Codex CLI `0.144.6` | same trace (`"cli_version":"0.144.6"`), pinned in [klean-toolchain.lock.json](../second-pass/submission/supplementary_code_and_data/configs/klean-toolchain.lock.json) and installed by the [Dockerfile](../second-pass/docker/codex/Dockerfile) (`@openai/codex@0.144.6`) |
| Run-config family | `codex-gpt-5.6-sol-xhigh-{bare,semantics,kit-semantics}` | `config` field of the archived [run-input.json]; also recorded per task in each stage's `audit-input.json` and rollout trace(../second-pass/runs/bare/tasks/108-count-nums/02-k-audit/executions/001/evidence/provenance/run-input.json) |
| System prompt | Codex CLI default base instructions, captured verbatim per session | `base_instructions` in the `session_meta` line of every rollout trace (same file as above) |
| User prompt | exact text saved per invocation as `prompt.txt` | e.g. [3-below-zero stage-1 prompt.txt](../second-pass/runs/kit_semantics/tasks/3-below-zero/01-k-proof/invocations/001-initial/prompt.txt); its SHA-256 matches `instruction_prompt_sha256` in [task.json](../second-pass/runs/kit_semantics/tasks/3-below-zero/task.json) and the `prompt_sha256` in [invocation.json](../second-pass/runs/kit_semantics/tasks/3-below-zero/01-k-proof/invocations/001-initial/invocation.json) |

So for any task, the complete context of any model session is under
`runs/<arm>/tasks/<problem>/<stage>/invocations/<n>/`: the prompt sent
(`prompt.txt`), the full transcript including system prompt and model/effort
config (`codex-trace/.../rollout-*.jsonl`), and the container image id and
workspace hashes (`invocation.json`).

## Per-stage prompts

All prompt templates live in [second-pass/prompts/](../second-pass/prompts/).
Stages 1, 2, 3, 5, 6 are model sessions; stage 4 is deterministic and
model-free (per the [supplementary README](../second-pass/submission/supplementary_code_and_data/README.md)).

| Stage | Prompt file | What the session is asked to do |
| --- | --- | --- |
| 1 `01-k-proof` (bare arm) | [bare.md](../second-pass/prompts/bare.md) | Implement the HumanEval task and prove it correct in K, writing its own semantics |
| 1 `01-k-proof` (semantics arm) | [with-semantics.md](../second-pass/prompts/with-semantics.md) | Same task, using the provided frozen reference semantics |
| 1 `01-k-proof` (kit condition) | [kit-bare.md](../second-pass/prompts/kit-bare.md) | Own-semantics variant with the read-only Kit skill bundle mounted |
| 1 `01-k-proof` (kit_semantics arm) | [kit-semantics.md](../second-pass/prompts/kit-semantics.md) | Reference semantics plus the read-only Kit skill bundle |
| 2 `02-k-audit` | [audit.md](../second-pass/prompts/audit.md) | Independent adversarial audit of the K proof; fresh session, candidate treated as untrusted evidence |
| 3 `03-lemma-discovery` | [lemma-discovery.md](../second-pass/prompts/lemma-discovery.md) | Stage-1 session continues to classify every rule in the proof's trust boundary (operational rule vs. domain lemma vs. definition) |
| 4 `04-klean-generation` | none (no model) | Deterministic Dockerized exporter translates the frozen K workspace and stage-3 manifest into a Lean 4 project, with a mechanical gate |
| 5 `05-lean-proof` | [klean-prove.md](../second-pass/prompts/klean-prove.md) | Session continues to prove the generated Lean target `Proof.final` against the frozen, read-only Base project |
| 6 `06-lean-audit` | [klean-audit.md](../second-pass/prompts/klean-audit.md) | Independent adversarial audit of the stage-3 classification, stage-4 generation, and stage-5 Lean proof |

Continuation prompts for interrupted invocations (resource limits, transient
failures) are also frozen: [timeout-resume.md](../second-pass/prompts/timeout-resume.md),
[oom-resume.md](../second-pass/prompts/oom-resume.md),
[terminal-resume.md](../second-pass/prompts/terminal-resume.md), and
[infrastructure-resume.md](../second-pass/prompts/infrastructure-resume.md).

## What each arm can see

Every fresh task starts with exactly `prompt.py` (the unmodified HumanEval
prompt), the `py2mpy.py` translator, and `run-input.json` in the writable
`/work` mount; the launcher adds only the condition-specific inputs below.
The generation agent never receives `canonical.py`, hidden tests, an oracle,
a prior candidate, or audit feedback. This mirrors the condition-visible-inputs
table in the [second-pass README](../second-pass/README.md).

| Condition | Instruction prompt | Initial `/work` seed | Kit input |
| --- | --- | --- | --- |
| `bare` | `prompts/bare.md` | `prompt.py`, `py2mpy.py`, `run-input.json` | none |
| `semantics` | `prompts/with-semantics.md` | the common seed plus `reference-semantics/` | none |
| `kit` | `prompts/kit-bare.md` | the common seed | read-only `/kit-skills` |
| `kit-semantics` | `prompts/kit-semantics.md` | the common seed plus `reference-semantics/` | read-only `/kit-skills` |

The archived campaign's three arms are `bare`, `semantics`, and
`kit_semantics`; the base Compose file has no Kit mount, and only a Kit
condition selects the override that adds `/kit-skills`.

## Tools and environment

All agent and audit stages run inside one container image, defined by
[docker/codex/Dockerfile](../second-pass/docker/codex/Dockerfile): the
K framework base image (`kframework-k:ubuntu-jammy-7.1.293`, digest-pinned)
plus elan/Lean 4, pyk, Node, and the Codex CLI, with the toolchain asserted
frozen at build time and the pinned toolchain trees under `/opt` made read-only. Inside the workspace the
agent has `kompile`, `krun`, `kprove`, and `python3` on PATH.

Every version and input is pinned by lock files, mirrored for review in
[supplementary configs/](../second-pass/submission/supplementary_code_and_data/configs/)
(see its [README](../second-pass/submission/supplementary_code_and_data/configs/README.md)):

| Lock file | Pins |
| --- | --- |
| [klean-toolchain.lock.json](../second-pass/submission/supplementary_code_and_data/configs/klean-toolchain.lock.json) | K `7.1.293` (commit `ff15baac9e66`), pyk `7.1.293`, Lean `leanprover/lean4:v4.22.0` (commit `ba2cbbf09d49`), Codex CLI `0.144.6` |
| [audit-campaign.lock.json](../second-pass/submission/supplementary_code_and_data/configs/audit-campaign.lock.json) | Frozen stage-2 audit conditions: audit image digest, audit prompt SHA-256, campaign id, and the v3 docstring-first ground-truth amendment |
| [kit-skills.lock.json](../second-pass/submission/supplementary_code_and_data/configs/kit-skills.lock.json) | Exact file inventory and commit (`46af96a89de7`) of the generation Kit skill bundle mounted at `/kit-skills` |
| [audit-kit-skills.lock.json](../second-pass/submission/supplementary_code_and_data/configs/audit-kit-skills.lock.json) | Exact inventory and commit (`b9135325caf1`) of the separate frozen auditor Kit bundle |
| [klean-audit-tools.lock.json](../second-pass/submission/supplementary_code_and_data/configs/klean-audit-tools.lock.json) | SHA-256 of every stage-4/6 mechanical-checker tool (`klean.py`, gates, contracts), verified inside the image at build time |
| [humaneval-prompts.lock.json](../second-pass/submission/supplementary_code_and_data/configs/humaneval-prompts.lock.json) | SHA-256 of all 164 task inputs from `openai/openai_humaneval` |

Per-task provenance closes the loop: each `task.json` (e.g.
[3-below-zero](../second-pass/runs/kit_semantics/tasks/3-below-zero/task.json))
records the condition, the Kit commit and skills-tree hash, and SHA-256 of the
problem prompt, instruction prompt, translator, and reference semantics that
this particular task actually saw.

## Reproduction

The AAAI supplementary package at
[second-pass/submission/supplementary_code_and_data/](../second-pass/submission/supplementary_code_and_data/)
is self-contained — source, container definitions, prompts, pinned configs,
task inputs, and per-task result artifacts — and its
[README](../second-pass/submission/supplementary_code_and_data/README.md)
covers rebuilding the images and re-running the pipeline.
