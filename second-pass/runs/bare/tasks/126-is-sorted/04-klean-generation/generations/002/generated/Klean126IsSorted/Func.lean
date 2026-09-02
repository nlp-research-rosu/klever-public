import Klean126IsSorted.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _47ec730 : SortIntList → SortIntList → SortInt → Option SortBool
  | _Gen0, SortIntList.nil, _Gen1 => some true
  | _, _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _eb6e520 : SortInt → SortIntList → Option SortInt
  | _Gen0, SortIntList.nil => some 0
  | _, _ => none

def _8a1fef2 : SortIntList → SortIntList → Option SortBool
  | SortIntList.cons _Gen0 _Gen1, SortIntList.nil => some false
  | _, _ => none

def _64a23ac : SortInt → SortIntList → Option SortIntList
  | I, SortIntList.nil => some (SortIntList.cons I SortIntList.nil)
  | _, _ => none

def _4bf9274 : SortIntList → Option SortIntList
  | SortIntList.nil => some SortIntList.nil
  | _ => none

def _433d6f0 : SortIntList → SortIntList → Option SortBool
  | SortIntList.nil, SortIntList.nil => some true
  | _, _ => none

def _060b0e3 : SortIntList → SortIntList → Option SortBool
  | SortIntList.nil, SortIntList.cons _Gen0 _Gen1 => some false
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _888314d : SortInt → SortIntList → Option SortIntList
  | I, SortIntList.cons J JS => do
    let _Val0 <- «_<=Int_» I J
    guard _Val0
    return (SortIntList.cons I (SortIntList.cons J JS))
  | _, _ => none

mutual
  def «eqIntLists(_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList» (x0 : SortIntList) (x1 : SortIntList) : Option SortBool := (_060b0e3 x0 x1) <|> (_433d6f0 x0 x1) <|> (_8a1fef2 x0 x1) <|> (_e4fbf1f x0 x1)

  def _e4fbf1f : SortIntList → SortIntList → Option SortBool
    | SortIntList.cons I IS, SortIntList.cons J JS => do
      let _Val0 <- «_==Int_» I J
      let _Val1 <- «eqIntLists(_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList» IS JS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  def _0cc5cc7 : SortInt → SortIntList → Option SortIntList
    | I, SortIntList.cons J JS => do
      let _Val0 <- «_>Int_» I J
      let _Val1 <- «insertInt(_,_)_PY-LIST-DOMAIN_IntList_Int_IntList» I JS
      guard _Val0
      return (SortIntList.cons J _Val1)
    | _, _ => none

  def «insertInt(_,_)_PY-LIST-DOMAIN_IntList_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : Option SortIntList := (_0cc5cc7 x0 x1) <|> (_64a23ac x0 x1) <|> (_888314d x0 x1)
end

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  def «sortInts(_)_PY-LIST-DOMAIN_IntList_IntList» (x0 : SortIntList) : Option SortIntList := (_4bf9274 x0) <|> (_efa3454 x0)

  def _efa3454 : SortIntList → Option SortIntList
    | SortIntList.cons I IS => do
      let _Val0 <- «sortInts(_)_PY-LIST-DOMAIN_IntList_IntList» IS
      let _Val1 <- «insertInt(_,_)_PY-LIST-DOMAIN_IntList_Int_IntList» I _Val0
      return _Val1
    | _ => none
end

mutual
  def _0b87e9d : SortInt → SortIntList → Option SortInt
    | I, SortIntList.cons J JS => do
      let _Val0 <- «_=/=Int_» I J
      let _Val1 <- «countInt(_,_)_PY-LIST-DOMAIN_Int_Int_IntList» I JS
      guard _Val0
      return _Val1
    | _, _ => none

  def _48df53b : SortInt → SortIntList → Option SortInt
    | I, SortIntList.cons J JS => do
      let _Val0 <- «_==Int_» I J
      let _Val1 <- «countInt(_,_)_PY-LIST-DOMAIN_Int_Int_IntList» I JS
      let _Val2 <- «_+Int_» 1 _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «countInt(_,_)_PY-LIST-DOMAIN_Int_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : Option SortInt := (_0b87e9d x0 x1) <|> (_48df53b x0 x1) <|> (_eb6e520 x0 x1)
end

def _43c1406 : SortIntList → Option SortBool
  | IS => do
    let _Val0 <- «sortInts(_)_PY-LIST-DOMAIN_IntList_IntList» IS
    let _Val1 <- «eqIntLists(_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList» IS _Val0
    return _Val1

mutual
  def _146c568 : SortIntList → SortIntList → SortInt → Option SortBool
    | SOURCE, SortIntList.cons I IS, LIMIT => do
      let _Val0 <- «countInt(_,_)_PY-LIST-DOMAIN_Int_Int_IntList» I SOURCE
      let _Val1 <- «_<=Int_» _Val0 LIMIT
      let _Val2 <- «countsAtMost(_,_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList_Int» SOURCE IS LIMIT
      let _Val3 <- _andBool_ _Val1 _Val2
      return _Val3
    | _, _, _ => none

  def «countsAtMost(_,_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList_Int» (x0 : SortIntList) (x1 : SortIntList) (x2 : SortInt) : Option SortBool := (_146c568 x0 x1 x2) <|> (_47ec730 x0 x1 x2)
end

def «ascending(_)_VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := _43c1406 x0

def _b918b56 : SortIntList → SortIntList → Option SortBool
  | SOURCE, ITEMS => do
    let _Val0 <- «countsAtMost(_,_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList_Int» SOURCE ITEMS 2
    return _Val0

def «countsAtMostTwo(_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList» (x0 : SortIntList) (x1 : SortIntList) : Option SortBool := _b918b56 x0 x1

def _b97ea3f : SortIntList → Option SortBool
  | IS => do
    let _Val0 <- «countsAtMostTwo(_,_)_PY-LIST-DOMAIN_Bool_IntList_IntList» IS IS
    return _Val0

def «duplicateBound(_)_VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := _b97ea3f x0

def _9c90f8b : SortIntList → Option SortBool
  | IS => do
    let _Val0 <- «ascending(_)_VERIFICATION_Bool_IntList» IS
    let _Val1 <- «duplicateBound(_)_VERIFICATION_Bool_IntList» IS
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def «isSortedContract(_)_VERIFICATION_Bool_IntList» (x0 : SortIntList) : Option SortBool := _9c90f8b x0