# Supplementary Code and Data Package

Anonymous supplementary material for double-blind review. This package
contains the source code, container definitions, prompts, pinned
configuration, task inputs, per-arm results tables, and the per-task
result artifacts (proof sources, classifications, generated Lean targets,
proofs, and audit reviews) for the paper's three-arm formal-verification
experiment over the 164 HumanEval tasks.

This is a snapshot of the experiment state at packaging time. The results
tables in `data/results/` report the current recorded status of every
task in every arm, exactly as selected on disk by the pipeline's audit
stages.

## Experimental arms

The experiment runs the same 164 HumanEval tasks under three conditions
that differ only in what the proof-authoring model receives:

- **bare** — no skill bundle and no reference semantics: the model must
  author its own K semantics for the modeled Python subset alongside the
  proof.
- **semantics** — the frozen K reference semantics
  (`src/data/reference/`) is provided; no skill bundle.
- **kit_semantics** — both the reference semantics and the vendored
  K-verification skill bundle (`src/data/skills/`) are provided.

Every arm passes through the independent stage-2 K audit; the primary
verdict for the two control arms (bare, semantics) is that stage-2
status. The kit_semantics arm continues through the full six-stage
pipeline, and its primary verdict is the stage-6 adversarial Lean-audit
status. Control-arm tasks whose stage-2 audit was legitimate also
proceeded through the later stages; their tables include those statuses
where recorded. In every audit, `PASS` and `CONCERNS` count as
legitimate (`LEGIT`); `FAIL` does not.

## Pipeline overview

Each HumanEval task flows through six stages. Stages 1, 2, 3, 5, and 6 are
model sessions (OpenAI Codex CLI inside a container); stage 4 is
deterministic and model-free.

1. `01-k-proof` — a model authors a K-framework proof that the candidate
   solution satisfies a specification derived from the task docstring.
2. `02-k-audit` — an independent model session audits the K proof
   (fresh session, no shared state with stage 1).
3. `03-lemma-discovery` — the stage-1 session classifies every
   simplification rule it relied on across a trust boundary
   (operational rule vs. domain lemma vs. definition), producing a
   validated trust-boundary manifest.
4. `04-klean-generation` — a deterministic, Dockerized exporter
   (`docker/klean/`) translates the frozen K workspace and the protected
   stage-3 manifest into a Lean 4 project whose target proposition encodes
   the domain-lemma obligations. A hard mechanical gate rechecks the
   mapping, hashes, and a full `lake build`. No model runs.
5. `05-lean-proof` — a model session proves the generated Lean target
   (`Proof.final`) against the frozen generated Base project.
6. `06-lean-audit` — an independent adversarial audit
   (`docker/klean-audit/` launching the `docker/codex/` runner image):
   a fresh model session plus a no-network mechanical container re-verify
   the classification, provenance hashes, `lake clean && lake build`,
   the exact target identity, axiom usage, and the operational bridge of
   the proof. Verdicts are `PASS`/`CONCERNS` (legitimate) or `FAIL`.

Every stage records immutable numbered artifacts under
`runs/<run-id>/tasks/<task>/<stage>/`, with a `selected.json` marking the
authoritative selection per stage. Tool and prompt versions are pinned by
the lock files in `configs/` (mirrored at `src/data/` where the runners
read them).

## Package layout

