import Klean144Simplify.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

def _2be6d50 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 1, _Gen0, _Gen1, _Gen2, _Gen3 => some false
  | _, _, _, _, _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _7a40db2 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 2, _Gen0, _Gen1, _Gen2, _Gen3 => some false
  | _, _, _, _, _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _bbd5f7d : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | _Gen0, _Gen1, _Gen2, _Gen3, _Gen4, _Gen5 => some false

def _cdf66ec : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 0, _Gen0, _Gen1, _Gen2, _Gen3 => some false
  | _, _, _, _, _, _ => none

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidate = key then (key, value) :: rest
      else (candidate, oldValue) :: kleanMapUpdateModel rest key value

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _915fc5d : SortVal → SortVal → SortInt → SortInt → SortInt → SortInt → SortInt → SortVal → Option SortScope
  | X, N, P, A, B, C, D, CH => do
    let _Val0 <- «_|->_» ((@inj SortString SortKItem) "x") ((@inj SortVal SortKItem) X)
    let _Val1 <- «_|->_» ((@inj SortString SortKItem) "n") ((@inj SortVal SortKItem) N)
    let _Val2 <- _Map_ _Val0 _Val1
    let _Val3 <- «_|->_» ((@inj SortString SortKItem) "part") ((@inj SortInt SortKItem) P)
    let _Val4 <- _Map_ _Val2 _Val3
    let _Val5 <- «_|->_» ((@inj SortString SortKItem) "a") ((@inj SortInt SortKItem) A)
    let _Val6 <- _Map_ _Val4 _Val5
    let _Val7 <- «_|->_» ((@inj SortString SortKItem) "b") ((@inj SortInt SortKItem) B)
    let _Val8 <- _Map_ _Val6 _Val7
    let _Val9 <- «_|->_» ((@inj SortString SortKItem) "c") ((@inj SortInt SortKItem) C)
    let _Val10 <- _Map_ _Val8 _Val9
    let _Val11 <- «_|->_» ((@inj SortString SortKItem) "d") ((@inj SortInt SortKItem) D)
    let _Val12 <- _Map_ _Val10 _Val11
    let _Val13 <- «_|->_» ((@inj SortString SortKItem) "ch") ((@inj SortVal SortKItem) CH)
    let _Val14 <- _Map_ _Val12 _Val13
    return (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» _Val14 (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0))

def _7523c27 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 3, A, B, C, D => do
    let _Val0 <- «_>Int_» A 0
    let _Val1 <- «_>Int_» B 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>Int_» C 0
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_>Int_» D 0
    let _Val6 <- _andBool_ _Val4 _Val5
    return _Val6
  | _, _, _, _, _, _ => none

def _951deed : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 48
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def «simplifyScope(_,_,_,_,_,_,_,_)_VERIFICATION-SYNTAX_Scope_Val_Val_Int_Int_Int_Int_Int_Val» (x0 : SortVal) (x1 : SortVal) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) (x5 : SortInt) (x6 : SortInt) (x7 : SortVal) : Option SortScope := _915fc5d x0 x1 x2 x3 x4 x5 x6 x7

def «isDigitC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _951deed x0

noncomputable def _c49a4df : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», 3, A, B, C, D => do
    let _Val0 <- «_>Int_» A 0
    let _Val1 <- «_>Int_» B 0
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_>Int_» C 0
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_>Int_» D 0
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «_*Int_» A C
    let _Val8 <- «_*Int_» B D
    let _Val9 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val7 _Val8
    let _Val10 <- «_==Int_» _Val9 0
    guard _Val6
    return _Val10
  | _, _, _, _, _, _ => none

