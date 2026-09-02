import Klean90NextSmallest.Inj

noncomputable def _0c827ea : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _dcbe275 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «absFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

noncomputable def _0105150 : SortString → SortString → Option SortBool
  | _Gen0, _Gen1 => some false

noncomputable def _010fe30 : SortVal → Option SortBool
  | _Gen0 => some false

noncomputable def _dc25660 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

noncomputable def _0290a71 : SortVal → Option SortFloat
  | SortVal.inj_SortFloat F => some F
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

noncomputable def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

noncomputable def _c0da98c : SortString → SortParamNames → Option SortBool
  | _Gen0, SortParamNames.«.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}_ParamNames» => some false
  | _, _ => none

noncomputable def _49a8097 : SortValSeq → SortInt → SortVal → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _, _, _ => none

noncomputable def _fdfd33a : SortValSeq → SortInt → SortVal → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, 0, V => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S)
  | _, _, _ => none

noncomputable def _073f426 : SortString → SortInt → SortInt → Option SortInt
  | _Gen0, A, _Gen1 => some A

noncomputable def _076da9f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _fd49342 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some false
  | _, _ => none

axiom «_*Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def _c3be6f0 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

noncomputable def _c5937bc : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _Gen0, A => some A
  | _, _ => none

axiom md5hexCodes (x0 : SortIntSeq) : Option SortIntSeq

noncomputable def _0d21514 : SortInts → Option SortInts
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» _Gen0 XS => some XS
  | _ => none

noncomputable def _c3b9085 : SortInt → SortVals → Option SortInt
  | M, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some M
  | _, _ => none

noncomputable def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _0f9305e : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

noncomputable def _5dd92ea : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

noncomputable def _e688eef : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 1
  | _ => none

noncomputable def _105572a : SortK → Option SortBool
  | K => some false

noncomputable def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

axiom «Int2String(_)_STRING-COMMON_String_Int» (x0 : SortInt) : Option SortString

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _7c9eb36 : SortInts → Option SortBool
  | SortInts.«nilInts_NEXT-SMALLEST-VERIFICATION_Ints» => some true
  | _ => none

noncomputable def _bdc576b : SortInts → Option SortBool
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» _Gen0 _Gen1 => some false
  | _ => none

noncomputable def _121c40c : SortVal → Option SortBool
  | SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» _Gen0 _Gen1 => some true
  | _ => none

noncomputable def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def _28a37d3 : SortOptInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» S => some S
  | _ => none

noncomputable def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

noncomputable def _daab430 : SortOptInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» => some 1
  | _ => none

noncomputable def _611c5b2 : SortInt → SortValSeq → Option SortValSeq
  | X, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) X) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

noncomputable def _b12fe18 : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 _Gen0 => some true
  | _ => none

noncomputable def _e281c7f : SortIntSeq → Option SortBool
  | _Gen0 => some false

noncomputable def _e46b672 : SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 _Gen0 => some true
  | _ => none

noncomputable def _eceab8b : SortIntSeq → Option SortOpSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq»
  | _ => none

noncomputable def _fd6d3a4 : SortIntSeq → Option SortBool
  | _Gen0 => some false

noncomputable def _150c95b : SortK → Option SortVal
  | SortK.kseq _Pat0 SortK.dotk => match (@retr SortVal SortKItem) _Pat0 with
    | some K => some K
    | _ => none
  | _ => none

noncomputable def _34926f2 : SortOpSeq → SortString → Option SortOpSeq
  | SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», O => some (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq»)
  | _, _ => none

noncomputable def _84535a7 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», N => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

noncomputable def _4725bc2 : SortIntSeq → SortValSeq → Option SortValSeq
  | A, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

noncomputable def _7e4861f : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

noncomputable def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

noncomputable def _18b010b : SortIntSeq → SortInt → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, _Gen1 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _, _ => none

noncomputable def _18fc027 : SortInt → SortEvPair → Option SortEvPair
  | N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
  | _, _ => none

axiom «_^Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortFloat

noncomputable def _d83ba47 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», A => some A
  | _, _ => none

noncomputable def _d770725 : SortValSeq → SortInt → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _, _ => none

axiom «_-Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «_==Float_» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «_+Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «floorFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

noncomputable def _1dc0c6c : SortVals → SortVal → Option SortVals
  | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals», V => some (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)
  | _, _ => none

noncomputable def _1de0a86 : SortEvPair → Option SortInt
  | _Gen0 => some 0

noncomputable def _1f82817 : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _2553414 : SortOpSeq → SortIntSeq → Option SortEvPair
  | SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», NDS => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» NDS)
  | _, _ => none

noncomputable def _75246f8 : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

noncomputable def _89140a8 : SortEvPair → Option SortInt
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» _Gen0 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N _Gen1) => some N
  | _ => none

noncomputable def _8ad47ba : SortString → SortInt → SortEvPair → Option SortEvPair
  | O, N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS) (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS))

noncomputable def _eda2bc1 : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

noncomputable def _eeba85e : SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

noncomputable def _28cc140 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

noncomputable def _5e2c753 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

noncomputable def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

axiom «_>Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

noncomputable def _2867a75 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _28eddda : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 0 I 1))
  | _, _ => none

noncomputable def _46f4f7d : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _abb6b77 : SortInt → Option SortInt
  | C => some C

noncomputable def _a9065e7 : SortInts → Option SortInt
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints» X _Gen0 => some X
  | _ => none

axiom «_/Float__FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def _e4ff78f : SortValSeq → SortVal → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _f73c85c : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

noncomputable def _2e9dd52 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some CS
  | _, _ => none

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

noncomputable def _37dc11b : SortInt → SortIntSeq → Option SortIntSeq
  | 0, ACC => some ACC
  | _, _ => none

noncomputable def _324a76c : SortVals → Option SortValSeq
  | SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

noncomputable def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

noncomputable def _b92fdc6 : SortIntSeq → SortInt → SortIntSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _SEP, CUR => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CUR)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _, _ => none

noncomputable def _3695ec2 : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _9c2daf9 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _ => none

noncomputable def _a2318fa : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _ => none

noncomputable def _3c5ecf9 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», A => some A
  | _, _ => none

noncomputable def _3dabce1 : SortInt → Option SortInt
  | C => some C

noncomputable def _4154192 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _4183651 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

axiom «_<Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

noncomputable def _437b04b : SortString → SortVals → Option SortVal
  | "str", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS))
  | _, _ => none

noncomputable def _4613fdc : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1 => some true
  | _, _, _, _ => none

noncomputable def _495da55 : SortK → Option SortBool
  | K => some false

noncomputable def _49c55eb : SortInt → Option SortIntSeq
  | 0 => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _ => none

noncomputable def _4b80f98 : SortString → SortVals → Option SortVal
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals» _Pat0 (SortVals.«_,__MPY-CORE_Vals_Val_Vals» _Pat1 SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => some ((@inj SortIterable SortVal) (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» A B))
    | _, _ => none
  | _, _ => none

noncomputable def _7fd70ea : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _8751d92 : SortIntSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

noncomputable def _6cfd1c6 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

noncomputable def _542a815 : SortVal → Option SortBool
  | SortVal.«noneV_MPY-CORE_Val» => some false
  | _ => none

noncomputable def _55400f7 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _553ef43 : SortIntSeq → SortValSeq → Option SortIntSeq
  | _Gen0, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

noncomputable def _583f938 : SortString → SortVals → Option SortVal
  | "ord", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortInt SortVal) C)
  | _, _ => none

noncomputable def _e321d7c : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

noncomputable def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

noncomputable def _613283e : SortK → Option SortBool
  | K => some false

noncomputable def _6206d78 : SortVal → Option SortBool
  | SortVal.«ref(_)_MPY-CORE_Val_Int» _Gen0 => some true
  | _ => none

noncomputable def _6d20a96 : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortFloat SortVal) F)
  | _, _ => none

noncomputable def _8978072 : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0) => some true
  | _ => none

noncomputable def _c788a4b : SortVal → Option SortBool
  | _Gen0 => some false

noncomputable def _dfeef54 : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

noncomputable def _7573b98 : SortInt → Option SortInt
  | C => some C

noncomputable def _b5f8fbb : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _8403ac8 : SortVal → Option SortBool
  | _Gen0 => some false

noncomputable def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

noncomputable def _853fa53 : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt A) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt B) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => some ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» A B 1))
  | _, _ => none

noncomputable def _b48ab39 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0 => some C
  | _ => none

noncomputable def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

noncomputable def _9f02755 : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidate = key then (key, value) :: rest
      else (candidate, oldValue) :: kleanMapUpdateModel rest key value

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map» (x0 : SortKItem) (x1 : SortMap) : Option SortBool :=
  some (kleanMapContainsModel x1.coll x0)

axiom «_>=Float__FLOAT_Bool_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortBool

noncomputable def «_[_<-undef]» (x0 : SortMap) (x1 : SortKItem) : Option SortMap :=
  some ⟨kleanMapDeleteModel x0.coll x1⟩

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

noncomputable def «Map:lookup» (x0 : SortMap) (x1 : SortKItem) : Option SortKItem :=
  kleanMapLookupModel x0.coll x1

noncomputable def «Map:update» (x0 : SortMap) (x1 : SortKItem) (x2 : SortKItem) : Option SortMap :=
  some ⟨kleanMapUpdateModel x0.coll x1 x2⟩

axiom «absInt(_)_INT-COMMON_Int_Int» (x0 : SortInt) : Option SortInt

noncomputable def _a971c50 : SortString → SortVals → Option SortVal
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => some ((@inj SortIterable SortVal) (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» A B))
  | _, _ => none

noncomputable def _d1c3ede : SortInt → SortVals → Option SortInt
  | M, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some M
  | _, _ => none

noncomputable def _e4f0a30 : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortInt SortVal) I)
  | _, _ => none

noncomputable def _ec93494 : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

noncomputable def _fbb3e9c : SortVal → Option SortBool
  | _Gen0 => some false

noncomputable def _dc2e992 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "encode", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Gen0)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => some ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS))
  | _, _, _ => none

noncomputable def _f05ec3f : SortVal → Option SortBool
  | SortVal.inj_SortBool B => some B
  | _ => none

noncomputable def _c69a3d5 : SortVal → Option SortParamNames
  | SortVal.«cellsMark(_)_MPY-CORE_Val_ParamNames» CVS => some CVS
  | _ => none

noncomputable def _eb0d315 : SortValSeq → SortBool → Option SortValSeq
  | S, false => some S
  | _, _ => none

noncomputable def _a38c318 : SortValSeq → SortIntSeq → Option SortValSeq
  | ACC, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some ACC
  | _, _ => none

noncomputable def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

noncomputable def _d619e02 : SortVal → Option SortBool
  | SortVal.«cellRef(_)_MPY-CORE_Val_Int» _Gen0 => some true
  | _ => none

noncomputable def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

noncomputable def _afefecb : SortK → Option SortBool
  | K => some false

noncomputable def _f4c2469 : SortK → Option SortBool
  | SortK.kseq _Pat0 SortK.dotk => match (@retr SortKResult SortKItem) _Pat0 with
    | some KResult => some true
    | _ => none
  | _ => none

noncomputable def _f3b0384 : SortVal → Option SortBool
  | _Gen0 => some false

axiom «maxFloat(_,_)_FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

axiom «minFloat(_,_)_FLOAT_Float_Float_Float» (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat

noncomputable def _ef206f4 : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat K) SortK.dotk => some K
  | _ => none

