import Klean148Bf.Inj

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _eb829f9 : SortPlanet → Option SortInt
  | SortPlanet.«pJupiter_BF-VERIFICATION_Planet» => some 4
  | _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

noncomputable def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

noncomputable def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def _daab430 : SortOptInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» => some 1
  | _ => none

noncomputable def _28a37d3 : SortOptInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» S => some S
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

noncomputable def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

noncomputable def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

noncomputable def _63c36fb : SortPlanet → Option SortInt
  | SortPlanet.«pMars_BF-VERIFICATION_Planet» => some 3
  | _ => none

noncomputable def _0054b8c : SortPlanet → Option SortInt
  | SortPlanet.«pUranus_BF-VERIFICATION_Planet» => some 6
  | _ => none

noncomputable def _94f0ee1 : SortPlanet → Option SortInt
  | SortPlanet.«pVenus_BF-VERIFICATION_Planet» => some 1
  | _ => none

noncomputable def _f1d4331 : SortPlanet → Option SortInt
  | SortPlanet.«pMercury_BF-VERIFICATION_Planet» => some 0
  | _ => none

noncomputable def _0a04d34 : SortPlanet → Option SortInt
  | SortPlanet.«pSaturn_BF-VERIFICATION_Planet» => some 5
  | _ => none

noncomputable def _c864316 : SortPlanet → Option SortInt
  | SortPlanet.«pNeptune_BF-VERIFICATION_Planet» => some 7
  | _ => none

noncomputable def _bfe9715 : SortPlanet → Option SortInt
  | SortPlanet.«pEarth_BF-VERIFICATION_Planet» => some 2
  | _ => none

noncomputable def _ae27e7d : SortInt → Option SortExpr
  | 7 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Neptune")
  | _ => none

noncomputable def _17be908 : SortInt → Option SortExpr
  | 3 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Mars")
  | _ => none

noncomputable def _6bd8ec5 : SortInt → Option SortExpr
  | 4 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Jupiter")
  | _ => none

noncomputable def _0b6b1df : SortInt → Option SortExpr
  | 1 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Venus")
  | _ => none

noncomputable def _22a0801 : SortInt → Option SortExpr
  | 0 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Mercury")
  | _ => none

noncomputable def _bc51481 : SortInt → Option SortExpr
  | 6 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Uranus")
  | _ => none

noncomputable def _291661a : SortInt → Option SortExpr
  | 5 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Saturn")
  | _ => none

noncomputable def _b3acb11 : SortInt → Option SortExpr
  | 2 => some (SortExpr.«Str(_)_MPY-SYNTAX_Expr_String» "Earth")
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.Map» : Option SortMap

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _5615d55 : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_<Int_» I1 I2
    guard _Val0
    return I1

noncomputable def _ffe5f5d : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, _STEP => do
    let _Val0 <- «_<Int_» I LEN
    guard _Val0
    return I

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2500272 : SortInt → SortInt → Option SortInt
  | J, _STEP => do
    let _Val0 <- «_>=Int_» J 0
    guard _Val0
    return J

noncomputable def _e1effea : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_>=Int_» I1 I2
    guard _Val0
    return I2

noncomputable def «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» (x0 : SortOptInt) : Option SortInt := (_28a37d3 x0) <|> (_daab430 x0)

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

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

mutual
  noncomputable def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
end

noncomputable def «planetPosition(_)_BF-VERIFICATION_Int_Planet» (x0 : SortPlanet) : Option SortInt := (_0054b8c x0) <|> (_0a04d34 x0) <|> (_63c36fb x0) <|> (_94f0ee1 x0) <|> (_bfe9715 x0) <|> (_c864316 x0) <|> (_eb829f9 x0) <|> (_f1d4331 x0)

noncomputable def «planetExpr(_)_BF-VERIFICATION_Expr_Int» (x0 : SortInt) : Option SortExpr := (_0b6b1df x0) <|> (_17be908 x0) <|> (_22a0801 x0) <|> (_291661a x0) <|> (_6bd8ec5 x0) <|> (_ae27e7d x0) <|> (_b3acb11 x0) <|> (_bc51481 x0)

noncomputable def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «minInt(_,_)_INT-COMMON_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_5615d55 x0 x1) <|> (_e1effea x0 x1)

noncomputable def _396b61d : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return 0
  | _, _, _ => none

noncomputable def _6ddca9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    guard _Val1
    return (-1)
  | _, _, _ => none

noncomputable def _3cb3e9b : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_<Int_» _Val0 0
    let _Val2 <- «_-Int_» LEN 1
    guard _Val1
    return _Val2
  | _, _, _ => none

noncomputable def _72787fe : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return LEN
  | _, _, _ => none

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

