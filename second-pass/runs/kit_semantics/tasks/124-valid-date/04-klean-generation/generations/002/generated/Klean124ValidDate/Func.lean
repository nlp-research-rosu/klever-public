import Klean124ValidDate.Inj

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _d9b4697 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C _Gen0, 0 => some C
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

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

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

mutual
  def _24a45bb : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_24a45bb x0 x1) <|> (_d9b4697 x0 x1)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def _9b180ed : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_<=Int_» 48 C
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _3392351 : SortInt → SortInt → Option SortBool
  | M, D => do
    let _Val0 <- «_==Int_» M 2
    let _Val1 <- «_<=Int_» 1 D
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» D 29
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» M 4
    let _Val6 <- «_==Int_» M 6
    let _Val7 <- _orBool_ _Val5 _Val6
    let _Val8 <- «_==Int_» M 9
    let _Val9 <- _orBool_ _Val7 _Val8
    let _Val10 <- «_==Int_» M 11
    let _Val11 <- _orBool_ _Val9 _Val10
    let _Val12 <- «_<=Int_» 1 D
    let _Val13 <- _andBool_ _Val11 _Val12
    let _Val14 <- «_<=Int_» D 30
    let _Val15 <- _andBool_ _Val13 _Val14
    let _Val16 <- _orBool_ _Val4 _Val15
    let _Val17 <- «_==Int_» M 1
    let _Val18 <- «_==Int_» M 3
    let _Val19 <- _orBool_ _Val17 _Val18
    let _Val20 <- «_==Int_» M 5
    let _Val21 <- _orBool_ _Val19 _Val20
    let _Val22 <- «_==Int_» M 7
    let _Val23 <- _orBool_ _Val21 _Val22
    let _Val24 <- «_==Int_» M 8
    let _Val25 <- _orBool_ _Val23 _Val24
    let _Val26 <- «_==Int_» M 10
    let _Val27 <- _orBool_ _Val25 _Val26
    let _Val28 <- «_==Int_» M 12
    let _Val29 <- _orBool_ _Val27 _Val28
    let _Val30 <- «_<=Int_» 1 D
    let _Val31 <- _andBool_ _Val29 _Val30
    let _Val32 <- «_<=Int_» D 31
    let _Val33 <- _andBool_ _Val31 _Val32
    let _Val34 <- _orBool_ _Val16 _Val33
    return _Val34

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def «asciiDigit(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _9b180ed x0

def «validMonthDay(_,_)_VERIFICATION_Bool_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _3392351 x0 x1

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def _b9baa4e : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_==Int_» _Val0 10
    let _Val2 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 2
    let _Val3 <- «_==Int_» _Val2 45
    let _Val4 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 5
    let _Val5 <- «_==Int_» _Val4 45
    let _Val6 <- _andBool_ _Val3 _Val5
    let _Val7 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 0
    let _Val8 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val7
    let _Val9 <- _andBool_ _Val6 _Val8
    let _Val10 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 1
    let _Val11 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val10
    let _Val12 <- _andBool_ _Val9 _Val11
    let _Val13 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 3
    let _Val14 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val13
    let _Val15 <- _andBool_ _Val12 _Val14
    let _Val16 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 4
    let _Val17 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val16
    let _Val18 <- _andBool_ _Val15 _Val17
    let _Val19 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 6
    let _Val20 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val19
    let _Val21 <- _andBool_ _Val18 _Val20
    let _Val22 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 7
    let _Val23 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val22
    let _Val24 <- _andBool_ _Val21 _Val23
    let _Val25 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 8
    let _Val26 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val25
    let _Val27 <- _andBool_ _Val24 _Val26
    let _Val28 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 9
    let _Val29 <- «asciiDigit(_)_VERIFICATION_Bool_Int» _Val28
    let _Val30 <- _andBool_ _Val27 _Val29
    let _Val31 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 0
    let _Val32 <- «_-Int_» _Val31 48
    let _Val33 <- «_*Int_» _Val32 10
    let _Val34 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 1
    let _Val35 <- «_-Int_» _Val34 48
    let _Val36 <- «_+Int_» _Val33 _Val35
    let _Val37 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 3
    let _Val38 <- «_-Int_» _Val37 48
    let _Val39 <- «_*Int_» _Val38 10
    let _Val40 <- «intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int» CS 4
    let _Val41 <- «_-Int_» _Val40 48
    let _Val42 <- «_+Int_» _Val39 _Val41
    let _Val43 <- «validMonthDay(_,_)_VERIFICATION_Bool_Int_Int» _Val36 _Val42
    let _Val44 <- _andBool_ _Val30 _Val43
    guard _Val1
    return _Val44

def _35f9126 : SortIntSeq → Option SortBool
  | CS => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
    let _Val1 <- «_=/=Int_» _Val0 10
    guard _Val1
    return false

def «validDateResult(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_35f9126 x0) <|> (_b9baa4e x0)