noncomputable def _f316b87 : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt K) SortK.dotk => some K
  | _ => none

axiom «rootFloat(_,_)_FLOAT_Float_Float_Int» (x0 : SortFloat) (x1 : SortInt) : Option SortFloat

axiom sortKeyVS (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq

axiom append (x0 : SortK) (x1 : SortK) : Option SortK

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _30ee06e : SortString → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I => do
    let _Val0 <- «_-Int_» 0 I
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _614d946 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_-Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _778079e : SortString → SortInt → SortInt → Option SortInt
  | "-", A, B => do
    let _Val0 <- «_-Int_» A B
    return _Val0
  | _, _, _ => none

noncomputable def _b37e75d : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_==Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _151fb31 : SortString → SortInt → SortInt → Option SortInt
  | "+", A, B => do
    let _Val0 <- «_+Int_» A B
    return _Val0
  | _, _, _ => none

noncomputable def _bc844c7 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_+Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _13d6ee6 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_*Int_» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _19c50ab : SortString → SortInt → SortInt → Option SortInt
  | "*", A, B => do
    let _Val0 <- «_*Int_» A B
    return _Val0
  | _, _, _ => none

mutual
  noncomputable def _6778888 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «_*Int_» A 10
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «_+Int_» _Val0 _Val1
      let _Val3 <- «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val2
      return _Val3
    | _, _ => none

  noncomputable def «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_0c827ea x0 x1) <|> (_6778888 x0 x1)
end

noncomputable def _00d63fc : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «absFloat(_)_FLOAT_Float_Float» F
    return _Val0

mutual
  noncomputable def _01ae2fc : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, ACC => do
      let _Val0 <- «_*Int_» ACC 10
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «_+Int_» _Val0 _Val1
      let _Val3 <- «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» R _Val2
      return _Val3
    | _, _ => none

  noncomputable def «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_01ae2fc x0 x1) <|> (_dc25660 x0 x1)
end

noncomputable def _03e60c5 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _0a30025 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen1 VR, K, V => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VR)
  | _, _, _, _ => none

noncomputable def _220c8a2 : SortString → SortVal → SortVal → Option SortBool
  | "is", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _57afa07 : SortString → SortVal → SortVal → Option SortBool
  | "==", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    return _Val0
  | _, _, _ => none

noncomputable def _58bdc88 : SortValSeq → SortVal → SortInt → Option SortInt
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, V, I => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    guard _Val0
    return I
  | _, _, _ => none

noncomputable def _6b7e0d4 : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

noncomputable def _78864a2 : SortValSeq → SortVal → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return true
  | _, _ => none

noncomputable def _dbd242d : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B _Gen1, K => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
    guard _Val0
    return B
  | _, _, _ => none

noncomputable def _f64794f : SortString → SortVal → SortVal → Option SortBool
  | "==", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      return _Val0
    | _, _ => none
  | _, _, _ => none

mutual
  noncomputable def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  noncomputable def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _6b454b2 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

noncomputable def _2ba1fdc : SortInt → SortInt → Option SortInt
  | I, LEN => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    guard _Val0
    return _Val1

noncomputable def _41490e6 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _5615d55 : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_<Int_» I1 I2
    guard _Val0
    return I1

noncomputable def _6e2ceae : SortInt → SortInt → Option SortInt
  | I, LEN => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    guard _Val0
    return _Val1

noncomputable def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

noncomputable def _ef1735c : SortValSeq → SortInt → SortVal → Option SortValSeq
  | VS, I, _Gen0 => do
    let _Val0 <- «_<Int_» I 0
    guard _Val0
    return VS

noncomputable def _ffe5f5d : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, _STEP => do
    let _Val0 <- «_<Int_» I LEN
    guard _Val0
    return I

noncomputable def _07c1bf0 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_*Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _0ae23e4 : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _2500272 : SortInt → SortInt → Option SortInt
  | J, _STEP => do
    let _Val0 <- «_>=Int_» J 0
    guard _Val0
    return J

noncomputable def _92d2fec : SortInt → SortInt → Option SortInt
  | I, _Gen0 => do
    let _Val0 <- «_>=Int_» I 0
    guard _Val0
    return I

noncomputable def _e1effea : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    guard _Val0
    return I2

noncomputable def _f4dd040 : SortInt → SortInt → Option SortInt
  | I, _Gen0 => do
    let _Val0 <- «_>=Int_» I 0
    guard _Val0
    return I

noncomputable def _0ce199a : SortVal → SortString → SortVals → Option SortVal
  | SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» CS, "hexdigest", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- md5hexCodes CS
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def «intsTail(_)_NEXT-SMALLEST-VERIFICATION_Ints_Ints» (x0 : SortInts) : Option SortInts := _0d21514 x0

mutual
  noncomputable def «maxVals(_,_)_MPY-BUILTINS_Int_Int_Vals» (x0 : SortInt) (x1 : SortVals) : Option SortInt := (_b660a31 x0 x1) <|> (_c3b9085 x0 x1)

  noncomputable def _b660a31 : SortInt → SortVals → Option SortInt
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «maxInt(_,_)_INT-COMMON_Int_Int_Int» M I
      let _Val1 <- «maxVals(_,_)_MPY-BUILTINS_Int_Int_Vals» _Val0 R
      return _Val1
    | _, _ => none
end

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  noncomputable def «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_5dd92ea x0 x1) <|> (_dcd0f49 x0 x1)

  noncomputable def _dcd0f49 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, A => do
      let _Val0 <- «_*Int_» A 10
      let _Val1 <- «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val0
      return _Val1
    | _, _ => none
end

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

noncomputable def «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» (x0 : SortInts) : Option SortBool := (_7c9eb36 x0) <|> (_bdc576b x0)

mutual
  noncomputable def _24a45bb : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_24a45bb x0 x1) <|> (_d9b4697 x0 x1)
end

noncomputable def «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» (x0 : SortOptInt) : Option SortInt := (_28a37d3 x0) <|> (_daab430 x0)

noncomputable def _16468f1 : SortIntSeq → SortInt → Option SortIntSeq
  | S, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return S

noncomputable def _1c34a14 : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_<=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _2c9e949 : SortInt → SortValSeq → Option SortValSeq
  | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt Y) R => do
    let _Val0 <- «_<=Int_» X Y
    guard _Val0
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) X) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) Y) R))
  | _, _ => none

noncomputable def «evHead47(_)_MPY-BUILTINS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_e46b672 x0) <|> (_e281c7f x0)

noncomputable def «evHead42(_)_MPY-BUILTINS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_b12fe18 x0) <|> (_fd6d3a4 x0)

noncomputable def «project:Val» (x0 : SortK) : Option SortVal := _150c95b x0

mutual
  noncomputable def _358ff3c : SortOpSeq → SortString → Option SortOpSeq
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» H T, O => do
      let _Val0 <- «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» T O
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» H _Val0)
    | _, _ => none

  noncomputable def «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» (x0 : SortOpSeq) (x1 : SortString) : Option SortOpSeq := (_34926f2 x0 x1) <|> (_358ff3c x0 x1)
end

mutual
  noncomputable def _781a952 : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, N => do
      let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» T N
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none

  noncomputable def «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_781a952 x0 x1) <|> (_84535a7 x0 x1)
end

noncomputable def _1e60d22 : SortInt → SortEvPair → Option SortEvPair
  | N, SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» M REST) => do
    let _Val0 <- «_^Int_» N M
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 REST))
  | _, _ => none

noncomputable def _4f03d42 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_>=Int_» I2 0
    let _Val1 <- «_^Int_» I1 I2
    guard _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _d72724a : SortString → SortInt → SortInt → Option SortInt
  | "**", A, B => do
    let _Val0 <- «_^Int_» A B
    return _Val0
  | _, _, _ => none

noncomputable def _9daeaea : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_^Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _e5f1d08 : SortInt → Option SortFloat
  | I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    return _Val0

mutual
  noncomputable def «revVSAcc(_,_)_MPY-SORT_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_d83ba47 x0 x1) <|> (_ed3ce26 x0 x1)

  noncomputable def _ed3ce26 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, A => do
      let _Val0 <- «revVSAcc(_,_)_MPY-SORT_ValSeq_ValSeq_ValSeq» R (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V A)
      return _Val0
    | _, _ => none
end

mutual
  noncomputable def _1a85154 : SortValSeq → SortInt → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, I => do
      let _Val0 <- «_+Int_» I 1
      let _Val1 <- «enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» R _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortIterable SortVal) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)))) _Val1)
    | _, _ => none

  noncomputable def «enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortValSeq := (_1a85154 x0 x1) <|> (_d770725 x0 x1)
end

noncomputable def _69b3bda : SortString → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» (0.0 : Float) F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _fabe8f9 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_-Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _3994b91 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0

noncomputable def _b558675 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def _dc1bc34 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_+Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _3836331 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

noncomputable def _85cabd6 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

mutual
  noncomputable def «appendVal(_,_)_MPY-CORE_Vals_Vals_Val» (x0 : SortVals) (x1 : SortVal) : Option SortVals := (_1dc0c6c x0 x1) <|> (_b10f912 x0 x1)

  noncomputable def _b10f912 : SortVals → SortVal → Option SortVals
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals» V0 VS, V => do
      let _Val0 <- «appendVal(_,_)_MPY-CORE_Vals_Vals_Val» VS V
      return (SortVals.«_,__MPY-CORE_Vals_Val_Vals» V0 _Val0)
    | _, _ => none
end

noncomputable def «firstNdE(_)_MPY-BUILTINS_Int_EvPair» (x0 : SortEvPair) : Option SortInt := (_89140a8 x0) <|> (_1de0a86 x0)

noncomputable def «powCarryE(_,_,_)_MPY-BUILTINS_EvPair_String_Int_EvPair» (x0 : SortString) (x1 : SortInt) (x2 : SortEvPair) : Option SortEvPair := _8ad47ba x0 x1 x2

mutual
  noncomputable def «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_5e2c753 x0 x1) <|> (_cd5036e x0 x1)

  noncomputable def _cd5036e : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, C => do
      let _Val0 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» T C
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none
end

noncomputable def _fee1f6e : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_>Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

noncomputable def «intsHead(_)_NEXT-SMALLEST-VERIFICATION_Int_Ints» (x0 : SortInts) : Option SortInt := _a9065e7 x0

noncomputable def _2b8c3d8 : SortInt → SortFloat → Option SortFloat
  | I, F => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» _Val0 F
    return _Val1

noncomputable def _ca2a05d : SortFloat → SortInt → Option SortFloat
  | F, I => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I 53 11
    let _Val1 <- «_/Float__FLOAT_Float_Float_Float» F _Val0
    return _Val1

noncomputable def _d8a2a0c : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    return _Val0

noncomputable def _ea38624 : SortFloat → SortFloat → Option SortFloat
  | F1, F2 => do
    let _Val0 <- «_/Float__FLOAT_Float_Float_Float» F1 F2
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» _Val0
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» _Val1 F2
    let _Val3 <- «_-Float__FLOAT_Float_Float_Float» F1 _Val2
    return _Val3

noncomputable def _edb22f9 : SortInt → SortInt → Option SortFloat
  | I1, I2 => do
    let _Val0 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I1 53 11
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» I2 53 11
    let _Val2 <- «_/Float__FLOAT_Float_Float_Float» _Val0 _Val1
    return _Val2

noncomputable def _9e5ad0c : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    return _Val0
  | _, _, _ => none

