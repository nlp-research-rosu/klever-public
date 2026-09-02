import Klean85Add.Inj

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _c698578 : SortIntSeq → SortBool → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, ACC => some ACC
  | _, _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _915a931 : SortScope → Option SortMap
  | SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» M _Gen0 => some M

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def «scopeMap(_)_VERIFICATION_Map_Scope» (x0 : SortScope) : Option SortMap := _915a931 x0

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  noncomputable def _090f6a8 : SortIntSeq → SortBool → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I REST, true, ACC => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_==Int_» _Val0 0
      let _Val2 <- «_+Int_» ACC I
      let _Val3 <- «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» REST false _Val2
      guard _Val1
      return _Val3
    | _, _, _ => none

  noncomputable def _4447085 : SortIntSeq → SortBool → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I REST, true, ACC => do
      let _Val0 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val1 <- «_=/=Int_» _Val0 0
      let _Val2 <- «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» REST false ACC
      guard _Val1
      return _Val2
    | _, _, _ => none

  noncomputable def «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» (x0 : SortIntSeq) (x1 : SortBool) (x2 : SortInt) : Option SortInt := (_090f6a8 x0 x1 x2) <|> (_4447085 x0 x1 x2) <|> (_add813d x0 x1 x2) <|> (_c698578 x0 x1 x2)

  noncomputable def _add813d : SortIntSeq → SortBool → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 REST, false, ACC => do
      let _Val0 <- «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» REST true ACC
      return _Val0
    | _, _, _ => none
end