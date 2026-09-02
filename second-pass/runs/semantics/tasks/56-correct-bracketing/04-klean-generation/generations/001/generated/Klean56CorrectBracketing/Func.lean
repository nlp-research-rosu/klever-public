import Klean56CorrectBracketing.Inj

axiom «.Map» : Option SortMap

def _ead6c5a : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 0 => some true
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.List» : Option SortList

def _e987ecf : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», D => do
    let _Val0 <- «_<Int_» D 0
    guard _Val0
    return false
  | _, _ => none

def _ffce371 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _C _REST, D => do
    let _Val0 <- «_<Int_» D 0
    guard _Val0
    return false
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _5fb3af1 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», D => do
    let _Val0 <- «_>Int_» D 0
    guard _Val0
    return false
  | _, _ => none

def _45941e0 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _REST, 0 => do
    let _Val0 <- «_==Int_» C 60
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

mutual
  def _075dd19 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, D => do
      let _Val0 <- «_==Int_» C 60
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «_>Int_» D 0
      let _Val3 <- _andBool_ _Val1 _Val2
      let _Val4 <- «_-Int_» D 1
      let _Val5 <- «bracketResult(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val4
      guard _Val3
      return _Val5
    | _, _ => none

  def _3376361 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 60 REST, D => do
      let _Val0 <- «_>Int_» D 0
      let _Val1 <- «_+Int_» D 1
      let _Val2 <- «bracketResult(_,_)_VERIFICATION_Bool_IntSeq_Int» REST _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def _497d20d : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 60 REST, 0 => do
      let _Val0 <- «bracketResult(_,_)_VERIFICATION_Bool_IntSeq_Int» REST 1
      return _Val0
    | _, _ => none

  def «bracketResult(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_075dd19 x0 x1) <|> (_3376361 x0 x1) <|> (_45941e0 x0 x1) <|> (_497d20d x0 x1) <|> (_5fb3af1 x0 x1) <|> (_e987ecf x0 x1) <|> (_ead6c5a x0 x1) <|> (_ffce371 x0 x1)
end