mutual
  noncomputable def _930c3bf : SortVals → Option SortValSeq
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals» V VS => do
      let _Val0 <- «vals2valSeq(_)_MPY-CORE_ValSeq_Vals» VS
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _ => none

  noncomputable def «vals2valSeq(_)_MPY-CORE_ValSeq_Vals» (x0 : SortVals) : Option SortValSeq := (_324a76c x0) <|> (_930c3bf x0)
end

mutual
  noncomputable def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  noncomputable def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

mutual
  noncomputable def «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_3c5ecf9 x0 x1) <|> (_cf6961f x0 x1)

  noncomputable def _cf6961f : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» R (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C A)
      return _Val0
    | _, _ => none
end

noncomputable def _5667141 : SortFloat → SortFloat → Option SortBool
  | F1, F2 => do
    let _Val0 <- «_<Float__FLOAT_Bool_Float_Float» F1 F2
    return _Val0

mutual
  noncomputable def _5230742 : SortIntSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «charsOf(_)_MPY-BUILTINS_ValSeq_IntSeq» R
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) _Val0)
    | _ => none

  noncomputable def «charsOf(_)_MPY-BUILTINS_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := (_5230742 x0) <|> (_8751d92 x0)
end

mutual
  noncomputable def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

noncomputable def «isRefV(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_6206d78 x0) <|> (_010fe30 x0)

noncomputable def «isStrV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_8978072 x0) <|> (_c788a4b x0)

mutual
  noncomputable def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

noncomputable def «headIS(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _b48ab39 x0

noncomputable def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

noncomputable def _d16bd47 : SortString → SortVals → Option SortVal
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «absInt(_)_INT-COMMON_Int_Int» I
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def «isIntV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_ec93494 x0) <|> (_fbb3e9c x0)

noncomputable def «cellsOf(_)_MPY-CORE_ParamNames_Val» (x0 : SortVal) : Option SortParamNames := _c69a3d5 x0

noncomputable def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

noncomputable def «isCellRef(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_d619e02 x0) <|> (_8403ac8 x0)

noncomputable def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

noncomputable def isKResult (x0 : SortK) : Option SortBool := (_f4c2469 x0) <|> (_afefecb x0)

noncomputable def «isKwV(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_121c40c x0) <|> (_f3b0384 x0)

noncomputable def «project:Float» (x0 : SortK) : Option SortFloat := _ef206f4 x0

noncomputable def «project:Int» (x0 : SortK) : Option SortInt := _f316b87 x0

noncomputable def _fc1f1e4 : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «rootFloat(_,_)_FLOAT_Float_Float_Int» F 2
    return _Val0

mutual
  noncomputable def _2b96129 : SortValSeq → SortVal → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» R V
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def _8f0e06e : SortValSeq → SortVal → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» R V
      let _Val2 <- «_+Int_» 1 _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  noncomputable def «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortInt := (_2b96129 x0 x1) <|> (_8f0e06e x0 x1) <|> (_e4ff78f x0 x1)
end

noncomputable def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _31fe72e : SortBool → SortBool → Option SortBool
  | B1, B2 => do
    let _Val0 <- «_==Bool_» B1 B2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _57f520f : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _7a57b51 : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

noncomputable def _882c519 : SortString → SortVal → SortVal → Option SortBool
  | "!=", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9f9c54d : SortString → SortVal → SortVal → Option SortBool
  | "!=", _Pat0, _Pat1 => match (@retr SortIterable SortVal) _Pat0, (@retr SortIterable SortVal) _Pat1 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» A), some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» B) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) B) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _, _ => none
  | _, _, _ => none

mutual
  noncomputable def «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortIntSeq := (_18b010b x0 x1 x2) <|> (_b5057da x0 x1 x2) <|> (_f58851d x0 x1 x2)

  noncomputable def _b5057da : SortIntSeq → SortInt → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A, B => do
      let _Val0 <- «_==Int_» C A
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» R A B
      guard _Val1
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Val2)
    | _, _, _ => none

  noncomputable def _f58851d : SortIntSeq → SortInt → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A, B => do
      let _Val0 <- «_==Int_» C A
      let _Val1 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» R A B
      guard _Val0
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B _Val1)
    | _, _, _ => none
end

noncomputable def _a99224c : SortVal → Option SortBool
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» S) => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) S) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _ => none

noncomputable def _c0092c8 : SortString → SortVal → SortVal → Option SortBool
  | "is not", V, SortVal.«noneV_MPY-CORE_Val» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) SortVal.«noneV_MPY-CORE_Val») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _c91e9fa : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- «_==Float_» F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _e6ccd5c : SortVal → Option SortBool
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» V) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _ => none

noncomputable def _f37ebb3 : SortVal → Option SortBool
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» V) => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortValSeq SortKItem) V) SortK.dotk) (SortK.kseq ((@inj SortValSeq SortKItem) SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk)
      let _Val1 <- notBool_ _Val0
      return _Val1
    | _ => none

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def _6ef1389 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fracAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 0
    return _Val0
  | _ => none

noncomputable def absF (x0 : SortFloat) : Option SortFloat := _00d63fc x0

mutual
  noncomputable def «idxOfVS(_,_,_)_MPY-TUPLE_Int_ValSeq_Val_Int» (x0 : SortValSeq) (x1 : SortVal) (x2 : SortInt) : Option SortInt := (_58bdc88 x0 x1 x2) <|> (_f6caf05 x0 x1 x2)

  noncomputable def _f6caf05 : SortValSeq → SortVal → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, V, I => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «_+Int_» I 1
      let _Val3 <- «idxOfVS(_,_,_)_MPY-TUPLE_Int_ValSeq_Val_Int» R V _Val2
      guard _Val1
      return _Val3
    | _, _, _ => none
end

mutual
  noncomputable def _07ab7bb : SortValSeq → SortVal → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A R, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» R K
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortBool := (_07ab7bb x0 x1) <|> (_78864a2 x0 x1) <|> (_fd49342 x0 x1)
end

mutual
  noncomputable def «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) : Option SortVal := (_a22e93c x0 x1 x2) <|> (_dbd242d x0 x1 x2)

  noncomputable def _a22e93c : SortValSeq → SortValSeq → SortVal → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 VR, K => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KR VR K
      guard _Val1
      return _Val2
    | _, _, _ => none
end

noncomputable def _04b6349 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
  | _KS, VS, _K, V => do
    let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    return _Val0

noncomputable def _ac76db8 : SortValSeq → SortIntSeq → Option SortValSeq
  | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C T => do
    let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C T))) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    return _Val0
  | _, _ => none

mutual
  noncomputable def _04c5fd3 : SortString → SortParamNames → Option SortBool
    | X, SortParamNames.«_,__MPY-SYNTAX_ParamNames_String_ParamNames» P R => do
      let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» X P
      let _Val1 <- «pnMember(_,_)_MPY-CORE_Bool_String_ParamNames» X R
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «pnMember(_,_)_MPY-CORE_Bool_String_ParamNames» (x0 : SortString) (x1 : SortParamNames) : Option SortBool := (_04c5fd3 x0 x1) <|> (_c0da98c x0 x1)
end

noncomputable def _390b355 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_==Int_» C 32
    let _Val1 <- «_==Int_» C 9
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» C 10
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» C 13
    let _Val6 <- _orBool_ _Val4 _Val5
    return _Val6

noncomputable def _6873178 : SortString → Option SortBool
  | M => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» M "append"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» M "sort"
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» M "extend"
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==String__STRING-COMMON_Bool_String_String» M "insert"
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==String__STRING-COMMON_Bool_String_String» M "pop"
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==String__STRING-COMMON_Bool_String_String» M "remove"
    let _Val10 <- _orBool_ _Val8 _Val9
    return _Val10

noncomputable def _8291415 : SortString → SortString → Option SortBool
  | "add", O => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» O "+"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» O "-"
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2
  | _, _ => none

mutual
  noncomputable def «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_80a1ae7 x0 x1) <|> (_c27c6a9 x0 x1)

  noncomputable def _c27c6a9 : SortInt → SortIntSeq → Option SortBool
    | C, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
      let _Val0 <- «_==Int_» C H
      let _Val1 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C T
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

noncomputable def _bb63bc4 : SortString → SortString → Option SortBool
  | "mul", O => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» O "*"
    let _Val1 <- «_==String__STRING-COMMON_Bool_String_String» O "//"
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==String__STRING-COMMON_Bool_String_String» O "/"
    let _Val4 <- _orBool_ _Val2 _Val3
    return _Val4
  | _, _ => none

mutual
  noncomputable def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  noncomputable def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

mutual
  noncomputable def _06c5fb7 : SortValSeq → SortInt → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W S, I, V => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «setVSAt(_,_,_)_MPY-CORE_ValSeq_ValSeq_Int_Val» S _Val1 V
      guard _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» W _Val2)
    | _, _, _ => none

  noncomputable def «setVSAt(_,_,_)_MPY-CORE_ValSeq_ValSeq_Int_Val» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortVal) : Option SortValSeq := (_06c5fb7 x0 x1 x2) <|> (_49a8097 x0 x1 x2) <|> (_ef1735c x0 x1 x2) <|> (_fdfd33a x0 x1 x2)
end

noncomputable def mulF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _07c1bf0 x0 x1

noncomputable def «normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_6e2ceae x0 x1) <|> (_92d2fec x0 x1)

noncomputable def «minInt(_,_)_INT-COMMON_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_5615d55 x0 x1) <|> (_e1effea x0 x1)

noncomputable def «normIdxD(_,_)_MPY-DICT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2ba1fdc x0 x1) <|> (_f4dd040 x0 x1)

noncomputable def _0d5862f : SortString → SortVals → Option SortVal
  | "max", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) REST => do
    let _Val0 <- «maxVals(_,_)_MPY-BUILTINS_Int_Int_Vals» I REST
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _18746b8 : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_>Int_» ST 0
    let _Val1 <- «_>Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» HI LO
    let _Val4 <- «_+Int_» _Val3 ST
    let _Val5 <- «_-Int_» _Val4 1
    let _Val6 <- «_/Int_» _Val5 ST
    guard _Val2
    return _Val6

noncomputable def _1c1496e : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq
  | _Gen0, I, STOP, STEP => do
    let _Val0 <- «_>Int_» STEP 0
    let _Val1 <- «_<Int_» I STOP
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» STEP 0
    let _Val4 <- «_>Int_» I STOP
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    guard _Val7
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _1f3d8f0 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 97
    let _Val1 <- «_<=Int_» C 122
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _2928123 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
  | _Gen0, I, STOP, STEP => do
    let _Val0 <- «_>Int_» STEP 0
    let _Val1 <- «_<Int_» I STOP
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» STEP 0
    let _Val4 <- «_>Int_» I STOP
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    let _Val7 <- notBool_ _Val6
    guard _Val7
    return SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

mutual
  noncomputable def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

noncomputable def _4ec3bb5 : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_>Int_» ST 0
    let _Val1 <- «_<=Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» ST 0
    let _Val4 <- «_>=Int_» HI LO
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    guard _Val6
    return 0

mutual
  noncomputable def _54ab88f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_2867a75 x0 x1) <|> (_54ab88f x0 x1) <|> (_55400f7 x0 x1)
end

noncomputable def _72eff8b : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<=Int_» 48 C
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» C 48
    guard _Val2
    return ((@inj SortInt SortVal) _Val3)
  | _, _ => none