mutual
  def _6de5f48 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 2, A, B, C, D => do
      let _Val0 <- «_==Int_» CODE 47
      let _Val1 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 3 A B C D
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val4 <- «_*Int_» C 10
      let _Val5 <- «_-Int_» CODE 48
      let _Val6 <- «_+Int_» _Val4 _Val5
      let _Val7 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 2 A B _Val6 D
      let _Val8 <- _andBool_ _Val3 _Val7
      let _Val9 <- _orBool_ _Val2 _Val8
      return _Val9
    | _, _, _, _, _, _ => none

  def _9704ac6 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 0, A, B, C, D => do
      let _Val0 <- «_==Int_» CODE 47
      let _Val1 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 1 A B C D
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val4 <- «_*Int_» A 10
      let _Val5 <- «_-Int_» CODE 48
      let _Val6 <- «_+Int_» _Val4 _Val5
      let _Val7 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 0 _Val6 B C D
      let _Val8 <- _andBool_ _Val3 _Val7
      let _Val9 <- _orBool_ _Val2 _Val8
      return _Val9
    | _, _, _, _, _, _ => none

  def «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) (x5 : SortInt) : Option SortBool := (_2be6d50 x0 x1 x2 x3 x4 x5) <|> (_6de5f48 x0 x1 x2 x3 x4 x5) <|> (_7523c27 x0 x1 x2 x3 x4 x5) <|> (_7a40db2 x0 x1 x2 x3 x4 x5) <|> (_9704ac6 x0 x1 x2 x3 x4 x5) <|> (_a183b7b x0 x1 x2 x3 x4 x5) <|> (_a94488a x0 x1 x2 x3 x4 x5) <|> (_cdf66ec x0 x1 x2 x3 x4 x5) <|> (_bbd5f7d x0 x1 x2 x3 x4 x5)

  def _a183b7b : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 3, A, B, C, D => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val1 <- «_*Int_» D 10
      let _Val2 <- «_-Int_» CODE 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 3 A B C _Val3
      let _Val5 <- _andBool_ _Val0 _Val4
      return _Val5
    | _, _, _, _, _, _ => none

  def _a94488a : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 1, A, B, C, D => do
      let _Val0 <- «_==Int_» CODE 47
      let _Val1 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 2 A B C D
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val4 <- «_*Int_» B 10
      let _Val5 <- «_-Int_» CODE 48
      let _Val6 <- «_+Int_» _Val4 _Val5
      let _Val7 <- «validScan(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 1 A _Val6 C D
      let _Val8 <- _andBool_ _Val3 _Val7
      let _Val9 <- _orBool_ _Val2 _Val8
      return _Val9
    | _, _, _, _, _, _ => none
end

mutual
  noncomputable def _1a73a94 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 1, A, B, C, D => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val1 <- «_*Int_» B 10
      let _Val2 <- «_-Int_» CODE 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 1 A _Val3 C D
      guard _Val0
      return _Val4
    | _, _, _, _, _, _ => none

  noncomputable def _1c3660e : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 3, A, B, C, D => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val1 <- «_*Int_» D 10
      let _Val2 <- «_-Int_» CODE 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 3 A B C _Val3
      guard _Val0
      return _Val4
    | _, _, _, _, _, _ => none

  noncomputable def _2291f99 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 0, A, B, C, D => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val1 <- «_*Int_» A 10
      let _Val2 <- «_-Int_» CODE 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 0 _Val3 B C D
      guard _Val0
      return _Val4
    | _, _, _, _, _, _ => none

  noncomputable def «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) (x5 : SortInt) : Option SortBool := (_1a73a94 x0 x1 x2 x3 x4 x5) <|> (_1c3660e x0 x1 x2 x3 x4 x5) <|> (_2291f99 x0 x1 x2 x3 x4 x5) <|> (_a62ab13 x0 x1 x2 x3 x4 x5) <|> (_c49a4df x0 x1 x2 x3 x4 x5) <|> (_e72c7ec x0 x1 x2 x3 x4 x5)

  noncomputable def _a62ab13 : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» CODE REST, 2, A, B, C, D => do
      let _Val0 <- «isDigitC(_)_MPY-METHODS_Bool_Int» CODE
      let _Val1 <- «_*Int_» C 10
      let _Val2 <- «_-Int_» CODE 48
      let _Val3 <- «_+Int_» _Val1 _Val2
      let _Val4 <- «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST 2 A B _Val3 D
      guard _Val0
      return _Val4
    | _, _, _, _, _, _ => none

  noncomputable def _e72c7ec : SortIntSeq → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 REST, P, A, B, C, D => do
      let _Val0 <- «_<=Int_» 0 P
      let _Val1 <- «_<Int_» P 3
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «_+Int_» P 1
      let _Val4 <- «scanResult(_,_,_,_,_,_)_VERIFICATION-SYNTAX_Bool_IntSeq_Int_Int_Int_Int_Int» REST _Val3 A B C D
      guard _Val2
      return _Val4
    | _, _, _, _, _, _ => none
end