# Second-pass runs — provenance

Each arm directory is the complete, final run tree of that experimental
arm, copied from the `humaneval-benchmark` working repository on
2026-08-11. Directory names here are arm names; the original run ids are:

| Arm | Original run id | Primary verdict stage | Final tally (164 tasks) |
| --- | --- | --- | --- |
| `bare/` | `codex-gpt-5.6-sol-xhigh-bare` | stage 2 (K audit) | 23 PASS + 41 CONCERNS = 64 LEGIT, 100 FAIL |
| `semantics/` | `codex-gpt-5.6-sol-xhigh-semantics` | stage 2 (K audit) | 37 PASS + 36 CONCERNS = 73 LEGIT, 91 FAIL |
| `kit_semantics/` | `codex-gpt-5.6-sol-xhigh-kit-semantics-frozen-20260724` | stage 6 (Lean audit) | 162 PASS + 2 CONCERNS = 164/164 LEGIT |

Task trees are complete six-stage records (invocations, workspaces,
audit executions with evidence), minus compiled K output
(`*-kompiled/`, regenerable), Lean build caches (`.lake/`), and
container credential homes.

The kit_semantics arm was consolidated in-place during the campaign:
staged rescue attempts ran in separate variant runs and, once audited,
were promoted into this frozen run (`ops/promote_staging.py` in the
source repo); superseded stage directories were moved to the source
repo's `legacy/`, never deleted. Eighteen variant/rescue run trees
(`...-r021*` through `...-v3k0210*`, `...-129final-20260731`, etc.) and
`legacy/` remain in the local `humaneval-benchmark` archive and the team
zip; they are not part of this organized archive.

Verification at copy time: per-task selected verdicts re-tallied from
these trees match the packaged results tables exactly for all three
arms; all 1,093 stage `selected.json` records resolve to their artifact
directories; zero credential files and zero real credential values
present (filename scan + exact-value content scan against every local
credential file).
