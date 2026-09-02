import Klean7FilterBySubstring.Inj

def _8f99830 : SortValSeq → SortIntSeq → SortStrSeq → Option SortValSeq
  | ACC, _Gen0, SortStrSeq.«.StrSeq_FILTER-VERIFICATION_StrSeq» => some ACC
  | _, _, _ => none

def _9ce44bb : SortIntSeq → SortStrSeq → Option SortIntSeq
  | S, SortStrSeq.«.StrSeq_FILTER-VERIFICATION_StrSeq» => some S
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» (x0 : SortValSeq) (x1 : SortIntSeq) (x2 : SortStrSeq) : Option SortValSeq := _8f99830 x0 x1 x2

mutual
  def «lastCodes(_,_)_FILTER-VERIFICATION_IntSeq_IntSeq_StrSeq» (x0 : SortIntSeq) (x1 : SortStrSeq) : Option SortIntSeq := (_9ce44bb x0 x1) <|> (_e07f561 x0 x1)

  def _e07f561 : SortIntSeq → SortStrSeq → Option SortIntSeq
    | _Gen0, SortStrSeq.«ssCons(_,_)_FILTER-VERIFICATION_StrSeq_IntSeq_StrSeq» S SS => do
      let _Val0 <- «lastCodes(_,_)_FILTER-VERIFICATION_IntSeq_IntSeq_StrSeq» S SS
      return _Val0
    | _, _ => none
end

def _363c2de : SortIntSeq → SortStrSeq → Option SortValSeq
  | P, SS => do
    let _Val0 <- «filterAccStrings(_,_,_)_FILTER-VERIFICATION_ValSeq_ValSeq_IntSeq_StrSeq» SortValSeq.«.ValSeq_MPY-CORE_ValSeq» P SS
    return _Val0

def «filterStrings(_,_)_FILTER-VERIFICATION_ValSeq_IntSeq_StrSeq» (x0 : SortIntSeq) (x1 : SortStrSeq) : Option SortValSeq := _363c2de x0 x1