noncomputable def _951deed : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 48
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _b6acdbd : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 65
    let _Val1 <- «_<=Int_» C 90
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _bb50555 : SortString → SortVals → Option SortVal
  | "chr", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<=Int_» 0 I
    let _Val1 <- «_<Int_» I 128
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
  | _, _ => none

noncomputable def _c0365fe : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 48
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def _d31716c : SortInt → SortInt → SortInt → Option SortInt
  | LO, HI, ST => do
    let _Val0 <- «_<Int_» ST 0
    let _Val1 <- «_<Int_» HI LO
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_-Int_» LO HI
    let _Val4 <- «_-Int_» _Val3 ST
    let _Val5 <- «_-Int_» _Val4 1
    let _Val6 <- «_-Int_» 0 ST
    let _Val7 <- «_/Int_» _Val5 _Val6
    guard _Val2
    return _Val7

noncomputable def _f46b3e6 : SortInt → SortInt → SortInt → Option SortBool
  | I, HI, ST => do
    let _Val0 <- «_>Int_» ST 0
    let _Val1 <- «_<Int_» I HI
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<Int_» ST 0
    let _Val4 <- «_>Int_» I HI
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    return _Val6

noncomputable def _c02b510 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 R => do
    let _Val0 <- «fscAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R 1
    return _Val0
  | _ => none

noncomputable def _213f0c2 : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_>=Int_» _Val0 2
    let _Val2 <- «intDigAcc(_,_)_MPY-BUILTINS_Int_IntSeq_Int» CS 0
    guard _Val1
    return ((@inj SortInt SortVal) _Val2)
  | _, _ => none

noncomputable def _4b33ea6 : SortVal → Option SortInt
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» IS) => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    return _Val0
  | _ => none

noncomputable def _d4293df : SortVal → Option SortInt
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» DS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» DS
    return _Val0
  | _ => none

noncomputable def _11f64e6 : SortInts → SortInt → SortInt → SortInt → Option SortVal
  | IS, _Gen0, _Gen1, C => do
    let _Val0 <- «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» IS
    let _Val1 <- «_==Int_» C 2
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    guard _Val3
    return SortVal.«noneV_MPY-CORE_Val»

noncomputable def _c68f9d7 : SortInts → SortInt → SortInt → SortInt → Option SortVal
  | IS, _Gen0, N, C => do
    let _Val0 <- «intsEmpty(_)_NEXT-SMALLEST-VERIFICATION_Bool_Ints» IS
    let _Val1 <- «_==Int_» C 2
    let _Val2 <- _andBool_ _Val0 _Val1
    guard _Val2
    return ((@inj SortInt SortVal) N)

noncomputable def _396b61d : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return 0
  | _, _, _ => none

noncomputable def _3cb3e9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    let _Val2 <- «_-Int_» LEN 1
    guard _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _6ddca9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    guard _Val1
    return (-1)
  | _, _, _ => none

noncomputable def _72787fe : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return LEN
  | _, _, _ => none

mutual
  noncomputable def «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_16468f1 x0 x1) <|> (_aa907da x0 x1) <|> (_4183651 x0 x1)

  noncomputable def _aa907da : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, N => do
      let _Val0 <- «_>Int_» N 0
      let _Val1 <- «_-Int_» N 1
      let _Val2 <- «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def _1422124 : SortInt → SortValSeq → Option SortValSeq
    | X, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt Y) R => do
      let _Val0 <- «_>Int_» X Y
      let _Val1 <- «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» X R
      guard _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) Y) _Val1)
    | _, _ => none

  noncomputable def «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortValSeq := (_1422124 x0 x1) <|> (_2c9e949 x0 x1) <|> (_611c5b2 x0 x1)
end

noncomputable def _a6e6ac4 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, CUR, SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq», _Gen1, OO, ON => do
    let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OO _Val0)
  | _, _, _, _, _, _ => none

noncomputable def _ce2bdd1 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
  | _Gen0, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» _Gen1 _Gen2, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OO, ON => do
    let _Val0 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
    return (SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OO _Val0)
  | _, _, _, _, _, _ => none

noncomputable def «powCombE(_,_)_MPY-BUILTINS_EvPair_Int_EvPair» (x0 : SortInt) (x1 : SortEvPair) : Option SortEvPair := (_18fc027 x0 x1) <|> (_1e60d22 x0 x1)

noncomputable def powF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _9daeaea x0 x1

noncomputable def intToF (x0 : SortInt) : Option SortFloat := _e5f1d08 x0

noncomputable def _1ef05bd : SortValSeq → Option SortValSeq
  | S => do
    let _Val0 <- «revVSAcc(_,_)_MPY-SORT_ValSeq_ValSeq_ValSeq» S SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    return _Val0

noncomputable def subF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _fabe8f9 x0 x1

noncomputable def eqF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _3994b91 x0 x1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def addF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _dc1bc34 x0 x1

noncomputable def ceilF (x0 : SortVal) : Option SortInt := (_0f9305e x0) <|> (_3836331 x0)

noncomputable def floorFI (x0 : SortVal) : Option SortInt := (_85cabd6 x0) <|> (_f73c85c x0)

noncomputable def gtF (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _fee1f6e x0 x1

noncomputable def intFloatDiv (x0 : SortInt) (x1 : SortFloat) : Option SortFloat := _2b8c3d8 x0 x1

noncomputable def divFloatIntV (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _ca2a05d x0 x1

noncomputable def divF (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _d8a2a0c x0 x1

noncomputable def floatMod (x0 : SortFloat) (x1 : SortFloat) : Option SortFloat := _ea38624 x0 x1

noncomputable def divII (x0 : SortInt) (x1 : SortInt) : Option SortFloat := _edb22f9 x0 x1

mutual
  noncomputable def _367d67f : SortIntSeq → SortInt → SortIntSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, SEP, CUR => do
      let _Val0 <- «_==Int_» C SEP
      let _Val1 <- «splitSep(_,_,_)_MPY-METHODS_ValSeq_IntSeq_Int_IntSeq» R SEP SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
      guard _Val0
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CUR)) _Val1)
    | _, _, _ => none

  noncomputable def «splitSep(_,_,_)_MPY-METHODS_ValSeq_IntSeq_Int_IntSeq» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortIntSeq) : Option SortValSeq := (_367d67f x0 x1 x2) <|> (_b92fdc6 x0 x1 x2) <|> (_dedba64 x0 x1 x2)

  noncomputable def _dedba64 : SortIntSeq → SortInt → SortIntSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, SEP, CUR => do
      let _Val0 <- «_==Int_» C SEP
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «splitSep(_,_,_)_MPY-METHODS_ValSeq_IntSeq_Int_IntSeq» R SEP _Val2
      guard _Val1
      return _Val3
    | _, _, _ => none
end

mutual
  noncomputable def _6dbca3c : SortIntSeq → SortValSeq → Option SortIntSeq
    | SEP, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R) => do
      let _Val0 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» SEP (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R)
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» SEP _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CS _Val1
      return _Val2
    | _, _ => none

  noncomputable def «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortIntSeq := (_2e9dd52 x0 x1) <|> (_553ef43 x0 x1) <|> (_6dbca3c x0 x1)
end

noncomputable def _c2eab84 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» A B
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def _4c429fa : SortIntSeq → Option SortIntSeq
  | S => do
    let _Val0 <- «revISAcc(_,_)_MPY-METHODS_IntSeq_IntSeq_IntSeq» S SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

noncomputable def floatLt (x0 : SortFloat) (x1 : SortFloat) : Option SortBool := _5667141 x0 x1

noncomputable def _8501a34 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      return _Val0
    | _ => none

noncomputable def _90ec921 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      return _Val0
    | _ => none

noncomputable def _73630e2 : SortString → SortVals → Option SortVal
  | "isinstance", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.«typeV(_)_MPY-CORE_Val_String» "str") SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- «isStrV(_)_MPY-BUILTINS_Bool_Val» V
    return ((@inj SortBool SortVal) _Val0)
  | _, _ => none

noncomputable def _eb8c1ed : SortString → SortVals → Option SortVal
  | "isinstance", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.«typeV(_)_MPY-CORE_Val_String» "int") SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- «isIntV(_)_MPY-BUILTINS_Bool_Val» V
    return ((@inj SortBool SortVal) _Val0)
  | _, _ => none

noncomputable def «sqrtFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat := _fc1f1e4 x0

noncomputable def _711e2c3 : SortVal → SortString → SortVals → Option SortVal
  | _Pat0, "count", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» VS V
      return ((@inj SortInt SortVal) _Val0)
    | _ => none
  | _, _, _ => none

noncomputable def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool := _31fe72e x0 x1

noncomputable def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _dde015f : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "replace", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- «replaceC(_,_,_)_MPY-METHODS_IntSeq_IntSeq_Int_Int» CS A B
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

noncomputable def _606434e : SortString → SortVals → Option SortVal
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- absF F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _445e463 : SortVal → SortString → SortVals → Option SortVal
  | _Pat0, "index", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «idxOfVS(_,_,_)_MPY-TUPLE_Int_ValSeq_Val_Int» VS V 0
      return ((@inj SortInt SortVal) _Val0)
    | _ => none
  | _, _, _ => none

noncomputable def _4a032b9 : SortValSeq → SortVal → Option SortValSeq
  | KS, K => do
    let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS K
    guard _Val0
    return KS

noncomputable def _4e69e6b : SortValSeq → SortVal → Option SortValSeq
  | KS, K => do
    let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS K
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» KS (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» K SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
    guard _Val1
    return _Val2

noncomputable def _9ea5167 : SortVal → SortVal → Option SortVal
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS VS, K => do
    let _Val0 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KS VS K
    return _Val0
  | _, _ => none

mutual
  noncomputable def «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) (x3 : SortValSeq) : Option SortBool := (_4613fdc x0 x1 x2 x3) <|> (_e2b14d5 x0 x1 x2 x3)

  noncomputable def _e2b14d5 : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» K KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V VR, KS2, VS2 => do
      let _Val0 <- «dHasKey(_,_)_MPY-DICT_Bool_ValSeq_Val» KS2 K
      let _Val1 <- «dGet(_,_,_)_MPY-DICT_Val_ValSeq_ValSeq_Val» KS2 VS2 K
      let _Val2 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) _Val1) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KR VR KS2 VS2
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _, _, _, _ => none
end

mutual
  noncomputable def _1a0a867 : SortValSeq → SortValSeq → SortVal → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» A KR, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B VR, K, V => do
      let _Val0 <- «_==K_» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortVal SortKItem) K) SortK.dotk)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» KR VR K V
      guard _Val1
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» B _Val2)
    | _, _, _, _ => none

  noncomputable def «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortVal) (x3 : SortVal) : Option SortValSeq := (_0a30025 x0 x1 x2 x3) <|> (_1a0a867 x0 x1 x2 x3) <|> (_04b6349 x0 x1 x2 x3)
end

noncomputable def «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» (x0 : SortValSeq) (x1 : SortIntSeq) : Option SortValSeq := (_a38c318 x0 x1) <|> (_ac76db8 x0 x1)

noncomputable def «isWSC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _390b355 x0

noncomputable def «isMutMethod(_)_MPY-CALL_Bool_String» (x0 : SortString) : Option SortBool := _6873178 x0

mutual
  noncomputable def _37448bb : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» ACC C
      let _Val3 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S _Val2
      guard _Val1
      return _Val3
    | _, _ => none

  noncomputable def _5d1e314 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S ACC
      guard _Val0
      return _Val1
    | _, _ => none

  noncomputable def «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_28cc140 x0 x1) <|> (_37448bb x0 x1) <|> (_5d1e314 x0 x1)
