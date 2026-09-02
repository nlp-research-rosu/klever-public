# Implement and prove a HumanEval task correct in K — using the provided reference semantics

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
- `reference-semantics/` — the supplied read-only K semantics for Python. It
  is not a full Python semantics. Read it, but do not modify any file in it.

## Kit workflow

The Kit K-verification skills are installed and discoverable by the harness.
Start with `using-kit/SKILL.md` and follow its routing. In particular, apply
the shared proof-extension contract and validate Gate A, Gate B, and Gate C.
Write `PROOF.md` beginning with the exact status required by that contract.
Use the shared contract's exact `PROOF.md` headline outcomes:

- If Gate A fails, begin with `Incomplete work`; do not issue a successful
  proof report.
- If Gate A passes and Gate B fails, begin with `SOUND-BUT-LIMITED`.
- If Gates A and B pass and Gate C fails, begin with
  `FORMALLY-SOUND-UNVALIDATED`.
- If Gates A, B, and C pass, begin with `VALIDATED`.

The final `RESULT:` runner marker is separate from the `PROOF.md` proof-quality
headline. `KPROVE_PASSED` reports positive target-proof execution only; it
neither requires nor implies a `VALIDATED` proof-quality headline; never equate
that execution marker with soundness or intent validation.

For this benchmark, the required target proof must cover the material input
domain of the full HumanEval contract. If the prompt permits arbitrary finite
lists or another symbolic unbounded domain, finitely many fixed sizes, examples,
or bounded unrollings are supporting progress only. They do not count as the
required target proof.

## Required work

1. Read `prompt.py`, then create `solution.py` and implement the requested
   entry point yourself. Preserve the signature. You may reuse helper or setup
   code that the prompt intentionally supplies.
2. Keep `solution.py` within the subset accepted by `py2mpy.py` and generate
   `solution.mpy` with `python3 py2mpy.py solution.py > solution.mpy`.
3. Write `verification.k` and `spec.k`.
4. Exercise the program with `krun`, prove every claim in `spec.k` with
   `kprove`, and record exact commands in `prove.sh`.

- For concrete LLVM execution, compile `reference-semantics/semantics.k` with
  `--main-module MPY-KRUN --syntax-module MPY-SYNTAX`.
- For symbolic proof definitions, import the supplied `MPY` modules without
  modifying files under `reference-semantics/`.

## Deliverables

`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`.

The container has 8 GB of memory. Keep working while a concrete path remains;
if the proof cannot close, preserve the best artifacts and explain the blocker
in `NOTES.md`.

End your final message with exactly one line and nothing after it:
RESULT: <KPROVE_PASSED|PARTIAL|BLOCKED> — <one sentence>

Choose exactly one marker using this ordered decision; stop at the first
matching case.

1. `KPROVE_PASSED` iff every required positive target-proof command (commands
   intended to close the task's proof claims) printed `#Top`, exited 0, and Gate
   B passes for the full HumanEval contract. A `SOUND-BUT-LIMITED` result is
   `PARTIAL`, even when every narrower supporting claim prints `#Top`.
   Expected-failure mutation probes and other negative validation probes are
   judged by their expected non-zero result and do not disqualify this marker.
2. Otherwise, `BLOCKED` iff a concrete hard blocker—such as a missing required
   input, capability, tool, or semantic support—prevented completion. Name it.
3. Otherwise, `PARTIAL`: the positive proof condition was not met; preserve and
   report the best artifacts or progress available.

This ordered precedence is total and mutually exclusive. Incomplete
deliverables or a later Gate status do not create a second marker. This runner
marker reports positive proof execution only, not a `VALIDATED` judgment.

When a required loop proof needs symbolic induction beyond the K backend's
capability — in particular doubly-nested loops over heap-allocated
structures — do NOT attempt the full nested induction in K. Instead:
state each loop's summary as a separate guarded `[simplification]` domain
lemma (one per loop level, following the Kit's per-loop decomposition),
with guards that make each lemma a true statement exactly as strong as
what the surrounding proof needs — never stronger than what holds. Close
the K proof using those assumed lemmas; the pipeline's Lean arm discharges
them as machine-checked obligations downstream. Keep each lemma's
statement small and self-contained (avoid folding both loop levels into
one lemma) so the downstream obligations stay tractable.

Three hard requirements on every summary function and bridging
`[simplification]` rule (each has produced audit-refuted proofs):

1. **Concrete adequacy check before use.** Before building the proof on a
   summary function that constructs a loop's result, execute the fixed
   operational semantics (`krun`) on at least two small concrete inputs
   satisfying the precondition — covering BOTH parities of any
   length/count parameter — and confirm the summary computes the
   byte-identical result. A sequence that must start at a fixed element
   must pin that head positionally (e.g. two mutually recursive helpers,
   one per position class), never derive it from the parity of the
   REMAINING length: that construction silently flips the head for one
   parity of the total length.
2. **Footprint preservation.** A bridging rule must preserve every cell,
   scope binding, and subsequent write it does not explicitly summarize.
   If the summarized region is followed by writes (e.g. `value := ...`)
   that a continuation could read, the bridge must reproduce them.
3. **Match domain no broader than justification.** Never match arbitrary
   continuation `REST` unless the rule is true for ALL continuations.
   Restrict the match to the exact continuation shape the proof needs.
   Declare `[total]` only when the equations cover the full domain.

When a loop summary would otherwise be assumed, do NOT install it as an
operational rewrite rule (any priority): an unproved answer-bearing
operational rule fails the audit even when its footprint is perfect.
Instead DERIVE each loop summary as a separate reachability CLAIM in the
spec module — kprove proves all claims of a module together, so each
claim's induction is handled coinductively (the claim set is available
as circularities after one rewrite step). State each loop claim over a
generalized mid-loop state (symbolic iteration counter with the
invariant as the requires-clause; the accumulated partial result as a
symbolic prefix), so the circularity applies to the loop's own back
edge. The final claim then composes the loop claims sequentially.
If fixed evaluation stalls on symbolic collection access (e.g. a
subscript function stuck on a symbolic sequence), add guarded FUNCTIONAL
`[simplification]` lemmas reducing exactly those stuck accesses to the
spec selectors under the precondition's validity guards — these are
ordinary data-access domain lemmas, dischargeable by the pipeline's Lean
arm. Functional lemmas may simplify stuck function terms; they must
never bypass control flow.
