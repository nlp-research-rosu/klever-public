# K rule/declaration inventory summary

- Source files: 26
- Total inventoried blocks: 946
- Kinds: {'claim': 5, 'configuration': 1, 'context': 5, 'rule': 705, 'syntax': 230}
- Attribute/category counts: {'concrete': 35, 'function': 148, 'macro': 4, 'macro-rec': 1, 'no-evaluators': 23, 'ordinary': 593, 'owise': 26, 'priority': 45, 'seqstrict': 1, 'simplification': 6, 'strict': 2, 'symbol': 25, 'total': 110}
- Assessments: {'CLAIM_REVIEWED': 5, 'PROOF_LOCAL_DEFINITION_TRUE': 3, 'PROOF_LOCAL_EXACT_ABBREVIATION': 3, 'PROOF_LOCAL_SUMMARY_TRUE': 7, 'SUPPLIED_FIXED_OPAQUE_UNUSED': 25, 'SUPPLIED_FIXED_UNUSED': 788, 'SUPPLIED_FIXED_USED_REVIEWED': 115}
- Opaque/symbol blocks: 26
- Priority blocks: 45
- Simplification blocks: 6

The complete text and per-block assessment are in `rule-inventory.tsv`.

## Opaque/symbol declarations

- semantics/builtins.k:285 —   syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
- semantics/float.k:24 —   syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
- semantics/float.k:30 —   syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
- semantics/float.k:37 —   syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
- semantics/float.k:50 —   syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
- semantics/float.k:54 —   syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
- semantics/float.k:73 —   syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
- semantics/float.k:86 —   syntax Float ::= toF(Val) [function, total, symbol(toF)]
- semantics/float.k:93 —   syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
- semantics/float.k:103 —   syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
- semantics/float.k:107 —   syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
- semantics/float.k:111 —   syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
- semantics/float.k:115 —   syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
- semantics/float.k:119 —   syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
- semantics/float.k:125 —   syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
- semantics/float.k:142 —   syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
- semantics/float.k:160 —   syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
- semantics/float.k:190 —   syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
- semantics/float.k:195 —   syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
- semantics/float.k:209 —   syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
- semantics/float.k:217 —   syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
- semantics/float.k:223 —   syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
- semantics/float.k:230 —   syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
- semantics/sort.k:18 —   syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
- semantics/sort.k:49 —   syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
- verification.k:76 —   syntax Val ::= bored0(IntSeq, Int) [function, total, no-evaluators]
