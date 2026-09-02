import Klean100MakeAPile.Inj

axiom «.List» : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _218e890 : SortValSeq → SortValSeq → Option SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», T => some T
  | _, _ => none

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _d7c7cfd : SortInt → SortInt → Option SortValSeq
  | N, I => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

mutual
  def _830ee66 : SortValSeq → SortValSeq → Option SortValSeq
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V S, T => do
      let _Val0 <- «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» S T
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Val0)
    | _, _ => none

  def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) : Option SortValSeq := (_218e890 x0 x1) <|> (_830ee66 x0 x1)
end

axiom _24a9cd2 : SortInt → SortInt → Option SortValSeq
axiom «pile(_,_)_PILE-VERIFICATION_ValSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortValSeq