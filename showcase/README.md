# Showcase: formally verified HumanEval, end to end

This program produced machine-checked correctness proofs for Python
solutions to all 164 problems of the HumanEval benchmark. It ran in two
passes: a hand-derived K semantics for a Python subset with hand-built
proofs of all 164 problems (which yielded the reusable **kit** skill
plugin), followed by a controlled campaign in which coding agents solved
and proved every problem under a six-stage verify-and-audit pipeline.
The headline result: an agent equipped with the kit verified **164 of
164** problems, every verdict confirmed by an independent audit session.

## Results

Each of the 164 problems ran through the same six-stage pipeline in
three arms that differ only in what the agent is given:

| Arm | Agent receives | Verified (LEGIT) | PASS | CONCERNS |
| --- | --- | --- | --- | --- |
| `bare` | the problem only | 64 / 164 | 23 | 41 |
| `semantics` | + the frozen reference semantics | 73 / 164 | 37 | 36 |
| `kit_semantics` | + the kit | **164 / 164** | 162 | 2 |

LEGIT = PASS + CONCERNS, where PASS means the audit found no issues and
CONCERNS means it flagged only non-fatal ones. Every verdict comes from
an independent audit session, never from the agent that wrote the proof.
For `bare` and `semantics` the primary verdict is the stage-2 K audit;
for `kit_semantics` it is the stage-6 adversarial Lean audit, the
strictest gate in the pipeline. Source of record:
[`arms_summary.csv`](../second-pass/submission/supplementary_code_and_data/data/results/arms_summary.csv).

The six stages: (1) an agent writes the solution and its K proof, (2) an
independent session audits the K proof, (3) the proof's lemmas are
classified against a trust boundary, (4) the remaining domain
obligations are deterministically exported from K to Lean (a proof
assistant), (5) a session proves them in Lean, and (6) an independent
adversarial session audits the Lean proofs under mechanical gates.

## In this folder

- [`example-3-below-zero.md`](example-3-below-zero.md) — the simplest
  end-to-end walkthrough: the exact prompt, the generated code and spec,
  and the proof reaching `#Top` (K's proof-complete signal).
- [`example-55-fib.md`](example-55-fib.md) — an end-to-end proof that
  needs a loop invariant, showing how the pipeline handles the harder,
  more typical case.
- [`full-context.md`](full-context.md) — the exact model, prompts,
  tools, and version pins behind every run, for anyone who asks "what
  precisely was the setup?"

## Map of the repo

- [`../first-pass/questions/`](../first-pass/questions/) — the original
  hand-built proofs: one directory per HumanEval problem with solution,
  spec, and verification files.
- [`../first-pass/semantic/`](../first-pass/semantic/) — the unified
  reference semantics and shared lemma library, frozen as it stood at
  the end of the first pass (`src/`).
- [nlp-research-rosu/kit](https://github.com/nlp-research-rosu/kit) (private org repo) —
  the kit: the verification method from the first pass packaged as a
  skill plugin that walks an agent from intent to code, spec, and proof.
- [`../second-pass/runs/`](../second-pass/runs/) — the complete campaign
  output, one tree per arm:
  [`bare/`](../second-pass/runs/bare/),
  [`semantics/`](../second-pass/runs/semantics/),
  [`kit_semantics/`](../second-pass/runs/kit_semantics/).
- [`../second-pass/prompts/`](../second-pass/prompts/) — the verbatim
  per-stage prompts used in every run.
- [`../second-pass/submission/`](../second-pass/submission/) — the
  self-contained AAAI supplementary package: code, data, and results
  tables.

## How to demo this in 2 minutes

Open [`example-3-below-zero.md`](example-3-below-zero.md) and scroll
top to bottom: prompt in, code and spec out, proof checked. That is the
whole story on one page. If your audience wants to see a proof with
real reasoning in it, follow with
[`example-55-fib.md`](example-55-fib.md), which does the same for a
loop-invariant proof. The results table above is the summary slide;
everything else in the repo is evidence behind it.
