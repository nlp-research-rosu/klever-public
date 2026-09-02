import Klean125SplitWords.Inj

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _4154192 : SortIntSeq → SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _4183651 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _, _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

noncomputable def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

noncomputable def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

noncomputable def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

noncomputable def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

noncomputable def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

noncomputable def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

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

noncomputable def _16468f1 : SortIntSeq → SortInt → Option SortIntSeq
  | S, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return S

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

mutual
  noncomputable def «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_16468f1 x0 x1) <|> (_aa907da x0 x1) <|> (_4183651 x0 x1)

  noncomputable def _aa907da : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, N => do
      let _Val0 <- «_>Int_» N 0
      let _Val1 <- «_-Int_» N 1
      let _Val2 <- «dropIS(_,_)_MPY-METHODS_IntSeq_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

axiom «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortInt
axiom _b153473 : SortIntSeq → SortIntSeq → Option SortInt
axiom _f1b90b3 : SortIntSeq → SortIntSeq → Option SortInt

noncomputable def _2eba8ff : SortIntSeq → Option SortInt
  | CS => do
    let _Val0 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val1 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 100 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val2 <- «_+Int_» _Val0 _Val1
    let _Val3 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 102 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val4 <- «_+Int_» _Val2 _Val3
    let _Val5 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 104 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val6 <- «_+Int_» _Val4 _Val5
    let _Val7 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 106 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val8 <- «_+Int_» _Val6 _Val7
    let _Val9 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 108 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val10 <- «_+Int_» _Val8 _Val9
    let _Val11 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 110 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val12 <- «_+Int_» _Val10 _Val11
    let _Val13 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 112 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val14 <- «_+Int_» _Val12 _Val13
    let _Val15 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 114 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val16 <- «_+Int_» _Val14 _Val15
    let _Val17 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 116 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val18 <- «_+Int_» _Val16 _Val17
    let _Val19 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 118 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val20 <- «_+Int_» _Val18 _Val19
    let _Val21 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 120 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val22 <- «_+Int_» _Val20 _Val21
    let _Val23 <- «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» CS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 122 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
    let _Val24 <- «_+Int_» _Val22 _Val23
    return _Val24

noncomputable def «oddAlphabetCount(_)_VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _2eba8ff x0