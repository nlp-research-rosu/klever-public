import Klean114Minsubarraysum.Inj

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

def _c647c22 : SortIntList → Option SortInt
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» H SortIntList.«nil_MPY-SYNTAX_IntList» => some H
  | _ => none

def _097aa4c : SortIntList → Option SortInt
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» H SortIntList.«nil_MPY-SYNTAX_IntList» => some H
  | _ => none

axiom «.List» : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _5992adf : SortInt → SortInt → Option SortInt
  | I, J => do
    let _Val0 <- «_>Int_» I J
    guard _Val0
    return J

def _8aeb938 : SortInt → SortInt → Option SortInt
  | I, J => do
    let _Val0 <- «_<=Int_» I J
    guard _Val0
    return I

def «intMin(_,_)_MPY_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_5992adf x0 x1) <|> (_8aeb938 x0 x1)

mutual
  def _339aa65 : SortIntList → Option SortInt
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» H (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J T) => do
      let _Val0 <- «minPrefix(_)_VERIFICATION_Int_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J T)
      let _Val1 <- «_+Int_» H _Val0
      let _Val2 <- «intMin(_,_)_MPY_Int_Int_Int» H _Val1
      return _Val2
    | _ => none

  def «minPrefix(_)_VERIFICATION_Int_IntList» (x0 : SortIntList) : Option SortInt := (_339aa65 x0) <|> (_c647c22 x0)
end

mutual
  def _6df59e6 : SortIntList → Option SortInt
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» H (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J T) => do
      let _Val0 <- «minSubarray(_)_VERIFICATION_Int_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J T)
      let _Val1 <- «minPrefix(_)_VERIFICATION_Int_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» H (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J T))
      let _Val2 <- «intMin(_,_)_MPY_Int_Int_Int» _Val0 _Val1
      return _Val2
    | _ => none

  def «minSubarray(_)_VERIFICATION_Int_IntList» (x0 : SortIntList) : Option SortInt := (_097aa4c x0) <|> (_6df59e6 x0)
end