end

mutual
  noncomputable def _9bcb96b : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, B => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C B
      let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» S B
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_076da9f x0 x1) <|> (_9bcb96b x0 x1)
end

noncomputable def «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := (_8291415 x0 x1) <|> (_bb63bc4 x0 x1) <|> (_0105150 x0 x1)

noncomputable def _758418c : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _8a4564e : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9b4e435 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» B A
    return _Val0
  | _, _, _ => none

noncomputable def _f10cf1b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B) => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

noncomputable def _ffbdc85 : SortIntSeq → SortValSeq → Option SortValSeq
  | A, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R => do
    let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    guard _Val2
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» A)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R))
  | _, _ => none

noncomputable def _30456db : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- mulF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _77afc7e : SortVal → SortInt → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» IS), I => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val1 <- «normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int» I _Val0
    let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» IS _Val1
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val2 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
  | _, _ => none

noncomputable def _ae682a5 : SortVal → SortInt → Option SortVal
  | _Pat0, I => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int» I _Val0
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» VS _Val1
      return _Val2
    | _ => none

noncomputable def _dff41b0 : SortVal → SortInt → Option SortVal
  | _Pat0, I => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int» I _Val0
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» VS _Val1
      return _Val2
    | _ => none

mutual
  noncomputable def «minVals(_,_)_MPY-BUILTINS_Int_Int_Vals» (x0 : SortInt) (x1 : SortVals) : Option SortInt := (_cc77ef1 x0 x1) <|> (_d1c3ede x0 x1)

  noncomputable def _cc77ef1 : SortInt → SortVals → Option SortInt
    | M, SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» M I
      let _Val1 <- «minVals(_,_)_MPY-BUILTINS_Int_Int_Vals» _Val0 R
      return _Val1
    | _, _ => none
end

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

noncomputable def «isLowerC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _1f3d8f0 x0

axiom _5bd0f09 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
axiom «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortIntSeq

noncomputable def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

noncomputable def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

noncomputable def _8060dd0 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» XC), "startswith", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» PC)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» PC XC
    return ((@inj SortBool SortVal) _Val0)
  | _, _, _ => none

noncomputable def «isDigitC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _951deed x0

noncomputable def «isUpperC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _b6acdbd x0

noncomputable def «evDigit(_)_MPY-BUILTINS_Bool_Int» (x0 : SortInt) : Option SortBool := _c0365fe x0

noncomputable def «rangeLen(_,_,_)_MPY-RANGE_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_18746b8 x0 x1 x2) <|> (_4ec3bb5 x0 x1 x2) <|> (_d31716c x0 x1 x2)

noncomputable def «inRange(_,_,_)_MPY-RANGE_Bool_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortBool := _f46b3e6 x0 x1 x2

axiom _29d7acd : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _4d3e91d : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _4e28461 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _784fa17 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int» (x0 : SortInts) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortVal
axiom _b0d9be8 : SortInts → SortInt → SortInt → SortInt → Option SortVal
axiom _ffacc98 : SortInts → SortInt → SortInt → SortInt → Option SortVal

axiom «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt
axiom _b153473 : SortIntSeq → SortIntSeq → Option SortInt
axiom _f1b90b3 : SortIntSeq → SortIntSeq → Option SortInt

noncomputable def _a4f5818 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- powF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _1909c2e : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- powF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _50f1b5a : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- mulF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _b02af7e : SortVal → Option SortFloat
  | SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    return _Val0
  | _ => none

noncomputable def _ca41a23 : SortString → SortVal → SortVal → Option SortVal
  | "*", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- mulF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _e0a3283 : SortString → SortVal → SortVal → Option SortVal
  | "**", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- powF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _e64428a : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- intToF I
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def «revVS(_)_MPY-SORT_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := _1ef05bd x0

noncomputable def _a6670cb : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- subF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _d8961f0 : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- subF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _ebcc6ed : SortString → SortVal → SortVal → Option SortVal
  | "-", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- subF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _1eb1e83 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- eqF _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _31a7ce9 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- eqF F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9ec2057 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- eqF _Val0 F
    let _Val2 <- notBool_ _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _b076352 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- eqF F _Val0
    let _Val2 <- notBool_ _Val1
    return _Val2
  | _, _, _ => none

axiom _62d7600 : SortInt → SortIntSeq → Option SortIntSeq
axiom «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq

noncomputable def _7f23ecf : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def _dece19f : SortString → SortVal → SortVal → Option SortVal
  | "//", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I1 I2
    let _Val1 <- «_-Int_» I1 _Val0
    let _Val2 <- «_/Int_» _Val1 I2
    return ((@inj SortInt SortVal) _Val2)
  | _, _, _ => none

noncomputable def _a4f63fd : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- addF F _Val0
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _b009d60 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- addF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _f394023 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- addF _Val0 F
    return ((@inj SortFloat SortVal) _Val1)
  | _, _, _ => none

noncomputable def _4807966 : SortString → SortVals → Option SortVal
  | "ceil", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- ceilF V
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _2d8e778 : SortString → SortVals → Option SortVal
  | "floor", SortVals.«_,__MPY-CORE_Vals_Val_Vals» V SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- floorFI V
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _21c3768 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- gtF F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _3762d3f : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _641b30a : SortString → SortVal → SortVal → Option SortBool
  | "<=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- gtF F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f5cd646 : SortString → SortVal → SortVal → Option SortBool
  | ">", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- gtF _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _4f373ea : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intFloatDiv I F
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _3598da3 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- divFloatIntV F I
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _42bfa12 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- divF F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _2acce51 : SortString → SortVal → SortVal → Option SortVal
  | "%", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatMod F1 F2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _798d463 : SortString → SortVal → SortVal → Option SortVal
  | "/", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- divII I1 I2
    return ((@inj SortFloat SortVal) _Val0)
  | _, _, _ => none

noncomputable def _5667eab : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» SEP), "join", SortVals.«_,__MPY-CORE_Vals_Val_Vals» _Pat0 SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «joinCodes(_,_)_MPY-METHODS_IntSeq_IntSeq_ValSeq» SEP VS
      return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
    | _ => none
  | _, _, _ => none

noncomputable def «revIS(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _4c429fa x0

noncomputable def _42db81d : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortInt I, SortVal.inj_SortFloat F => do
    let _Val0 <- intToF I
    let _Val1 <- floatLt _Val0 F
    return _Val1
  | _, _, _ => none

noncomputable def _b69f73f : SortString → SortVal → SortVal → Option SortBool
  | ">=", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _beb7b49 : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F, SortVal.inj_SortInt I => do
    let _Val0 <- intToF I
    let _Val1 <- floatLt F _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _f53e67b : SortString → SortVal → SortVal → Option SortBool
  | "<", SortVal.inj_SortFloat F1, SortVal.inj_SortFloat F2 => do
    let _Val0 <- floatLt F1 F2
    return _Val0
  | _, _, _ => none

noncomputable def _e8f314f : SortFloat → Option SortFloat
  | F => do
    let _Val0 <- «sqrtFloat(_)_FLOAT_Float_Float» F
    return _Val0

noncomputable def _3cc6493 : SortInt → SortInt → Option SortInt
  | J, STEP => do
    let _Val0 <- «_<Int_» J 0
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- kite _Val1 (-1) 0
    guard _Val0
    return _Val2

noncomputable def _4865897 : SortVal → Option SortInt
  | SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    return _Val0
  | _ => none

noncomputable def _6f49a32 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I LEN
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- «_-Int_» LEN 1
    let _Val3 <- kite _Val1 _Val2 LEN
    guard _Val0
    return _Val3

noncomputable def _7ff1b9f : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortBool B, SortVal.inj_SortInt I => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» _Val0 I
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _addf2bf : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «_>=Float__FLOAT_Bool_Float_Float» F (0.0 : Float)
    let _Val1 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val2 <- «Float2Int(_)_FLOAT_Int_Float» _Val1
    let _Val3 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val4 <- «Float2Int(_)_FLOAT_Int_Float» _Val3
    let _Val5 <- kite _Val0 _Val2 _Val4
    return _Val5

noncomputable def _b220c77 : SortFloat → Option SortInt
  | F => do
    let _Val0 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «_-Float__FLOAT_Float_Float_Float» F _Val0
    let _Val2 <- «_==Float_» _Val1 (0.5 : Float)
    let _Val3 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val4 <- «Float2Int(_)_FLOAT_Int_Float» _Val3
    let _Val5 <- «_%Int_» _Val4 2
    let _Val6 <- «_==Int_» _Val5 0
    let _Val7 <- «floorFloat(_)_FLOAT_Float_Float» F
    let _Val8 <- «Float2Int(_)_FLOAT_Int_Float» _Val7
    let _Val9 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val10 <- «Float2Int(_)_FLOAT_Int_Float» _Val9
    let _Val11 <- kite _Val6 _Val8 _Val10
    let _Val12 <- «_+Float__FLOAT_Float_Float_Float» F (0.5 : Float)
    let _Val13 <- «floorFloat(_)_FLOAT_Float_Float» _Val12
    let _Val14 <- «Float2Int(_)_FLOAT_Int_Float» _Val13
    let _Val15 <- kite _Val2 _Val11 _Val14
    return _Val15

noncomputable def _bb59890 : SortString → SortVal → SortVal → Option SortVal
  | "+", SortVal.inj_SortInt I, SortVal.inj_SortBool B => do
    let _Val0 <- kite B 1 0
    let _Val1 <- «_+Int_» I _Val0
    return ((@inj SortInt SortVal) _Val1)
  | _, _, _ => none

noncomputable def _7031c92 : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortBool B1, SortVal.inj_SortBool B2 => do
    let _Val0 <- «_=/=Bool_» B1 B2
    return _Val0
  | _, _, _ => none

mutual
  noncomputable def _002e323 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «fracPart(_)_MPY-FLOAT_Int_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  noncomputable def «fracPart(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_002e323 x0) <|> (_6ef1389 x0) <|> (_dcbe275 x0)
end

mutual
  noncomputable def _10441cc : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «fracScale(_)_MPY-FLOAT_Int_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  noncomputable def «fracScale(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_10441cc x0) <|> (_c02b510 x0) <|> (_e688eef x0)
end

noncomputable def _296075e : SortVal → Option SortBool
  | SortVal.inj_SortInt I => do
    let _Val0 <- «_=/=Int_» I 0
    return _Val0
  | _ => none

noncomputable def _83dcf9b : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_=/=Int_» I2 0
    let _Val1 <- _modInt_ I1 I2
    let _Val2 <- «_-Int_» I1 _Val1
    let _Val3 <- «_/Int_» _Val2 I2
    guard _Val0
    return _Val3

mutual
  noncomputable def «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_a28602a x0 x1) <|> (_c3be6f0 x0 x1) <|> (_c5937bc x0 x1)

  noncomputable def _a28602a : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, A => do
      let _Val0 <- «_=/=Int_» C 46
      let _Val1 <- «_*Int_» A 10
      let _Val2 <- «_-Int_» C 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» R _Val3
      guard _Val0
      return _Val4
    | _, _ => none
end

noncomputable def _c986c4d : SortString → SortVal → SortVal → Option SortBool
  | "!=", SortVal.inj_SortInt I1, SortVal.inj_SortInt I2 => do
    let _Val0 <- «_=/=Int_» I1 I2
    return _Val0
  | _, _, _ => none

