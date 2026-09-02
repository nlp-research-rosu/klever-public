# Independent Stage 3 classification assessment

The trusted inventory reconstructed 55 rules in the single local closure module
`VERIFICATION`. The following decisions were made from the frozen rule bodies,
their heads, attributes, and their role in `spec.k`, before comparison with the
protected classification.

## Independent classification by frozen source span

| Classification | `verification.k` spans | Count | Judgment basis |
|---|---|---:|---|
| `DOMAIN_LEMMA` | 9–11, 15–17, 22–25, 46–48, 52–54, 63–64, 68–70, 74–76, 81–83, 87–89, 132–135, 136–139, 143–145, 146–148, 149–151 | 15 | These rewrite existing K casts, `applyCmp`, `maxFloat`, definedness, or sort predicates. They are theorem-like facts installed as simplifications and are never first proved against a module omitting the rule. |
| `DEFINITION` | 12–14, 18, 30–31, 34, 35–36, 39, 40–41, 49–51, 55, 62, 71–73, 77, 84–86, 90, 93, 102–103, 104–105, 106–107, 108–109, 114, 115–116, 117–118, 119–120, 121, 122, 123, 124–125, 126–127, 128, 129, 156, 157–164, 167, 168–178, 183, 184–187, 188–191, 194, 195–201, 202–205 | 40 | Every rule is headed by a new proof-local symbol and is a guarded equation, case, base case, structural recurrence, or named summary term. |
| `OPERATIONAL_RULE` | none | 0 | No inventory rule is an ordinary cell-level execution or observation step; all are equations in the proof-local verification module. |
| `PROVED_DERIVED_LEMMA` | none | 0 | No exact rule is first proved in a module that omits it. Every Stage 1 spec module imports `VERIFICATION`, which already contains all 55 rules. |

This independently determined ordered classification is identical to
`lemma-discovery.json`. All rules carrying a `simplification` or
`simplification(...)` attribute fall in `DEFINITION` or `DOMAIN_LEMMA`.

## Relevance of all 15 domain lemmas

| Spans | Role in the frozen max program and claims |
|---|---|
| 9–11, 15–17 | Int-cast definedness and projection reorientation used by the Int-seeded max fold and numeric dispatch. |
| 22–25 | The dynamic-Val/static-Int `applyCmp(">", ...)` case needed by the Int accumulator proof. |
| 46–48, 52–54 | Float-cast definedness and projection reorientation used by Float-seeded and mixed numeric max. |
| 63–64 | Connects the homogeneous-float max fold's fixed `maxFloat` hook to its proof-local opaque twin. |
| 68–70, 74–76 | Bool-cast definedness and projection reorientation used by Bool values in the general numeric max fold. |
| 81–83, 87–89 | String-cast definedness and projection reorientation used by string max and `strLt`. |
| 132–135 | Dynamic numeric `applyCmp(">", ...)` dispatch used by mixed Int/Bool/Float max. |
| 136–139 | Dynamic string `applyCmp(">", ...)` dispatch used by string max. |
| 143–145, 146–148, 149–151 | Mutual exclusion of Int, Float, and Bool tags, needed to establish the guarded numeric-view cases and dispatch. |

All 15 are load-bearing for a source program whose body is `return max(l)` and
whose Stage 1 claims cover nonempty Int/Bool/Float mixtures and strings. None is
an irrelevant theorem imported from another problem.
