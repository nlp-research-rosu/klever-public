import Klean85Add.Inj

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «.List» : Option SortList

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

axiom «.Map» : Option SortMap

def _32b126a : SortISeq → Option SortInt
  | SortISeq.«cons(_,_)_MPY-SYNTAX_ISeq_Int_ISeq» _Gen0 SortISeq.«nil_MPY-SYNTAX_ISeq» => some 0
  | _ => none

def _2f58738 : SortISeq → Option SortInt
  | SortISeq.«nil_MPY-SYNTAX_ISeq» => some 0
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _a192364 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 2
    let _Val1 <- «_==Int_» _Val0 0
    guard _Val1
    return I

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

noncomputable def _4d97758 : SortInt → Option SortInt
  | I => do
    let _Val0 <- «_%Int_» I 2
    let _Val1 <- «_=/=Int_» _Val0 0
    guard _Val1
    return 0

noncomputable def «evenPart(_)_MPY_Int_Int» (x0 : SortInt) : Option SortInt := (_4d97758 x0) <|> (_a192364 x0)

mutual
  noncomputable def _462355f : SortISeq → Option SortInt
    | SortISeq.«cons(_,_)_MPY-SYNTAX_ISeq_Int_ISeq» _Gen0 (SortISeq.«cons(_,_)_MPY-SYNTAX_ISeq_Int_ISeq» ITEM REST) => do
      let _Val0 <- «evenPart(_)_MPY_Int_Int» ITEM
      let _Val1 <- «oddIndexEvenSum(_)_VERIFICATION_Int_ISeq» REST
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  noncomputable def «oddIndexEvenSum(_)_VERIFICATION_Int_ISeq» (x0 : SortISeq) : Option SortInt := (_2f58738 x0) <|> (_32b126a x0) <|> (_462355f x0)
end