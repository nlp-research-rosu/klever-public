import Klean29FilterByPrefix.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _2867a75 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

def _55400f7 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _28fa65f : SortIntSeq → SortStrList → Option SortValSeq
  | _Gen0, SortStrList.«.StrList_VERIFICATION_StrList» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _, _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

axiom «.List» : Option SortList

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def _54ab88f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_2867a75 x0 x1) <|> (_54ab88f x0 x1) <|> (_55400f7 x0 x1)
end

mutual
  noncomputable def _5b57fa4 : SortIntSeq → SortStrList → Option SortValSeq
    | P, SortStrList.«sCons(_,_)_VERIFICATION_StrList_IntSeq_StrList» S REST => do
      let _Val0 <- «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» P S
      let _Val1 <- «_==Bool_» _Val0 false
      let _Val2 <- «prefixFilter(_,_)_VERIFICATION_ValSeq_IntSeq_StrList» P REST
      guard _Val1
      return _Val2
    | _, _ => none

  noncomputable def _6dc8f91 : SortIntSeq → SortStrList → Option SortValSeq
    | P, SortStrList.«sCons(_,_)_VERIFICATION_StrList_IntSeq_StrList» S REST => do
      let _Val0 <- «startsWith(_,_)_MPY-METHODS_Bool_IntSeq_IntSeq» P S
      let _Val1 <- «_==Bool_» _Val0 true
      let _Val2 <- «prefixFilter(_,_)_VERIFICATION_ValSeq_IntSeq_StrList» P REST
      guard _Val1
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» S)) _Val2)
    | _, _ => none

  noncomputable def «prefixFilter(_,_)_VERIFICATION_ValSeq_IntSeq_StrList» (x0 : SortIntSeq) (x1 : SortStrList) : Option SortValSeq := (_28fa65f x0 x1) <|> (_5b57fa4 x0 x1) <|> (_6dc8f91 x0 x1)
end