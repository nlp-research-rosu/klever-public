import Klean56CorrectBracketing.Inj

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

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

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

  def «bracketResult(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_075dd19 x0 x1) <|> (_3376361 x0 x1)
end