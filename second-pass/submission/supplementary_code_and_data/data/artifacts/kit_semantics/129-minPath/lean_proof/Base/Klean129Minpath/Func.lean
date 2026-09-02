import Klean129Minpath.Inj

noncomputable def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

noncomputable def _306ef4e : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

noncomputable def _4ab8e18 : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

noncomputable def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

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

noncomputable def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

noncomputable def _bdc895a : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X _Gen0, 0 => some X
  | _, _ => none

noncomputable def _ee6e82d : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some 0
  | _, _ => none

noncomputable def _3e8cc38 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 1 _Gen0, A => some A
  | _, _ => none

noncomputable def _ceb9d05 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some (-1)
  | _, _ => none

noncomputable def _5515d1c : SortInt → SortInt → SortBool → Option SortInt
  | B, _Gen0, false => some B
  | _, _, _ => none

noncomputable def «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt :=
  if x1 = 0 then none else some (Int.tmod x0 x1)

noncomputable def _54f81b1 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
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

private noncomputable def kleanKeyOrderModel : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortInt a,    SortKItem.inj_SortInt b    => decide (a < b)
  | SortKItem.inj_SortInt _,    _                          => true
  | _,                          SortKItem.inj_SortInt _    => false
  | SortKItem.inj_SortString a, SortKItem.inj_SortString b => decide (a < b)
  | SortKItem.inj_SortString _, _                          => true
  | _,                          SortKItem.inj_SortString _ => false
  | _, _ => false

