import Klean26RemoveDuplicates.Inj

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «.List» : Option SortList

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _ec93494 : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

def _e4ff78f : SortValSeq → SortVal → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0 => some 0
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_==K_» (x0 : SortK) (x1 : SortK) : Option SortBool

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _fbb3e9c : SortVal → Option SortBool
  | _Gen0 => some false

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _34e9261 : SortValSeq → SortValSeq → SortValSeq → Option SortValSeq
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ALL => some ACC
  | _, _, _ => none

axiom «.Map» : Option SortMap

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _09cbcbb : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def «isIntV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_ec93494 x0) <|> (_fbb3e9c x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

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

mutual
  def _0571d9e : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isIntV(_)_MPY-BUILTINS_Bool_Val» V
      let _Val1 <- «allInts(_)_REMOVE-DUPLICATES-VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_REMOVE-DUPLICATES-VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0571d9e x0) <|> (_09cbcbb x0)
end

mutual
  noncomputable def _5e974ea : SortValSeq → SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, ALL => do
      let _Val0 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» ALL V
      let _Val1 <- «_==Int_» 1 _Val0
      let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val3 <- «keepSinglesAcc(_,_,_)_REMOVE-DUPLICATES-VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» _Val2 REST ALL
      guard _Val1
      return _Val3
    | _, _, _ => none

  noncomputable def _617b8ed : SortValSeq → SortValSeq → SortValSeq → Option SortValSeq
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST, ALL => do
      let _Val0 <- «cntOccVS(_,_)_MPY-METHODS_Int_ValSeq_Val» ALL V
      let _Val1 <- «_==Int_» 1 _Val0
      let _Val2 <- notBool_ _Val1
      let _Val3 <- «keepSinglesAcc(_,_,_)_REMOVE-DUPLICATES-VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» ACC REST ALL
      guard _Val2
      return _Val3
    | _, _, _ => none

  noncomputable def «keepSinglesAcc(_,_,_)_REMOVE-DUPLICATES-VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) : Option SortValSeq := (_34e9261 x0 x1 x2) <|> (_5e974ea x0 x1 x2) <|> (_617b8ed x0 x1 x2)
end