noncomputable def _dc46a10 : SortString → SortVals → Option SortVal
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt A) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt B) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt S) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) => do
    let _Val0 <- «_=/=Int_» S 0
    guard _Val0
    return ((@inj SortIterable SortVal) (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» A B S))
  | _, _ => none

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

mutual
  noncomputable def _65f01c5 : SortOpSeq → SortIntSeq → Option SortEvPair
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "**" OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS => do
      let _Val0 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS
      let _Val1 <- «powCombE(_,_)_MPY-BUILTINS_EvPair_Int_EvPair» N _Val0
      return _Val1
    | _, _ => none

  noncomputable def «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» (x0 : SortOpSeq) (x1 : SortIntSeq) : Option SortEvPair := (_2553414 x0 x1) <|> (_65f01c5 x0 x1) <|> (_c7dba0d x0 x1) <|> (_eeba85e x0 x1)

  noncomputable def _c7dba0d : SortOpSeq → SortIntSeq → Option SortEvPair
    | SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS => do
      let _Val0 <- «_=/=String__STRING-COMMON_Bool_String_String» O "**"
      let _Val1 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS NDS
      let _Val2 <- «powCarryE(_,_,_)_MPY-BUILTINS_EvPair_String_Int_EvPair» O N _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

noncomputable def «dPutK(_,_)_MPY-DICT_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_4a032b9 x0 x1) <|> (_4e69e6b x0 x1)

noncomputable def «applyIndexD(_,_)_MPY-DICT_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortVal := _9ea5167 x0 x1

noncomputable def _9a8a33a : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS1 VS1, SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS2 VS2 => do
    let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS1
    let _Val1 <- «vsLen(_)_MPY-CORE_Int_ValSeq» KS2
    let _Val2 <- «_==Int_» _Val0 _Val1
    let _Val3 <- «dSubset(_,_,_,_)_MPY-DICT_Bool_ValSeq_ValSeq_ValSeq_ValSeq» KS1 VS1 KS2 VS2
    let _Val4 <- _andBool_ _Val2 _Val3
    return _Val4
  | _, _, _ => none

noncomputable def _adaabae : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», CUR, ACC => do
    let _Val0 <- «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» ACC CUR
    return _Val0
  | _, _, _ => none

noncomputable def _f46896b : SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
    let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R)
  | _ => none

noncomputable def _a8c9961 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

noncomputable def _d3d248d : SortIntSeq → SortIntSeq → Option SortBool
  | A, B => do
    let _Val0 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    let _Val1 <- «subsetCodes(_,_)_MPY-SET_Bool_IntSeq_IntSeq» B A
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

mutual
  noncomputable def _92629aa : SortIntSeq → SortValSeq → Option SortValSeq
    | A, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) R => do
      let _Val0 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» A B
      let _Val1 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) A) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) B) SortK.dotk)
      let _Val2 <- _orBool_ _Val0 _Val1
      let _Val3 <- notBool_ _Val2
      let _Val4 <- «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» A R
      guard _Val3
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» B)) _Val4)
    | _, _ => none

  noncomputable def «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortValSeq) : Option SortValSeq := (_4725bc2 x0 x1) <|> (_92629aa x0 x1) <|> (_ffbdc85 x0 x1)
end

noncomputable def «applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int» (x0 : SortVal) (x1 : SortInt) : Option SortVal := (_77afc7e x0 x1) <|> (_ae682a5 x0 x1) <|> (_dff41b0 x0 x1)

noncomputable def _d7fe6d3 : SortString → SortVals → Option SortVal
  | "min", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) REST => do
    let _Val0 <- «minVals(_,_)_MPY-BUILTINS_Int_Int_Vals» I REST
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _756c9a9 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_-Int_» C 32
    guard _Val0
    return _Val1

noncomputable def _84d037f : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_-Int_» C 32
    guard _Val0
    return _Val1

mutual
  noncomputable def «hasLower(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_a2318fa x0) <|> (_af583db x0)

  noncomputable def _af583db : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «hasLower(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

mutual
  noncomputable def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  noncomputable def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def _59e9bba : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «allDigit(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «allDigit(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_59e9bba x0) <|> (_e321d7c x0)
end

noncomputable def _19d844e : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_+Int_» C 32
    guard _Val0
    return _Val1

noncomputable def _810a7fe : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_+Int_» C 32
    guard _Val0
    return _Val1

mutual
  noncomputable def «hasUpper(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_9c2daf9 x0) <|> (_b8d1bc2 x0)

  noncomputable def _b8d1bc2 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «hasUpper(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

noncomputable def _d240c9a : SortInt → Option SortBool
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2

mutual
  noncomputable def _14cc9b7 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 43 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "+" _Val0)
    | _ => none

  noncomputable def _3cea09f : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 R => do
      let _Val0 <- «evHead42(_)_MPY-BUILTINS_Bool_IntSeq» R
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val1
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "*" _Val2)
    | _ => none

  noncomputable def _6191372 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 R) => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "**" _Val0)
    | _ => none

  noncomputable def _6493ac0 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 R) => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "//" _Val0)
    | _ => none

  noncomputable def «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» (x0 : SortIntSeq) : Option SortOpSeq := (_14cc9b7 x0) <|> (_3cea09f x0) <|> (_6191372 x0) <|> (_6493ac0 x0) <|> (_afebecb x0) <|> (_cbc323c x0) <|> (_d2e1914 x0) <|> (_eceab8b x0) <|> (_f976bf9 x0)

  noncomputable def _afebecb : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "-" _Val0)
    | _ => none

  noncomputable def _cbc323c : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 R => do
      let _Val0 <- «evHead47(_)_MPY-BUILTINS_Bool_IntSeq» R
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val1
      return (SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» "/" _Val2)
    | _ => none

  noncomputable def _d2e1914 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  noncomputable def _f976bf9 : SortIntSeq → Option SortOpSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 R => do
      let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» R
      return _Val0
    | _ => none
end

mutual
  noncomputable def «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortIntSeq := (_b965464 x0 x1) <|> (_f2650fa x0 x1)

  noncomputable def «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_1f82817 x0) <|> (_a9081b9 x0) <|> (_cd3c56b x0) <|> (_d31de50 x0)

  noncomputable def _a9081b9 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «_=/=Int_» C 32
      let _Val3 <- _andBool_ _Val1 _Val2
      let _Val4 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» R
      guard _Val3
      return _Val4
    | _ => none

  noncomputable def _b965464 : SortInt → SortIntSeq → Option SortIntSeq
    | A, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «_*Int_» A 10
      let _Val2 <- «_-Int_» C 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» _Val3 R
      guard _Val0
      return _Val4
    | _, _ => none

  noncomputable def _cd3c56b : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «evDigit(_)_MPY-BUILTINS_Bool_Int» C
      let _Val1 <- «_-Int_» C 48
      let _Val2 <- «tokNdAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» _Val1 R
      guard _Val0
      return _Val2
    | _ => none

  noncomputable def _d31de50 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 R => do
      let _Val0 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» R
      return _Val0
    | _ => none

  noncomputable def _f2650fa : SortInt → SortIntSeq → Option SortIntSeq
    | A, S => do
      let _Val0 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» S
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A _Val0)
end

noncomputable def _1719aa8 : SortVal → Option SortInt
  | _Pat0 => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» LO HI ST) => do
      let _Val0 <- «rangeLen(_,_,_)_MPY-RANGE_Int_Int_Int_Int» LO HI ST
      return _Val0
    | _ => none

noncomputable def _88460b3 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "count", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» PC)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS PC
    return ((@inj SortInt SortVal) _Val0)
  | _, _, _ => none

noncomputable def toF (x0 : SortVal) : Option SortFloat := (_0290a71 x0) <|> (_b02af7e x0)

noncomputable def _1a20c58 : SortValSeq → SortBool → Option SortValSeq
  | S, true => do
    let _Val0 <- «revVS(_)_MPY-SORT_ValSeq_ValSeq» S
    return _Val0
  | _, _ => none

noncomputable def _323c995 : SortInt → Option SortIntSeq
  | N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- «binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq» N SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    guard _Val0
    return _Val1

noncomputable def sqrtF (x0 : SortFloat) : Option SortFloat := _e8f314f x0

noncomputable def «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2500272 x0 x1) <|> (_3cc6493 x0 x1)

noncomputable def «intOf(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_4865897 x0) <|> (_9f02755 x0)

noncomputable def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6f49a32 x0 x1 x2) <|> (_ffe5f5d x0 x1 x2)

noncomputable def truncF (x0 : SortFloat) : Option SortInt := _addf2bf x0

noncomputable def roundF (x0 : SortFloat) : Option SortInt := _b220c77 x0

noncomputable def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortVal := (_13d6ee6 x0 x1 x2) <|> (_1909c2e x0 x1 x2) <|> (_2acce51 x0 x1 x2) <|> (_30456db x0 x1 x2) <|> (_3598da3 x0 x1 x2) <|> (_42bfa12 x0 x1 x2) <|> (_4f03d42 x0 x1 x2) <|> (_4f373ea x0 x1 x2) <|> (_50f1b5a x0 x1 x2) <|> (_50f1b5a x0 x1 x2) <|> (_614d946 x0 x1 x2) <|> (_798d463 x0 x1 x2) <|> (_7f23ecf x0 x1 x2) <|> (_7ff1b9f x0 x1 x2) <|> (_a4f5818 x0 x1 x2) <|> (_a4f63fd x0 x1 x2) <|> (_a4f63fd x0 x1 x2) <|> (_a6670cb x0 x1 x2) <|> (_b009d60 x0 x1 x2) <|> (_bb59890 x0 x1 x2) <|> (_bc844c7 x0 x1 x2) <|> (_c2eab84 x0 x1 x2) <|> (_ca41a23 x0 x1 x2) <|> (_ca41a23 x0 x1 x2) <|> (_d8961f0 x0 x1 x2) <|> (_d8961f0 x0 x1 x2) <|> (_dece19f x0 x1 x2) <|> (_e0a3283 x0 x1 x2) <|> (_ebcc6ed x0 x1 x2) <|> (_ebcc6ed x0 x1 x2) <|> (_f394023 x0 x1 x2) <|> (_f394023 x0 x1 x2)

noncomputable def «truthy(_)_MPY-CORE_Bool_Val» (x0 : SortVal) : Option SortBool := (_296075e x0) <|> (_542a815 x0) <|> (_a99224c x0) <|> (_e6ccd5c x0) <|> (_f05ec3f x0) <|> (_f37ebb3 x0)

noncomputable def _divInt_ (x0 : SortInt) (x1 : SortInt) : Option SortInt := _83dcf9b x0 x1

noncomputable def _0bf42d3 : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «intPartAcc(_,_)_MPY-FLOAT_Int_IntSeq_Int» CS 0
    return _Val0

noncomputable def _108b118 : SortString → SortVals → Option SortVal
  | "str", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt I) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» I
    let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1))
  | _, _ => none

mutual
  noncomputable def _73ac687 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) R => do
      let _Val0 <- «Int2String(_)_STRING-COMMON_String_Int» I
      let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» _Val0
      let _Val2 <- «mapStrVS(_)_MPY-BUILTINS_ValSeq_ValSeq» R
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1)) _Val2)
    | _ => none

  noncomputable def «mapStrVS(_)_MPY-BUILTINS_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_73ac687 x0) <|> (_dfeef54 x0) <|> (_fe27687 x0)

  noncomputable def _fe27687 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) R => do
      let _Val0 <- «mapStrVS(_)_MPY-BUILTINS_ValSeq_ValSeq» R
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) _Val0)
    | _ => none
