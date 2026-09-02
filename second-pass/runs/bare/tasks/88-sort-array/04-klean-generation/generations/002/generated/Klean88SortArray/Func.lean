import Klean88SortArray.Inj

def _01cbf5b : SortInt → SortIntList → Option SortIntList
  | I, SortIntList.«nil_MPY-SYNTAX_IntList» => some (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I SortIntList.«nil_MPY-SYNTAX_IntList»)
  | _, _ => none

def _6c35853 : SortIntList → Option SortBool
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _c50a6ae : SortIntList → SortIntList → Option SortIntList
  | SortIntList.«nil_MPY-SYNTAX_IntList», ACC => some ACC
  | _, _ => none

def _67df8e2 : SortIntList → Option SortIntList
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some SortIntList.«nil_MPY-SYNTAX_IntList»
  | _ => none

def _9010fa7 : SortIntList → Option SortBool
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» _Gen0 SortIntList.«nil_MPY-SYNTAX_IntList» => some true
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _0ef88fe : SortIntList → Option SortInt
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some 0
  | _ => none

def _f277588 : SortIntList → Option SortInt
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I SortIntList.«nil_MPY-SYNTAX_IntList» => some I
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _85382ee : SortIntList → Option SortBool
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some true
  | _ => none

def _86348b3 : SortIntList → Option SortBool
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some true
  | _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

def _48cd49c : SortIntList → Option SortBool
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» _Gen0 SortIntList.«nil_MPY-SYNTAX_IntList» => some true
  | _ => none

def _89730c1 : SortIntList → Option SortIntList
  | SortIntList.«nil_MPY-SYNTAX_IntList» => some SortIntList.«nil_MPY-SYNTAX_IntList»
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _2bcbaa6 : SortInt → SortIntList → Option SortIntList
  | I, SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS => do
    let _Val0 <- «_<=Int_» I J
    guard _Val0
    return (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS))
  | _, _ => none

mutual
  def _5eda9de : SortIntList → SortIntList → Option SortIntList
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS, ACC => do
      let _Val0 <- «reverseAcc(_,_)_MPY_IntList_IntList_IntList» IS (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I ACC)
      return _Val0
    | _, _ => none

  def «reverseAcc(_,_)_MPY_IntList_IntList_IntList» (x0 : SortIntList) (x1 : SortIntList) : Option SortIntList := (_5eda9de x0 x1) <|> (_c50a6ae x0 x1)
end

mutual
  def _691fbc0 : SortIntList → Option SortInt
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» _Gen0 (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS) => do
      let _Val0 <- «ilast(_)_MPY_Int_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS)
      return _Val0
    | _ => none

  def «ilast(_)_MPY_Int_IntList» (x0 : SortIntList) : Option SortInt := (_0ef88fe x0) <|> (_691fbc0 x0) <|> (_f277588 x0)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def «insertAsc(_,_)_MPY_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : Option SortIntList := (_01cbf5b x0 x1) <|> (_2bcbaa6 x0 x1) <|> (_f8c09e4 x0 x1)

  def _f8c09e4 : SortInt → SortIntList → Option SortIntList
    | I, SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS => do
      let _Val0 <- «_>Int_» I J
      let _Val1 <- «insertAsc(_,_)_MPY_IntList_Int_IntList» I JS
      guard _Val0
      return (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J _Val1)
    | _, _ => none
end

def _83c4d59 : SortIntList → Option SortIntList
  | L => do
    let _Val0 <- «reverseAcc(_,_)_MPY_IntList_IntList_IntList» L SortIntList.«nil_MPY-SYNTAX_IntList»
    return _Val0

noncomputable def _225be15 : SortIntList → Option SortBool
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS => do
    let _Val0 <- «ilast(_)_MPY_Int_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS)
    let _Val1 <- «_+Int_» I _Val0
    let _Val2 <- «_%Int_» _Val1 2
    let _Val3 <- «_==Int_» _Val2 0
    return _Val3
  | _ => none

mutual
  def _74fd232 : SortIntList → Option SortBool
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS => do
      let _Val0 <- «_>=Int_» I 0
      let _Val1 <- «nonnegative(_)_MPY-VERIFICATION_Bool_IntList» IS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «nonnegative(_)_MPY-VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := (_74fd232 x0) <|> (_85382ee x0)
end

mutual
  def «ascending(_)_MPY-VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := (_6c35853 x0) <|> (_9010fa7 x0) <|> (_fd939a5 x0)

  def _fd939a5 : SortIntList → Option SortBool
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS) => do
      let _Val0 <- «_<=Int_» I J
      let _Val1 <- «ascending(_)_MPY-VERIFICATION_Bool_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS)
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none
end

mutual
  def _539e2ac : SortIntList → Option SortBool
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS) => do
      let _Val0 <- «_>=Int_» I J
      let _Val1 <- «descending(_)_MPY-VERIFICATION_Bool_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» J JS)
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «descending(_)_MPY-VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := (_48cd49c x0) <|> (_539e2ac x0) <|> (_86348b3 x0)
end

mutual
  def _2e41ed2 : SortIntList → Option SortIntList
    | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS => do
      let _Val0 <- «sortAsc(_)_MPY_IntList_IntList» IS
      let _Val1 <- «insertAsc(_,_)_MPY_IntList_Int_IntList» I _Val0
      return _Val1
    | _ => none

  def «sortAsc(_)_MPY_IntList_IntList» (x0 : SortIntList) : Option SortIntList := (_2e41ed2 x0) <|> (_67df8e2 x0)
end

def «reverse(_)_MPY_IntList_IntList» (x0 : SortIntList) : Option SortIntList := _83c4d59 x0

noncomputable def «endpointEven(_)_MPY-VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := _225be15 x0

def _2cf4e89 : SortIntList → SortBool → Option SortIntList
  | L, false => do
    let _Val0 <- «sortAsc(_)_MPY_IntList_IntList» L
    return _Val0
  | _, _ => none

def _942baea : SortIntList → SortBool → Option SortIntList
  | L, true => do
    let _Val0 <- «sortAsc(_)_MPY_IntList_IntList» L
    let _Val1 <- «reverse(_)_MPY_IntList_IntList» _Val0
    return _Val1
  | _, _ => none

def «sortFlag(_,_)_MPY_IntList_IntList_Bool» (x0 : SortIntList) (x1 : SortBool) : Option SortIntList := (_2cf4e89 x0 x1) <|> (_942baea x0 x1)

noncomputable def _91390ef : SortIntList → Option SortIntList
  | SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS => do
    let _Val0 <- «endpointEven(_)_MPY-VERIFICATION_Bool_IntList» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS)
    let _Val1 <- «sortFlag(_,_)_MPY_IntList_IntList_Bool» (SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS) _Val0
    return _Val1
  | _ => none

noncomputable def «expectedSort(_)_MPY-VERIFICATION_IntList_IntList» (x0 : SortIntList) : Option SortIntList := (_89730c1 x0) <|> (_91390ef x0)