```text
supplementary_code_and_data/
├── README.md                  this file
├── requirements.txt           no third-party Python packages required
├── src/                       runnable tree (repository-root layout)
│   ├── tools/                 pipeline runners, exporter, mechanical gates
│   ├── prompts/               stage prompts for the model sessions
│   ├── docker/                container definitions and stage entrypoints
│   │   ├── codex/             model-session runner image (stages 1,3,5; audits)
│   │   ├── audit/             stage-2 independent K-audit launcher
│   │   ├── klean/             stage-4 deterministic exporter image
│   │   └── klean-audit/       stage-6 independent audit launcher + checker
│   └── data/                  inputs and pinned state the runners read
│       ├── questions/         the 164 HumanEval task inputs
│       ├── skills/            vendored generation skill bundle (Kit)
│       ├── audit-skills/      vendored audit skill bundle
│       ├── reference/         frozen K reference semantics (current, v3)
│       ├── semantic-archive/v1, v2  earlier frozen semantics
│       │                      versions, addressed by
│       ├── reference-semantics-versions.json  sha256 → version-tree map the
│       │                      stage-2 audit uses to mount the exact semantics
│       │                      a candidate was generated with
│       ├── reference-semantics.md          semantics scope/validation notes
│       ├── stage4-producer-sources/        content-addressed stage-4 producer
│       │                      source bundles; the stage-6 mechanical check
│       │                      resolves the recorded producer hash here
│       │                      (path fixed by the hash-pinned checker code)
│       ├── kit-archive/       historic Kit skill bundles by commit, for
│       │                      re-validating recorded provenance (fresh runs
│       │                      use data/skills directly; path fixed by the
│       │                      hash-pinned checker code)
│       └── *.lock.json        pinned tool/prompt/toolchain versions
├── scripts/
│   ├── census.py              tallies audit statuses (runs tree or CSV)
│   ├── s6pump.sh, s6daemon.sh, s6sweep.sh, s6sweepd.sh
│   │                          path-sanitized operational audit drivers
├── configs/                   reviewer-facing copies of all lock files
├── data/artifacts/            per-task result artifacts, one dir per arm
│   ├── kit_semantics/<task>/  full six-stage artifacts (see below)
│   ├── bare/<task>/           control-arm artifacts
│   └── semantics/<task>/      control-arm artifacts
├── data/results/
│   ├── results_kit_semantics.csv   task, stage-6 status, obligation count
│   ├── results_bare.csv            task, stage-2/4/6 statuses, obligations
│   ├── results_semantics.csv       task, stage-2/4/6 statuses, obligations
│   ├── arms_summary.csv            the per-arm headline comparison
│   └── census.json                 per-arm status tallies at packaging time
└── expected_results/
    ├── census_kit_semantics.txt, census_bare.txt, census_semantics.txt
    └── claims_to_artifacts.md paper claim → package artifact map
```

The full per-task run trees (invocation logs, traces, raw audit evidence,
compiled binaries) exceed the supplementary upload allowance and are not
included. This package contains the complete code, configuration, and
task inputs needed to produce them, the agent-written result artifacts
for all 164 tasks of every arm, and the per-arm result tables.

## Per-task result artifacts (`data/artifacts/`)

One directory per arm, then one per task: all 164 tasks ship artifacts
in every arm, whatever their *primary-verdict* status (kit_semantics:
stage 6; bare and semantics: stage 2). Tasks whose primary verdict is
`FAIL` ship the artifacts of the stages they completed — in the control
arms that is the authored `k_proof/` and the selected stage-2 audit
review recording the failure. Legitimate (`PASS`/`CONCERNS`) tasks ship
the full selected artifact set described below.

Contents map to the six stages as follows: stage 1 → `k_proof/` (the
authored `.k` specification/verification sources — in the bare arm this
includes the model's own authored semantics — plus `prompt.py`,
`prove.sh`, and any authored proof notes such as `PROOF.md`); stage 2 →
`audits/stage2-k-audit-REVIEW.md` (the selected independent K-audit
review); stage 3 → `classification/` (`DISCOVERY.md` and the validated
`validated-trust-boundary.json` with per-rule classifications and
rationales); stage 4 → `lean_proof/Base/` (the deterministic exporter's
generated Lean tree — the root of every `lean_proof/Base/` directory
contains the four per-task export manifests: `obligation-map.json`,
`generator-manifest.json`, `trust-inventory.json`, and
`export-result.json`); stage 5 → `lean_proof/` (the authored
`Proof.lean` and support files); stage 6 →
`audits/stage6-lean-audit-REVIEW.md` (the selected independent
adversarial audit review). Stage-4 exports are deterministic per
exporter version: the shipped `Base/` trees are the campaign's selected
outputs, and re-running the included exporter (`src/tools/klean.py` and
`src/tools/klean_export.py` via `src/docker/klean/`) reproduces trees
under the current, final exporter version.