noncomputable def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

axiom _5bd0f09 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
axiom «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortIntSeq

noncomputable def _6f49a32 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I LEN
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- «_-Int_» LEN 1
    let _Val3 <- kite _Val1 _Val2 LEN
    guard _Val0
    return _Val3

noncomputable def _3cc6493 : SortInt → SortInt → Option SortInt
  | J, STEP => do
    let _Val0 <- «_<Int_» J 0
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- kite _Val1 (-1) 0
    guard _Val0
    return _Val2

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6f49a32 x0 x1 x2) <|> (_ffe5f5d x0 x1 x2)

noncomputable def «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2500272 x0 x1) <|> (_3cc6493 x0 x1)

noncomputable def _3b0729c : SortPlanet → Option SortIntSeq
  | SortPlanet.«pUranus_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Uranus"
    return _Val0
  | _ => none

noncomputable def _5989b6f : SortPlanet → Option SortIntSeq
  | SortPlanet.«pNeptune_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Neptune"
    return _Val0
  | _ => none

noncomputable def _73d8862 : SortPlanet → Option SortIntSeq
  | SortPlanet.«pJupiter_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Jupiter"
    return _Val0
  | _ => none

noncomputable def _6e914d8 : SortPlanet → Option SortIntSeq
  | SortPlanet.«pEarth_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Earth"
    return _Val0
  | _ => none

noncomputable def _77dadd2 : SortPlanet → Option SortIntSeq
  | SortPlanet.«pSaturn_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Saturn"
    return _Val0
  | _ => none

noncomputable def _a60efe1 : SortPlanet → Option SortIntSeq
  | SortPlanet.«pMercury_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mercury"
    return _Val0
  | _ => none

noncomputable def _e2a669a : SortPlanet → Option SortIntSeq
  | SortPlanet.«pMars_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mars"
    return _Val0
  | _ => none

noncomputable def _a084a9e : Option SortValSeq := do
  let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mercury"
  let _Val1 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Venus"
  let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Earth"
  let _Val3 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Mars"
  let _Val4 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Jupiter"
  let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Saturn"
  let _Val6 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Uranus"
  let _Val7 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Neptune"
  return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val1)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val3)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val4)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val6)) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val7)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))))))))

noncomputable def _fc46ae1 : SortPlanet → Option SortIntSeq
  | SortPlanet.«pVenus_BF-VERIFICATION_Planet» => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Venus"
    return _Val0
  | _ => none

noncomputable def _4b524a8 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I 0
    let _Val1 <- «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN STEP
    guard _Val0
    return _Val1

noncomputable def _e75deb6 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_<Int_» I 0
    let _Val1 <- «_+Int_» I LEN
    let _Val2 <- «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» _Val1 STEP
    guard _Val0
    return _Val2

noncomputable def «planetVals_BF-VERIFICATION_ValSeq» : Option SortValSeq := _a084a9e

noncomputable def «planetCodes(_)_BF-VERIFICATION_IntSeq_Planet» (x0 : SortPlanet) : Option SortIntSeq := (_3b0729c x0) <|> (_5989b6f x0) <|> (_6e914d8 x0) <|> (_73d8862 x0) <|> (_77dadd2 x0) <|> (_a60efe1 x0) <|> (_e2a669a x0) <|> (_fc46ae1 x0)

noncomputable def «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_4b524a8 x0 x1 x2) <|> (_e75deb6 x0 x1 x2)

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

noncomputable def «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_396b61d x0 x1 x2) <|> (_3cb3e9b x0 x1 x2) <|> (_4ae8014 x0 x1 x2)

noncomputable def «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_6ddca9b x0 x1 x2) <|> (_72787fe x0 x1 x2) <|> (_e2e4c93 x0 x1 x2)

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

noncomputable def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortOptInt) (x3 : SortOptInt) : Option SortVal := (_13a7bb3 x0 x1 x2 x3) <|> (_84f67ef x0 x1 x2 x3) <|> (_8f16e60 x0 x1 x2 x3)

noncomputable def _76c48d2 : SortInt → SortInt → Option SortVal
  | I, J => do
    let _Val0 <- «planetVals_BF-VERIFICATION_ValSeq»
    let _Val1 <- «minInt(_,_)_INT-COMMON_Int_Int_Int» I J
    let _Val2 <- «_+Int_» _Val1 1
    let _Val3 <- «maxInt(_,_)_INT-COMMON_Int_Int_Int» I J
    let _Val4 <- «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» ((@inj SortIterable SortVal) (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» _Val0)) (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» _Val2) (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» _Val3) SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
    return _Val4

noncomputable def «expectedBetween(_,_)_BF-VERIFICATION_Val_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortVal := _76c48d2 x0 x1