# Exhaustive K source inventory summary

Inventory: `/audit-output/evidence/k_inventory.tsv`. Rule/claim review: `/audit-output/evidence/static_rule_review.tsv`.

Files scanned: 28.

Statements inventoried: 963.

## Counts by statement kind

- claim: 4
- configuration: 1
- context: 5
- rule: 716
- syntax: 237

## Counts by source class

- candidate-validation-claims: 2
- proof-extension: 31
- target-claims: 2
- trusted-fixed-semantics: 928

## Attribute-sensitive counts

- total declarations/statements: 117
- explicit functional declarations: 0
- no-evaluators declarations: 23
- priority rules/statements: 45
- simplification rules/statements: 7

## Per-file counts

| File | Syntax | Rule | Claim | Context | Configuration |
|---|---:|---:|---:|---:|---:|
| `/candidate/connection-spec.k` | 0 | 0 | 2 | 0 | 0 |
| `/candidate/spec.k` | 0 | 0 | 2 | 0 | 0 |
| `/candidate/verification.k` | 10 | 21 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/assert.k` | 0 | 3 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/bool.k` | 0 | 13 | 0 | 1 | 0 |
| `/reference/reference-semantics/semantics/builtins.k` | 38 | 137 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/call.k` | 3 | 21 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/comprehension.k` | 3 | 7 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/concrete.k` | 5 | 16 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/controls.k` | 3 | 34 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/core.k` | 37 | 46 | 0 | 0 | 1 |
| `/reference/reference-semantics/semantics/dict.k` | 12 | 28 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/float.k` | 34 | 121 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/functions.k` | 4 | 15 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/int.k` | 1 | 16 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/iter.k` | 1 | 0 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/list.k` | 5 | 27 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/methods.k` | 27 | 75 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/operators.k` | 0 | 10 | 0 | 2 | 0 |
| `/reference/reference-semantics/semantics/range.k` | 2 | 6 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/set.k` | 6 | 12 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/sort.k` | 6 | 19 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/str.k` | 5 | 28 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/subscript.k` | 15 | 40 | 0 | 2 | 0 |
| `/reference/reference-semantics/semantics/syntax.k` | 16 | 0 | 0 | 0 | 0 |
| `/reference/reference-semantics/semantics/tuple.k` | 4 | 21 | 0 | 0 | 0 |

## Opaque/no-evaluators declarations

- `/reference/reference-semantics/semantics/builtins.k:285` — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).`
- `/reference/reference-semantics/semantics/float.k:24` — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:30` — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:37` — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:50` — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:54` — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:103` — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:107` — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:111` — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:115` — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:119` — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:125` — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:142` — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:160` — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:190` — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:195` — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:209` — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:217` — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:223` — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- `/reference/reference-semantics/semantics/float.k:230` — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- `/reference/reference-semantics/semantics/sort.k:18` — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- `/reference/reference-semantics/semantics/sort.k:49` — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
- `/candidate/verification.k:10` — `syntax Str ::= projectStrTotal(Val) [function, total, symbol(projectStrTotal), no-evaluators]`
