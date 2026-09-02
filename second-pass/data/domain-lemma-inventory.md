# Domain-lemma inventory — kit-semantics arm (Stage 3, 2026-07-30)

Aggregated from every task's `03-lemma-discovery/workspace/trust-boundary.json`
in `runs/codex-gpt-5.6-sol-xhigh-kit-semantics-frozen-20260724`. Machine-readable
form: `data/domain-lemma-inventory.json` (instances + deduplicated statements).

## Totals

- Tasks with completed lemma discovery: **163 / 163** (all LEGIT tasks)
- Rules classified: **1,550**
  - DEFINITION: 1,326
  - **DOMAIN_LEMMA: 186** (the trusted mathematical facts)
  - PROVED_DERIVED_LEMMA: 30
  - OPERATIONAL_RULE: 8
- Tasks needing at least one domain lemma: **65 / 163** (98 close with
  definitions alone)
- Unique domain-lemma statements after cross-task deduplication: **160**

## Themes (by rationale/text keyword)

| Theme | Instances |
| --- | --- |
| float/rounding trust (#Ceil characterizations, casts, IEEE bridges) | 45 |
| ordering / min-max / sort facts | 24 |
| string/sequence facts | 20 |
| integer & modular arithmetic | 16 |
| digit/base representation | 8 |
| number theory (primality, Collatz, Fibonacci) | 3 |
| list/multiset facts | 2 |
| uncategorized (task-specific mathematical facts) | 68 |

## Most shared statements

The guarded-total-projection family (the Kit 0.2.1 `ceils.k` idiom)
dominates reuse:

- `#Ceil({@V:Val}:>Int) => isInt(@V) #And #Ceil(@V)` — 12 tasks
- `projectIntTotal(projectIntTotal(V)) => projectIntTotal(V)` — 3 tasks
- `{V:Val}:>Int => projectIntTotal(V)` (guarded orientation) — 3 tasks
- `applyBin("%", V:Val, I:Int)` supersort dispatch twin — 3 tasks
- `#Ceil({@V:Val}:>Float)` — 2 tasks

## Heaviest tasks

35-max-element (15), 94-skjkasdkd (13), 155-even-odd-count (10),
123-get-odd-collatz (8), 151-double-the-difference (8), 72-will-it-fly (7),
69-search (5), 108-count-nums (5).

These are the natural first targets for Stage 4/5 Lean formalization effort,
since each trusted fact becomes a Lean proof obligation or documented axiom.
