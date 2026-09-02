# klever — formally verifying HumanEval in K, twice

This repository is the organized archive of a two-pass research program:
formally verifying the partial correctness of all 164 HumanEval problems
in the K framework, distilling the method into a reusable agent skill
plugin, and then re-proving everything under a rigorous, independently
audited pipeline.

## The two passes

**[`first-pass/`](first-pass/)** — the derivation. A K semantics for a
Python subset was hand-derived bottom-up, one problem at a time, and all
164 solutions were proven (`kprove` → `#Top`) against it, using a
112-repo corpus of proven K techniques as the knowledge base. This is
where the unified reference semantics and the methodology came from;
both were later packaged as the **kit** — an
`intent → code → spec → proof` skill plugin for coding agents.

- `first-pass/questions/<id>-<name>/` — per-problem proof: `solution.py`,
  `spec.k` (reachability claims), `verification.k` (invariants, summary
  functions, lemmas), smoke + differential tests.
- `first-pass/semantic/` — the unified semantics + shared lemma
  library, frozen as it stood at the end of the first pass; the live,
  still-developed semantics moved to the org's `semantics` repository.
- [`first-pass/README.md`](first-pass/README.md) — how the pass worked
  and what is where.
- `first-pass/references/` — the technique corpus (submodules).

**[`second-pass/`](second-pass/)** — the audited campaign. Fresh agents,
three experimental arms, six stages per problem: Codex K proof →
independent K audit → trust-boundary classification → deterministic
K-to-Lean export → Lean proof → independent adversarial Lean audit. The
kit and semantics continued to evolve during this pass; every revision
is pinned in the second-pass lock files and per-task artifacts.

| Arm | Agent receives | Result (of 164) |
| --- | --- | --- |
| `bare` | the problem only | 64 LEGIT (23 PASS + 41 CONCERNS) |
| `semantics` | + the reference semantics | 73 LEGIT (37 PASS + 36 CONCERNS) |
| `kit_semantics` | + the kit | **164 LEGIT (162 PASS + 2 CONCERNS)** |

Start at [`second-pass/README.md`](second-pass/README.md), or take the
guided tour in [`showcase/`](showcase/README.md) — two end-to-end worked
examples plus the full experimental context on one card. The AAAI-27
supplementary package, exactly as shipped, is self-contained under
`second-pass/submission/`. The paper itself — the AAAI-27 submission
and tech report — is kept in a separate private org repo.

## History

An earlier interim second-pass run (a scratch-bed kit validation) used a
wrong setup; it was removed from the working tree in the 2026-08
reorganization and survives only in git history, superseded by
`second-pass/`.
