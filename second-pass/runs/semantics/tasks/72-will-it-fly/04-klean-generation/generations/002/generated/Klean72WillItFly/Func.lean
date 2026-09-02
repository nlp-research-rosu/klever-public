import Klean72WillItFly.Inj

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _0aef589 : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

noncomputable def _daab430 : SortOptInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» => some 1
  | _ => none

noncomputable def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _28a37d3 : SortOptInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» S => some S
  | _ => none

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _b662ad7 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

noncomputable def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

noncomputable def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

noncomputable def _105572a : SortK → Option SortBool
  | K => some false

axiom «.List» : Option SortList

noncomputable def _9addc79 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

noncomputable def _4d85165 : SortValSeq → SortVal → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», V => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

noncomputable def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

axiom «.Map» : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

noncomputable def «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» (x0 : SortOptInt) : Option SortInt := (_28a37d3 x0) <|> (_daab430 x0)

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

noncomputable def _2500272 : SortInt → SortInt → Option SortInt
  | J, _STEP => do
    let _Val0 <- «_>=Int_» J 0
    guard _Val0
    return J

noncomputable def _ffe5f5d : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, _STEP => do
    let _Val0 <- «_<Int_» I LEN
    guard _Val0
    return I

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  noncomputable def _5d69a53 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S => do
      let _Val0 <- «vsLen(_)_MPY-CORE_Int_ValSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «vsLen(_)_MPY-CORE_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_5d69a53 x0) <|> (_b662ad7 x0)
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

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

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

noncomputable def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

mutual
  noncomputable def _6f33f98 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) REST => do
      let _Val0 <- «sumIntVS(_)_VERIFICATION_Int_ValSeq» REST
      let _Val1 <- «_+Int_» I _Val0
      return _Val1
    | _ => none

  noncomputable def «sumIntVS(_)_VERIFICATION_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_6f33f98 x0) <|> (_9addc79 x0)
end

mutual
  noncomputable def _79c6d16 : SortValSeq → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H T, V => do
      let _Val0 <- «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» T V
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H _Val0)
    | _, _ => none

  noncomputable def «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_4d85165 x0 x1) <|> (_79c6d16 x0 x1)
end

noncomputable def _396b61d : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, _LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return 0
  | _, _, _ => none

noncomputable def _72787fe : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «_>Int_» _Val0 0
    guard _Val1
    return LEN
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

noncomputable def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

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

noncomputable def _9030ea8 : SortValSeq → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0 => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _ => none

mutual
  noncomputable def «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_0aef589 x0) <|> (_a3c814a x0)

  noncomputable def _a3c814a : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H T => do
      let _Val0 <- «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» T
      let _Val1 <- «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» _Val0 H
      return _Val1
    | _ => none
end

noncomputable def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

axiom «buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq
axiom _fefa459 : SortValSeq → SortInt → SortInt → SortInt → Option SortValSeq

axiom _5bd0f09 : SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
axiom «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortIntSeq

mutual
  noncomputable def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_9030ea8 x0) <|> (_d0a8392 x0) <|> (_ed5809e x0)

  noncomputable def _ed5809e : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) REST => do
      let _Val0 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REST
      return _Val0
    | _ => none
end

noncomputable def _6524538 : SortVal → SortOptInt → SortOptInt → SortOptInt → Option SortVal
  | _Pat0, SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», SortOptInt.«noB_MPY-SUBSCRIPT_OptInt», SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1) => match (@retr SortIterable SortVal) _Pat0 with
    | some (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) => do
      let _Val0 <- «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» VS
      return ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» _Val0))
    | _ => none
  | _, _, _, _ => none

noncomputable def _3cc6493 : SortInt → SortInt → Option SortInt
  | J, STEP => do
    let _Val0 <- «_<Int_» J 0
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- kite _Val1 (-1) 0
    guard _Val0
    return _Val2

noncomputable def _6f49a32 : SortInt → SortInt → SortInt → Option SortInt
  | I, LEN, STEP => do
    let _Val0 <- «_>=Int_» I LEN
    let _Val1 <- «_<Int_» STEP 0
    let _Val2 <- «_-Int_» LEN 1
    let _Val3 <- kite _Val1 _Val2 LEN
    guard _Val0
    return _Val3

noncomputable def «clampLo(_,_)_MPY-SUBSCRIPT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_2500272 x0 x1) <|> (_3cc6493 x0 x1)

noncomputable def «clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_6f49a32 x0 x1 x2) <|> (_ffe5f5d x0 x1 x2)

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

noncomputable def «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_4b524a8 x0 x1 x2) <|> (_e75deb6 x0 x1 x2)

noncomputable def _e2e4c93 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def _4ae8014 : SortOptInt → SortOptInt → SortInt → Option SortInt
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» I, ST, LEN => do
    let _Val0 <- «slStep(_)_MPY-SUBSCRIPT_Int_OptInt» ST
    let _Val1 <- «slAdjust(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» I LEN _Val0
    return _Val1
  | _, _, _ => none

noncomputable def «slStop(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_6ddca9b x0 x1 x2) <|> (_72787fe x0 x1 x2) <|> (_e2e4c93 x0 x1 x2)

noncomputable def «slStart(_,_,_)_MPY-SUBSCRIPT_Int_OptInt_OptInt_Int» (x0 : SortOptInt) (x1 : SortOptInt) (x2 : SortInt) : Option SortInt := (_396b61d x0 x1 x2) <|> (_3cb3e9b x0 x1 x2) <|> (_4ae8014 x0 x1 x2)

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

noncomputable def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (x0 : SortVal) (x1 : SortOptInt) (x2 : SortOptInt) (x3 : SortOptInt) : Option SortVal := (_6524538 x0 x1 x2 x3) <|> (_13a7bb3 x0 x1 x2 x3) <|> (_84f67ef x0 x1 x2 x3) <|> (_8f16e60 x0 x1 x2 x3)