end

noncomputable def _f2c33a4 : SortVal → SortVal → SortVal → Option SortVal
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» KS VS, K, V => do
    let _Val0 <- «dPutK(_,_)_MPY-DICT_ValSeq_ValSeq_Val» KS K
    let _Val1 <- «dPutV(_,_,_,_)_MPY-DICT_ValSeq_ValSeq_ValSeq_Val_Val» KS VS K V
    return (SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» _Val0 _Val1)
  | _, _, _ => none

mutual
  noncomputable def «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortValSeq) : Option SortValSeq := (_a8a9e75 x0 x1 x2) <|> (_adaabae x0 x1 x2) <|> (_ceeef05 x0 x1 x2)

  noncomputable def _a8a9e75 : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, CUR, ACC => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» CUR (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» R _Val2 ACC
      guard _Val1
      return _Val3
    | _, _, _ => none

  noncomputable def _ceeef05 : SortIntSeq → SortIntSeq → SortValSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R, CUR, ACC => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «flushTok(_,_)_MPY-METHODS_ValSeq_ValSeq_IntSeq» ACC CUR
      let _Val2 <- «splitWS(_,_,_)_MPY-METHODS_ValSeq_IntSeq_IntSeq_ValSeq» R SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» _Val1
      guard _Val0
      return _Val2
    | _, _, _ => none
end

mutual
  noncomputable def _7b2ab54 : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C R => do
      let _Val0 <- «isWSC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» R
      guard _Val0
      return _Val1
    | _ => none

  noncomputable def «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_7b2ab54 x0) <|> (_b5f8fbb x0) <|> (_f46896b x0)
end

noncomputable def «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _a8c9961 x0

noncomputable def «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := _d3d248d x0 x1

mutual
  noncomputable def _185c4a4 : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) R => do
      let _Val0 <- sortVS R
      let _Val1 <- «insVSs(_,_)_MPY-SORT_ValSeq_IntSeq_ValSeq» CS _Val0
      return _Val1
    | _ => none

  noncomputable def _57346fe : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt X) R => do
      let _Val0 <- sortVS R
      let _Val1 <- «insVS(_,_)_MPY-SORT_ValSeq_Int_ValSeq» X _Val0
      return _Val1
    | _ => none

  noncomputable def sortVS (x0 : SortValSeq) : Option SortValSeq := (_185c4a4 x0) <|> (_57346fe x0) <|> (_7e4861f x0)
end

noncomputable def «upperC(_)_MPY-METHODS_Int_Int» (x0 : SortInt) : Option SortInt := (_84d037f x0) <|> (_abb6b77 x0)

noncomputable def _0d7d6b1 : SortString → SortVal → SortVal → Option SortBool
  | "not in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    let _Val1 <- notBool_ _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _9d30e79 : SortString → SortVal → SortVal → Option SortBool
  | "in", SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» P), SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» X) => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    return _Val0
  | _, _, _ => none

noncomputable def _5d102b6 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "isdigit", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) CS) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «allDigit(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val3 <- _andBool_ _Val1 _Val2
    return ((@inj SortBool SortVal) _Val3)
  | _, _, _ => none

noncomputable def «swapC(_)_MPY-METHODS_Int_Int» (x0 : SortInt) : Option SortInt := (_19d844e x0) <|> (_756c9a9 x0) <|> (_3dabce1 x0)

noncomputable def «lowerC(_)_MPY-METHODS_Int_Int» (x0 : SortInt) : Option SortInt := (_810a7fe x0) <|> (_7573b98 x0)

noncomputable def _37ed508 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "islower", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «hasLower(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val1 <- «hasUpper(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    return ((@inj SortBool SortVal) _Val3)
  | _, _, _ => none

noncomputable def _755caa7 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "isupper", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «hasUpper(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val1 <- «hasLower(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val2 <- notBool_ _Val1
    let _Val3 <- _andBool_ _Val0 _Val2
    return ((@inj SortBool SortVal) _Val3)
  | _, _, _ => none

noncomputable def «isAlphaC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _d240c9a x0

noncomputable def «seqLen(_)_MPY-BUILTINS_Int_Val» (x0 : SortVal) : Option SortInt := (_1719aa8 x0) <|> (_4b33ea6 x0) <|> (_8501a34 x0) <|> (_90ec921 x0) <|> (_d4293df x0)

noncomputable def «condRev(_,_)_MPY-SORT_ValSeq_ValSeq_Bool» (x0 : SortValSeq) (x1 : SortBool) : Option SortValSeq := (_1a20c58 x0 x1) <|> (_eb0d315 x0 x1)

noncomputable def «binCodes(_)_MPY-BUILTINS_IntSeq_Int» (x0 : SortInt) : Option SortIntSeq := (_323c995 x0) <|> (_49c55eb x0)

noncomputable def _e75deb6 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    let _Val2 <- «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» _Val1 STEP
    guard _Val0
    return _Val2

noncomputable def _4b524a8 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN STEP
    guard _Val0
    return _Val1

noncomputable def _ecd3e5c : SortString → SortVals → Option SortVal
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- truncF F
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _1b20c41 : SortString → SortVals → Option SortVal
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- roundF F
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _63e8a81 : SortFloat → SortInt → Option SortFloat
  | F, N => do
    let _Val0 <- «_^Int_» 10 N
    let _Val1 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val0 53 11
    let _Val2 <- «_*Float__FLOAT_Float_Float_Float» F _Val1
    let _Val3 <- roundF _Val2
    let _Val4 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val3 53 11
    let _Val5 <- «_^Int_» 10 N
    let _Val6 <- «Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» _Val5 53 11
    let _Val7 <- «_/Float__FLOAT_Float_Float_Float» _Val4 _Val6
    return _Val7

noncomputable def _b48e091 : SortString → SortVal → Option SortVal
  | "not", V => do
    let _Val0 <- «truthy(_)_MPY-CORE_Bool_Val» V
    let _Val1 <- notBool_ _Val0
    return ((@inj SortBool SortVal) _Val1)
  | _, _ => none

noncomputable def _e865ca1 : SortString → SortInt → SortInt → Option SortInt
  | "//", A, B => do
    let _Val0 <- _divInt_ A B
    return _Val0
  | _, _, _ => none

noncomputable def «intPart(_)_MPY-FLOAT_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _0bf42d3 x0

noncomputable def «dictSet(_,_,_)_MPY-DICT_Val_Val_Val_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortVal) : Option SortVal := _f2c33a4 x0 x1 x2

noncomputable def _f0d69ff : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "strip", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» CS
    let _Val1 <- «revIS(_)_MPY-METHODS_IntSeq_IntSeq» _Val0
    let _Val2 <- «trimWS(_)_MPY-METHODS_IntSeq_IntSeq» _Val1
    let _Val3 <- «revIS(_)_MPY-METHODS_IntSeq_IntSeq» _Val2
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3))
  | _, _, _ => none

noncomputable def _20b19cf : SortString → SortVals → Option SortVal
  | "set", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» CS
    return (SortVal.«setV(_)_MPY-SET_Val_IntSeq» _Val0)
  | _, _ => none

noncomputable def _87bf7c6 : SortString → SortVal → SortVal → Option SortBool
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» A, SortVal.«setV(_)_MPY-SET_Val_IntSeq» B => do
    let _Val0 <- «sameSet(_,_)_MPY-SET_Bool_IntSeq_IntSeq» A B
    return _Val0
  | _, _, _ => none

mutual
  noncomputable def _297335c : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «upperC(_)_MPY-METHODS_Int_Int» C
      let _Val1 <- «mapUpper(_)_MPY-METHODS_IntSeq_IntSeq» S
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 _Val1)
    | _ => none

  noncomputable def «mapUpper(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_297335c x0) <|> (_46f4f7d x0)
end

mutual
  noncomputable def «mapSwap(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_7fd70ea x0) <|> (_bce067a x0)

  noncomputable def _bce067a : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «swapC(_)_MPY-METHODS_Int_Int» C
      let _Val1 <- «mapSwap(_)_MPY-METHODS_IntSeq_IntSeq» S
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 _Val1)
    | _ => none
end

mutual
  noncomputable def «mapLower(_)_MPY-METHODS_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := (_3695ec2 x0) <|> (_a6e4b3b x0)

  noncomputable def _a6e4b3b : SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «lowerC(_)_MPY-METHODS_Int_Int» C
      let _Val1 <- «mapLower(_)_MPY-METHODS_IntSeq_IntSeq» S
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 _Val1)
    | _ => none
end

mutual
  noncomputable def «allAlpha(_)_MPY-METHODS_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_6cfd1c6 x0) <|> (_bbba114 x0)

  noncomputable def _bbba114 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S => do
      let _Val0 <- «isAlphaC(_)_MPY-METHODS_Bool_Int» C
      let _Val1 <- «allAlpha(_)_MPY-METHODS_Bool_IntSeq» S
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

noncomputable def _f1c888d : SortString → SortVals → Option SortVal
  | "len", SortVals.«_,__MPY-CORE_Vals_Val_Vals» OBJ SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «seqLen(_)_MPY-BUILTINS_Int_Val» OBJ
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def _a4fd04a : SortString → SortVals → Option SortVal
  | "bin", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_>=Int_» N 0
    let _Val1 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» N
    guard _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 _Val1))))
  | _, _ => none

noncomputable def _e22316b : SortString → SortVals → Option SortVal
  | "bin", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_<Int_» N 0
    let _Val1 <- «_-Int_» 0 N
    let _Val2 <- «binCodes(_)_MPY-BUILTINS_IntSeq_Int» _Val1
    guard _Val0
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 _Val2)))))
  | _, _ => none

noncomputable def «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_4b524a8 x0 x1 x2) <|> (_e75deb6 x0 x1 x2)

noncomputable def roundFN (x0 : SortFloat) (x1 : SortInt) : Option SortFloat := _63e8a81 x0 x1

noncomputable def «applyUn(_,_)_MPY-CORE_Val_String_Val» (x0 : SortString) (x1 : SortVal) : Option SortVal := (_30ee06e x0 x1) <|> (_69b3bda x0 x1) <|> (_b48e091 x0 x1)

noncomputable def «applyOpE(_,_,_)_MPY-BUILTINS_Int_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_151fb31 x0 x1 x2) <|> (_19c50ab x0 x1 x2) <|> (_778079e x0 x1 x2) <|> (_d72724a x0 x1 x2) <|> (_e865ca1 x0 x1 x2) <|> (_073f426 x0 x1 x2)

