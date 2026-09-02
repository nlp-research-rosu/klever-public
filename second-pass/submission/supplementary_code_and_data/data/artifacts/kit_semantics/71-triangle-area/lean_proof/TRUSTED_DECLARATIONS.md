# Remaining trusted declarations in generated Klean Base

The read-only generated project `/workspace/Base` contains 88 `axiom`
declarations and no `opaque` declarations. They are reported here as part of
the generated-base trust boundary; none was introduced or invoked as a
shortcut in `Proof.lean`.

## Prelude axioms (41)

- `MapHookDef` (17): `unitAx`, `consAx`, `lookupAx`, `lookupAx?`, `updateAx`,
  `deleteAx`, `concatAx`, `differenceAx`, `updateMapAx`, `removeAllAx`,
  `keysAx`, `in_keysAx`, `valuesAx`, `sizeAx`, `includesAx`, `choiceAx`,
  `splitAx`.
- `SetHookDef` (11): `unitAx`, `concatAx`, `elementAx`, `unionAx`,
  `intersectionAx`, `differenceAx`, `inSetAx`, `inclusionAx`, `sizeAx`,
  `choiceAx`, `splitAx`.
- `ListHookDef` (13): `unitAx`, `concatAx`, `elementAx`, `pushAx`, `getAx`,
  `updteAx`, `makeAx`, `updateAllAx`, `fillAx`, `rangeAx`, `inListAx`,
  `sizeAx`, `splitAx`.

These declarations occur in
`Base/Klean71TriangleArea/Prelude.lean`; they model hooked K map, set, and list
operations.

## Generated function axioms (47)

The following root declarations occur in
`Base/Klean71TriangleArea/Func.lean`:

- `absFloat(_)_FLOAT_Float_Float`
- `_*Float__FLOAT_Float_Float_Float`
- `_>Float__FLOAT_Bool_Float_Float`
- `_<Float__FLOAT_Bool_Float_Float`
- `--Float__FLOAT_Float_Float`
- `Float2Int(_)_FLOAT_Int_Float`
- `Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int`
- `exponentBitsFloat(_)_FLOAT_Int_Float`
- `floorFloat(_)_FLOAT_Float_Float`
- `isNaN(_)_FLOAT_Bool_Float`
- `maxValueFloat(_,_)_FLOAT_Float_Int_Int`
- `precisionFloat(_)_FLOAT_Int_Float`
- `_==String__STRING-COMMON_Bool_String_String`
- `Int2String(_)_STRING-COMMON_String_Int`
- `lengthString(_)_STRING-COMMON_Int_String`
- `ordChar(_)_STRING-COMMON_Int_String`
- `substrString(_,_,_)_STRING-COMMON_String_String_Int_Int`
- `_^Int_`
- `_^Float__FLOAT_Float_Float_Float`
- `_==Bool_`
- `_==Float_`
- `ceilFloat(_)_FLOAT_Float_Float`
- `_-Float__FLOAT_Float_Float_Float`
- `_+Float__FLOAT_Float_Float_Float`
- `exponentFloat(_)_FLOAT_Int_Float`
- `_/Float__FLOAT_Float_Float_Float`
- `_>=Float__FLOAT_Bool_Float_Float`
- `absInt(_)_INT-COMMON_Int_Int`
- `rootFloat(_,_)_FLOAT_Float_Float_Int`
- `signFloat(_)_FLOAT_Bool_Float`
- `proofIntToF`
- `_62d7600`
- `binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq`
- `_5711fdc`
- `strToCodes(_)_MPY-STR_IntSeq_String`
- `_60e6213`
- `_6b2bff4`
- `_7346d9f`
- `applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val`
- `_fc81955`
- `_ff208f3`
- `_7602aea`
- `_9669df5`
- `_9a4e525`
- `_9fe303a`
- `applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val`
- `_cb210bb`

`#print axioms Proof.final` reports only Lean core axioms `propext` and
`Classical.choice`. It reports no dependency on any of the 88 generated Klean
axioms above.
