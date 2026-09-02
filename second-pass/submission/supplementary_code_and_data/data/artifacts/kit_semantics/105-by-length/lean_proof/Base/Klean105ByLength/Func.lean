import Klean105ByLength.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _218dc3a : SortString → Option SortIntSeq
  | "" => some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_==String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «ordChar(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

axiom «substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» (x0 : SortString) (x1 : SortInt) (x2 : SortInt) : Option SortString

def _8227416 : SortValSeq → SortInt → SortVal → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, _Gen1, ACC => some ACC
  | _, _, _, _ => none

def _f316b87 : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt K) SortK.dotk => some K
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

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def «project:Int» (x0 : SortK) : Option SortInt := _f316b87 x0

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

noncomputable def _f390a9b : SortString → SortString → Option SortBool
  | S1, S2 => do
    let _Val0 <- «_==String__STRING-COMMON_Bool_String_String» S1 S2
    let _Val1 <- notBool_ _Val0
    return _Val1

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

noncomputable def «_=/=String__STRING-COMMON_Bool_String_String» (x0 : SortString) (x1 : SortString) : Option SortBool := _f390a9b x0 x1

mutual
  def «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortVal) (x3 : SortValSeq) : Option SortValSeq := (_8227416 x0 x1 x2 x3) <|> (_f059335 x0 x1 x2 x3)

  def _f059335 : SortValSeq → SortInt → SortVal → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» X REST, D, N, ACC => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) X) SortK.dotk)
      let _Val1 <- «project:Int» (SortK.kseq ((@inj SortVal SortKItem) X) SortK.dotk)
      let _Val2 <- «_==Int_» _Val1 D
      let _Val3 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» N SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val4 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» REST D N _Val3
      let _Val5 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» REST D N ACC
      let _Val6 <- kite _Val2 _Val4 _Val5
      let _Val7 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» REST D N ACC
      let _Val8 <- kite _Val0 _Val6 _Val7
      return _Val8
    | _, _, _, _ => none
end

axiom _5711fdc : SortString → Option SortIntSeq
axiom «strToCodes(_)_MPY-STR_IntSeq_String» (x0 : SortString) : Option SortIntSeq

noncomputable def _57187c2 : SortValSeq → Option SortValSeq
  | VS => do
    let _Val0 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Nine"
    let _Val1 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 9 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val0)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val2 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Eight"
    let _Val3 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 8 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val2)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val4 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val1 _Val3
    let _Val5 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Seven"
    let _Val6 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 7 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val5)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val7 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val4 _Val6
    let _Val8 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Six"
    let _Val9 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 6 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val8)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val10 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val7 _Val9
    let _Val11 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Five"
    let _Val12 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 5 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val11)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val13 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val10 _Val12
    let _Val14 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Four"
    let _Val15 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 4 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val14)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val16 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val13 _Val15
    let _Val17 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Three"
    let _Val18 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 3 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val17)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val19 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val16 _Val18
    let _Val20 <- «strToCodes(_)_MPY-STR_IntSeq_String» "Two"
    let _Val21 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 2 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val20)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val22 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val19 _Val21
    let _Val23 <- «strToCodes(_)_MPY-STR_IntSeq_String» "One"
    let _Val24 <- «collectAcc(_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Val_ValSeq» VS 1 ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» _Val23)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val25 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Val22 _Val24
    return _Val25

noncomputable def «byLengthVS(_)_VERIFICATION_ValSeq_ValSeq» (x0 : SortValSeq) : Option SortValSeq := _57187c2 x0