private noncomputable def kleanMapInsertModel
    (key value : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if kleanKeyOrderModel candidate key then
        (candidate, oldValue) :: kleanMapInsertModel key value rest
      else (key, value) :: (candidate, oldValue) :: rest

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  kleanMapInsertModel key value (kleanMapDeleteModel entries key)

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll.foldr
      (fun kv acc => kleanMapInsertModel kv.1 kv.2 acc)
      x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

axiom finishRel (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortBool

axiom neighborMin (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt

axiom oddDone (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) : Option SortBool

axiom pairDone (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortInt) (x3 : SortInt) : Option SortBool

axiom pathRel (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) : Option SortBool

mutual
  noncomputable def snocVS (x0 : SortValSeq) (x1 : SortVal) : Option SortValSeq := _ddc441e x0 x1

  noncomputable def _ddc441e : SortValSeq → SortVal → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X R, V => do
      let _Val0 <- snocVS R V
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X _Val0)
    | _, _ => none
end

noncomputable def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

noncomputable def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

noncomputable def _7e10ba8 : SortIntSeq → SortInt → SortInt → SortInt → Option SortValSeq
  | _Gen0, N, _Gen1, J => do
    let _Val0 <- «_>=Int_» J N
    guard _Val0
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _a9a9899 : SortInt → SortInt → SortBool → Option SortInt
  | B, V, true => do
    let _Val0 <- «_>=Int_» V B
    guard _Val0
    return B
  | _, _, _ => none

noncomputable def _cef5416 : SortIntSeq → SortInt → SortInt → Option SortValSeq
  | _Gen0, N, I => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

noncomputable def _9787670 : SortInt → SortInt → SortBool → Option SortInt
  | B, V, true => do
    let _Val0 <- «_<Int_» V B
    guard _Val0
    return V
  | _, _, _ => none

noncomputable def _ab5ed18 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, I => do
    let _Val0 <- «_<Int_» I 0
    guard _Val0
    return 0
  | _, _ => none

mutual
  noncomputable def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  noncomputable def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

noncomputable def _2070e92 : SortIntSeq → SortInt → Option SortInt
  | _Gen0, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return 0

noncomputable def _94ab512 : SortIntSeq → SortInt → Option SortInt
  | _Gen0, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return 0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

noncomputable def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

mutual
  noncomputable def «allInRange(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_54f81b1 x0 x1) <|> (_e8235c8 x0 x1)

  noncomputable def _e8235c8 : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X R, M => do
      let _Val0 <- «_<=Int_» 1 X
      let _Val1 <- «_<=Int_» X M
      let _Val2 <- _andBool_ _Val0 _Val1
      let _Val3 <- «allInRange(_,_)_VERIFICATION_Bool_IntSeq_Int» R M
      let _Val4 <- _andBool_ _Val2 _Val3
      return _Val4
    | _, _ => none
end

mutual
  noncomputable def _927b1f1 : SortInt → SortIntSeq → Option SortBool
    | X, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» Y R => do
      let _Val0 <- «_==Int_» X Y
      let _Val1 <- «intMember(_,_)_VERIFICATION_Bool_Int_IntSeq» X R
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  noncomputable def «intMember(_,_)_VERIFICATION_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_306ef4e x0 x1) <|> (_927b1f1 x0 x1)
end

noncomputable def «chooseMin(_,_,_)_VERIFICATION_Int_Int_Int_Bool» (x0 : SortInt) (x1 : SortInt) (x2 : SortBool) : Option SortInt := (_5515d1c x0 x1 x2) <|> (_9787670 x0 x1 x2) <|> (_a9a9899 x0 x1 x2)

mutual
  noncomputable def «pAtTotal(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_ab5ed18 x0 x1) <|> (_bdc895a x0 x1) <|> (_dd2140b x0 x1) <|> (_ee6e82d x0 x1)

  noncomputable def _dd2140b : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 R, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «pAtTotal(_,_)_VERIFICATION_Int_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

noncomputable def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

mutual
  noncomputable def _0a577fd : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X R => do
      let _Val0 <- «intMember(_,_)_VERIFICATION_Bool_Int_IntSeq» X R
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «uniqueInts(_)_VERIFICATION_Bool_IntSeq» R
      let _Val3 <- _andBool_ _Val1 _Val2
      return _Val3
    | _ => none

  noncomputable def «uniqueInts(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_0a577fd x0) <|> (_4ab8e18 x0)
end

axiom _1b057af : SortIntSeq → SortInt → SortInt → SortInt → Option SortValSeq
axiom gridRowFrom (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortValSeq

noncomputable def _ec89b92 : SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | P, N, I, J => do
    let _Val0 <- «_*Int_» I N
    let _Val1 <- «_+Int_» _Val0 J
    let _Val2 <- «pAtTotal(_,_)_VERIFICATION_Int_IntSeq_Int» P _Val1
    return _Val2

mutual
  noncomputable def «findOne(_,_)_VERIFICATION_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_3e8cc38 x0 x1) <|> (_a29ddb2 x0 x1) <|> (_ceb9d05 x0 x1)

  noncomputable def _a29ddb2 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X R, A => do
      let _Val0 <- «_=/=Int_» X 1
      let _Val1 <- «_+Int_» A 1
      let _Val2 <- «findOne(_,_)_VERIFICATION_Int_IntSeq_Int» R _Val1
      guard _Val0
      return _Val2
    | _, _ => none
end

noncomputable def _fc9a49f : SortIntSeq → SortInt → Option SortBool
  | P, M => do
    let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» P
    let _Val1 <- «_==Int_» _Val0 M
    let _Val2 <- «allInRange(_,_)_VERIFICATION_Bool_IntSeq_Int» P M
    let _Val3 <- _andBool_ _Val1 _Val2
    let _Val4 <- «uniqueInts(_)_VERIFICATION_Bool_IntSeq» P
    let _Val5 <- _andBool_ _Val3 _Val4
    return _Val5

noncomputable def _b611fa7 : SortIntSeq → SortInt → SortInt → Option SortValSeq
  | P, N, I => do
    let _Val0 <- gridRowFrom P N I 0
    return _Val0

noncomputable def gridAt (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _ec89b92 x0 x1 x2 x3

noncomputable def _298165c : SortIntSeq → Option SortInt
  | P => do
    let _Val0 <- «findOne(_,_)_VERIFICATION_Int_IntSeq_Int» P 0
    return _Val0

noncomputable def validPerm (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := _fc9a49f x0 x1

noncomputable def gridRow (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortValSeq := _b611fa7 x0 x1 x2

noncomputable def _5b76b26 : SortInt → SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | B, P, N, R, C => do
    let _Val0 <- «_-Int_» R 1
    let _Val1 <- gridAt P N _Val0 C
    let _Val2 <- «_>Int_» R 0
    let _Val3 <- «chooseMin(_,_,_)_VERIFICATION_Int_Int_Int_Bool» B _Val1 _Val2
    return _Val3

noncomputable def _8d3f540 : SortInt → SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | B, P, N, R, C => do
    let _Val0 <- «_-Int_» C 1
    let _Val1 <- gridAt P N R _Val0
    let _Val2 <- «_>Int_» C 0
    let _Val3 <- «chooseMin(_,_,_)_VERIFICATION_Int_Int_Int_Bool» B _Val1 _Val2
    return _Val3

noncomputable def _dcc37c8 : SortInt → SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | B, P, N, R, C => do
    let _Val0 <- «_+Int_» C 1
    let _Val1 <- gridAt P N R _Val0
    let _Val2 <- «_+Int_» C 1
    let _Val3 <- «_<Int_» _Val2 N
    let _Val4 <- «chooseMin(_,_,_)_VERIFICATION_Int_Int_Int_Bool» B _Val1 _Val3
    return _Val4

noncomputable def _de4248c : SortInt → SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | B, P, N, R, C => do
    let _Val0 <- «_+Int_» R 1
    let _Val1 <- gridAt P N _Val0 C
    let _Val2 <- «_+Int_» R 1
    let _Val3 <- «_<Int_» _Val2 N
    let _Val4 <- «chooseMin(_,_,_)_VERIFICATION_Int_Int_Int_Bool» B _Val1 _Val3
    return _Val4

noncomputable def oneIndex (x0 : SortIntSeq) : Option SortInt := _298165c x0

axiom gridRowsFrom (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortValSeq
axiom _cb14610 : SortIntSeq → SortInt → SortInt → Option SortValSeq

noncomputable def «afterUp(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortInt := _5b76b26 x0 x1 x2 x3 x4

noncomputable def «afterLeft(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortInt := _8d3f540 x0 x1 x2 x3 x4

noncomputable def «afterRight(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortInt := _dcc37c8 x0 x1 x2 x3 x4

noncomputable def «afterDown(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» (x0 : SortInt) (x1 : SortIntSeq) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortInt := _de4248c x0 x1 x2 x3 x4

noncomputable def _38f6892 : SortIntSeq → SortInt → Option SortInt
  | P, N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- oneIndex P
    let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 N
    guard _Val0
    return _Val2

noncomputable def _da80ff1 : SortIntSeq → SortInt → Option SortInt
  | P, N => do
    let _Val0 <- «_>Int_» N 0
    let _Val1 <- oneIndex P
    let _Val2 <- «_/Int_» _Val1 N
    guard _Val0
    return _Val2

noncomputable def _613f4b8 : SortIntSeq → SortInt → Option SortValSeq
  | P, N => do
    let _Val0 <- gridRowsFrom P N 0
    return _Val0

noncomputable def _448175f : SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | P, N, R, C => do
    let _Val0 <- «_*Int_» N N
    let _Val1 <- «_+Int_» _Val0 1
    let _Val2 <- «afterUp(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» _Val1 P N R C
    return _Val2

noncomputable def oneCol (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_38f6892 x0 x1) <|> (_94ab512 x0 x1)

noncomputable def oneRow (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_2070e92 x0 x1) <|> (_da80ff1 x0 x1)

noncomputable def gridRows (x0 : SortIntSeq) (x1 : SortInt) : Option SortValSeq := _613f4b8 x0 x1

noncomputable def «bestUp(_,_,_,_)_VERIFICATION_Int_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _448175f x0 x1 x2 x3

noncomputable def _4893a10 : SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | P, N, R, C => do
    let _Val0 <- «bestUp(_,_,_,_)_VERIFICATION_Int_IntSeq_Int_Int_Int» P N R C
    let _Val1 <- «afterDown(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» _Val0 P N R C
    return _Val1

noncomputable def «bestDown(_,_,_,_)_VERIFICATION_Int_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _4893a10 x0 x1 x2 x3

noncomputable def _2d08430 : SortIntSeq → SortInt → SortInt → SortInt → Option SortInt
  | P, N, R, C => do
    let _Val0 <- «bestDown(_,_,_,_)_VERIFICATION_Int_IntSeq_Int_Int_Int» P N R C
    let _Val1 <- «afterLeft(_,_,_,_,_)_VERIFICATION_Int_Int_IntSeq_Int_Int_Int» _Val0 P N R C
    return _Val1

noncomputable def «bestLeft(_,_,_,_)_VERIFICATION_Int_IntSeq_Int_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt := _2d08430 x0 x1 x2 x3