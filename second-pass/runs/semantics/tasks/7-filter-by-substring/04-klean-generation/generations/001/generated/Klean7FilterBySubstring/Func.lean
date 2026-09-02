import Klean7FilterBySubstring.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

def _8f99830 : SortValSeq → SortIntSeq → SortStrSeq → Option SortValSeq
  | ACC, _Gen0, SortStrSeq.«.StrSeq_FILTER-VERIFICATION_StrSeq» => some ACC
  | _, _, _ => none

axiom «_==Bool_» (x0 : SortBool) (x1 : SortBool) : Option SortBool

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _9ce44bb : SortIntSeq → SortStrSeq → Option SortIntSeq
  | S, SortStrSeq.«.StrSeq_FILTER-VERIFICATION_StrSeq» => some S
  | _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

mutual
  def «lastCodes(_,_)_FILTER-VERIFICATION_IntSeq_IntSeq_StrSeq» (x0 : SortIntSeq) (x1 : SortStrSeq) : Option SortIntSeq := (_9ce44bb x0 x1) <|> (_e07f561 x0 x1)

  def _e07f561 : SortIntSeq → SortStrSeq → Option SortIntSeq
    | _Gen0, SortStrSeq.«ssCons(_,_)_FILTER-VERIFICATION_StrSeq_IntSeq_StrSeq» S SS => do
      let _Val0 <- «lastCodes(_,_)_FILTER-VERIFICATION_IntSeq_IntSeq_StrSeq» S SS
      return _Val0
    | _, _ => none
end

mutual
  def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

mutual
  def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

mutual
  noncomputable def _32d420f : SortValSeq → SortIntSeq → SortStrSeq → Option SortValSeq
    | ACC, P, SortStrSeq.«ssCons(_,_)_FILTER-VERIFICATION_StrSeq_IntSeq_StrSeq» S SS => do
      let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P S
      let _Val1 <- «_==Bool_» _Val0 true
      let _Val2 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» ACC (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» S)) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)
      let _Val3 <- «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» _Val2 P SS
      guard _Val1
      return _Val3
    | _, _, _ => none

  noncomputable def _91dab7e : SortValSeq → SortIntSeq → SortStrSeq → Option SortValSeq
    | ACC, P, SortStrSeq.«ssCons(_,_)_FILTER-VERIFICATION_StrSeq_IntSeq_StrSeq» S SS => do
      let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P S
      let _Val1 <- «_==Bool_» _Val0 false
      let _Val2 <- «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» ACC P SS
      guard _Val1
      return _Val2
    | _, _, _ => none

  noncomputable def «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» (x0 : SortValSeq) (x1 : SortIntSeq) (x2 : SortStrSeq) : Option SortValSeq := (_32d420f x0 x1 x2) <|> (_8f99830 x0 x1 x2) <|> (_91dab7e x0 x1 x2)
end

noncomputable def _363c2de : SortIntSeq → SortStrSeq → Option SortValSeq
  | P, SS => do
    let _Val0 <- «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq» P SS
    return _Val0

noncomputable def «filterStrings(_,_)_FILTER-VERIFICATION_ValSeq_IntSeq_StrSeq» (x0 : SortIntSeq) (x1 : SortStrSeq) : Option SortValSeq := _363c2de x0 x1