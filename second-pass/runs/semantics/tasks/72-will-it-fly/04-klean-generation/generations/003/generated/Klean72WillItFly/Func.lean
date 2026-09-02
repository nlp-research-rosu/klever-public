import Klean72WillItFly.Inj

def _0aef589 : SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

def _105572a : SortK → Option SortBool
  | K => some false

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _4d85165 : SortValSeq → SortVal → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», V => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _9addc79 : SortValSeq → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some 0
  | _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

mutual
  def _79c6d16 : SortValSeq → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H T, V => do
      let _Val0 <- «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» T V
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H _Val0)
    | _, _ => none

  def «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := (_4d85165 x0 x1) <|> (_79c6d16 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _6f33f98 : SortValSeq → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt I) REST => do
      let _Val0 <- «sumIntVS(_)_VERIFICATION_Int_ValSeq» REST
      let _Val1 <- «_+Int_» I _Val0
      return _Val1
    | _ => none

  def «sumIntVS(_)_VERIFICATION_Int_ValSeq» (x0 : SortValSeq) : Option SortInt := (_6f33f98 x0) <|> (_9addc79 x0)
end

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

mutual
  def «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := (_0aef589 x0) <|> (_a3c814a x0)

  def _a3c814a : SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» H T => do
      let _Val0 <- «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» T
      let _Val1 <- «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» _Val0 H
      return _Val1
    | _ => none
end

def _9030ea8 : SortValSeq → Option SortBool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0 => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _ => none

mutual
  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_9030ea8 x0) <|> (_d0a8392 x0) <|> (_ed5809e x0)

  def _ed5809e : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) REST => do
      let _Val0 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REST
      return _Val0
    | _ => none
end