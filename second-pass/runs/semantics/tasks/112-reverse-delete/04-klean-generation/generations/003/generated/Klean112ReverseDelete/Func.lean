import Klean112ReverseDelete.Inj

def _c678a94 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, A => some A
  | _, _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.List» : Option SortList

def _fe3a470 : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», V => some V
  | _, _ => none

def _2691e6c : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, A => some A
  | _, _, _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def «reversedKeptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := _c678a94 x0 x1 x2

mutual
  def _0c3a867 : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X XS, _Gen0 => do
      let _Val0 <- «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val» XS ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» X SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «lastCharacter(_,_)_MPY-VERIFICATION-BASE_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_0c3a867 x0 x1) <|> (_fe3a470 x0 x1)
end

def «keptAcc(_,_,_)_MPY-VERIFICATION-BASE_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := _2691e6c x0 x1 x2