noncomputable def _f17777e : SortIntSeq → Option SortFloat
  | CS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_>Int_» _Val0 0
    let _Val2 <- «headIS(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val3 <- «_=/=Int_» _Val2 45
    let _Val4 <- _andBool_ _Val1 _Val3
    let _Val5 <- «intPart(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val6 <- intToF _Val5
    let _Val7 <- «fracPart(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val8 <- intToF _Val7
    let _Val9 <- «fracScale(_)_MPY-FLOAT_Int_IntSeq» CS
    let _Val10 <- intToF _Val9
    let _Val11 <- «_/Float__FLOAT_Float_Float_Float» _Val8 _Val10
    let _Val12 <- «_+Float__FLOAT_Float_Float_Float» _Val6 _Val11
    guard _Val4
    return _Val12

noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» (x0 : SortString) (x1 : SortVal) (x2 : SortVal) : Option SortBool := (_03e60c5 x0 x1 x2) <|> (_0ae23e4 x0 x1 x2) <|> (_0d7d6b1 x0 x1 x2) <|> (_1c34a14 x0 x1 x2) <|> (_1eb1e83 x0 x1 x2) <|> (_21c3768 x0 x1 x2) <|> (_21c3768 x0 x1 x2) <|> (_220c8a2 x0 x1 x2) <|> (_31a7ce9 x0 x1 x2) <|> (_3762d3f x0 x1 x2) <|> (_41490e6 x0 x1 x2) <|> (_42db81d x0 x1 x2) <|> (_42db81d x0 x1 x2) <|> (_57afa07 x0 x1 x2) <|> (_57f520f x0 x1 x2) <|> (_641b30a x0 x1 x2) <|> (_6b454b2 x0 x1 x2) <|> (_6b7e0d4 x0 x1 x2) <|> (_7031c92 x0 x1 x2) <|> (_758418c x0 x1 x2) <|> (_7a57b51 x0 x1 x2) <|> (_87bf7c6 x0 x1 x2) <|> (_882c519 x0 x1 x2) <|> (_8a4564e x0 x1 x2) <|> (_9a8a33a x0 x1 x2) <|> (_9b4e435 x0 x1 x2) <|> (_9d30e79 x0 x1 x2) <|> (_9e5ad0c x0 x1 x2) <|> (_9ec2057 x0 x1 x2) <|> (_9f9c54d x0 x1 x2) <|> (_b076352 x0 x1 x2) <|> (_b37e75d x0 x1 x2) <|> (_b558675 x0 x1 x2) <|> (_b69f73f x0 x1 x2) <|> (_beb7b49 x0 x1 x2) <|> (_beb7b49 x0 x1 x2) <|> (_c0092c8 x0 x1 x2) <|> (_c91e9fa x0 x1 x2) <|> (_c986c4d x0 x1 x2) <|> (_f10cf1b x0 x1 x2) <|> (_f53e67b x0 x1 x2) <|> (_f5cd646 x0 x1 x2) <|> (_f5cd646 x0 x1 x2) <|> (_f64794f x0 x1 x2)

noncomputable def _c781373 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "upper", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «mapUpper(_)_MPY-METHODS_IntSeq_IntSeq» CS
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def _4f910e7 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "swapcase", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «mapSwap(_)_MPY-METHODS_IntSeq_IntSeq» CS
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def _9243a19 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "lower", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «mapLower(_)_MPY-METHODS_IntSeq_IntSeq» CS
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0))
  | _, _, _ => none

noncomputable def _536f6b6 : SortVal → SortString → SortVals → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS), "isalpha", SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «_==K_» (SortK.kseq ((@inj SortIntSeq SortKItem) CS) SortK.dotk) (SortK.kseq ((@inj SortIntSeq SortKItem) SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») SortK.dotk)
    let _Val1 <- notBool_ _Val0
    let _Val2 <- «allAlpha(_)_MPY-METHODS_Bool_IntSeq» CS
    let _Val3 <- _andBool_ _Val1 _Val2
    return ((@inj SortBool SortVal) _Val3)
  | _, _, _ => none

noncomputable def _4ae8014 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _e2e4c93 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _727142b : SortString → SortVals → Option SortVal
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortFloat F) (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt N) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») => do
    let _Val0 <- roundFN F N
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

mutual
  noncomputable def _7032cf2 : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
    | L, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS, OO, ON => do
      let _Val0 <- «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» L O
      let _Val1 <- «applyOpE(_,_,_)_MPY-BUILTINS_Int_String_Int_Int» O CUR N
      let _Val2 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» L _Val1 OPS NDS OO ON
      guard _Val0
      return _Val2
    | _, _, _, _, _, _ => none

  noncomputable def «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» (x0 : SortString) (x1 : SortInt) (x2 : SortOpSeq) (x3 : SortIntSeq) (x4 : SortOpSeq) (x5 : SortIntSeq) : Option SortEvPair := (_7032cf2 x0 x1 x2 x3 x4 x5) <|> (_a6e6ac4 x0 x1 x2 x3 x4 x5) <|> (_a7ad23b x0 x1 x2 x3 x4 x5) <|> (_ce2bdd1 x0 x1 x2 x3 x4 x5)

  noncomputable def _a7ad23b : SortString → SortInt → SortOpSeq → SortIntSeq → SortOpSeq → SortIntSeq → Option SortEvPair
    | L, CUR, SortOpSeq.«oCons(_,_)_MPY-BUILTINS_OpSeq_String_OpSeq» O OPS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N NDS, OO, ON => do
      let _Val0 <- «inLevelE(_,_)_MPY-BUILTINS_Bool_String_String» L O
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «appendOpE(_,_)_MPY-BUILTINS_OpSeq_OpSeq_String» OO O
      let _Val3 <- «appendIE(_,_)_MPY-BUILTINS_IntSeq_IntSeq_Int» ON CUR
      let _Val4 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» L N OPS NDS _Val2 _Val3
      guard _Val1
      return _Val4
    | _, _, _, _, _, _ => none
end

mutual
  noncomputable def decStrToF (x0 : SortIntSeq) : Option SortFloat := (_ed58d1a x0) <|> (_f17777e x0)

  noncomputable def _ed58d1a : SortIntSeq → Option SortFloat
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 CS => do
      let _Val0 <- decStrToF CS
      let _Val1 <- «_-Float__FLOAT_Float_Float_Float» (0.0 : Float) _Val0
      return _Val1
    | _ => none
end

noncomputable def «applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» (x0 : SortVal) (x1 : SortString) (x2 : SortVals) : Option SortVal := (_0ce199a x0 x1 x2) <|> (_37ed508 x0 x1 x2) <|> (_445e463 x0 x1 x2) <|> (_4f910e7 x0 x1 x2) <|> (_536f6b6 x0 x1 x2) <|> (_5667eab x0 x1 x2) <|> (_5d102b6 x0 x1 x2) <|> (_711e2c3 x0 x1 x2) <|> (_755caa7 x0 x1 x2) <|> (_8060dd0 x0 x1 x2) <|> (_88460b3 x0 x1 x2) <|> (_9243a19 x0 x1 x2) <|> (_c781373 x0 x1 x2) <|> (_dc2e992 x0 x1 x2) <|> (_dde015f x0 x1 x2) <|> (_f0d69ff x0 x1 x2)

noncomputable def «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_396b61d x0 x1 x2) <|> (_3cb3e9b x0 x1 x2) <|> (_4ae8014 x0 x1 x2)

noncomputable def «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_6ddca9b x0 x1 x2) <|> (_72787fe x0 x1 x2) <|> (_e2e4c93 x0 x1 x2)

noncomputable def _16b47fd : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N0 NDS) => do
    let _Val0 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» "add" N0 OPS NDS SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0
  | _ => none

noncomputable def _c6b686a : SortEvPair → Option SortEvPair
  | SortEvPair.«evp(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» OPS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» N0 NDS) => do
    let _Val0 <- «passLGoE(_,_,_,_,_,_)_MPY-BUILTINS_EvPair_String_Int_OpSeq_IntSeq_OpSeq_IntSeq» "mul" N0 OPS NDS SortOpSeq.«.OpSeq_MPY-BUILTINS_OpSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0
  | _ => none

noncomputable def _8f573a0 : SortString → SortVals → Option SortVal
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- decStrToF CS
    return ((@inj SortFloat SortVal) _Val0)
  | _, _ => none

noncomputable def _13a7bb3 : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» IS), LO, HI, ST => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
    let _Val2 <- «isLen(_)_MPY-CORE_Int_IntSeq» IS
    let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
    let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val5 <- «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» IS _Val1 _Val3 _Val4
    return ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5))
  | _, _, _, _ => none

noncomputable def _84f67ef : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | _Pat0, LO, HI, ST => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
      let _Val2 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
      let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
      let _Val5 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS _Val1 _Val3 _Val4
      return ((@inj SortIterable SortVal) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» _Val5))
    | _ => none

noncomputable def _8f16e60 : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | _Pat0, LO, HI, ST => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val1 <- «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» LO ST _Val0
      let _Val2 <- «vsLen(_)_MPY-CORE_Int_ValSeq» VS
      let _Val3 <- «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» HI ST _Val2
      let _Val4 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
      let _Val5 <- «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» VS _Val1 _Val3 _Val4
      return ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» _Val5))
    | _ => none

noncomputable def «passAddE(_)_MPY-BUILTINS_EvPair_EvPair» (x0 : SortEvPair) : Option SortEvPair := (_16b47fd x0) <|> (_75246f8 x0)

noncomputable def «passMulE(_)_MPY-BUILTINS_EvPair_EvPair» (x0 : SortEvPair) : Option SortEvPair := (_c6b686a x0) <|> (_eda2bc1 x0)

noncomputable def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortOptInt) (x3 : SortOptInt) : Option SortVal := (_13a7bb3 x0 x1 x2 x3) <|> (_84f67ef x0 x1 x2 x3) <|> (_8f16e60 x0 x1 x2 x3)

noncomputable def _3f2311f : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «tokOps(_)_MPY-BUILTINS_OpSeq_IntSeq» CS
    let _Val1 <- «tokNds(_)_MPY-BUILTINS_IntSeq_IntSeq» CS
    let _Val2 <- «passPowE(_,_)_MPY-BUILTINS_EvPair_OpSeq_IntSeq» _Val0 _Val1
    let _Val3 <- «passMulE(_)_MPY-BUILTINS_EvPair_EvPair» _Val2
    let _Val4 <- «passAddE(_)_MPY-BUILTINS_EvPair_EvPair» _Val3
    let _Val5 <- «firstNdE(_)_MPY-BUILTINS_Int_EvPair» _Val4
    return _Val5

noncomputable def «evalArith(_)_MPY-BUILTINS_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _3f2311f x0

noncomputable def _1de45ff : SortString → SortVals → Option SortVal
  | "eval", SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» => do
    let _Val0 <- «evalArith(_)_MPY-BUILTINS_Int_IntSeq» CS
    return ((@inj SortInt SortVal) _Val0)
  | _, _ => none

noncomputable def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» (x0 : SortString) (x1 : SortVals) : Option SortVal := (_0d5862f x0 x1) <|> (_108b118 x0 x1) <|> (_1b20c41 x0 x1) <|> (_1de45ff x0 x1) <|> (_20b19cf x0 x1) <|> (_213f0c2 x0 x1) <|> (_28eddda x0 x1) <|> (_2d8e778 x0 x1) <|> (_437b04b x0 x1) <|> (_4807966 x0 x1) <|> (_4b80f98 x0 x1) <|> (_583f938 x0 x1) <|> (_606434e x0 x1) <|> (_6d20a96 x0 x1) <|> (_6d20a96 x0 x1) <|> (_727142b x0 x1) <|> (_72eff8b x0 x1) <|> (_73630e2 x0 x1) <|> (_853fa53 x0 x1) <|> (_8f573a0 x0 x1) <|> (_a4fd04a x0 x1) <|> (_a971c50 x0 x1) <|> (_bb50555 x0 x1) <|> (_d16bd47 x0 x1) <|> (_d7fe6d3 x0 x1) <|> (_dc46a10 x0 x1) <|> (_e22316b x0 x1) <|> (_e4f0a30 x0 x1) <|> (_e64428a x0 x1) <|> (_e64428a x0 x1) <|> (_eb8c1ed x0 x1) <|> (_ecd3e5c x0 x1) <|> (_f1c888d x0 x1)