Later-stage artifacts appear only where a legitimate selected artifact
exists. In the kit_semantics arm every task has stages 1-3 and 6, and
`lean_proof/` exists for the tasks whose selected stage-4 generation
exports obligations (classification-only tasks ship `k_proof/`,
`classification/`, and `audits/` alone). In the control arms every
legitimate task has stages 1-3 (`FAIL` tasks ship stages 1-2 only);
stage-6 reviews ship where the selected stage-6 audit is legitimate
(bare: 63, semantics: 64), and `lean_proof/` ships where additionally
the selected stage-4 generation exports obligations (bare: 3,
semantics: 17).

Absolute repository paths inside these files are rewritten to `/REPO`.
Audit reviews cite files from their `evidence/` directories; those raw
evidence trees are not included in the package (only the reviews are).

To rebuild a shipped Lean proof against its exact generated Base with
the pinned toolchain (requires `elan`; the `lean-toolchain` files pin
`leanprover/lean4:v4.22.0`, which elan fetches automatically):

```bash
cd data/artifacts/<arm>/<task>/lean_proof
lake build          # builds the Base tree, then the Proof library
```

Verified on this package: `data/artifacts/kit_semantics/55-fib/lean_proof`
builds in about 30 seconds (first build of a task also elaborates its
Base). Note the generated Base packages set
`buildDir = "/tmp/klean-generated-build"` (a scratch location inherited
from the containerized pipeline); remove that directory between different
tasks' builds to avoid stale cache confusion.

## Environment

- Operating system: Linux (x86-64). All experiment stages run inside
  Docker containers.
- Python: 3.10 inside the containers; the host tooling is routinely run
  with Python 3.14. Any Python >= 3.10 should work on the host. Only the
  Python standard library is used (see `requirements.txt`).
- Hardware: any x86-64 machine with Docker. Containers are memory-capped;
  allow 4-8 GiB RAM per concurrent container (the stage-6 audit container
  is capped at 8 GiB). No GPU is required.
- Pinned toolchain (see `configs/klean-toolchain.lock.json`):
  K framework 7.1.293 (commit-pinned), pyk/Klean 7.1.293,
  Lean 4 `leanprover/lean4:v4.22.0` (commit-pinned),
  Codex CLI 0.144.6.
- Random seeds: the model-bearing stages (1, 2, 3, 5, 6) are LLM sessions
  and are not seed-reproducible; their outputs are archived by the
  pipeline as immutable evidence. Stage 4 and the stage-6 mechanical gate
  are deterministic given frozen inputs.

## What you can run without model credentials

The model stages require an OpenAI Codex CLI subscription; nothing in this
package requires the authors' accounts or infrastructure. Without any
credentials you can:

1. Rebuild both container images from the pinned definitions
   (from `src/`):

   ```bash
   cd src
   docker build -f docker/klean/Dockerfile -t humaneval-klean-runner:locked .
   docker build -f docker/codex/Dockerfile -t humaneval-codex-runner:latest .
   ```

   Estimated time: roughly 30-60 minutes each on a typical workstation
   (the K framework and Lean toolchains are downloaded/pinned during the
   build).

2. Verify the pinned stage-4/6 tool bundle against its lock
   (this rechecks SHA-256 hashes of the shipped mechanical tools):

   ```bash
   cd src
   python3 docker/klean-audit/check_tool_bundle.py \
     --root . --lock data/klean-audit-tools.lock.json
   ```

3. Populate and validate task directories for a run (creates/validates
   task folders only; starts no model):

   ```bash
   cd src
   python3 tools/populate_runs.py \
     codex-gpt-5.6-sol-xhigh-bare \
     codex-gpt-5.6-sol-xhigh-semantics \
     codex-gpt-5.6-sol-xhigh-kit-semantics
   python3 tools/run_pipeline.py status <run-id>
   python3 tools/run_pipeline.py dry-run <run-id>
   ```

4. Rebuild any shipped Lean proof against its exact generated Base with
   the pinned Lean toolchain (requires `elan`; ~0.5-5 minutes per task):

   ```bash
   cd data/artifacts/<arm>/<task>/lean_proof && lake build
   ```

