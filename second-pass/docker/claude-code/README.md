# Claude Code benchmark runner

This runner starts one headless Claude Code session in an 8 GB, one-hour K
Framework container. Only the selected task directory is mounted at `/work`;
OAuth or API-key auth is isolated from task inputs.

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
read-only `/kit-skills` mount and uses `KIT=1`. Kit conditions omit Claude's
`--safe-mode` only so the locked skills can be discovered; the profile remains
ephemeral and otherwise clean.

Config names use
`claude-code-<opus|fable>-xhigh-<version-label>-<condition>`, for example
`claude-code-opus-xhigh-4-8-kit-semantics`. The anchored grammar maps `opus`
and `fable` to the corresponding runner model and always uses `xhigh` effort.

## Setup and population

```bash
cd docker/claude-code
docker build -t humaneval-claude-runner .

# OAuth option (read-only mount):
mkdir -p secrets/claude
cp ~/.claude/.credentials.json secrets/claude/.credentials.json
```

Alternatively, put `ANTHROPIC_API_KEY` in the ignored `.env` and adjust the
auth volume as documented in `docker-compose.yml`. Credentials under
`secrets/` and `.env` must never be committed.

From the repository root, populate any or all supported conditions. This only
creates/validates task folders; it does not start Claude:

```bash
python3 tools/populate_runs.py \
  claude-code-opus-xhigh-4-8-bare \
  claude-code-opus-xhigh-4-8-semantics \
  claude-code-opus-xhigh-4-8-kit \
  claude-code-opus-xhigh-4-8-kit-semantics
```

## Safe route inspection

Use `--print-config` to inspect a populated task. It runs the same
`--validate-task` check used immediately before a real launch and exits before
Docker or Claude is invoked:

```bash
docker/claude-code/run_task.sh --print-config \
  claude-code-opus-xhigh-4-8-kit-semantics 8-sum-product
```

Do not call `run_task.sh` without `--print-config` until the sample launch has
been explicitly briefed. `run_matrix.sh --dry-run` lists pending tasks only;
actual matrix execution launches models.

After launch authorization, the same wrapper without `--print-config` runs one
task. `run_matrix.sh --jobs N` discovers only direct `claude-code-*`
configurations and delegates each pending task to the wrapper. The quota-aware
throttle also delegates each actual task launch to this wrapper. Reset helpers
preserve only the validated seed inputs and remove run artifacts after a
recognized auth/session-limit failure.

## Outputs and status

The entrypoint writes `claude-output.json`, `claude-stderr.log`,
`claude-trace/`, and `metrics.json` into the task directory. Exit `124` is the
wall-clock timeout; exit `137` can be the kill-after signal or OOM. The shared
`status.sh` reports active Codex, Claude, and OpenCode configurations while
ignoring archived and hidden directories.

The required runner marker is
`RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED>`. `KPROVE_PASSED` reports that every
required positive target-proof command printed `#Top` and exited zero; it does
not by itself claim a validated or sound proof.
