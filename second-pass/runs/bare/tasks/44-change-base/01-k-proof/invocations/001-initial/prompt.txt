# Implement and prove a HumanEval task correct in K — writing your own semantics

You are working entirely inside the current directory. Everything you produce
must be written here. The K toolchain (`kompile`, `krun`, `kprove`) and
`python3` are on PATH.

## Inputs

- `prompt.py` — the exact original HumanEval task prompt. It contains the
  required entry-point signature, natural-language contract, examples, and any
  helper code intentionally supplied with the task. It contains no completed
  implementation of the target function. Do not modify it.
- `py2mpy.py` — the fixed CPython-AST to K-constructor translator. Do not
  modify it.

There is no supplied K semantics in this condition.

## Required work

1. Read `prompt.py`, then create `solution.py` and implement the requested
   entry point yourself. Preserve the signature. You may reuse helper or setup
   code that the prompt intentionally supplies.
2. Keep `solution.py` within the subset accepted by `py2mpy.py` and generate
   `solution.mpy` with `python3 py2mpy.py solution.py > solution.mpy`.
3. Write `semantic.k`, `verification.k`, and `spec.k`.
4. Exercise the program with `krun`, prove every claim in `spec.k` with
   `kprove`, and record exact commands in `prove.sh`.

## Deliverables

`solution.py`, `solution.mpy`, `semantic.k` and any helper K files,
`verification.k`, `spec.k`, and `prove.sh`.

The container has 8 GB of memory. Keep working while a concrete path remains;
if the proof cannot close, preserve the best artifacts and explain the blocker
in `NOTES.md`.

End your final message with exactly one line and nothing after it:
RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED> — <one sentence>

Choose exactly one marker using this ordered decision; stop at the first
matching case.

1. `KPROVE_PASSED` iff every required positive target-proof command (commands
   intended to close the task's proof claims) printed `#Top` and exited 0.
   Expected-failure mutation probes and other negative validation probes are
   judged by their expected non-zero result and do not disqualify this marker.
2. Otherwise, `BLOCKED` iff a concrete hard blocker—such as a missing required
   input, capability, tool, or semantic support—prevented completion. Name it.
3. Otherwise, `PARTIAL`: the positive proof condition was not met; preserve and
   report the best artifacts or progress available.

This ordered precedence is total and mutually exclusive. Incomplete
deliverables or a later Gate status do not create a second marker. This runner
marker reports positive proof execution only, not a `VALIDATED` judgment.