5. Re-tally the packaged per-arm results tables (seconds):

   ```bash
   python3 scripts/census.py --results data/results/results_kit_semantics.csv
   python3 scripts/census.py --results data/results/results_bare.csv --column stage2_status
   python3 scripts/census.py --results data/results/results_semantics.csv --column stage2_status
   ```

   Expected outputs: `expected_results/census_kit_semantics.txt`,
   `census_bare.txt`, `census_semantics.txt`.

Given a run tree in which stages 1-3 have completed for a task, stage 4 is
fully deterministic and model-free:

```bash
cd src
docker/klean/generate_task.sh <run-id> <problem>   # ~minutes per task
docker/klean/check_task.sh <run-id> <problem>
```

## What requires model credentials

Stages 1, 2, 3, 5, and 6 launch model sessions through the Codex CLI.
To run them, place a valid Codex CLI credential at
`src/docker/codex/secrets/codex/auth.json` (never committed or shipped),
then, from `src/`:

```bash
docker/codex/run_task.sh <run-id> <problem>                  # stage 1 (~1-2 h)
docker/audit/run_task.sh <run-id> <problem>                  # stage 2 (~1 h)
docker/codex/resume_lemma_discovery_task.sh <run-id> <problem>  # stage 3 (~20 min)
docker/codex/resume_lean_task.sh <run-id> <problem>          # stage 5 (~1-2 h)
docker/klean-audit/run_task.sh <run-id> <problem>            # stage 6 (~1 h)
```

`scripts/s6pump.sh` and the accompanying daemon scripts are the
path-sanitized operational drivers used to keep batches of stage-6 audits
running; they are provided for completeness.

### Re-pinning the stage-2 audit image gate

`docker/audit/run_task.sh` refuses to launch unless the local
`humaneval-codex-runner` image matches the `audit_image_id` recorded in
`data/audit-campaign.lock.json`. Docker image IDs are content-addressed
per local build and are not bit-reproducible across hosts, so after
rebuilding the image you must re-pin this one field before launching
stage-2 audits:

```bash
cd src
python3 - <<'PY'
import json, pathlib, subprocess
image_id = subprocess.check_output(
    ["docker", "image", "inspect", "-f", "{{.Id}}",
     "humaneval-codex-runner:latest"], text=True).strip()
lock = pathlib.Path("data/audit-campaign.lock.json")
data = json.loads(lock.read_text())
data["audit_image_id"] = image_id
lock.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
PY
```

Every other field of the campaign lock (prompt hash, Kit lock hash,
toolchain versions) is content-derived from files shipped in this
package and needs no change. The Kit locks record
`"source_repository": "ANONYMIZED"`; the historic-commit fallback that
would consult that repository is instead backed by the vendored
`data/kit-archive/<commit>/` bundles, and fresh runs resolve the current
lock to `data/skills` without consulting either.

## Results in this package

`data/results/arms_summary.csv` is the headline per-arm comparison: for
each arm, the primary-verdict stage and its `LEGIT` (= `PASS` +
`CONCERNS`), `PASS`, `CONCERNS`, `FAIL`, and not-reached counts over the
164 tasks.

Per-arm tables list every task. `results_kit_semantics.csv` gives the
currently selected stage-6 audit status (`PASS`, `CONCERNS`, `FAIL`, or
`NOT_REACHED` when no stage-6 selection is recorded) and the number of
exported Lean proof obligations for the selected stage-4 generation
(blank when no stage-4 generation is selected; `0` denotes a validated
empty domain-lemma set, which still receives a classification-only
stage-6 audit). `results_bare.csv` and `results_semantics.csv` give the
primary stage-2 K-audit status plus the stage-4 and stage-6 selected
statuses and obligation counts where those stages were reached (blank
otherwise). `data/results/census.json` aggregates all three arms.
`data/artifacts/` holds the per-task result artifacts described above.
`expected_results/claims_to_artifacts.md` maps the paper's claims to the
artifacts here.

## Reproducibility checklist quick reference

- Install dependencies: Docker plus Python >= 3.10 (standard library only).
- Data: complete task inputs under `src/data/questions/`; pinned
  semantics and skill bundles under `src/data/`.
- Main experiment: the staged commands above, per task.
- Expected outputs: `data/results/` and `expected_results/`.
