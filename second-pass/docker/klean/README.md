# Deterministic Klean generation

Stage `04-klean-generation` is a model-free translation and sanity gate. The
host requires a selected Stage 2 `LEGIT` result, but the generator container
does not receive the Stage 2 audit. It mounts only the frozen
`01-k-proof/workspace/` and protected Stage 3
`validated-trust-boundary.json` read-only.

The image pins:

- Runtime Verification K commit
  `ff15baac9e66426612ec45ff912af7f14965b64a` (`7.1.293`);
- pyk/Klean `7.1.293` from that checkout; and
- `leanprover/lean4:v4.22.0`.

Build it from the repository root:

```bash
docker build -f docker/klean/Dockerfile \
  -t humaneval-klean-runner:locked .
```

Generate and preflight one eligible problem:

```bash
docker/klean/generate_task.sh <run-id> <problem>
```

The exporter creates a new numbered directory below
`04-klean-generation/generations/`. It records frozen Stage 1 and Stage 3
input hashes, generator provenance, the generated Lean project, the exact
target declaration, the explicit trust inventory, export logs, and preflight
results. It never uses Codex authentication or `runner-state/`.

The exporter binds the protected Stage 3 manifest and generator image ID,
then maps exactly the selected `DOMAIN_LEMMA` rules bijectively to hashed Lean
conjuncts. `SUMMARY_DEFINITION` records remain definition metadata and never
become obligations. The Base project defines the exact parameterized
proposition but contains no proof of it. The hard gate independently rechecks
that mapping, input hashes, target uniqueness and identity, imports, zero Base
proof holes, forbidden proposition trust, the executable-trust allowlist,
`lake clean`, and `lake build`. Only `PASS` is exposed to Stage 5.

A genuinely empty domain set records `KLEAN_NO_OBLIGATIONS`, emits no
`targetStatement`, and skips Stage 5 instead of inventing a `True` target.
This status is not pipeline completion: it still proceeds to Stage 6
classification-only audit. A nonempty generated target proceeds through
Stage 5 and then Stage 6 classification-plus-proof audit.

`KLEAN_PREFLIGHT_ERROR` is not an agent failure and is not automatically
retried. Diagnose it manually, repair the exporter/adapter/pinned toolchain,
and invoke the explicit stage again:

```bash
python3 tools/run_pipeline.py stage <run-id> <problem> 4
```

The failed generation remains immutable evidence and the repaired tooling
creates the next number from the unchanged Stage 1 workspace and Stage 3
manifest. Never edit generated Lean output by hand, change the Stage 1
candidate or classification, or show diagnostics to the benchmark agent.

No live model runs in this stage.
