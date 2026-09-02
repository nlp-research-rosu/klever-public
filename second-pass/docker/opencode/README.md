# OpenCode benchmark runner

This runner starts one headless OpenCode session in an 8 GB, one-hour K
Framework container. Only the selected task directory is mounted at `/work`;
API-key auth is mounted read-only.

Each populated task begins with `prompt.py`, `py2mpy.py`, and
`run-input.json`. A semantics condition also has `reference-semantics/`. The
launcher calls `tools/populate_runs.py --validate-task` before printing a
configuration or invoking Docker, so missing, stale, linked, or forbidden seed
inputs fail closed.

## Supported conditions

| Suffix | Prompt | Reference semantics |
| --- | --- | ---: |
| `bare` | `prompts/bare.md` | no |
| `semantics` | `prompts/with-semantics.md` | yes |

OpenCode does not support Kit conditions. A `kit` or `kit-semantics` suffix is
rejected explicitly before task-path resolution. Its base Compose file has no
Kit input.

Known model routes include `opencode-kimi-k3-*` for
`openrouter/moonshotai/kimi-k3` and `opencode-glm-5.2-*` for
`zai-coding-plan/glm-5.2`.

## Setup and population

```bash
cd docker/opencode
docker build -t humaneval-opencode-runner .
```

Place the provider keys in ignored `secrets/api_key.json`; never commit that
file. From the repository root, populate either supported condition. This only
creates/validates task folders; it does not start OpenCode:

```bash
python3 tools/populate_runs.py \
  opencode-kimi-k3-bare \
  opencode-kimi-k3-semantics
```

## Safe route inspection

Use `--print-config` to inspect a populated task. It runs the same
`--validate-task` check used immediately before a real launch and exits before
Docker or OpenCode is invoked:

```bash
docker/opencode/run_task.sh --print-config \
  opencode-kimi-k3-semantics 8-sum-product
```

Do not call `run_task.sh` without `--print-config` until the sample launch has
been explicitly briefed. `run_matrix.sh --dry-run` lists pending tasks only;
actual matrix execution launches models.

After launch authorization, the same wrapper without `--print-config` runs one
task, while `run_matrix.sh --jobs N` delegates every pending `opencode-*` task
to that wrapper.

## Entrypoint and outputs

The `< /dev/null` redirection on `opencode run` is required: a backgrounded
Compose process otherwise leaves stdin attached and can block before the
message is processed. `--print-logs` preserves progress in
`opencode-stderr.log`. The entrypoint may continue the same session after an
empty response, within its original timeout, until it sees a result line or
reaches the bounded retry count.

Outputs are `opencode-output.log`, `opencode-last.txt`, `opencode-stderr.log`,
`opencode-trace/`, and `metrics.json`. The required runner marker is
`RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED>`. `KPROVE_PASSED` reports that every
required positive target-proof command printed `#Top` and exited zero; it does
not by itself claim a validated or sound proof.
