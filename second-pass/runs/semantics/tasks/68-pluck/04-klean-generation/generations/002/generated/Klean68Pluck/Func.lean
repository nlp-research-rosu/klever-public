import Klean68Pluck.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _105572a : SortK → Option SortBool
  | K => some false

def _12aa098 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _4c14fba : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

def _5b6ccba : SortValSeq → SortInt → SortInt → SortInt → SortInt → Option SortPluckState
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», B, BI, I, LAST => some (SortPluckState.«pstate(_,_,_,_)_PLUCK-VERIFICATION_PluckState_Int_Int_Int_Int» B BI I LAST)
  | _, _, _, _, _ => none

def _6493828 : SortPluckState → Option SortInt
  | SortPluckState.«pstate(_,_,_,_)_PLUCK-VERIFICATION_PluckState_Int_Int_Int_Int» B _Gen0 _Gen1 _Gen2 => some B

def _357387a : SortPluckState → Option SortInt
  | SortPluckState.«pstate(_,_,_,_)_PLUCK-VERIFICATION_PluckState_Int_Int_Int_Int» _Gen0 BI _Gen1 _Gen2 => some BI

def _4aa26e4 : SortPluckState → Option SortInt
  | SortPluckState.«pstate(_,_,_,_)_PLUCK-VERIFICATION_PluckState_Int_Int_Int_Int» _Gen0 _Gen1 I _Gen2 => some I

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _f2b5c69 : SortPluckState → Option SortInt
  | SortPluckState.«pstate(_,_,_,_)_PLUCK-VERIFICATION_PluckState_Int_Int_Int_Int» _Gen0 _Gen1 _Gen2 LAST => some LAST

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def «asInt(_)_PLUCK-VERIFICATION_Int_Val» (x0 : SortVal) : Option SortInt := _4c14fba x0

def «stateBest(_)_PLUCK-VERIFICATION_Int_PluckState» (x0 : SortPluckState) : Option SortInt := _6493828 x0

def «stateBestIndex(_)_PLUCK-VERIFICATION_Int_PluckState» (x0 : SortPluckState) : Option SortInt := _357387a x0

def «stateIndex(_)_PLUCK-VERIFICATION_Int_PluckState» (x0 : SortPluckState) : Option SortInt := _4aa26e4 x0

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def «stateLast(_)_PLUCK-VERIFICATION_Int_PluckState» (x0 : SortPluckState) : Option SortInt := _f2b5c69 x0

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  def _8075acd : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «asInt(_)_PLUCK-VERIFICATION_Int_Val» V
      let _Val2 <- «_>=Int_» _Val1 0
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «allNonNegative(_)_PLUCK-VERIFICATION_Bool_ValSeq» REST
      let _Val5 <- _andBool_ _Val3 _Val4
      return _Val5
    | _ => none

  def «allNonNegative(_)_PLUCK-VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_12aa098 x0) <|> (_8075acd x0)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _4d6a12c : SortInt → SortInt → Option SortInt
  | V, B => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_==Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    guard _Val3
    return V

noncomputable def _c4a6c75 : SortInt → SortInt → Option SortBool
  | V, B => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_==Int_» B (-1)
    let _Val3 <- «_<Int_» V B
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- _andBool_ _Val1 _Val4
    return _Val5

noncomputable def _f5ba7cc : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | V, B, _Gen0, I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_==Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    guard _Val3
    return I

noncomputable def _04cf029 : SortInt → SortInt → Option SortInt
  | V, B => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_=/=Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «_<Int_» V B
    let _Val5 <- _andBool_ _Val3 _Val4
    guard _Val5
    return V

noncomputable def _61611bd : SortInt → SortInt → Option SortInt
  | V, B => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_=/=Int_» _Val0 0
    guard _Val1
    return B

noncomputable def _6fd05f6 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | V, B, BI, _Gen0 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_=/=Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «_>=Int_» V B
    let _Val5 <- _andBool_ _Val3 _Val4
    guard _Val5
    return BI

noncomputable def _8361a89 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | V, B, _Gen0, I => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_=/=Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «_<Int_» V B
    let _Val5 <- _andBool_ _Val3 _Val4
    guard _Val5
    return I

noncomputable def _aef4fb8 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | V, _B, BI, _Gen0 => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_=/=Int_» _Val0 0
    guard _Val1
    return BI

noncomputable def _cc5f1d3 : SortInt → SortInt → Option SortInt
  | V, B => do
    let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» V 2
    let _Val1 <- «_==Int_» _Val0 0
    let _Val2 <- «_=/=Int_» B (-1)
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «_>=Int_» V B
    let _Val5 <- _andBool_ _Val3 _Val4
    guard _Val5
    return B

noncomputable def «pluckTake(_,_)_PLUCK-VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _c4a6c75 x0 x1

noncomputable def «nextBestIndex(_,_,_,_)_PLUCK-VERIFICATION_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := (_6fd05f6 x0 x1 x2 x3) <|> (_8361a89 x0 x1 x2 x3) <|> (_aef4fb8 x0 x1 x2 x3) <|> (_f5ba7cc x0 x1 x2 x3)

noncomputable def «nextBest(_,_)_PLUCK-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_04cf029 x0 x1) <|> (_4d6a12c x0 x1) <|> (_61611bd x0 x1) <|> (_cc5f1d3 x0 x1)

mutual
  noncomputable def «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortPluckState := (_5b6ccba x0 x1 x2 x3 x4) <|> (_ed37057 x0 x1 x2 x3 x4)

  noncomputable def _ed37057 : SortValSeq → SortInt → SortInt → SortInt → SortInt → Option SortPluckState
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, B, BI, I, _Gen0 => do
      let _Val0 <- «asInt(_)_PLUCK-VERIFICATION_Int_Val» V
      let _Val1 <- «nextBest(_,_)_PLUCK-VERIFICATION_Int_Int_Int» _Val0 B
      let _Val2 <- «asInt(_)_PLUCK-VERIFICATION_Int_Val» V
      let _Val3 <- «nextBestIndex(_,_,_,_)_PLUCK-VERIFICATION_Int_Int_Int_Int_Int» _Val2 B BI I
      let _Val4 <- «_+Int_» I 1
      let _Val5 <- «asInt(_)_PLUCK-VERIFICATION_Int_Val» V
      let _Val6 <- «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» REST _Val1 _Val3 _Val4 _Val5
      return _Val6
    | _, _, _, _, _ => none
end

noncomputable def _2419ea1 : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» VS (-1) (-1) 0 0
    let _Val1 <- «stateBest(_)_PLUCK-VERIFICATION_Int_PluckState» _Val0
    let _Val2 <- «_==Int_» _Val1 (-1)
    guard _Val2
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _6115e15 : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» VS (-1) (-1) 0 0
    let _Val1 <- «stateBest(_)_PLUCK-VERIFICATION_Int_PluckState» _Val0
    let _Val2 <- «_=/=Int_» _Val1 (-1)
    let _Val3 <- «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» VS (-1) (-1) 0 0
    let _Val4 <- «stateBest(_)_PLUCK-VERIFICATION_Int_PluckState» _Val3
    let _Val5 <- «scanPluck(_,_,_,_,_)_PLUCK-VERIFICATION_PluckState_ValSeq_Int_Int_Int_Int» VS (-1) (-1) 0 0
    let _Val6 <- «stateBestIndex(_)_PLUCK-VERIFICATION_Int_PluckState» _Val5
    guard _Val2
    return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val4) (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) _Val6) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))

noncomputable def «pluckResult(_)_PLUCK-VERIFICATION_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_2419ea1 x0) <|> (_6115e15 x0)