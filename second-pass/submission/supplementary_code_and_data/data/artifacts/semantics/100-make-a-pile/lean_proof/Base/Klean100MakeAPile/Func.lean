import Klean100MakeAPile.Inj

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _d7c7cfd : SortInt → SortInt → Option SortValSeq
  | N, I => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

axiom _24a9cd2 : SortInt → SortInt → Option SortValSeq
axiom «pile(_,_)_PILE-VERIFICATION_ValSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortValSeq